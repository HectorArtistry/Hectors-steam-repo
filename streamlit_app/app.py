# streamlit run streamlit_app/app.py
import streamlit as st
import sqlite3
import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

DB_PATH = os.path.abspath(os.path.join("..", "hector's-steam-repo", "data", "steam_data.db"))

def get_table_names(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]

def get_table_preview(conn, table, limit=100000000):
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT {limit}", conn)
    return df

def get_table_count(conn, table):
    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
    return cursor.fetchone()[0]

def get_games_df(conn):
    return pd.read_sql_query("SELECT * FROM games", conn)

def get_tags_df(conn):
    return pd.read_sql_query("SELECT * FROM tags", conn)

def get_reviews_df(conn):
    return pd.read_sql_query("SELECT * FROM reviews", conn)

def get_full_game_info(conn, appid):
    # Join all tables on appid for a summary
    query = """
    SELECT g.*, d.game_summary, s.developer, s.publisher, s.owners_range, s.price, s.languages, s.genre, r.review_score, r.review_score_text, r.positive_likes, r.negative_dislikes, r.total_reviews, r.recommendations, p.head_image, p.background_image, t.tag
    FROM games g
    LEFT JOIN descriptions d ON g.appid = d.appid
    LEFT JOIN steam_spy s ON g.appid = s.appid
    LEFT JOIN reviews r ON g.appid = r.appid
    LEFT JOIN promotional p ON g.appid = p.appid
    LEFT JOIN tags t ON g.appid = t.appid
    WHERE g.appid = ?
    """
    return pd.read_sql_query(query, conn, params=(appid,))

def main():
    st.title("Hector's Steam Data Explorer")

    if not os.path.exists(DB_PATH):
        st.error(f"Database not found at {DB_PATH}")
        return
    conn = sqlite3.connect(DB_PATH)

    # Sidebar: Table selection and filters
    st.sidebar.header("Filters & Options")
    tables = get_table_names(conn)
    table = st.sidebar.selectbox("Select a table", tables)

    st.header(f"Preview of `{table}` table")
    preview_df = get_table_preview(conn, table)
    st.dataframe(preview_df)
    
    # 1. Line chart: Tag usage percentage vs. releases per month
    st.header("Tag Usage Over Time")
    tags_df = get_tags_df(conn)
    games_df = get_games_df(conn)
    games_df['release_date'] = pd.to_datetime(games_df['release_date'], errors='coerce')
    tags_df['appid'] = tags_df['appid'].astype(str)
    games_df['appid'] = games_df['appid'].astype(str)
    tag_list = sorted(set([tag for tags in tags_df['tag'].dropna() for tag in tags.split(',')]))
    selected_tag = st.selectbox("Select a tag for trend analysis", tag_list)
    # Merge tags and games
    merged = pd.merge(tags_df, games_df[['appid', 'release_date']], on='appid', how='left')
    merged['has_tag'] = merged['tag'].apply(lambda tags: selected_tag in tags if pd.notnull(tags) else False)
    merged = merged.dropna(subset=['release_date'])
    merged['year'] = merged['release_date'].dt.year
    tag_counts = merged.groupby('year')['has_tag'].sum()
    total_counts = merged.groupby('year')['appid'].count()
    percent = (tag_counts / total_counts * 100).fillna(0)

    # Separate line charts
    st.subheader(f"Percentage of Releases with Tag '{selected_tag}'")
    percent.index = percent.index.astype(str)  # Convert year to string to avoid commas
    st.line_chart(percent)

    st.subheader("Total Releases Per Year")
    total_counts.index = total_counts.index.astype(str)  # Convert year to string to avoid commas
    st.line_chart(total_counts)

    # 2. Word cloud for any column in any table
    st.header("Word Cloud Generator")
    col_table = st.selectbox("Select table for word cloud", tables)
    col_df = pd.read_sql_query(f"SELECT * FROM {col_table}", conn)
    wordcloud_columns = [c for c in col_df.columns if c.lower() != "appid"] # Exclude appid column
    col = st.selectbox("Select column for word cloud", wordcloud_columns)
    text = " ".join(str(x) for x in col_df[col].dropna())
    if st.button("Generate Word Cloud"):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

    # 3. Bar chart: releases per year, with indicator for positively reviewed games
    st.header("Game Releases Per Year & Positive Reviews")
    games_df['year'] = games_df['release_date'].dt.year
    reviews_df = get_reviews_df(conn)
    reviews_df['appid'] = reviews_df['appid'].astype(str)
    merged_reviews = pd.merge(games_df, reviews_df[['appid', 'review_score_text']], on='appid', how='left')
    releases_per_year = merged_reviews.groupby('year')['appid'].count()
    positive_reviews = merged_reviews[merged_reviews['review_score_text'].isin(['Very Positive', 'Overwhelmingly Positive'])]
    positive_per_year = positive_reviews.groupby('year')['appid'].count()
    bar_df = pd.DataFrame({'Total Releases': releases_per_year, 'Positive Reviews': positive_per_year}).fillna(0)
    st.bar_chart(bar_df)

    # 4. Game summary filter with images
    st.header("Game Summary Filter")
    titles = games_df[['appid', 'title']].drop_duplicates().sort_values('title')
    selected_title = st.selectbox("Select a game (title)", titles['title'])
    selected_appid = titles[titles['title'] == selected_title]['appid'].iloc[0]
    summary_df = get_full_game_info(conn, selected_appid)
    if not summary_df.empty:
        row = summary_df.iloc[0]
        st.subheader(row['title'])
        if pd.notnull(row.get('head_image', None)):
            st.image(row['head_image'])
        # Only show background if available
        if pd.notnull(row.get('background_image', None)):
            bg_url = row['background_image']
            st.markdown(
                f"""
                <div style="
                    background-image: url('{bg_url}');
                    background-size: cover;
                    background-position: center;
                    padding: 2em;
                    border-radius: 10px;
                    color: white;
                    text-shadow: 1px 1px 2px #000;
                    ">
                    <h4>Release Date: {row['release_date']}</h4>
                    <p><b>App ID:</b> {row['appid']}</p>
                    <p><b>Summary:</b> {row.get('game_summary', 'No summary available.')}</p>
                    <p><b>Tags:</b> {row.get('tag', 'No tags')}</p>
                    <p><b>Review Score:</b> {row.get('review_score_text', 'N/A')}</p>
                    <p><b>Developer:</b> {row.get('developer', 'N/A')}</p>
                    <p><b>Publisher:</b> {row.get('publisher', 'N/A')}</p>
                    <p><b>Price:</b> £{(int(row['price'])/100):.2f}</p>
                    <p><b>Languages:</b> {row.get('languages', 'N/A')}</p>
                    <p><b>Genre:</b> {row.get('genre', 'N/A')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Fallback to normal display if no background image
            st.write(f"**Release Date:** {row['release_date']}")
            st.write(f"**Summary:** {row.get('game_summary', 'No summary available.')}")
            st.write(f"**Tags:** {row.get('tag', 'No tags')}")
            st.write(f"**Review Score:** {row.get('review_score_text', 'N/A')}")
            st.write(f"**Developer:** {row.get('developer', 'N/A')}")
            st.write(f"**Publisher:** {row.get('publisher', 'N/A')}")
            st.write(f"**Price:** {row.get('price', 'N/A')}")
            st.write(f"**Languages:** {row.get('languages', 'N/A')}")
            st.write(f"**Genre:** {row.get('genre', 'N/A')}")
    # 5. Order games by any column
    games_df['appid'] = pd.to_numeric(games_df['appid'], errors='coerce')
    tags_df['appid'] = pd.to_numeric(tags_df['appid'], errors='coerce')
    st.header("Order Games By Any Column")
    order_col = st.selectbox("Select column to order by", games_df.columns)
    order_dir = st.radio("Order direction", ["Ascending", "Descending"])
    ordered_games = games_df.sort_values(order_col, ascending=(order_dir == "Ascending"))
    st.dataframe(ordered_games)

        # 6. Developer/Publisher Output
    st.header("Developer/Publisher Output")

    dev_pub_option = st.radio("Group by", ["Developer", "Publisher"])
    group_col = "developer" if dev_pub_option == "Developer" else "publisher"

    # Join games and steam_spy to get developer/publisher for all games
    dev_pub_df = pd.read_sql_query(
        f"""
        SELECT g.appid, s.{group_col}, r.review_score, r.review_score_text
        FROM games g
        LEFT JOIN steam_spy s ON g.appid = s.appid
        LEFT JOIN reviews r ON g.appid = r.appid
        """, conn
    )

    dev_pub_df = dev_pub_df[
    dev_pub_df[group_col].notnull() &
    (dev_pub_df[group_col] != '') &
    (dev_pub_df[group_col] != '\\N')
    ]

    # Count games per developer/publisher
    count_df = dev_pub_df.groupby(group_col)['appid'].count().reset_index(name='Game Count')

    # Average review score (if numeric) or proportion of positive reviews (if text)
    if 'review_score' in dev_pub_df.columns and pd.api.types.is_numeric_dtype(dev_pub_df['review_score']):
        avg_score = dev_pub_df.groupby(group_col)['review_score'].mean().reset_index(name='Avg Review Score')
        merged_df = pd.merge(count_df, avg_score, on=group_col)
    elif 'review_score_text' in dev_pub_df.columns:
        dev_pub_df['is_positive'] = dev_pub_df['review_score_text'].isin(['Very Positive', 'Overwhelmingly Positive'])
        avg_score = dev_pub_df.groupby(group_col)['is_positive'].mean().reset_index(name='% Positive Reviews')
        merged_df = pd.merge(count_df, avg_score, on=group_col)
    else:
        merged_df = count_df.copy()
        merged_df['Avg Review Score'] = None

    # Show top 20 by game count
    merged_df = merged_df.sort_values('Game Count', ascending=False).head(20)

    import altair as alt
    if 'Avg Review Score' in merged_df.columns:
        color_col = 'Avg Review Score'
    elif '% Positive Reviews' in merged_df.columns:
        color_col = '% Positive Reviews'
    else:
        color_col = None

    chart = alt.Chart(merged_df).mark_bar().encode(
        x=alt.X('Game Count:Q', title='Number of Games'),
        y=alt.Y(f'{group_col}:N', sort='-x', title=dev_pub_option),
        color=alt.Color(f'{color_col}:Q', scale=alt.Scale(scheme='blues'), legend=alt.Legend(title=color_col)) if color_col else alt.value('steelblue'),
        tooltip=[group_col, 'Game Count', color_col] if color_col else [group_col, 'Game Count']
    ).properties(width=700, height=500)

    st.altair_chart(chart, use_container_width=True)

    conn.close()

if __name__ == "__main__":
    main()
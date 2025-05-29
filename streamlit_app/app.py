# streamlit run streamlit_app/app.py
 
import streamlit as st
import sqlite3
import pandas as pd
import os

DB_PATH = os.path.abspath(os.path.join("..", "hector's-steam-repo", "data", "steam_data.db"))

def get_table_names(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]

def get_table_preview(conn, table, limit=20):
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT {limit}", conn)
    return df

def get_table_count(conn, table):
    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
    return cursor.fetchone()[0]

def main():
    st.title("Hector's Steam Data Explorer")

    # Connect to database
    if not os.path.exists(DB_PATH):
        st.error(f"Database not found at {DB_PATH}")
        return
    conn = sqlite3.connect(DB_PATH)

    # Sidebar: Table selection
    tables = get_table_names(conn)
    table = st.sidebar.selectbox("Select a table", tables)

    # Show row count
    count = get_table_count(conn, table)
    st.write(f"**Table `{table}` has {count} rows.**")

    # Show preview
    st.subheader(f"Preview of `{table}`")
    df = get_table_preview(conn, table)
    st.dataframe(df)

    # Optionally: Download as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download preview as CSV",
        data=csv,
        file_name=f"{table}_preview.csv",
        mime='text/csv',
    )

    conn.close()

if __name__ == "__main__":
    main()
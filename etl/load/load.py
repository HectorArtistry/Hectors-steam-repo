import sqlite3
import pandas as pd
import os

def connect_db(db_path="steam_data.db"):
    return sqlite3.connect(db_path)

def load_csv_to_sqlite(csv_path, table_name, conn, limit=None):
    print(f"Loading {table_name} from {csv_path}")
    df = pd.read_csv(csv_path)
    if limit is not None:
        df = df.head(limit)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    
def load_all_tables():
    conn = connect_db()

    data_files = {
        "games": "data/raw/games.csv",
        "categories": "data/raw/categories.csv",
        "descriptions": "data/raw/descriptions.csv",
        "genres": "data/raw/genres.csv",
        "promotional": "data/raw/promotional.csv",
        "reviews": "data/raw/reviews.csv",
        "steamspy": "data/raw/steamspy_insights.csv",
        "tags": "data/raw/tags.csv",
    }

    for table, path in data_files.items():
        if os.path.exists(path):
            load_csv_to_sqlite(path, table, conn, limit=1000)
            print(f"Loaded {table} into the database")
        else:
            print(f"Warning: {path} not found")

    conn.commit()
    conn.close()
# To run "python etl/load/load.py"
import sqlite3
import pandas as pd
import os


def connect_db(db_path="data/steam_data.db"):
    return sqlite3.connect(db_path)

def is_db_initialized(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    return len(tables) > 0

def load_csv_to_sqlite(csv_path, table_name, conn, limit=None):
    print(f"Loading {table_name} from {csv_path}")
    df = pd.read_csv(csv_path)
    if limit is not None:
        df = df.head(limit)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    
def load_all_tables():
    conn = connect_db()
    try:
        print("Connecting to SQLite database...")
        if not is_db_initialized(conn):
            print("Database does not exist, creating a new one.")
            with open("etl/SQL/steam_schema.sql", "r") as f:
                schema_sql = f.read()
                conn.executescript(schema_sql)
        else:
            print("Database already exists, skipping creation.")
    
        # Define the paths to the CSV files
        print("Loading data into the database...")
        data_files = {
            "games": "data/raw/games.csv",
            "categories": "data/raw/categories.csv",
            "descriptions": "data/raw/descriptions.csv",
            "genres": "data/raw/genres.csv",
            "promotional": "data/raw/promotional.csv",
            "reviews": "data/raw/reviews.csv",
            "steam_spy": "data/raw/steamspy_insights.csv",
            "tags": "data/raw/tags.csv",
        }
        # Load each CSV file into the corresponding table
        for table, path in data_files.items():
            if os.path.exists(path):
                load_csv_to_sqlite(path, table, conn, limit=1000)
                print(f"Loaded {table} into the database")
            else:
                print(f"Warning: {path} not found")

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
        
        
if __name__ == "__main__":
    load_all_tables()
# To run "python etl/load/load.py"

import pandas as pd # Always import your modules at the top of your script, 
                    # so they are available everywhere in your code. 
                    # This will fix the cannot access local variable 'pd' error.
import sqlite3
import os


def connect_db(db_path="data/steam_data.db"):
    return sqlite3.connect(db_path)

def is_db_initialized(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    return len(tables) > 0

def pick_first_from_set(val):
    # If the value looks like a set, pick the first item
    if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
        # Remove braces and split by comma
        items = val[1:-1].split(",")
        if items:
            # Remove quotes and whitespace
            first = items[0].strip().strip("'").strip('"')
            return first
    return val

def load_csv_to_sqlite(csv_path, table_name, conn, limit=None):
    print(f"Loading {table_name} from {csv_path}")  # Print which table and file are being loaded
    if table_name == "games":  # Special cleaning for the games table
        import csv
        cleaned_rows = []  # List to store cleaned rows
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.reader(f)  # Read the CSV file line by line
            next(reader)  # Skip the header row
            for _, row in enumerate(reader, start=2):  # Loop through each row, starting at line 2
                try:
                    app_id = None
                    for idx, val in enumerate(row):  # Find the first numeric value (app_id)
                        if val.isdigit():
                            app_id = val
                            app_id_idx = idx
                            break
                    if app_id is None:
                        continue  # Skip if no numeric app_id found
                    title = row[app_id_idx + 1]  # Next column after app_id
                    release_date = row[app_id_idx + 2]  # Next column after title
                    is_free = row[app_id_idx + 3] # Convert is_free to boolean: 1 for yes, 0 for no
                    is_free = True if is_free.strip() == '1' else False
                    type_col = None
                    for val in row[app_id_idx + 4:]:  # Find the next mention of "game" or "demo"
                        if val.strip().lower() in ("game", "demo"):
                            type_col = val.strip().lower()
                            break
                    if type_col is None:
                        continue  # Skip if no type found
                    cleaned_rows.append([app_id, title, release_date, is_free, type_col])  # Add cleaned row
                    if limit and len(cleaned_rows) >= limit:
                        break  # Stop if we've reached the limit
                except Exception:
                    continue  # Skip any row that causes an error
        df = pd.DataFrame(cleaned_rows, columns=["app_id", "title", "release_date", "is_free", "type"])  # Create DataFrame
    
    elif table_name == "descriptions":
        import csv
        cleaned_rows = []
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                try:
                    # Find the first numeric value (appid)
                    app_id = None
                    for idx, val in enumerate(row):
                        if val.isdigit():
                            app_id = val
                            app_id_idx = idx
                            break
                    if app_id is None:
                        continue
                    # The next column is game_summary
                    game_summary = row[app_id_idx + 1] if len(row) > app_id_idx + 1 else ""
                    cleaned_rows.append([app_id, game_summary])
                    if limit and len(cleaned_rows) >= limit:
                        break
                except Exception:
                    continue
        df = pd.DataFrame(cleaned_rows, columns=["app_id", "game_summary"])
    
    elif table_name == "reviews":
        import csv
        cleaned_rows = []
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                try:
                    # Pad row if it's short
                    row = row + [""] * (max(9, len(header)) - len(row))
                    # Select only the columns you want
                    selected = [
                        row[0],  # appid
                        row[1],  # review_score
                        row[2],  # review_score_text
                        row[3],  # positive_likes
                        row[4],  # negative_dislikes
                        row[5],  # total_reviews
                        row[8],  # recommendations (9th column, index 8)
                    ]
                    cleaned_rows.append(selected)
                    if limit and len(cleaned_rows) >= limit:
                        break
                except Exception:
                    continue
        df = pd.DataFrame(
            cleaned_rows,
            columns=["appid", "review_score", "review_score_text", "positive_likes", "negative_dislikes", "total_reviews", "recommendations"],
            )
    
    elif table_name == "steam_spy":
        import csv
        cleaned_rows = []
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                try:
                    # Pad row if it's short
                    row = row + [""] * (14 - len(row))
                    selected = [
                        row[0],  # app_id
                        row[1],  # developer
                        row[2],  # publisher
                        row[3],  # owners_range
                        row[9],  # price
                        row[12], # languages
                        row[13], # genres
                    ]
                    cleaned_rows.append(selected)
                    if limit and len(cleaned_rows) >= limit:
                        break
                except Exception:
                    continue
        df = pd.DataFrame(
            cleaned_rows,
            columns=[
                "appid",
                "developer",
                "publisher",
                "owners_range",
                "price",
                "languages",
                "genre"
            ],
        )
    
    else:
        import csv
        cleaned_rows = []
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                try:
                    # Pad row if it's short
                    row = row + [""] * (len(header) - len(row))
                    # Pick first from set for each field
                    cleaned_row = [pick_first_from_set(val) for val in row[:len(header)]]
                    cleaned_rows.append(cleaned_row)
                    if limit and len(cleaned_rows) >= limit:
                        break
                except Exception:
                    continue
        df = pd.DataFrame(cleaned_rows, columns=header)
    df.to_sql(table_name, conn, if_exists="replace", index=False)  # Write DataFrame to SQLite table
    
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
                load_csv_to_sqlite(path, table, conn, limit=10000)
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
import sqlite3

conn = sqlite3.connect("data/steam_data.db")
cursor = conn.cursor()

tables = ["games", "categories", "descriptions", "genres", "promotional", "reviews", "steam_spy", "tags"]
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"Steam table {table} has: {count} rows")

def preview_db(db_path="data/steam_data.db"):
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables in {db_path}: {tables}")
    for table in tables:
        print(f"\nPreview of '{table}':")
        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT 5;")
            rows = cursor.fetchall()
            # Print column names
            col_names = [description[0] for description in cursor.description]
            print(col_names)
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Could not preview table {table}: {e}")
    conn.close()

if __name__ == "__main__":
    preview_db()


conn.close()


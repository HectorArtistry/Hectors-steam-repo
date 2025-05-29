import sqlite3

def print_table_counts(conn):
    tables = ["games", "categories", "descriptions", "genres", "promotional", "reviews", "steam_spy", "tags"]
    for table in tables:
        cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"Steam table '{table}' has: {count} rows")
    print()  # Add a blank line for separation

def preview_db(db_path="data/steam_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"Tables in {db_path}: {tables}")
    for table in tables:
        print(f"\nPreview of '{table}':")
        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT 20;") # Limit to 20 rows for preview
            rows = cursor.fetchall()
            # Print column names
            col_names = [description[0] for description in cursor.description]
            print(col_names)
            for row in rows:
                print(row)
        except Exception as e:
            print(f"Could not preview table {table}: {e}")
    print()
    conn.close()

def check_pass_mark_and_preview(db_path="data/steam_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Check pass mark for games table
    cursor.execute("SELECT COUNT(*) FROM games")
    games_count = cursor.fetchone()[0]
    if games_count == 10000:
        print(f"PASS: 'games' table has {games_count} rows")
    else:
        print(f"FAIL: 'games' table has {games_count} rows, expected 10000")

    # Check preview match for games table (example: check first row)
    expected_first_game = ('10', 'Counter-Strike', '2000-11-01', 0, 'game')
    cursor.execute("SELECT * FROM games ORDER BY appid LIMIT 1")
    first_game = cursor.fetchone()
    if first_game == expected_first_game:
        print("MATCH: First row in 'games' table matches expected preview data.")
    else:
        print("NO MATCH: First row in 'games' table does not match expected preview data.")
        print(f"Expected: {expected_first_game}")
        print(f"Found:    {first_game}")
    print()
    conn.close()
    
if __name__ == "__main__":
    conn = sqlite3.connect("data/steam_data.db")
    print_table_counts(conn)
    preview_db()
    check_pass_mark_and_preview()
    conn.close()
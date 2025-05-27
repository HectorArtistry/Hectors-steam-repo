import sqlite3

conn = sqlite3.connect("data/steam_data.db")
cursor = conn.cursor()

tables = ["games", "categories", "descriptions", "genres", "promotional", "reviews", "steam_spy", "tags"]
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"Steam table {table} has: {count} rows")

conn.close()

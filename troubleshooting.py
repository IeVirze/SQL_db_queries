import sqlite3

conn = sqlite3.connect("loans.db")
cursor = conn.cursor()

# Get all table names
cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table' AND name NOT LIKE 'sqlite_%';
""")

tables = cursor.fetchall()

print(f"Total tables: {len(tables)}")

for (table_name,) in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    print(f"Table '{table_name}': {row_count} rows")

conn.close()

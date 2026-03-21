import sqlite3
conn = sqlite3.connect('C:\\Users\\Administrator\\.openclaw\\workspace-finance\\tradingagents_local.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", tables)

for table in tables:
    table_name = table[0]
    print(f"\n=== {table_name} ===")
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
    rows = cursor.fetchall()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print("Columns:", [c[1] for c in columns])
    for row in rows:
        print(row)

conn.close()

import sqlite3

# Check the token table structure
conn = sqlite3.connect('C:\\Users\\Administrator\\.openclaw\\workspace-finance\\tradingagents_local.db')
cursor = conn.cursor()

# Check table info
cursor.execute("PRAGMA table_info(user_tokens)")
columns = cursor.fetchall()
print("user_tokens table columns:")
for col in columns:
    print(f"  {col}")

print("\n--- All tokens ---")
cursor.execute("SELECT * FROM user_tokens")
for row in cursor.fetchall():
    print(row)

# Check if there's any token usage tracking
print("\n--- Check users table ---")
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)

conn.close()

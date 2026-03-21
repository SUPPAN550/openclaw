import sqlite3

# Add a proper token in ta-sk- format
conn = sqlite3.connect('C:\\Users\\Administrator\\.openclaw\\workspace-finance\\tradingagents_local.db')
cursor = conn.cursor()

# Insert a token with proper format
cursor.execute("""
INSERT INTO user_tokens (id, user_id, name, token, is_active, created_at)
VALUES (?, ?, ?, ?, ?, datetime('now'))
""", ('new-token-001', 'dcbe1630-6645-4817-8ea2-6cb6490985f2', 'test_token', 'ta-sk-local-test-token-123', 1))

conn.commit()

# Verify
cursor.execute("SELECT * FROM user_tokens")
rows = cursor.fetchall()
print("All tokens:")
for row in rows:
    print(row)

conn.close()

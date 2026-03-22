import sqlite3
conn = sqlite3.connect('/app/tradingagents.db')
c = conn.cursor()
c.execute("PRAGMA table_info(reports)")
cols = [row[1] for row in c.fetchall()]
print('Available columns:')
for col in cols:
    print(f'  {col}')
conn.close()

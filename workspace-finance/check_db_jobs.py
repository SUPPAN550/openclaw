import sqlite3

conn = sqlite3.connect('C:/Users/Administrator/.openclaw/workspace-finance/tradingagents_local.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables:", cursor.fetchall())

cursor.execute("SELECT id, symbol, trade_date, status, decision, direction, confidence, created_at FROM reports WHERE id = 'a8fd1e5306384bca87cc5082e8d8cc48'")
report = cursor.fetchone()
print("ID:", report[0])
print("Symbol:", report[1])
print("Trade Date:", report[2])
print("Status:", report[3])
print("Decision:", report[4])
print("Direction:", report[5])
print("Confidence:", report[6])
print("Created:", report[7])

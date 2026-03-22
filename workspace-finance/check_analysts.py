import sqlite3
conn = sqlite3.connect('/app/tradingagents.db')
c = conn.cursor()
c.execute("SELECT id, status, decision, analyst_traces FROM reports WHERE symbol = '002467.SZ' ORDER BY created_at DESC LIMIT 1")
r = c.fetchone()
if r:
    print('ID:', r[0])
    print('Status:', r[1])
    print('Decision:', r[2])
    print('Traces:', r[3][:500] if r[3] else 'None')
conn.close()

import sqlite3
conn = sqlite3.connect('/app/tradingagents.db')
c = conn.cursor()
c.execute("SELECT market_report, sector_report, industry_report, news_report, fundamentals_report, macro_report, smart_money_report, game_theory_report, decision, direction, confidence, target_price, stop_loss_price, risk_items FROM reports WHERE symbol = '002467.SZ' ORDER BY created_at DESC LIMIT 1")
r = c.fetchone()
if r:
    for i, col in enumerate(['market', 'sector', 'industry', 'news', 'fundamentals', 'macro', 'smart_money', 'game_theory', 'decision', 'direction', 'confidence', 'target', 'stop_loss', 'risk']):
        print(f'=== {col.upper()} ===')
        val = r[i]
        if val:
            print(val[:2000] if len(str(val)) > 2000 else val)
        else:
            print('None')
        print()
conn.close()

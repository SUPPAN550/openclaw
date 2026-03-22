# Fix trading_graph.py tool nodes - correct version

with open('/app/tradingagents/graph/trading_graph.py', 'r') as f:
    content = f.read()

# Check if already has sector, if so skip
if '"sector"' in content:
    print('Already has sector')
else:
    print('Need to fix')

# Let me see the actual content around smart_money
print('Checking file...')

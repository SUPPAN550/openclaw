# Fix trading_graph.py to add new tool nodes
import re

with open('/app/tradingagents/graph/trading_graph.py', 'r') as f:
    content = f.read()

# Find _create_tool_nodes method and add new nodes
# Add after "smart_money" section

new_analysts = [
    ('sector', 'Sector analysis tools', 'get_news'),
    ('industry', 'Industry analysis tools', 'get_news'),
    ('peer', 'Peer analysis tools', 'get_news'),
    ('valuation', 'Valuation analysis tools', 'get_news'),
    ('catalyst', 'Catalyst analysis tools', 'get_news'),
    ('earnings', 'Earnings analysis tools', 'get_news'),
    ('insider', 'Insider analysis tools', 'get_news'),
    ('regulatory', 'Regulatory analysis tools', 'get_news'),
]

# Build new tool node entries
new_nodes = ''
for name, desc, tool in new_analysts:
    new_nodes += f'''
            "{name}": ToolNode(
                [
                    # {desc}
                    {tool},
                ]
            ),'''

# Find position after smart_money closing
pattern = r'(            "smart_money": ToolNode\(\s*\[\s*# Smart money analyst tools.*?\s*\]\s*\),'
replacement = r'\1' + new_nodes

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('/app/tradingagents/graph/trading_graph.py', 'w') as f:
    f.write(content)

print('Fixed trading_graph.py')

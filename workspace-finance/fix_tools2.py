# Fix trading_graph.py tool nodes

new_analysts = [
    'sector',
    'industry', 
    'peer',
    'valuation',
    'catalyst',
    'earnings',
    'insider',
    'regulatory',
]

with open('/app/tradingagents/graph/trading_graph.py', 'r') as f:
    content = f.read()

# Add tool nodes after sentiment
insert_pos = '''"sentiment": ToolNode(
                [
                    # Sentiment analysis tools
                    get_news,
                    get_zt_pool,
                    get_hot_stocks_xq,
                ]
            ),'''

new_tool_nodes = insert_pos
for name in new_analysts:
    new_tool_nodes += f'''
            "{name}": ToolNode(
                [
                    # {name} analysis tools
                    get_news,
                    get_zt_pool,
                ]
            ),'''

content = content.replace(insert_pos, new_tool_nodes)

with open('/app/tradingagents/graph/trading_graph.py', 'w') as f:
    f.write(content)

print('Updated trading_graph.py')

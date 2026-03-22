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

# Add tool nodes after smart_money
if '"sector"' not in content:
    insert_pos = '''"smart_money": ToolNode(
                [
                    # Smart money analyst tools
                    get_individual_fund_flow,
                    get_lhb_detail,
                    get_indicators,
                ]
            ),
        }'''

    new_tool_nodes = insert_pos
    for name in new_analysts:
        new_tool_nodes += f''',
            "{name}": ToolNode(
                [
                    # {name} analysis tools
                    get_news,
                    get_zt_pool,
                ]
            )'''

    # Replace the closing brace
    content = content.replace(insert_pos, new_tool_nodes)

with open('/app/tradingagents/graph/trading_graph.py', 'w') as f:
    f.write(content)

print('Updated trading_graph.py')

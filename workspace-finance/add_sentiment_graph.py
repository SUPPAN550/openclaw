# Read trading_graph.py
with open('/app/tradingagents/graph/trading_graph.py', 'r') as f:
    content = f.read()

# Add sentiment ToolNode if not exists
if '"sentiment": ToolNode' not in content:
    # Find a good place to add it - after the news block
    # Look for the pattern after smart_money
    old_block = '''"smart_money": ToolNode(
                [
                    # Smart money analyst tools
                    get_individual_fund_flow,
                    get_lhb_detail,
                    get_indicators,
                ]
            ),
            "sector": ToolNode([get_news]),'''
    
    new_block = '''"smart_money": ToolNode(
                [
                    # Smart money analyst tools
                    get_individual_fund_flow,
                    get_lhb_detail,
                    get_indicators,
                ]
            ),
            "sentiment": ToolNode([get_news]),
            "sector": ToolNode([get_news]),'''
    
    content = content.replace(old_block, new_block)

# Write back
with open('/app/tradingagents/graph/trading_graph.py', 'w') as f:
    f.write(content)

print('Added sentiment ToolNode to trading_graph.py')

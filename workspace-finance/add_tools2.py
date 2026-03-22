# Simpler fix - directly add to _create_tool_nodes return dict

with open('/app/tradingagents/graph/trading_graph.py', 'r') as f:
    content = f.read()

# Find the return statement in _create_tool_nodes
# and add new tool nodes before the closing brace

new_entries = '''
            "sector": ToolNode([get_news]),
            "industry": ToolNode([get_news]),
            "peer": ToolNode([get_news]),
            "valuation": ToolNode([get_news]),
            "catalyst": ToolNode([get_news]),
            "earnings": ToolNode([get_news]),
            "insider": ToolNode([get_news]),
            "regulatory": ToolNode([get_news]),
'''

# Find position to insert - before the final closing brace of _create_tool_nodes
# Look for the pattern where smart_money is the last entry
if '"sector"' not in content:
    # Replace the ending of _create_tool_nodes 
    content = content.replace(
        '''"smart_money": ToolNode(
                [
                    # Smart money analyst tools
                    get_individual_fund_flow,
                    get_lhb_detail,
                    get_indicators,
                ]
            ),
        }''',
        '''"smart_money": ToolNode(
                [
                    # Smart money analyst tools
                    get_individual_fund_flow,
                    get_lhb_detail,
                    get_indicators,
                ]
            ),
            "sector": ToolNode([get_news]),
            "industry": ToolNode([get_news]),
            "peer": ToolNode([get_news]),
            "valuation": ToolNode([get_news]),
            "catalyst": ToolNode([get_news]),
            "earnings": ToolNode([get_news]),
            "insider": ToolNode([get_news]),
            "regulatory": ToolNode([get_news]),
        }'''
    )

with open('/app/tradingagents/graph/trading_graph.py', 'w') as f:
    f.write(content)

print('Fixed trading_graph.py')

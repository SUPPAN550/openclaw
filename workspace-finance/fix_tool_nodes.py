# Add sentiment tool node to trading_graph.py

with open('/app/tradingagents/graph/trading_graph.py', 'r') as f:
    content = f.read()

# Check if already has sentiment
if '"sentiment"' in content:
    print('sentiment already exists')
else:
    # Add sentiment to tool_nodes
    # Find the position after "social"
    old_social = '''"social": ToolNode(
                [
                    # News tools for social media analysis
                    get_news,
                ]
            ),'''
    
    new_social = '''"social": ToolNode(
                [
                    # News tools for social media analysis
                    get_news,
                ]
            ),
            "sentiment": ToolNode(
                [
                    # Sentiment analysis tools
                    get_news,
                    get_zt_pool,
                    get_hot_stocks_xq,
                ]
            ),'''
    
    content = content.replace(old_social, new_social)
    
    with open('/app/tradingagents/graph/trading_graph.py', 'w') as f:
        f.write(content)
    print('Added sentiment tool node')

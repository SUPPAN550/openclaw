# Fix setup.py to add sentiment analyst

with open('/app/tradingagents/graph/setup.py', 'r') as f:
    content = f.read()

# Check if already modified
if 'sentiment' in content:
    print('sentiment already in setup.py')
else:
    # Add import
    content = content.replace(
        'from tradingagents.agents import *',
        'from tradingagents.agents import *\nfrom tradingagents.agents.analysts.sentiment_analyst import create_sentiment_analyst'
    )
    
    # Add default analyst
    content = content.replace(
        'selected_analysts=["market", "social", "news", "fundamentals", "macro", "smart_money"]',
        'selected_analysts=["market", "sentiment", "social", "news", "fundamentals", "macro", "smart_money"]'
    )
    
    # Add sentiment node before smart_money
    sentiment_code = '''
        if "sentiment" in selected_analysts:
            analyst_nodes["sentiment"] = create_sentiment_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["sentiment"] = self.tool_nodes["sentiment"]
            done_nodes["sentiment"] = analyst_done_node

'''
    content = content.replace(
        '        if "smart_money" in selected_analysts:',
        sentiment_code + '        if "smart_money" in selected_analysts:'
    )
    
    with open('/app/tradingagents/graph/setup.py', 'w') as f:
        f.write(content)
    print('Added sentiment to setup.py')

import re

# Read setup.py
with open('/app/tradingagents/graph/setup.py', 'r') as f:
    content = f.read()

# Add sentiment import if not exists
if 'sentiment_analyst' not in content:
    # Add after regulatory_analyst import
    content = content.replace(
        'from tradingagents.agents.analysts.regulatory_analyst import create_regulatory_analyst',
        'from tradingagents.agents.analysts.regulatory_analyst import create_regulatory_analyst\nfrom tradingagents.agents.analysts.sentiment_analyst import create_sentiment_analyst'
    )

# Write back
with open('/app/tradingagents/graph/setup.py', 'w') as f:
    f.write(content)

print('Added sentiment import to setup.py')

# Now add sentiment handling in setup_graph function
with open('/app/tradingagents/graph/setup.py', 'r') as f:
    content = f.read()

# Find the location after 'if "social" in selected_analysts:' block and add sentiment block
# We'll add it after the social block
social_block = '''        if "social" in selected_analysts:
            analyst_nodes["social"] = create_social_media_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["social"] = self.tool_nodes["social"]
            done_nodes["social"] = analyst_done_node

        if "news" in selected_analysts:'''

sentiment_block = '''        if "social" in selected_analysts:
            analyst_nodes["social"] = create_social_media_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["social"] = self.tool_nodes["social"]
            done_nodes["social"] = analyst_done_node

        if "sentiment" in selected_analysts:
            analyst_nodes["sentiment"] = create_sentiment_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["sentiment"] = self.tool_nodes["sentiment"]
            done_nodes["sentiment"] = analyst_done_node

        if "news" in selected_analysts:'''

content = content.replace(social_block, sentiment_block)

with open('/app/tradingagents/graph/setup.py', 'w') as f:
    f.write(content)

print('Added sentiment handling to setup.py')

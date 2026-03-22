# Fix conditional_logic.py to add sentiment support
import sys

# Read the file
with open('/app/tradingagents/graph/conditional_logic.py', 'r') as f:
    content = f.read()

# Check if sentiment already exists
if 'should_continue_sentiment' in content:
    print('sentiment method already exists')
    sys.exit(0)

# Add sentiment method before should_continue_debate
sentiment_method = '''
    def should_continue_sentiment(self, state: AgentState):
        """Determine if sentiment analysis should continue."""
        messages = state["messages"]
        if not messages:
            return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None):
            return "continue"
        return "done"

'''

# Insert before should_continue_debate
content = content.replace('    def should_continue_debate', sentiment_method + '    def should_continue_debate')

# Write back
with open('/app/tradingagents/graph/conditional_logic.py', 'w') as f:
    f.write(content)

print('Added sentiment method')

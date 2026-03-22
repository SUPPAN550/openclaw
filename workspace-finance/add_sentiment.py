# Fix conditional_logic.py - add sentiment method

with open('/app/tradingagents/graph/conditional_logic.py', 'r') as f:
    content = f.read()

# Add sentiment method if not exists
if 'should_continue_sentiment' not in content:
    new_method = '''
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
    # Add before should_continue_debate
    content = content.replace('    def should_continue_debate', new_method + '    def should_continue_debate')

with open('/app/tradingagents/graph/conditional_logic.py', 'w') as f:
    f.write(content)

print('Fixed conditional_logic.py')

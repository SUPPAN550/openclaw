# Fix conditional_logic.py to add all new analyst methods

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

with open('/app/tradingagents/graph/conditional_logic.py', 'r') as f:
    content = f.read()

# Add methods after sentiment
method_template = '''
    def should_continue_{name}(self, state: AgentState):
        """Determine if {name} analysis should continue."""
        messages = state["messages"]
        if not messages:
            return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None):
            return "continue"
        return "done"
'''

# Find position before should_continue_debate
insert_marker = '    def should_continue_debate'

new_methods = method_template.format(name='sentiment')
for name in new_analysts:
    new_methods += method_template.format(name=name)

content = content.replace(insert_marker, new_methods + insert_marker)

with open('/app/tradingagents/graph/conditional_logic.py', 'w') as f:
    f.write(content)

print('Updated conditional_logic.py')

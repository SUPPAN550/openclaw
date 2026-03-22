# Fix conditional_logic.py to add new analyst methods

with open('/app/tradingagents/graph/conditional_logic.py', 'r') as f:
    content = f.read()

# Add new methods
new_methods = '''
    def should_continue_sector(self, state: AgentState):
        messages = state["messages"]
        if not messages: return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None): return "continue"
        return "done"

    def should_continue_industry(self, state: AgentState):
        messages = state["messages"]
        if not messages: return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None): return "continue"
        return "done"

    def should_continue_peer(self, state: AgentState):
        messages = state["messages"]
        if not messages: return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None): return "continue"
        return "done"

    def should_continue_valuation(self, state: AgentState):
        messages = state["messages"]
        if not messages: return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None): return "continue"
        return "done"

    def should_continue_catalyst(self, state: AgentState):
        messages = state["messages"]
        if not messages: return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None): return "continue"
        return "done"

    def should_continue_earnings(self, state: AgentState):
        messages = state["messages"]
        if not messages: return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None): return "continue"
        return "done"

    def should_continue_insider(self, state: AgentState):
        messages = state["messages"]
        if not messages: return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None): return "continue"
        return "done"

    def should_continue_regulatory(self, state: AgentState):
        messages = state["messages"]
        if not messages: return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None): return "continue"
        return "done"
'''

if 'should_continue_sector' not in content:
    content = content.replace(
        '    def should_continue_debate',
        new_methods + '\n    def should_continue_debate'
    )

with open('/app/tradingagents/graph/conditional_logic.py', 'w') as f:
    f.write(content)

print('Fixed conditional_logic.py')

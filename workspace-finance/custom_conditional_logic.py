# Custom ConditionalLogic that supports any analyst
# This extends the base class to handle dynamically named analysts

from tradingagents.graph.conditional_logic import ConditionalLogic as BaseConditionalLogic
from tradingagents.agents.utils.agent_states import AgentState

class ConditionalLogic(BaseConditionalLogic):
    """Extended ConditionalLogic that supports dynamic analyst names."""

    def should_continue_market(self, state: AgentState):
        return self._generic_should_continue(state)

    def should_continue_social(self, state: AgentState):
        return self._generic_should_continue(state)

    def should_continue_news(self, state: AgentState):
        return self._generic_should_continue(state)

    def should_continue_fundamentals(self, state: AgentState):
        return self._generic_should_continue(state)

    def should_continue_macro(self, state: AgentState):
        return self._generic_should_continue(state)

    def should_continue_smart_money(self, state: AgentState):
        return self._generic_should_continue(state)

    def _generic_should_continue(self, state: AgentState):
        """Generic logic for any analyst."""
        messages = state["messages"]
        if not messages:
            return "done"
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None):
            return "continue"
        return "done"

    # Override to support sentiment if needed
    def should_continue_sentiment(self, state: AgentState):
        return self._generic_should_continue(state)

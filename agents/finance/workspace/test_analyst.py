import os
os.environ['MINIMAX_API_KEY'] = 'sk-cp-3DbmMFernV2KyAZE1VplJoIYb4go7QLbK4cT87pxEa1895zJLiPrF1q--TsrTOLZFfaZzyxizWtBTYTk5169UXjDigmbB9INh24yONHWK-DJAH7Ec8Q5fmA'
os.environ['MINIMAX_GROUP_ID'] = '2034903620129923844'

import sys
sys.path.insert(0, 'C:/Users/Administrator/.openclaw/agents/finance/workspace/TradingAgents')

from tradingagents.agents.analysts.market_analyst import create_market_analyst
from tradingagents.llm_clients.factory import create_llm_client
from tradingagents.agents.utils.agent_states import AgentState
from datetime import datetime

# Create the LLM client
client = create_llm_client('minimax', 'MiniMax-M2.5')
llm = client.get_llm()

# Create the market analyst
analyst = create_market_analyst(llm)

# Create a test state
state = {
    "messages": [("human", "300558.SZ")],
    "company_of_interest": "300558.SZ",
    "trade_date": "2026-03-20",
}

print("Running market analyst...")
try:
    result = analyst(state)
    print("Keys:", result.keys())
    print("Messages:", result.get("messages"))
    if result.get("market_report"):
        print("Report:", result["market_report"][:1000])
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()

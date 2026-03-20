import os
import sys
# Disable any proxy settings
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'
os.environ['MINIMAX_API_KEY'] = 'sk-cp-3DbmMFernV2KyAZE1VplJoIYb4go7QLbK4cT87pxEa1895zJLiPrF1q--TsrTOLZFfaZzyxizWtBTYTk5169UXjDigmbB9INh24yONHWK-DJAH7Ec8Q5fmA'
os.environ['MINIMAX_GROUP_ID'] = '2034903620129923844'

# Add TradingAgents to path
sys.path.insert(0, 'C:/Users/Administrator/.openclaw/agents/finance/workspace/TradingAgents')

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config['llm_provider'] = 'minimax'
config['deep_think_llm'] = 'MiniMax-M2.5'
config['quick_think_llm'] = 'MiniMax-M2.5'
config['backend_url'] = 'https://api.minimax.chat/v1'  # 添加这个！

ta = TradingAgentsGraph(selected_analysts=['market'], debug=True, config=config)
print('Testing with AAPL...')
_, decision = ta.propagate('AAPL', '2026-03-20')
print('Result:', decision[:200] if decision else 'No result')

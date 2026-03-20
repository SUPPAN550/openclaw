import sys
sys.path.insert(0, 'C:/Users/Administrator/.openclaw/agents/finance/workspace/TradingAgents')

import os
os.environ['MINIMAX_API_KEY'] = 'sk-cp-3DbmMFernV2KyAZE1VplJoIYb4go7QLbK4cT87pxEa1895zJLiPrF1q--TsrTOLZFfaZzyxizWtBTYTk5169UXjDigmbB9INh24yONHWK-DJAH7Ec8Q5fmA'
os.environ['MINIMAX_GROUP_ID'] = '2034903620129923844'

from tradingagents.llm_clients.factory import create_llm_client
client = create_llm_client('minimax', 'MiniMax-M2.5')
llm = client.get_llm()
result = llm.invoke('Say hi')
print('OK:', result.content[:100] if result.content else 'empty')

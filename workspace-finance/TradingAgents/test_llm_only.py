"""Test MiniMax LLM without network - no tools, just chat"""
import os
import sys

sys.path.insert(0, r"C:\Users\Administrator\.openclaw\workspace-finance\TradingAgents")

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

load_dotenv()

# Create config - use minimal settings
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "minimax"
config["deep_think_llm"] = "MiniMax-M2.7"
config["quick_think_llm"] = "MiniMax-M2.5"
config["backend_url"] = "https://api.minimaxi.com/v1"
config["max_debate_rounds"] = 1

print(f"Testing MiniMax with TradingAgents...")
print(f"Provider: {config['llm_provider']}")
print(f"Model: {config['deep_think_llm']}")
print(f"URL: {config['backend_url']}")

# Create the graph
ta = TradingAgentsGraph(debug=False, config=config)

print("\nTesting LLM directly...")

# Test the LLM directly without any tools
try:
    from langchain_core.messages import HumanMessage
    response = ta.quick_thinking_llm.invoke([HumanMessage(content="Say 'MiniMax works!' in Chinese")])
    print(f"\nLLM Response: {response.content}")
    print("\n" + "="*50)
    print("SUCCESS! MiniMax is working with TradingAgents!")
    print("="*50)
except Exception as e:
    print(f"\nError: {e}")

"""Test MiniMax with TradingAgents"""
import os
import sys

# Add the TradingAgents to path
sys.path.insert(0, r"C:\Users\Administrator\.openclaw\workspace-finance\TradingAgents")

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create custom config for MiniMax
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = os.getenv("TRADINGAGENTS_LLM_PROVIDER", "openai")
config["deep_think_llm"] = os.getenv("TRADINGAGENTS_DEEP_THINK_LLM", "MiniMax-M2.7")
config["quick_think_llm"] = os.getenv("TRADINGAGENTS_QUICK_THINK_LLM", "MiniMax-M2.5")
config["backend_url"] = os.getenv("TRADINGAGENTS_BACKEND_URL", "https://api.minimaxi.com/v1")
config["max_debate_rounds"] = 1
config["max_risk_discuss_rounds"] = 1

print(f"Using LLM Provider: {config['llm_provider']}")
print(f"Deep Think Model: {config['deep_think_llm']}")
print(f"Quick Think Model: {config['quick_think_llm']}")
print(f"Backend URL: {config['backend_url']}")

# Initialize
ta = TradingAgentsGraph(debug=True, config=config)

# Quick test - just analyze one stock
print("\nTesting with NVDA...")
try:
    _, decision = ta.propagate("NVDA", "2024-05-10")
    print(f"\nDecision: {decision}")
    print("\n✅ MiniMax works with TradingAgents!")
except Exception as e:
    print(f"\n❌ Error: {e}")

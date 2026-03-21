"""Test with Alpha Vantage data source"""
import os
import sys

# Set Alpha Vantage key BEFORE importing tradingagents
os.environ["ALPHA_VANTAGE_API_KEY"] = "demo"

sys.path.insert(0, r"C:\Users\Administrator\.openclaw\workspace-finance\TradingAgents")

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

load_dotenv()

# Config with Alpha Vantage
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "minimax"
config["deep_think_llm"] = "MiniMax-M2.7"
config["quick_think_llm"] = "MiniMax-M2.5"
config["backend_url"] = "https://api.minimaxi.com/v1"
config["max_debate_rounds"] = 1
config["max_risk_discuss_rounds"] = 1

# Switch to alpha_vantage
config["data_vendors"] = {
    "core_stock_apis": "alpha_vantage",
    "technical_indicators": "alpha_vantage",
    "fundamental_data": "alpha_vantage",
    "news_data": "alpha_vantage",
}

print("Using data source: Alpha Vantage (demo key)")
print("Testing MiniMax + TradingAgents...")

ta = TradingAgentsGraph(debug=False, config=config)

print("\nTesting with AAPL...")
try:
    _, decision = ta.propagate("AAPL", "2024-05-10")
    print(f"\nDecision: {decision}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)[:200]}")

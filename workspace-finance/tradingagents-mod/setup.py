# TradingAgents/graph/setup.py

from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode

from tradingagents.agents import *
from tradingagents.agents.utils.agent_states import AgentState

from .conditional_logic import ConditionalLogic


class GraphSetup:
    """Handles the setup and configuration of the agent graph."""

    def __init__(
        self,
        quick_thinking_llm: ChatOpenAI,
        deep_thinking_llm: ChatOpenAI,
        tool_nodes: Dict[str, ToolNode],
        bull_memory,
        bear_memory,
        trader_memory,
        invest_judge_memory,
        risk_manager_memory,
        conditional_logic: ConditionalLogic,
        data_collector=None,
    ):
        """Initialize with required components."""
        self.quick_thinking_llm = quick_thinking_llm
        self.deep_thinking_llm = deep_thinking_llm
        self.tool_nodes = tool_nodes
        self.bull_memory = bull_memory
        self.bear_memory = bear_memory
        self.trader_memory = trader_memory
        self.invest_judge_memory = invest_judge_memory
        self.risk_manager_memory = risk_manager_memory
        self.conditional_logic = conditional_logic
        self.data_collector = data_collector

    def setup_graph(
        self, selected_analysts=["market", "social", "news", "fundamentals", "macro", "smart_money"],
        checkpointer=None
    ):
        """Set up and compile the agent workflow graph.

        Args:
            selected_analysts (list): List of analyst types to include.
            checkpointer: Optional LangGraph checkpointer for state persistence.
        """
        if len(selected_analysts) == 0:
            raise ValueError("Trading Agents Graph Setup Error: no analysts selected!")

        # Create analyst nodes
        analyst_nodes = {}
        tool_nodes = {}
        done_nodes = {}

        def analyst_done_node(_state):
            return {}

        # Market analyst
        if "market" in selected_analysts:
            from tradingagents.agents.analysts.market_analyst import create_market_analyst
            analyst_nodes["market"] = create_market_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["market"] = self.tool_nodes["market"]
            done_nodes["market"] = analyst_done_node

        # Social media analyst
        if "social" in selected_analysts:
            from tradingagents.agents.analysts.social_media_analyst import create_social_media_analyst
            analyst_nodes["social"] = create_social_media_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["social"] = self.tool_nodes["social"]
            done_nodes["social"] = analyst_done_node

        # News analyst
        if "news" in selected_analysts:
            from tradingagents.agents.analysts.news_analyst import create_news_analyst
            analyst_nodes["news"] = create_news_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["news"] = self.tool_nodes["news"]
            done_nodes["news"] = analyst_done_node

        # Fundamentals analyst
        if "fundamentals" in selected_analysts:
            from tradingagents.agents.analysts.fundamentals_analyst import create_fundamentals_analyst
            analyst_nodes["fundamentals"] = create_fundamentals_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["fundamentals"] = self.tool_nodes["fundamentals"]
            done_nodes["fundamentals"] = analyst_done_node

        # Macro analyst
        if "macro" in selected_analysts:
            from tradingagents.agents.analysts.macro_analyst import create_macro_analyst
            analyst_nodes["macro"] = create_macro_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["macro"] = self.tool_nodes["macro"]
            done_nodes["macro"] = analyst_done_node

        # Smart money analyst
        if "smart_money" in selected_analysts:
            from tradingagents.agents.analysts.smart_money_analyst import create_smart_money_analyst
            analyst_nodes["smart_money"] = create_smart_money_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["smart_money"] = self.tool_nodes["smart_money"]
            done_nodes["smart_money"] = analyst_done_node

        # Sector analyst (custom)
        if "sector" in selected_analysts:
            from tradingagents.agents.analysts.sector_analyst import create_sector_analyst
            analyst_nodes["sector"] = create_sector_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["sector"] = self.tool_nodes.get("sector", self.tool_nodes["news"])
            done_nodes["sector"] = analyst_done_node

        # Industry analyst (custom)
        if "industry" in selected_analysts:
            from tradingagents.agents.analysts.industry_analyst import create_industry_analyst
            analyst_nodes["industry"] = create_industry_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["industry"] = self.tool_nodes.get("industry", self.tool_nodes["news"])
            done_nodes["industry"] = analyst_done_node

        # Peer analyst (custom)
        if "peer" in selected_analysts:
            from tradingagents.agents.analysts.peer_analyst import create_peer_analyst
            analyst_nodes["peer"] = create_peer_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["peer"] = self.tool_nodes.get("peer", self.tool_nodes["news"])
            done_nodes["peer"] = analyst_done_node

        # Valuation analyst (custom)
        if "valuation" in selected_analysts:
            from tradingagents.agents.analysts.valuation_analyst import create_valuation_analyst
            analyst_nodes["valuation"] = create_valuation_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["valuation"] = self.tool_nodes.get("valuation", self.tool_nodes["news"])
            done_nodes["valuation"] = analyst_done_node

        # Catalyst analyst (custom)
        if "catalyst" in selected_analysts:
            from tradingagents.agents.analysts.catalyst_analyst import create_catalyst_analyst
            analyst_nodes["catalyst"] = create_catalyst_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["catalyst"] = self.tool_nodes.get("catalyst", self.tool_nodes["news"])
            done_nodes["catalyst"] = analyst_done_node

        # Earnings analyst (custom)
        if "earnings" in selected_analysts:
            from tradingagents.agents.analysts.earnings_analyst import create_earnings_analyst
            analyst_nodes["earnings"] = create_earnings_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["earnings"] = self.tool_nodes.get("earnings", self.tool_nodes["news"])
            done_nodes["earnings"] = analyst_done_node

        # Insider analyst (custom)
        if "insider" in selected_analysts:
            from tradingagents.agents.analysts.insider_analyst import create_insider_analyst
            analyst_nodes["insider"] = create_insider_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["insider"] = self.tool_nodes.get("insider", self.tool_nodes["news"])
            done_nodes["insider"] = analyst_done_node

        # Regulatory analyst (custom)
        if "regulatory" in selected_analysts:
            from tradingagents.agents.analysts.regulatory_analyst import create_regulatory_analyst
            analyst_nodes["regulatory"] = create_regulatory_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["regulatory"] = self.tool_nodes.get("regulatory", self.tool_nodes["news"])
            done_nodes["regulatory"] = analyst_done_node

        # Sentiment analyst (custom)
        if "sentiment" in selected_analysts:
            from tradingagents.agents.analysts.sentiment_analyst import create_sentiment_analyst
            analyst_nodes["sentiment"] = create_sentiment_analyst(
                self.quick_thinking_llm, self.data_collector
            )
            tool_nodes["sentiment"] = self.tool_nodes.get("sentiment", self.tool_nodes["news"])
            done_nodes["sentiment"] = analyst_done_node

        # Create researcher and manager nodes
        bull_researcher_node = create_bull_researcher(
            self.quick_thinking_llm, self.bull_memory
        )
        bear_researcher_node = create_bear_researcher(
            self.quick_thinking_llm, self.bear_memory
        )
        game_theory_manager_node = create_game_theory_manager(self.quick_thinking_llm)
        research_manager_node = create_research_manager(
            self.deep_thinking_llm, self.invest_judge_memory
        )
        trader_node = create_trader(self.quick_thinking_llm, self.trader_memory)

        # Create risk analysis nodes
        aggressive_analyst = create_aggressive_debator(self.quick_thinking_llm)
        neutral_analyst = create_neutral_debator(self.quick_thinking_llm)
        conservative_analyst = create_conservative_debator(self.quick_thinking_llm)
        risk_manager_node = create_risk_manager(
            self.deep_thinking_llm, self.risk_manager_memory
        )

        # Create workflow
        workflow = StateGraph(AgentState)

        def analyst_display_name(analyst_type: str) -> str:
            """Convert analyst_type key to display name, e.g. 'smart_money' -> 'Smart Money'."""
            return analyst_type.replace("_", " ").title()

        # Add analyst nodes to the graph
        for analyst_type, node in analyst_nodes.items():
            workflow.add_node(f"{analyst_display_name(analyst_type)} Analyst", node)
            workflow.add_node(f"tools_{analyst_type}", tool_nodes[analyst_type])
            workflow.add_node(f"{analyst_display_name(analyst_type)} Analyst Done", done_nodes[analyst_type])

        # Add other nodes
        workflow.add_node("Game Theory Manager", game_theory_manager_node)
        workflow.add_node("Bull Researcher", bull_researcher_node)
        workflow.add_node("Bear Researcher", bear_researcher_node)
        workflow.add_node("Research Manager", research_manager_node)
        workflow.add_node("Trader", trader_node)
        workflow.add_node("Aggressive Analyst", aggressive_analyst)
        workflow.add_node("Neutral Analyst", neutral_analyst)
        workflow.add_node("Conservative Analyst", conservative_analyst)
        workflow.add_node("Risk Judge", risk_manager_node)

        # Define edges
        # Fan out all selected analysts in parallel from START
        for analyst_type in selected_analysts:
            workflow.add_edge(START, f"{analyst_display_name(analyst_type)} Analyst")

        # Each analyst runs independently, then fans in to Bull Researcher
        for analyst_type in selected_analysts:
            current_analyst = f"{analyst_display_name(analyst_type)} Analyst"
            current_tools = f"tools_{analyst_type}"
            current_done = f"{analyst_display_name(analyst_type)} Analyst Done"
            # Add conditional edges for current analyst
            workflow.add_conditional_edges(
                current_analyst,
                getattr(self.conditional_logic, f"should_continue_{analyst_type}"),
                {
                    "continue": current_tools,
                    "done": current_done,
                },
            )
            workflow.add_edge(current_tools, current_analyst)

        # All analysts complete → Game Theory Manager
        workflow.add_edge(
            [f"{analyst_display_name(analyst_type)} Analyst Done" for analyst_type in selected_analysts],
            "Game Theory Manager",
        )
        # Game Theory Manager → Bull Researcher
        workflow.add_edge("Game Theory Manager", "Bull Researcher")

        # Add remaining edges
        workflow.add_conditional_edges(
            "Bull Researcher",
            self.conditional_logic.should_continue_debate,
            {
                "Bear Researcher": "Bear Researcher",
                "Research Manager": "Research Manager",
            },
        )
        workflow.add_conditional_edges(
            "Bear Researcher",
            self.conditional_logic.should_continue_debate,
            {
                "Bull Researcher": "Bull Researcher",
                "Research Manager": "Research Manager",
            },
        )
        workflow.add_edge("Research Manager", "Trader")
        workflow.add_edge("Trader", "Aggressive Analyst")
        workflow.add_conditional_edges(
            "Aggressive Analyst",
            self.conditional_logic.should_continue_risk_analysis,
            {
                "Conservative Analyst": "Conservative Analyst",
                "Risk Judge": "Risk Judge",
            },
        )
        workflow.add_conditional_edges(
            "Conservative Analyst",
            self.conditional_logic.should_continue_risk_analysis,
            {
                "Neutral Analyst": "Neutral Analyst",
                "Risk Judge": "Risk Judge",
            },
        )
        workflow.add_conditional_edges(
            "Neutral Analyst",
            self.conditional_logic.should_continue_risk_analysis,
            {
                "Aggressive Analyst": "Aggressive Analyst",
                "Risk Judge": "Risk Judge",
            },
        )

        workflow.add_conditional_edges(
            "Risk Judge",
            self.conditional_logic.should_revise_after_risk_judge,
            {
                "Trader": "Trader",
                "END": END,
            },
        )

        # Compile and return
        return workflow.compile(checkpointer=checkpointer)

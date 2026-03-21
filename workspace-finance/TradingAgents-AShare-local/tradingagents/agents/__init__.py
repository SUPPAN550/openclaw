from .utils.agent_utils import create_msg_delete
from .utils.agent_states import AgentState, InvestDebateState, RiskDebateState
from .utils.memory import FinancialSituationMemory

from .analysts.fundamentals_analyst import create_fundamentals_analyst
from .analysts.macro_analyst import create_macro_analyst
from .analysts.market_analyst import create_market_analyst
from .analysts.news_analyst import create_news_analyst
from .analysts.smart_money_analyst import create_smart_money_analyst
from .analysts.social_media_analyst import create_social_media_analyst
from .analysts.sentiment_analyst import create_sentiment_analyst
from .analysts.game_theory_analyst import create_game_theory_analyst
# New analysts for 15-analyst version
from .analysts.industry_analyst import create_industry_analyst
from .analysts.valuation_analyst import create_valuation_analyst
from .analysts.financial_quality_analyst import create_financial_quality_analyst
from .analysts.management_analyst import create_management_analyst
from .analysts.risk_analyst import create_risk_analyst
from .analysts.institutional_analyst import create_institutional_analyst
from .analysts.flows_analyst import create_flows_analyst

from .researchers.bear_researcher import create_bear_researcher
from .researchers.bull_researcher import create_bull_researcher

from .risk_mgmt.aggressive_debator import create_aggressive_debator
from .risk_mgmt.conservative_debator import create_conservative_debator
from .risk_mgmt.neutral_debator import create_neutral_debator

from .managers.research_manager import create_research_manager
from .managers.risk_manager import create_risk_manager
from .managers.game_theory_manager import create_game_theory_manager

from .trader.trader import create_trader

__all__ = [
    "FinancialSituationMemory",
    "AgentState",
    "create_msg_delete",
    "InvestDebateState",
    "RiskDebateState",
    "create_bear_researcher",
    "create_bull_researcher",
    "create_research_manager",
    "create_fundamentals_analyst",
    "create_macro_analyst",
    "create_market_analyst",
    "create_neutral_debator",
    "create_smart_money_analyst",
    "create_news_analyst",
    "create_aggressive_debator",
    "create_risk_manager",
    "create_conservative_debator",
    "create_social_media_analyst",
    "create_sentiment_analyst",
    "create_game_theory_analyst",
    "create_trader",
    "create_game_theory_manager",
    # New analysts
    "create_industry_analyst",
    "create_valuation_analyst",
    "create_financial_quality_analyst",
    "create_management_analyst",
    "create_risk_analyst",
    "create_institutional_analyst",
    "create_flows_analyst",
]

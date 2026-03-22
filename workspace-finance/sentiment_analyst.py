"""Sentiment Analyst - 分析市场情绪和舆情"""
import asyncio
from datetime import datetime, timedelta
from langchain_core.messages import HumanMessage, SystemMessage
from tradingagents.dataflows.config import get_config
from tradingagents.prompts import get_prompt
from tradingagents.graph.intent_parser import build_horizon_context
from tradingagents.agents.utils.agent_states import current_tracker_var


def create_sentiment_analyst(llm, data_collector):
    """Create a sentiment analyst agent.
    
    Args:
        llm: Language model instance
        data_collector: Data collector for fetching news and sentiment data
        
    Returns:
        Agent node for sentiment analysis
    """
    async def sentiment_analyst(state):
        from tradingagents.agents.utils.agent_states import AgentState, update_tracking
        from tradingagents.agents.analyst import _call_llm_with_tools, _create_system_message
        
        company_name = state.get("company_name")
        trade_date = state.get("trade_date")
        
        system_msg = """你是一位专业的市场情绪分析师。

你的主要任务是：
1. 分析标的股票的市场情绪和舆情
2. 评估新闻和社交媒体对股价的影响
3. 判断市场参与者的情绪偏向（多头/空头/中性）
4. 识别潜在的情绪拐点和反转信号

分析维度：
- 个股新闻情绪（正面/负面/中性）
- 市场整体情绪（狂热/谨慎/恐慌）
- 资金流向情绪（流入/流出）
- 分析师评级变化
- 股东大会/业绩公告等重大事件

请给出明确的市场情绪判断和短线交易建议。"""
        
        user_msg = f"""请分析 {company_name} 在 {trade_date} 的市场情绪和舆情。"""
        
        from tradingagents.agents.analyst import get_analyst_tools
        tools = get_analyst_tools(data_collector, ["get_news"])
        
        response = await _call_llm_with_tools(
            llm,
            [SystemMessage(content=system_msg), HumanMessage(content=user_msg)],
            tools,
            state
        )
        
        sentiment_report = response.content if hasattr(response, 'content') else str(response)
        
        return {"sentiment_report": sentiment_report}
    
    return sentiment_analyst

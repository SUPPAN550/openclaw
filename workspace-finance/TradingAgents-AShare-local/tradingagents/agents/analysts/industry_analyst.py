"""
Industry Analyst - 行业分析师
专注于行业趋势和竞争对手分析
"""

import asyncio

from langchain_core.messages import HumanMessage, SystemMessage
from tradingagents.dataflows.config import get_config
from tradingagents.prompts import get_prompt
from tradingagents.graph.intent_parser import build_horizon_context
from tradingagents.agents.utils.agent_states import current_tracker_var


def _extract_verdict(text):
    import re, json
    m = re.search(r'<!--\s*VERDICT:\s*(\{.*?\})\s*-->', text, re.DOTALL)
    if m:
        try:
            d = json.loads(m.group(1))
            return d.get("direction", "中性"), "中"
        except Exception:
            pass
    return "中性", "低"


def create_industry_analyst(llm, data_collector=None):
    """创建行业分析师节点"""
    
    async def _safe(tool, payload):
        try:
            return await asyncio.to_thread(tool.invoke, payload)
        except Exception as exc:
            return f"调用失败：{exc}"

    async def industry_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        print(f"[Industry Analyst] START {ticker} {current_date}")
        horizon = state.get("horizon", "short")
        user_intent = state.get("user_intent") or {}
        focus_areas = user_intent.get("focus_areas", [])
        specific_questions = user_intent.get("specific_questions", [])

        config = get_config()
        system_message = get_prompt("industry_system_message", config=config) or ""
        horizon_ctx = build_horizon_context(horizon, focus_areas, specific_questions, agent_type="industry")

        # 获取行业相关数据
        from tradingagents.agents.utils.agent_utils import get_stock_data, get_news, get_indicators
        
        # 并行获取数据
        results = await asyncio.gather(
            _safe(get_stock_data, {"symbol": ticker, "date": current_date, "data_window": "60天"}),
            _safe(get_news, {"symbol": ticker, "date": current_date, "data_window": "30天"}),
            _safe(get_indicators, {"symbol": ticker, "date": current_date}),
        )
        stock_data, news_data, indicators = results

        messages = [
            SystemMessage(content=(
                horizon_ctx + system_message
                + "\n\n请严格基于提供的行业数据输出报告，全程使用中文。"
            )),
            HumanMessage(content=(
                f"请分析 {ticker} 在 {current_date} 所属行业的趋势和竞争格局。\n\n"
                f"【股票走势数据】\n{stock_data}\n\n"
                f"【行业相关新闻】\n{news_data}\n\n"
                f"【技术指标】\n{indicators}"
            )),
        ]

        # Token 级流式输出
        tracker = current_tracker_var.get()
        full_content = ""
        async for chunk in llm.astream(messages):
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            full_content += content
            if tracker:
                tracker._emit_token("Industry Analyst", "industry_report", content)

        print(f"[Industry Analyst] DONE {ticker}, report length={len(full_content)}")
        verdict, confidence = _extract_verdict(full_content)
        return {
            "industry_report": full_content,
            "analyst_traces": [{
                "agent": "industry_analyst",
                "horizon": horizon,
                "data_window": "60天",
                "key_finding": f"行业分析结论：{verdict}",
                "verdict": verdict,
                "confidence": confidence,
            }],
        }

    return industry_analyst_node

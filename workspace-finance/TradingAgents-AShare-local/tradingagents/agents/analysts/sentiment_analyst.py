"""
Sentiment Analyst - 情绪分析师
专注于市场情绪分析，利用涨停数、雪球热度等数据
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


def create_sentiment_analyst(llm, data_collector=None):
    """创建情绪分析师节点"""
    
    async def _safe(tool, payload):
        try:
            return await asyncio.to_thread(tool.invoke, payload)
        except Exception as exc:
            return f"调用失败：{exc}"

    async def sentiment_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        print(f"[Sentiment Analyst] START {ticker} {current_date}")
        horizon = state.get("horizon", "short")
        user_intent = state.get("user_intent") or {}
        focus_areas = user_intent.get("focus_areas", [])
        specific_questions = user_intent.get("specific_questions", [])

        config = get_config()
        system_message = get_prompt("sentiment_system_message", config=config) or ""
        horizon_ctx = build_horizon_context(horizon, focus_areas, specific_questions, agent_type="sentiment")

        # 尝试从 data_collector 获取数据
        pool = data_collector.get(ticker, current_date) if data_collector else None

        if pool is not None:
            zt_data = pool.get("zt_pool", "无数据")
            hot_stocks = pool.get("hot_stocks", "无数据")
            lhb = pool.get("lhb", "无数据")
        else:
            from datetime import datetime, timedelta
            from tradingagents.agents.utils.agent_utils import get_zt_pool, get_hot_stocks_xq, get_lhb_detail
            
            # 并行获取情绪相关数据
            results = await asyncio.gather(
                _safe(get_zt_pool, {"date": current_date}),
                _safe(get_hot_stocks_xq, {}),
                _safe(get_lhb_detail, {"symbol": ticker, "date": current_date}),
            )
            zt_data, hot_stocks, lhb = results

        messages = [
            SystemMessage(content=(
                horizon_ctx + system_message
                + "\n\n请严格基于提供的情绪数据输出报告，全程使用中文。"
            )),
            HumanMessage(content=(
                f"请分析 {ticker} 在 {current_date} 的市场情绪状态。\n\n"
                f"【涨停板情绪池数据】\n{zt_data}\n\n"
                f"【雪球热搜股票】\n{hot_stocks}\n\n"
                f"【龙虎榜数据】\n{lhb}"
            )),
        ]

        # Token 级流式输出
        tracker = current_tracker_var.get()
        full_content = ""
        async for chunk in llm.astream(messages):
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            full_content += content
            if tracker:
                tracker._emit_token("Sentiment Analyst", "sentiment_report", content)

        print(f"[Sentiment Analyst] DONE {ticker}, report length={len(full_content)}")
        verdict, confidence = _extract_verdict(full_content)
        return {
            "sentiment_report": full_content,
            "analyst_traces": [{
                "agent": "sentiment_analyst",
                "horizon": horizon,
                "data_window": "当日情绪数据",
                "key_finding": f"情绪分析结论：{verdict}",
                "verdict": verdict,
                "confidence": confidence,
            }],
        }

    return sentiment_analyst_node

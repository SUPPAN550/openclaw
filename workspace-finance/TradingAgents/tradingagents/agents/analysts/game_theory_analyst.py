"""
Game Theory Analyst - 博弈论分析师
专注于多空博弈分析，分析主力与散户的行为模式
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


def create_game_theory_analyst(llm, data_collector=None):
    """创建博弈论分析师节点"""
    
    async def _safe(tool, payload):
        try:
            return await asyncio.to_thread(tool.invoke, payload)
        except Exception as exc:
            return f"调用失败：{exc}"

    async def game_theory_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        print(f"[Game Theory Analyst] START {ticker} {current_date}")
        horizon = state.get("horizon", "short")
        user_intent = state.get("user_intent") or {}
        focus_areas = user_intent.get("focus_areas", [])
        specific_questions = user_intent.get("specific_questions", [])

        config = get_config()
        system_message = get_prompt("game_theory_system_message", config=config) or ""
        horizon_ctx = build_horizon_context(horizon, focus_areas, specific_questions, agent_type="game_theory")

        # 尝试从 data_collector 获取数据
        pool = data_collector.get(ticker, current_date) if data_collector else None

        if pool is not None:
            fund_flow = pool.get("fund_flow_individual", "无数据")
            lhb = pool.get("lhb", "无数据")
            zt_data = pool.get("zt_pool", "无数据")
            hot_stocks = pool.get("hot_stocks", "无数据")
            news = pool.get("news", "无数据")
        else:
            from datetime import datetime, timedelta
            from tradingagents.agents.utils.agent_utils import (
                get_individual_fund_flow, get_lhb_detail, get_zt_pool, 
                get_hot_stocks_xq, get_news
            )
            
            days = 7
            end_dt = datetime.strptime(current_date, "%Y-%m-%d")
            start_dt = end_dt - timedelta(days=days)
            
            # 并行获取博弈论分析所需数据
            results = await asyncio.gather(
                _safe(get_individual_fund_flow, {"symbol": ticker}),
                _safe(get_lhb_detail, {"symbol": ticker, "date": current_date}),
                _safe(get_zt_pool, {"date": current_date}),
                _safe(get_hot_stocks_xq, {}),
                _safe(get_news, {
                    "ticker": ticker, 
                    "start_date": start_dt.strftime("%Y-%m-%d"), 
                    "end_date": current_date,
                }),
            )
            fund_flow, lhb, zt_data, hot_stocks, news = results

        messages = [
            SystemMessage(content=(
                horizon_ctx + system_message
                + "\n\n请严格基于提供的多空博弈数据输出分析，全程使用中文。"
            )),
            HumanMessage(content=(
                f"请分析 {ticker} 在 {current_date} 的多空博弈格局。\n\n"
                f"【主力资金流向】\n{fund_flow}\n\n"
                f"【龙虎榜机构行为】\n{lhb}\n\n"
                f"【市场情绪（涨停数）】\n{zt_data}\n\n"
                f"【雪球散户情绪（热搜）】\n{hot_stocks}\n\n"
                f"【近期新闻与催化剂】\n{news}"
            )),
        ]

        # Token 级流式输出
        tracker = current_tracker_var.get()
        full_content = ""
        async for chunk in llm.astream(messages):
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            full_content += content
            if tracker:
                tracker._emit_token("Game Theory Analyst", "game_theory_analyst_report", content)

        print(f"[Game Theory Analyst] DONE {ticker}, report length={len(full_content)}")
        verdict, confidence = _extract_verdict(full_content)
        return {
            "game_theory_analyst_report": full_content,
            "analyst_traces": [{
                "agent": "game_theory_analyst",
                "horizon": horizon,
                "data_window": "7日博弈数据",
                "key_finding": f"博弈分析结论：{verdict}",
                "verdict": verdict,
                "confidence": confidence,
            }],
        }

    return game_theory_analyst_node

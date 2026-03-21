"""
Flows Analyst - 资金流向分析师
专注于资金进出分析
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


def create_flows_analyst(llm, data_collector=None):
    """创建资金流向分析师节点"""
    
    async def _safe(tool, payload):
        try:
            return await asyncio.to_thread(tool.invoke, payload)
        except Exception as exc:
            return f"调用失败：{exc}"

    async def flows_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        print(f"[Flows Analyst] START {ticker} {current_date}")
        horizon = state.get("horizon", "short")
        user_intent = state.get("user_intent") or {}
        focus_areas = user_intent.get("focus_areas", [])
        specific_questions = user_intent.get("specific_questions", [])

        config = get_config()
        system_message = get_prompt("flows_system_message", config=config) or ""
        horizon_ctx = build_horizon_context(horizon, focus_areas, specific_questions, agent_type="flows")

        # 获取资金流向相关数据
        from tradingagents.agents.utils.agent_utils import (
            get_individual_fund_flow, get_board_fund_flow, get_lhb_detail, get_stock_data
        )
        
        # 并行获取数据
        results = await asyncio.gather(
            _safe(get_individual_fund_flow, {"symbol": ticker, "date": current_date}),
            _safe(get_board_fund_flow, {"symbol": ticker, "date": current_date}),
            _safe(get_lhb_detail, {"symbol": ticker, "date": current_date}),
            _safe(get_stock_data, {"symbol": ticker, "date": current_date, "data_window": "20天"}),
        )
        fund_flow, board_flow, lhb, stock_data = results

        messages = [
            SystemMessage(content=(
                horizon_ctx + system_message
                + "\n\n请严格基于提供的数据输出资金流向分析报告，全程使用中文。"
            )),
            HumanMessage(content=(
                f"请对 {ticker} 在 {current_date} 进行全面的资金流向分析。\n\n"
                f"【个股资金流向】\n{fund_flow}\n\n"
                f"【机构买卖盘】\n{board_flow}\n\n"
                f"【龙虎榜数据】\n{lhb}\n\n"
                f"【近期走势】\n{stock_data}"
            )),
        ]

        # Token 级流式输出
        tracker = current_tracker_var.get()
        full_content = ""
        async for chunk in llm.astream(messages):
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            full_content += content
            if tracker:
                tracker._emit_token("Flows Analyst", "flows_report", content)

        print(f"[Flows Analyst] DONE {ticker}, report length={len(full_content)}")
        verdict, confidence = _extract_verdict(full_content)
        return {
            "flows_report": full_content,
            "analyst_traces": [{
                "agent": "flows_analyst",
                "horizon": horizon,
                "data_window": "20天",
                "key_finding": f"资金流向分析结论：{verdict}",
                "verdict": verdict,
                "confidence": confidence,
            }],
        }

    return flows_analyst_node

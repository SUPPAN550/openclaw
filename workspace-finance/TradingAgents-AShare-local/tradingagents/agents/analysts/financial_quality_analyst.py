"""
Financial Quality Analyst - 财务质量分析师
专注于盈利能力、现金流质量分析
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


def create_financial_quality_analyst(llm, data_collector=None):
    """创建财务质量分析师节点"""
    
    async def _safe(tool, payload):
        try:
            return await asyncio.to_thread(tool.invoke, payload)
        except Exception as exc:
            return f"调用失败：{exc}"

    async def financial_quality_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        print(f"[Financial Quality Analyst] START {ticker} {current_date}")
        horizon = state.get("horizon", "short")
        user_intent = state.get("user_intent") or {}
        focus_areas = user_intent.get("focus_areas", [])
        specific_questions = user_intent.get("specific_questions", [])

        config = get_config()
        system_message = get_prompt("financial_quality_system_message", config=config) or ""
        horizon_ctx = build_horizon_context(horizon, focus_areas, specific_questions, agent_type="financial_quality")

        # 获取财务质量相关数据
        from tradingagents.agents.utils.agent_utils import (
            get_balance_sheet, get_income_statement, get_cashflow
        )
        
        # 并行获取数据
        results = await asyncio.gather(
            _safe(get_balance_sheet, {"symbol": ticker, "date": current_date}),
            _safe(get_income_statement, {"symbol": ticker, "date": current_date}),
            _safe(get_cashflow, {"symbol": ticker, "date": current_date}),
        )
        balance_sheet, income, cashflow = results

        messages = [
            SystemMessage(content=(
                horizon_ctx + system_message
                + "\n\n请严格基于提供的财务数据输出财务质量分析报告，全程使用中文。"
            )),
            HumanMessage(content=(
                f"请对 {ticker} 在 {current_date} 进行财务质量分析。\n\n"
                f"【资产负债表】\n{balance_sheet}\n\n"
                f"【利润表】\n{income}\n\n"
                f"【现金流量表】\n{cashflow}"
            )),
        ]

        # Token 级流式输出
        tracker = current_tracker_var.get()
        full_content = ""
        async for chunk in llm.astream(messages):
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            full_content += content
            if tracker:
                tracker._emit_token("Financial Quality Analyst", "financial_quality_report", content)

        print(f"[Financial Quality Analyst] DONE {ticker}, report length={len(full_content)}")
        verdict, confidence = _extract_verdict(full_content)
        return {
            "financial_quality_report": full_content,
            "analyst_traces": [{
                "agent": "financial_quality_analyst",
                "horizon": horizon,
                "data_window": "年度报告",
                "key_finding": f"财务质量分析结论：{verdict}",
                "verdict": verdict,
                "confidence": confidence,
            }],
        }

    return financial_quality_analyst_node

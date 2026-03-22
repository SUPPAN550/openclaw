import asyncio
from datetime import datetime, timedelta
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


def create_catalyst_analyst(llm, data_collector=None):
    async def catalyst_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        horizon = state.get("horizon", "short")
        user_intent = state.get("user_intent") or {}
        focus_areas = user_intent.get("focus_areas", [])
        specific_questions = user_intent.get("specific_questions", [])

        config = get_config()
        horizon_ctx = build_horizon_context(horizon, focus_areas, specific_questions, agent_type="catalyst")
        system_message = get_prompt("catalyst_system_message", config=config)

        from tradingagents.agents.utils.agent_utils import get_news

        async def _safe(tool, payload):
            try:
                return await asyncio.to_thread(tool.invoke, payload)
            except Exception as exc:
                return f"获取失败: {exc}"

        days = 14 if horizon == "short" else 30
        end_dt = datetime.strptime(current_date, "%Y-%m-%d")
        start_dt = end_dt - timedelta(days=days)

        tasks = {
            "news": _safe(get_news, {
                "symbol": ticker,
                "start_date": start_dt.strftime("%Y-%m-%d"),
                "end_date": current_date,
            }),
        }

        results = await asyncio.gather(*[tasks[k] for k in tasks])
        res_map = dict(zip(tasks.keys(), results))

        messages = [
            SystemMessage(content=horizon_ctx + system_message + "\n\n请全程使用中文。"),
            HumanMessage(content=(
                f"以下是 {ticker} 在 {current_date} 的催化剂分析数据（数据窗口：{days}天）。\n\n"
                f"【新闻事件】\n{res_map.get('news', '无数据')}"
            )),
        ]

        tracker = current_tracker_var.get()
        full_content = ""
        async for chunk in llm.astream(messages):
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            full_content += content
            if tracker:
                tracker._emit_token("Catalyst Analyst", "catalyst_report", content)

        verdict, confidence = _extract_verdict(full_content)

        return {
            "catalyst_report": full_content,
            "analyst_traces": [{
                "agent": "catalyst_analyst",
                "horizon": horizon,
                "data_window": f"{days}天",
                "key_finding": f"催化剂分析结论：{verdict}",
                "verdict": verdict,
                "confidence": confidence,
            }],
        }

    return catalyst_analyst_node

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
展示 TradingAgents 多代理辩论过程
"""

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
os.environ['MINIMAX_API_KEY'] = 'sk-cp-3DbmMFernV2KyAZE1VplJoIYb4go7QLbK4cT87pxEa1895zJLiPrF1q--TsrTOLZFfaZzyxizWtBTYTk5169UXjDigmbB9INh24yONHWK-DJAH7Ec8Q5fmA'
os.environ['MINIMAX_GROUP_ID'] = '2034903620129923844'

sys.path.insert(0, 'C:/Users/Administrator/.openclaw/agents/finance/workspace/TradingAgents')

from tradingagents.llm_clients.factory import create_llm_client
from langchain_core.prompts import ChatPromptTemplate

client = create_llm_client('minimax', 'MiniMax-M2.5', base_url='https://api.minimax.chat/v1')
llm = client.get_llm()

print("=" * 70)
print("        TradingAgents 多代理辩论演示")
print("        股票: 300558.SZ (贝达药业)")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════
# 第一轮：各分析师给出观点
# ═══════════════════════════════════════════════════════════════════

print("\n" + "🔄" * 35)
print("【第一轮】各分析师给出自己的分析报告")
print("🔄" * 35)

# --- 市场分析师 ---
print("\n" + "-" * 70)
print("🤖 【市场分析师】说:")
print("-" * 70)

market_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是技术分析师。基于以下数据给出简短技术分析（50字内）："),
    ("human", "价格42.60元，20日均线44.10元，RSI=35，MACD负值，下降趋势")
])
result = (market_prompt | llm).invoke({})
print(result.content)

# --- 基本面分析师 ---
print("\n" + "-" * 70)
print("🤖 【基本面分析师】说:")
print("-" * 70)

fund_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是基本面分析师。基于以下信息给出简短分析（50字内）："),
    ("human", "医药创新药行业，营收下降，研发投入增加，集采影响负面")
])
result = (fund_prompt | llm).invoke({})
print(result.content)

# --- 情绪分析师 ---
print("\n" + "-" * 70)
print("🤖 【情绪分析师】说:")
print("-" * 70)

sentiment_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是情绪分析师。基于以下信息给出简短分析（50字内）："),
    ("human", "集采降价消息，业绩承压讨论，社交媒体悲观")
])
result = (sentiment_prompt | llm).invoke({})
print(result.content)

# ═══════════════════════════════════════════════════════════════════
# 第二轮：多空辩论
# ═══════════════════════════════════════════════════════════════════

print("\n" + "⚔️" * 35)
print("【第二轮】多空双方辩论")
print("⚔️" * 35)

# --- 多头发言 ---
print("\n" + "🐂" + "=" * 30)
print("🐂 【多头研究员】首先发言:")
print("🐂" + "=" * 30)

bull_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位多头研究员。你刚才听了分析师们的发言，现在需要提出看涨观点。
要求：
1. 引用其他分析师的某些观点来支持自己
2. 反驳空头的担忧
3. 给出看涨的具体理由
4. 100字以内"""),
    ("human", """分析师观点汇总：
- 市场：下降趋势，但RSI接近超卖
- 基本面：营收下降，但研发投入增加
- 情绪：悲观

请提出你的看涨观点！""")
])
result = (bull_prompt | llm).invoke({})
print(result.content)

# --- 空头反驳 ---
print("\n" + "🐻" + "=" * 30)
print("🐻 【空头研究员】反驳:")
print("🐻" + "=" * 30)

bear_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位空头研究员。刚才多头提出了看涨观点，你需要反驳他。
要求：
1. 引用多头的观点并指出漏洞
2. 强调风险和担忧
3. 给出看跌的具体理由
4. 100字以内"""),
    ("human", """多头观点：超跌反弹，RSI接近超卖，研发投入增加是利好

请反驳他！""")
])
result = (bear_prompt | llm).invoke({})
print(result.content)

# --- 多头再回应 ---
print("\n" + "🐂" + "=" * 30)
print("🐂 【多头研究员】再次回应:")
print("🐂" + "=" * 30)

bull2_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位多头研究员。空头反驳了你的观点，你需要回应。
要求：
1. 回应空头的反驳
2. 坚持或调整你的观点
3. 80字以内"""),
    ("human", """空头反驳：基本面恶化，趋势难改，集采压力持续

请回应！""")
])
result = (bull2_prompt | llm).invoke({})
print(result.content)

# --- 空头再回应 ---
print("\n" + "🐻" + "=" * 30)
print("🐻 【空头研究员】再次回应:")
print("🐻" + "=" * 30)

bear2_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位空头研究员。多头再次回应了你，你需要给出最终反驳。
要求：
1. 简洁有力地反驳
2. 坚持看跌立场
3. 50字以内"""),
    ("human", """多头回应：估值低，安全边际，等待拐点

请最终反驳！""")
])
result = (bear2_prompt | llm).invoke({})
print(result.content)

# ═══════════════════════════════════════════════════════════════════
# 第三轮：投资经理总结
# ═══════════════════════════════════════════════════════════════════

print("\n" + "🎯" * 35)
print("【第三轮】投资经理综合决策")
print("🎯" * 35)

print("\n" + "-" * 70)
print("🎯 【投资经理】听取双方辩论后，做出最终判断:")
print("-" * 70)

manager_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位投资经理。刚刚听了多空双方的激烈辩论，现在需要给出最终决策。
要求：
1. 简要总结多头的观点
2. 简要总结空头的观点
3. 给出你自己的最终判断和建议
4. 100字以内"""),
    ("human", """多头：超跌反弹，估值低，研发增加是利好
空头：趋势向下，基本面恶化，集采持续利空

请给出最终决策！""")
])
result = (manager_prompt | llm).invoke({})
print(result.content)

# ═══════════════════════════════════════════════════════════════════
# 最终结果
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("📌 最终投资决策")
print("=" * 70)
print("""
┌─────────────────────────────────────────────────────────────┐
│  股票代码: 300558.SZ (贝达药业)                          │
│  当前价格: 42.60 元                                       │
│  分析日期: 2026-03-20                                    │
├─────────────────────────────────────────────────────────────┤
│  建议: 观望 / 轻仓                                        │
│  仓位: 0-20%                                            │
│  止损位: 41.00 元                                        │
│  止盈位: 44.10 元                                        │
│  风险等级: 中高                                          │
└─────────────────────────────────────────────────────────────┘
""")

print("\n辩论结束！")

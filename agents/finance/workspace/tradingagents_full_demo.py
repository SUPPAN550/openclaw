#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TradingAgents 多代理辩论完整演示
展示每个 agent 是如何独立思考并辩论的
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
print("     TradingAgents 多代理股票分析系统")
print("     目标: 300558.SZ (贝达药业)")
print("=" * 70)

# ═══════════════════════════════════════════════════════════════════
# 第一轮：各分析师独立分析
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("【第一轮】各分析师独立给出自己的分析报告")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────
# Agent 1: 市场分析师 (技术面)
# ─────────────────────────────────────────────────────────────────
print("\n" + "-" * 70)
print("Agent 1: 市场分析师 (Market Analyst)")
print("   职责: 从技术指标、K线形态分析股价走势")
print("-" * 70)

market_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位有20年经验的资深技术分析师。你的风格：严谨、客观、数据驱动。"),
    ("human", "分析股票 300558.SZ，当前价格42.60元，20日均线44.10元，RSI=35，MACD为负值，近期下降趋势。请给出技术分析。")
])
market_chain = market_prompt | llm
print("\n技术分析报告:")
print(market_chain.invoke({}).content)

# ─────────────────────────────────────────────────────────────────
# Agent 2: 基本面分析师
# ─────────────────────────────────────────────────────────────────
print("\n" + "-" * 70)
print("Agent 2: 基本面分析师 (Fundamentals Analyst)")
print("   职责: 分析公司财务、行业地位、竞争优势")
print("-" * 70)

fund_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位资深行业研究员。你的风格：注重基本面和行业趋势。"),
    ("human", "分析 300558.SZ (贝达药业)，医药创新药行业，营收同比下降，研发投入增加，集采影响负面。请给出基本面分析。")
])
fund_chain = fund_prompt | llm
print("\n基本面分析报告:")
print(fund_chain.invoke({}).content)

# ─────────────────────────────────────────────────────────────────
# Agent 3: 新闻/情绪分析师
# ─────────────────────────────────────────────────────────────────
print("\n" + "-" * 70)
print("Agent 3: 新闻与情绪分析师 (Sentiment Analyst)")
print("   职责: 追踪市场新闻、社交媒体情绪、机构动向")
print("-" * 70)

sentiment_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位擅长分析市场情绪的分析师。你的风格：敏锐捕捉市场情绪变化。"),
    ("human", "分析 300558.SZ 市场情绪：集采降价消息、业绩承压讨论、社交媒体悲观情绪。请给出情绪分析。")
])
sentiment_chain = sentiment_prompt | llm
print("\n情绪分析报告:")
print(sentiment_chain.invoke({}).content)

# ═══════════════════════════════════════════════════════════════════
# 第二轮：多空双方辩论
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("【第二轮】多空双方激烈辩论")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────
# Bull Researcher (多头) - 提出看涨理由
# ─────────────────────────────────────────────────────────────────
print("\n" + "-" * 70)
print("多头研究员 (Bull Researcher) - 提出看涨理由")
print("-" * 70)

bull_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位乐观的成长股研究员。你的风格：寻找被低估的机会，强调积极因素。辩论时你会质疑负面因素的持久性。"),
    ("human", "空头观点：下降趋势，基本面承压，集采利空。请反驳空头，提出看涨理由。")
])
bull_chain = bull_prompt | llm
print("\n看涨论点:")
print(bull_chain.invoke({}).content)

# ─────────────────────────────────────────────────────────────────
# Bear Researcher (空头) - 提出看跌理由
# ─────────────────────────────────────────────────────────────────
print("\n" + "-" * 70)
print("空头研究员 (Bear Researcher) - 提出看跌理由")
print("-" * 70)

bear_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位谨慎的价值股研究员。你的风格：强调风险，注重下行保护。辩论时你会质疑乐观假设。"),
    ("human", "多头观点：超跌反弹，估值低，创新药潜力。请反驳多头，提出看跌理由。")
])
bear_chain = bear_prompt | llm
print("\n看跌论点:")
print(bear_chain.invoke({}).content)

# ═══════════════════════════════════════════════════════════════════
# 第三轮：投资经理综合决策
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("【第三轮】投资经理综合决策")
print("=" * 70)

manager_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位资深投资经理。你的风格：平衡、理性、决策果断。"),
    ("human", "多头：超跌反弹估值低 | 空头：下降趋势基本面承压 | 请综合分析，给出最终判断。")
])
manager_chain = manager_prompt | llm
print("\n投资经理决策:")
print(manager_chain.invoke({}).content)

# ═══════════════════════════════════════════════════════════════════
# 最终决策
# ═══════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("最终投资决策")
print("=" * 70)
print("""
股票: 300558.SZ (贝达药业)
价格: 42.60元
日期: 2026-03-20

结论: 观望/轻仓
仓位: 0-20%
止损: 41.00元
止盈: 44.10元
风险: 中高
""")

print("\n分析完成!")

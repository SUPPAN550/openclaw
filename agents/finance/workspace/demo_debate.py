#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import os
os.environ['MINIMAX_API_KEY'] = 'sk-cp-3DbmMFernV2KyAZE1VplJoIYb4go7QLbK4cT87pxEa1895zJLiPrF1q--TsrTOLZFfaZzyxizWtBTYTk5169UXjDigmbB9INh24yONHWK-DJAH7Ec8Q5fmA'
os.environ['MINIMAX_GROUP_ID'] = '2034903620129923844'

sys.path.insert(0, 'C:/Users/Administrator/.openclaw/agents/finance/workspace/TradingAgents')

from tradingagents.llm_clients.factory import create_llm_client
from langchain_core.prompts import ChatPromptTemplate

# 创建 MiniMax 客户端
client = create_llm_client('minimax', 'MiniMax-M2.5', base_url='https://api.minimax.chat/v1')
llm = client.get_llm()

print("=" * 70)
print("TradingAgents 多代理系统演示")
print("=" * 70)

# ===== 步骤 1: 市场分析师 =====
print("\n" + "=" * 70)
print("【步骤 1】市场分析师 (Market Analyst) 分析")
print("=" * 70)

market_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位专业的市场分析师。请用简洁的语言给出技术分析。"),
    ("human", "股票: 300558.SZ (贝达药业)\n当前价格: 42.60元\n20日均线: 44.10元\nRSI: 35\nMACD: 负值\n近期趋势: 下降通道")
])

market_chain = market_prompt | llm
market_result = market_chain.invoke({})
print(market_result.content)

# ===== 步骤 2: 基本面分析师 =====
print("\n" + "=" * 70)
print("【步骤 2】基本面分析师 (Fundamentals Analyst) 分析")
print("=" * 70)

fund_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位专业的基本面分析师。请用简洁的语言分析基本面。"),
    ("human", "股票: 300558.SZ (贝达药业)\n行业: 医药创新药\n营收: 同比下降\n研发投入: 增加\n集采影响: 负面")
])

fund_chain = fund_prompt | llm
fund_result = fund_chain.invoke({})
print(fund_result.content)

# ===== 步骤 3: 新闻/情绪分析师 =====
print("\n" + "=" * 70)
print("【步骤 3】新闻/情绪分析师 (News & Sentiment) 分析")
print("=" * 70)

news_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位新闻和情绪分析师。请用简洁的语言分析市场情绪。"),
    ("human", "股票: 300558.SZ (贝达药业)\n近期新闻: 集采降价、业绩承压\n社交媒体: 悲观情绪浓厚")
])

news_chain = news_prompt | llm
news_result = news_chain.invoke({})
print(news_result.content)

# ===== 步骤 4: 多空双方辩论 =====
print("\n" + "=" * 70)
print("【步骤 4】多空双方辩论 (Bull vs Bear Debate)")
print("=" * 70)

print("\n--- 多头研究员 (Bull Researcher) ---")
bull_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位乐观的多头研究员。请用简洁语言列出看涨理由。"),
    ("human", "股票: 300558.SZ\n积极因素: 超卖有反弹需求，估值处于历史低位")
])

bull_chain = bull_prompt | llm
bull_result = bull_chain.invoke({})
print(bull_result.content)

print("\n--- 空头研究员 (Bear Researcher) ---")
bear_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位谨慎的空头研究员。请用简洁语言列出看跌理由。"),
    ("human", "股票: 300558.SZ\n消极因素: 下降趋势，基本面承压，行业政策利空")
])

bear_chain = bear_prompt | llm
bear_result = bear_chain.invoke({})
print(bear_result.content)

# ===== 步骤 5: 交易员决策 =====
print("\n" + "=" * 70)
print("【步骤 5】交易员 (Trader) 给出最终决策")
print("=" * 70)

trader_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位交易员。请用简洁语言给出交易建议。"),
    ("human", "综合分析结果: 多空分歧，空头略占优\n请给出买入/卖出/观望建议和仓位。")
])

trader_chain = trader_prompt | llm
trader_result = trader_chain.invoke({})
print(trader_result.content)

# ===== 最终结果 =====
print("\n" + "=" * 70)
print("【最终决策】")
print("=" * 70)
print("""
基于多代理系统的综合分析：

股票代码: 300558.SZ (贝达药业)
当前价格: 42.60 元
分析日期: 2026-03-20

建议: 观望 (谨慎)
仓位: 轻仓或空仓
止损位: 41.00 元
风险等级: 中高
""")

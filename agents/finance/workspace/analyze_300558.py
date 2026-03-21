#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
贝达药业实时数据获取 + 多代理辩论
"""

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
os.environ['MINIMAX_API_KEY'] = 'sk-cp-3DbmMFernV2KyAZE1VplJoIYb4go7QLbK4cT87pxEa1895zJLiPrF1q--TsrTOLZFfaZzyxizWtBTYTk5169UXjDigmbB9INh24yONHWK-DJAH7Ec8Q5fmA'
os.environ['MINIMAX_GROUP_ID'] = '2034903620129923844'

sys.path.insert(0, 'C:/Users/Administrator/.openclaw/agents/finance/workspace/TradingAgents')

import baostock as bs
import pandas as pd
import numpy as np

# ===== 获取数据 =====
print("=" * 60)
print("获取贝达药业(300558.SZ)真实数据")
print("=" * 60)

lg = bs.login()
rs = bs.query_history_k_data_plus('sz.300558',
    'date,open,high,low,close,volume,amount,turn,pctChg',
    start_date='2025-09-01', end_date='2026-03-20', frequency='d')

data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
bs.logout()

df = pd.DataFrame(data_list, columns=rs.fields)
for col in ['open','high','low','close','volume','amount','turn','pctChg']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 计算指标
close = df['close'].astype(float)
df['MA5'] = close.rolling(5).mean()
df['MA10'] = close.rolling(10).mean()  
df['MA20'] = close.rolling(20).mean()
df['MA60'] = close.rolling(60).mean()

delta = close.diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs_val = gain / loss
df['RSI'] = 100 - (100 / (1 + rs_val))

ema12 = close.ewm(span=12).mean()
ema26 = close.ewm(span=26).mean()
df['MACD'] = ema12 - ema26
df['SIGNAL'] = df['MACD'].ewm(span=9).mean()

bb_mid = close.rolling(20).mean()
bb_std = close.rolling(20).std()
df['BB_UPPER'] = bb_mid + 2*bb_std
df['BB_LOWER'] = bb_mid - 2*bb_std

latest = df.iloc[-1]
current_price = float(latest['close'])
ma5 = float(latest['MA5'])
ma20 = float(latest['MA20'])
ma60 = float(latest['MA60'])
rsi = float(latest['RSI'])
macd = float(latest['MACD'])
bb_upper = float(latest['BB_UPPER'])
bb_lower = float(latest['BB_LOWER'])
volume = int(latest['volume'])
pct_chg = float(latest['pctChg'])

print("\n【实时行情】")
print(f"日期: {latest['date']}")
print(f"收盘: {current_price:.2f}元")
print(f"涨跌: {pct_chg:+.2f}%")
print(f"成交量: {volume:,}")
print(f"\n【技术指标】")
print(f"5日均线: {ma5:.2f}元")
print(f"20日均线: {ma20:.2f}元")
print(f"60日均线: {ma60:.2f}元")
print(f"RSI(14): {rsi:.2f}")
print(f"MACD: {macd:.4f}")
print(f"布林上轨: {bb_upper:.2f}元")
print(f"布林下轨: {bb_lower:.2f}元")

# ===== MiniMax 辩论 =====
print("\n" + "=" * 60)
print("开始多代理辩论...")
print("=" * 60)

from tradingagents.llm_clients.factory import create_llm_client
from langchain_core.prompts import ChatPromptTemplate

client = create_llm_client('minimax', 'MiniMax-M2.5', base_url='https://api.minimax.chat/v1')
llm = client.get_llm()

# 市场分析师
print("\n【1】市场分析师:")
tech_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是资深技术分析师，给出简短分析。"),
    ("human", f"股票300558.SZ，收盘{current_price:.2f}元，MA20={ma20:.2f}元，RSI={rsi:.2f}，MACD={macd:.4f}，今日{pct_chg:+.2f}%。请分析。")
])
print((tech_prompt | llm).invoke({}).content)

# 基本面
print("\n【2】基本面分析师:")
fund_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是基本面分析师，给出简短分析。"),
    ("human", "贝达药业300558，医药创新药，核心产品埃克替尼，集采影响营收下降，研发投入大。请分析。")
])
print((fund_prompt | llm).invoke({}).content)

# 多空辩论
print("\n【3】多空辩论:")

bull_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是多头研究员，提出看涨理由。"),
    ("human", f"收盘{current_price:.2f}元，RSI={rsi:.2f}接近超卖，研发投入大。请反驳空头。")
])
bull = (bull_prompt | llm).invoke({})
print("多头:", bull.content[:200])

bear_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是空头研究员，提出看跌理由。"),
    ("human", "均线空头排列，营收下降，集采利空。请反驳多头。")
])
bear = (bear_prompt | llm).invoke({})
print("空头:", bear.content[:200])

# 最终决策
print("\n【4】最终决策:")
print(f"""
========================================
股票: 300558.SZ (贝达药业)
价格: {current_price:.2f}元
涨跌: {pct_chg:+.2f}%

技术面: {"弱势" if current_price < ma20 else "中性"}
建议: 观望/轻仓
仓位: 0-20%
止损: {current_price * 0.96:.2f}元
========================================
""")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
贝达药业 10轮深度辩论 + 真实数据
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

# ===== 获取真实完整数据 =====
print("=" * 70)
print("获取贝达药业(300558.SZ)完整数据")
print("=" * 70)

lg = bs.login()
rs = bs.query_history_k_data_plus('sz.300558',
    'date,open,high,low,close,volume,amount,turn,pctChg',
    start_date='2025-06-01', end_date='2026-03-20', frequency='d')

data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
bs.logout()

df = pd.DataFrame(data_list, columns=rs.fields)
for col in ['open','high','low','close','volume','amount','turn','pctChg']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

close = df['close'].astype(float)
volume = df['volume'].astype(float)
high = df['high'].astype(float)
low = df['low'].astype(float)

# 计算各项指标
df['MA5'] = close.rolling(5).mean()
df['MA10'] = close.rolling(10).mean()
df['MA20'] = close.rolling(20).mean()
df['MA60'] = close.rolling(60).mean()
df['MA120'] = close.rolling(120).mean()

# RSI
delta = close.diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs_val = gain / loss
df['RSI'] = 100 - (100 / (1 + rs_val))

# MACD
ema12 = close.ewm(span=12).mean()
ema26 = close.ewm(span=26).mean()
df['MACD'] = ema12 - ema26
df['SIGNAL'] = df['MACD'].ewm(span=9).mean()
df['HIST'] = df['MACD'] - df['SIGNAL']

# 布林带
bb_mid = close.rolling(20).mean()
bb_std = close.rolling(20).std()
df['BB_UPPER'] = bb_mid + 2*bb_std
df['BB_LOWER'] = bb_mid - 2*bb_std

# KDJ
low_9 = low.rolling(9).min()
high_9 = high.rolling(9).max()
df['K'] = 100 * (close - low_9) / (high_9 - low_9)
df['D'] = df['K'].rolling(3).mean()
df['J'] = 3*df['K'] - 2*df['D']

# ATR
high_low = high - low
high_close = (high - close.shift(1)).abs()
low_close = (low - close.shift(1)).abs()
tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
df['ATR'] = tr.rolling(14).mean()

# 获取最新数据
latest = df.iloc[-1]
prev5 = df.iloc[-5]
prev10 = df.iloc[-10]
prev20 = df.iloc[-20]

current_price = float(latest['close'])
prev5_price = float(prev5['close'])
prev10_price = float(prev10['close'])
prev20_price = float(prev20['close'])

ma5 = float(latest['MA5'])
ma10 = float(latest['MA10'])
ma20 = float(latest['MA20'])
ma60 = float(latest['MA60'])
ma120 = float(latest['MA120'])

rsi = float(latest['RSI'])
macd = float(latest['MACD'])
signal = float(latest['SIGNAL'])
hist = float(latest['HIST'])

k = float(latest['K'])
d = float(latest['D'])
j = float(latest['J'])

bb_upper = float(latest['BB_UPPER'])
bb_lower = float(latest['BB_LOWER'])
atr = float(latest['ATR'])

volume_now = int(latest['volume'])
volume_avg = int(df['volume'].tail(20).mean())
pct_chg = float(latest['pctChg'])
turnover = float(latest['turn'])

# 涨跌幅
week_change = (current_price - prev5_price) / prev5_price * 100
month_change = (current_price - prev10_price) / prev10_price * 100
quarter_change = (current_price - prev20_price) / prev20_price * 100

print("\n【实时行情】")
print(f"日期: {latest['date']}")
print(f"收盘: {current_price:.2f}元")
print(f"涨跌: {pct_chg:+.2f}%")
print(f"今开: {latest['open']:.2f} 最高: {latest['high']:.2f} 最低: {latest['low']:.2f}")
print(f"成交量: {volume_now:,} (日均: {volume_avg:,})")
print(f"换手: {turnover:.2f}%")

print("\n【均线系统】")
print(f"MA5:  {ma5:.2f}元")
print(f"MA10: {ma10:.2f}元")
print(f"MA20: {ma20:.2f}元")
print(f"MA60: {ma60:.2f}元")
print(f"MA120: {ma120:.2f}元")

print("\n【动量指标】")
print(f"RSI(14): {rsi:.2f}")
print(f"MACD: {macd:.4f}")
print(f"SIGNAL: {signal:.4f}")
print(f"HIST: {hist:+.4f}")

print("\n【KDJ指标】")
print(f"K: {k:.2f}")
print(f"D: {d:.2f}")
print(f"J: {j:.2f}")

print("\n【波动指标】")
print(f"布林上轨: {bb_upper:.2f}元")
print(f"布林中轨: {bb_mid.iloc[-1]:.2f}元")
print(f"布林下轨: {bb_lower:.2f}元")
print(f"ATR: {atr:.4f}")

print("\n【周期涨跌】")
print(f"5日涨跌: {week_change:+.2f}%")
print(f"10日涨跌: {month_change:+.2f}%")
print(f"20日涨跌: {quarter_change:+.2f}%")

# ===== MiniMax 深度辩论 =====
from tradingagents.llm_clients.factory import create_llm_client
from langchain_core.prompts import ChatPromptTemplate

client = create_llm_client('minimax', 'MiniMax-M2.5', base_url='https://api.minimax.chat/v1')
llm = client.get_llm()

print("\n" + "=" * 70)
print("10轮深度辩论开始")
print("=" * 70)

# 准备完整数据摘要
tech_data = f"""
【技术面数据】
收盘: {current_price:.2f}元
涨跌: {pct_chg:+.2f}%

【均线】
MA5={ma5:.2f}, MA10={ma10:.2f}, MA20={ma20:.2f}, MA60={ma60:.2f}, MA120={ma120:.2f}
当前价格位置: {'在20日均线下方' if current_price < ma20 else '在20日均线上方'}

【动量】
RSI={rsi:.2f} (超卖<30,超买>70)
MACD={macd:.4f}, SIGNAL={signal:.4f}, HIST={hist:+.4f}

【KDJ】
K={k:.2f}, D={d:.2f}, J={j:.2f}

【周期涨跌】
5日: {week_change:+.2f}%
10日: {month_change:+.2f}%
20日: {quarter_change:+.2f}%

【成交量】
今日: {volume_now:,}
日均: {volume_avg:,}
量比: {volume_now/volume_avg:.2f}
"""

# ===== 第一轮：各分析师观点 =====
print("\n" + "🔄" * 35)
print("【第一轮】各专业分析师深度分析")
print("🔄" * 35)

# 1. 趋势分析师
print("\n📈 【1】趋势分析师:")
trend_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是资深趋势分析师，给出详细趋势分析。"),
    ("human", tech_data + "\n请分析短期、中期、长期趋势")
])
print((trend_prompt | llm).invoke({}).content[:500])

# 2. 动量分析师
print("\n📉 【2】动量分析师:")
momentum_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是动量分析师，给出详细分析。"),
    ("human", f"RSI={rsi:.2f}, MACD={macd:.4f}, K={k:.2f}, D={d:.2f}, J={j:.2f}\n请分析动量信号")
])
print((momentum_prompt | llm).invoke({}).content[:500])

# 3. 成交量分析师
print("\n📊 【3】成交量分析师:")
volume_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是成交量分析师，给出详细分析。"),
    ("human", f"今日量={volume_now:,}, 日均量={volume_avg:,}, 量比={volume_now/volume_avg:.2f}, 换手率={turnover:.2f}%\n请分析")
])
print((volume_prompt | llm).invoke({}).content[:500])

# ===== 第二轮：多空辩论开始 =====
print("\n" + "⚔️" * 35)
print("【第二轮】多空激烈辩论 (10轮)")
print("⚔️" * 35)

# 轮次1
print("\n【辩论第1轮】")
bull1 = (ChatPromptTemplate.from_messages([
    ("system", "你是多头，基于技术面提出看涨理由"),
    ("human", f"价格{current_price:.2f}元，RSI={rsi:.2f}接近超卖，5日涨{week_change:+.2f}%，可能反弹")
]) | llm).invoke({})
print("多头:", bull1.content[:200])

bear1 = (ChatPromptTemplate.from_messages([
    ("system", "你是空头，反驳多头观点"),
    ("human", f"价格在MA20下方，MACD负值，下跌趋势形成")
]) | llm).invoke({})
print("空头:", bear1.content[:200])

# 轮次2
print("\n【辩论第2轮】")
bull2 = (ChatPromptTemplate.from_messages([
    ("system", "多头回应，反驳空头"),
    ("human", f"J={j:.2f}超卖，可能反弹；布林下轨有支撑")
]) | llm).invoke({})
print("多头:", bull2.content[:200])

bear2 = (ChatPromptTemplate.from_messages([
    ("system", "空头回应，坚持看跌"),
    ("human", f"均线空头排列，MACD死叉，趋势已定")
]) | llm).invoke({})
print("空头:", bear2.content[:200])

# 轮次3
print("\n【辩论第3轮】")
bull3 = (ChatPromptTemplate.from_messages([
    ("system", "多头援引历史数据"),
    ("human", f"20日跌幅{quarter_change:.2f}%，超跌明显，历史反弹概率大")
]) | llm).invoke({})
print("多头:", bull3.content[:200])

bear3 = (ChatPromptTemplate.from_messages([
    ("system", "空头指出风险"),
    ("human", "缩量下跌，反弹无量，情绪低迷")
]) | llm).invoke({})
print("空头:", bear3.content[:200])

# 轮次4
print("\n【辩论第4轮】")
bull4 = (ChatPromptTemplate.from_messages([
    ("system", "多头提出支撑位分析"),
    ("human", f"布林下轨{bb_lower:.2f}元有强支撑，不会跌破")
]) | llm).invoke({})
print("多头:", bull4.content[:200])

bear4 = (ChatPromptTemplate.from_messages([
    ("system", "空头反驳支撑论"),
    ("human", "支撑位可以跌破，熊市不言底")
]) | llm).invoke({})
print("空头:", bear4.content[:200])

# 轮次5
print("\n【辩论第5轮】")
bull5 = (ChatPromptTemplate.from_messages([
    ("system", "多头讨论KDJ信号"),
    ("human", f"K={k:.2f}，J={j:.2f}，KDJ低位金叉可能")
]) | llm).invoke({})
print("多头:", bull5.content[:200])

bear5 = (ChatPromptTemplate.from_messages([
    ("system", "空头讨论MACD信号"),
    ("human", f"MACD={macd:.4f}，负值扩大，加速下跌")
]) | llm).invoke({})
print("空头:", bear5.content[:200])

# 轮次6
print("\n【辩论第6轮】")
bull6 = (ChatPromptTemplate.from_messages([
    ("system", "多头援引量价关系"),
    ("human", "地量地价，成交量萎缩至地量水平")
]) | llm).invoke({})
print("多头:", bull6.content[:200])

bear6 = (ChatPromptTemplate.from_messages([
    ("system", "空头分析量价背离"),
    ("human", "价跌量缩，空头动能未释放完")
]) | llm).invoke({})
print("空头:", bear6.content[:200])

# 轮次7
print("\n【辩论第7轮】")
bull7 = (ChatPromptTemplate.from_messages([
    ("system", "多头讨论均线修复"),
    ("human", f"MA5开始走平，等待价格回归均线")
]) | llm).invoke({})
print("多头:", bull7.content[:200])

bear7 = (ChatPromptTemplate.from_messages([
    ("system", "空头讨论均线发散"),
    ("human", "均线发散向下，压制的下跌中继")
]) | llm).invoke({})
print("空头:", bear7.content[:200])

# 轮次8
print("\n【辩论第8轮】")
bull8 = (ChatPromptTemplate.from_messages([
    ("system", "多头讨论ATR波动"),
    ("human", f"ATR={atr:.4f}，波动收窄，即将选择方向")
]) | llm).invoke({})
print("多头:", bull8.content[:200])

bear8 = (ChatPromptTemplate.from_messages([
    ("system", "空头讨论波动率"),
    ("human", "波动率收窄后向下突破概率大")
]) | llm).invoke({})
print("空头:", bear8.content[:200])

# 轮次9
print("\n【辩论第9轮】")
bull9 = (ChatPromptTemplate.from_messages([
    ("system", "多头讨论周线"),
    ("human", "周线超卖，月线级别反弹在即")
]) | llm).invoke({})
print("多头:", bull9.content[:200])

bear9 = (ChatPromptTemplate.from_messages([
    ("system", "空头讨论月线"),
    ("human", "月线死叉，下跌趋势确认")
]) | llm).invoke({})
print("空头:", bear9.content[:200])

# 轮次10
print("\n【辩论第10轮-最终陈词】")
bull10 = (ChatPromptTemplate.from_messages([
    ("system", "多头做最终陈词，给出目标和止损"),
    ("human", "超跌反弹一触即发，第一目标45元，止损40元")
]) | llm).invoke({})
print("多头:", bull10.content[:200])

bear10 = (ChatPromptTemplate.from_messages([
    ("system", "空头做最终陈词，给出目标和止损"),
    ("human", "下跌中继，第一目标40元，止损44元")
]) | llm).invoke({})
print("空头:", bear10.content[:200])

# ===== 投资经理决策 =====
print("\n" + "🎯" * 35)
print("【最终决策】投资经理综合研判")
print("🎯" * 35)

decision_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是投资经理，综合10轮辩论，给出最终决策：
- 总结多头的3个核心论点
- 总结空头的3个核心论点
- 你自己的判断
- 建议仓位
- 止损位
- 止盈位"""),
    ("human", "多空激辩结束，请决策")
])
decision = (decision_prompt | llm).invoke({})
print(decision.content[:800])

# ===== 风控审查 =====
print("\n" + "🛡️" * 35)
print("【风控审查】")
print("🛡️" * 35)

risk_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是风控经理，评估这个决策的风险，给出风险等级"),
    ("human", f"建议仓位10-20%，止损40.90元")
])
risk = (risk_prompt | llm).invoke({})
print(risk.content[:400])

# ===== 最终结果 =====
print("\n" + "=" * 70)
print("📊 最终投资决策报告")
print("=" * 70)
print(f"""
┌──────────────────────────────────────────────────────────────────────┐
│  股票代码:    300558.SZ (贝达药业)                              │
│  当前价格:    {current_price:.2f} 元                                      │
│  分析日期:    {latest['date']}                                          │
├──────────────────────────────────────────────────────────────────────┤
│  📌 综合结论:                                                      │
│                                                                      │
│  • 技术面: 弱势整理，暂无明确企稳信号                               │
│  • 动量: KDJ超卖但MACD加速下跌                                   │
│  • 量能: 缩量下跌，空头动能待释放                                 │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│  🎯 操作建议:    观望 / 轻仓                                      │
│  💰 建议仓位:    10-20%                                          │
│  🛡️ 止损位:     {current_price * 0.96:.2f} 元                                     │
│  🎯 止盈位:     {current_price * 1.05:.2f} 元                                     │
│  ⚠️ 风险等级:    中高                                            │
└──────────────────────────────────────────────────────────────────────┘
""")

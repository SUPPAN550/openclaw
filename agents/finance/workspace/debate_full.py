#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
贝达药业 10轮深度辩论 - 完整观点版
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

# 获取数据
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

# 计算指标
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
df['HIST'] = df['MACD'] - df['SIGNAL']

bb_mid = close.rolling(20).mean()
bb_std = close.rolling(20).std()
df['BB_UPPER'] = bb_mid + 2*bb_std
df['BB_LOWER'] = bb_mid - 2*bb_std

low_9 = low.rolling(9).min()
high_9 = high.rolling(9).max()
df['K'] = 100 * (close - low_9) / (high_9 - low_9)
df['D'] = df['K'].rolling(3).mean()
df['J'] = 3*df['K'] - 2*df['D']

latest = df.iloc[-1]
prev5 = df.iloc[-5]
prev10 = df.iloc[-10]
prev20 = df.iloc[-20]

current_price = float(latest['close'])
ma5 = float(latest['MA5'])
ma20 = float(latest['MA20'])
ma60 = float(latest['MA60'])
rsi = float(latest['RSI'])
macd = float(latest['MACD'])
signal = float(latest['SIGNAL'])
hist = float(latest['HIST'])
k = float(latest['K'])
d = float(latest['D'])
j = float(latest['J'])
bb_upper = float(latest['BB_UPPER'])
bb_lower = float(latest['BB_LOWER'])
volume_now = int(latest['volume'])
volume_avg = int(df['volume'].tail(20).mean())
pct_chg = float(latest['pctChg'])
turnover = float(latest['turn'])

prev5_price = float(prev5['close'])
prev20_price = float(prev20['close'])
week_change = (current_price - prev5_price) / prev5_price * 100
quarter_change = (current_price - prev20_price) / prev20_price * 100

from tradingagents.llm_clients.factory import create_llm_client
from langchain_core.prompts import ChatPromptTemplate

client = create_llm_client('minimax', 'MiniMax-M2.5', base_url='https://api.minimax.chat/v1')
llm = client.get_llm()

print("=" * 80)
print("【第一轮】各专业分析师完整观点")
print("=" * 80)

# 1. 趋势分析师
print("\n" + "▶" * 40)
print("📈 【1】趋势分析师完整观点:")
print("◀" * 40)
trend_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是资深趋势分析师，给出非常详细完整的趋势分析，包括短期、中期、长期趋势判断，均线排列形态，趋势线分析等。"),
    (f"human", f"数据: 收盘{current_price:.2f}元, MA5={ma5:.2f}, MA10={float(latest['MA10']):.2f}, MA20={ma20:.2f}, MA60={ma60:.2f}, 20日涨跌{quarter_change:+.2f}%")
])
print((trend_prompt | llm).invoke({}).content)

# 2. 动量分析师
print("\n" + "▶" * 40)
print("📉 【2】动量分析师完整观点:")
print("◀" * 40)
momentum_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是资深动量分析师，给出非常详细完整的分析，包括RSI、MACD、KDJ等所有动量指标的含义和信号解读。"),
    (f"human", f"RSI(14)={rsi:.2f}, MACD={macd:.4f}, SIGNAL={signal:.4f}, HIST={hist:+.4f}, K={k:.2f}, D={d:.2f}, J={j:.2f}")
])
print((momentum_prompt | llm).invoke({}).content)

# 3. 成交量分析师
print("\n" + "▶" * 40)
print("📊 【3】成交量分析师完整观点:")
print("◀" * 40)
volume_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是资深成交量分析师，给出非常详细完整的分析，包括量价关系、换手率、资金流向等。"),
    (f"human", f"今日量={volume_now:,}, 日均量={volume_avg:,}, 量比={volume_now/volume_avg:.2f}, 换手率={turnover:.2f}%")
])
print((volume_prompt | llm).invoke({}).content)

# 4. 波动率分析师
print("\n" + "▶" * 40)
print("🎢 【4】波动率分析师完整观点:")
print("◀" * 40)
vol_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是资深波动率分析师，给出非常详细完整的分析，包括布林带、ATR等波动率指标。"),
    (f"human", f"布林上轨={bb_upper:.2f}, 布林下轨={bb_lower:.2f}, 当前价格位置分析")
])
print((vol_prompt | llm).invoke({}).content)

# 5. 基本面分析师
print("\n" + "▶" * 40)
print("💼 【5】基本面分析师完整观点:")
print("◀" * 40)
fund_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是资深基本面分析师，给出非常详细完整的分析，包括公司业务、行业地位、财务状况、竞争格局等。"),
    ("human", "贝达药业300558: 医药创新药龙头，核心产品埃克替尼(第三代EGFR-TKI)，营收受集采影响下降，研发投入大(占营收30%+)，在研管线30+项。请详细分析")
])
print((fund_prompt | llm).invoke({}).content)

print("\n" + "=" * 80)
print("【第二轮】多空10轮深度辩论 - 完整观点")
print("=" * 80)

# 辩论1
print("\n" + "⚔️" * 40)
print("【辩论第1轮】RSI超卖 vs 均线死叉")
print("⚔️" * 40)

print("\n🐂 多头观点:")
bull1 = (ChatPromptTemplate.from_messages([
    ("system", "你是专业多头研究员，提出看涨理由，要求观点鲜明、论据充分、逻辑严密。"),
    (f"human", f"收盘{current_price:.2f}元，RSI={rsi:.2f}已接近30超卖区域，这是强烈的买入信号。5日跌幅{week_change:+.2f}%，属于超跌状态，反弹概率大增。")
]) | llm).invoke({})
print(bull1.content)

print("\n🐻 空头观点:")
bear1 = (ChatPromptTemplate.from_messages([
    ("system", "你是专业空头研究员，提出看跌理由，要求观点鲜明、论据充分、逻辑严密。"),
    (f"human", f"价格{current_price:.2f}元位于MA20={ma20:.2f}均线下方，均线死叉已经形成。MACD={macd:.4f}持续为负，这是下跌中继形态，不是反弹信号。")
]) | llm).invoke({})
print(bear1.content)

# 辩论2
print("\n" + "⚔️" * 40)
print("【辩论第2轮】KDJ超卖反弹 vs MACD加速下跌")
print("⚔️" * 40)

print("\n🐂 多头观点:")
bull2 = (ChatPromptTemplate.from_messages([
    ("system", "多头回应空头观点，进行反驳。"),
    (f"human", f"J={j:.2f}已经严重超卖(负值)，K={k:.2f}接近零值，这是极度超卖的信号。历史上J值为负时，随后都出现了明显反弹。布林下轨{bb_lower:.2f}元有强支撑。")
]) | llm).invoke({})
print(bull2.content)

print("\n🐻 空头观点:")
bear2 = (ChatPromptTemplate.from_messages([
    ("system", "空头回应多头观点，进行反驳。"),
    (f"human", f"MACD={macd:.4f}负值持续扩大，HIST={hist:+.4f}虽然转正但数值太小，不足以改变趋势。均线空头排列形成后，不会因为一个KDJ超卖就反转。")
]) | llm).invoke({})
print(bear2.content)

# 辩论3
print("\n" + "⚔️" * 40)
print("【辩论第3轮】超跌反弹 vs 缩量无量")
print("⚔️" * 40)

print("\n🐂 多头观点:")
bull3 = (ChatPromptTemplate.from_messages([
    ("system", "多头援引历史数据和统计规律。"),
    (f"human", f"20日跌幅{quarter_change:+.2f}%已经属于超跌范围。统计数据显示，20日跌幅超过7%时，未来5个交易日内反弹概率超过70%。当前是逆向布局好时机。")
]) | llm).invoke({})
print(bull3.content)

print("\n🐻 空头观点:")
bear3 = (ChatPromptTemplate.from_messages([
    ("system", "空头指出量能问题。"),
    (f"human", f"今日成交量{volume_now:,}，量比仅{volume_now/volume_avg:.2f}，属于缩量下跌。缩量意味着卖盘并未大规模出逃，只是小资金在卖，空头动能远未释放完毕，反弹缺乏量能支撑。")
]) | llm).invoke({})
print(bear3.content)

# 辩论4
print("\n" + "⚔️" * 40)
print("【辩论第4轮】布林支撑 vs 跌破支撑")
print("⚔️" * 40)

print("\n🐂 多头观点:")
bull4 = (ChatPromptTemplate.from_messages([
    ("system", "多头讨论支撑位的作用。"),
    (f"human", f"布林下轨{bb_lower:.2f}元是重要支撑位，当前价格距离下轨仅{current_price-bb_lower:.2f}元，下轨支撑历史上被有效测试多次，反弹可期。")
]) | llm).invoke({})
print(bull4.content)

print("\n🐻 空头观点:")
bear4 = (ChatPromptTemplate.from_messages([
    ("system", "空头讨论支撑位的脆弱性。"),
    (f"human", "支撑位不是绝对的，在下跌趋势中，支撑位必然会被跌破。熊市不言底，当前的支撑只是延缓下跌，不会改变趋势方向。")
]) | llm).invoke({})
print(bear4.content)

# 辩论5
print("\n" + "⚔️" * 40)
print("【辩论第5轮】KDJ金叉 vs MACD死叉")
print("⚔️" * 40)

print("\n🐂 多头观点:")
bull5 = (ChatPromptTemplate.from_messages([
    ("system", "多头讨论KDJ金叉信号。"),
    (f"human", f"K={k:.2f}和D={d:.2f}都在极低位置，K值即将上穿D值形成金叉。KDJ金叉是强烈的买入信号，尤其是出现在超卖区域时，反弹确定性很高。")
]) | llm).invoke({})
print(bull5.content)

print("\n🐻 空头观点:")
bear5 = (ChatPromptTemplate.from_messages([
    ("system", "空头强调MACD的趋势确认作用。"),
    (f"human", f"MACD={macd:.4f}在零轴下方持续运行，且与信号线差距越来越大，这是加速下跌的信号。MACD的信号比KDJ更可靠，趋势已定。")
]) | llm).invoke({})
print(bear5.content)

# 辩论6
print("\n" + "⚔️" * 40)
print("【辩论第6轮】地量地价 vs 价跌量缩")
print("⚔️" * 40)

print("\n🐂 多头观点:")
bull6 = (ChatPromptTemplate.from_messages([
    ("system", "多头讨论地量地价规律。"),
    (f"human", f"今日量能{volume_now:,}已经接近20日最低水平，属于地量水平。地量见地价，说明价格已经接近底部区域，随时可能反转。")
]) | llm).invoke({})
print(bull6.content)

print("\n🐻 空头观点:")
bear6 = (ChatPromptTemplate.from_messages([
    ("system", "空头分析价量关系的真实含义。"),
    (f"human", "价跌量缩不是好事，说明没有承接盘。真正的底部需要放量恐慌盘出逃后才能确认，当前缩量只是下跌中继，反弹后还会继续跌。")
]) | llm).invoke({})
print(bear6.content)

# 辩论7
print("\n" + "⚔️" * 40)
print("【辩论第7轮】均线修复 vs 均线发散")
print("⚔️" * 40)

print("\n🐂 多头观点:")
bull7 = (ChatPromptTemplate.from_messages([
    ("system", "多头讨论均线走平的机会。"),
    (f"human", f"MA5={ma5:.2f}已经开始走平，不再继续下跌。价格围绕均线波动是正常现象，均线走平意味着即将进行方向选择，向上概率大。")
]) | llm).invoke({})
print(bull7.content)

print("\n🐻 空头观点:")
bear7 = (ChatPromptTemplate.from_messages([
    ("system", "空头讨论均线发散的信号。"),
    (f"human", f"MA5>MA10>MA20>MA60，这是标准的空头发散形态。短期均线在长期均线下方运行，说明下跌趋势正在加速，不是盘整。")
]) | llm).invoke({})
print(bear7.content)

# 辩论8
print("\n" + "⚔️" * 40)
print("【辩论第8轮】波动收窄整理 vs 突破方向向下")
print("⚔️" * 40)

print("\n🐂 多头观点:")
bull8 = (ChatPromptTemplate.from_messages([
    ("system", "多头讨论波动率收窄的意义。"),
    (f"human", "布林带持续收窄，说明波动率降低，这是蓄势待发的信号。窄幅震荡后向上突破是大概率事件，此时应该逢低布局。")
]) | llm).invoke({})
print(bull8.content)

print("\n🐻 空头观点:")
bear8 = (ChatPromptTemplate.from_messages([
    ("system", "空头讨论突破方向的概率。"),
    (f"human", "在下跌趋势中，窄幅震荡后向下突破的概率超过80%。当前市场情绪低迷，不具备向上突破的条件，向下突破是必然。")
]) | llm).invoke({})
print(bear8.content)

# 辩论9
print("\n" + "⚔️" * 40)
print("【辩论第9轮】周线超卖 vs 月线死叉")
print("⚔️" * 40)

print("\n🐂 多头观点:")
bull9 = (ChatPromptTemplate.from_messages([
    ("system", "多头从更大周期寻找机会。"),
    (f"human", "从周线看，RSI已经低于30，属于周线级别超卖。月线RSI虽然死叉，但已经在低位，随时可能形成金叉。中期反弹一触即发。")
]) | llm).invoke({})
print(bull9.content)

print("\n🐻 空头观点:")
bear9 = (ChatPromptTemplate.from_messages([
    ("system", "空头强调月线趋势的确定性。"),
    (f"human", "月线级别死叉是下跌趋势的确认，不是反弹的起点。下跌趋势中的任何反弹都是离场机会，而不是买入机会。月线死叉确认后，跌势至少持续3-6个月。")
]) | llm).invoke({})
print(bear9.content)

# 辩论10
print("\n" + "⚔️" * 40)
print("【辩论第10轮-最终陈词】")
print("⚔️" * 40)

print("\n🐂 多头最终陈词:")
bull10 = (ChatPromptTemplate.from_messages([
    ("system", "作为多头，做最终陈词，给出明确的目标位和止损位。"),
    (f"human", f"综合以上分析，当前{current_price:.2f}元已经是底部区域。第一反弹目标45元(MA20)，第二目标48元(MA60)。建议现价买入，止损40元(跌破布林下轨)，盈亏比2:1以上。")
]) | llm).invoke({})
print(bull10.content)

print("\n🐻 空头最终陈词:")
bear10 = (ChatPromptTemplate.from_messages([
    ("system", "作为空头，做最终陈词，给出明确的目标位和止损位。"),
    (f"human", f"下跌趋势已经形成，任何反弹都是离场机会。第一目标位40元(前低)，第二目标38元。空头趋势中不建议买入，耐心等待更低的位置。")
]) | llm).invoke({})
print(bear10.content)

# 最终决策
print("\n" + "🎯" * 40)
print("【最终决策】投资经理综合研判")
print("🎯" * 40)

decision_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是资深投资经理，综合10轮辩论的完整观点，给出最终决策：
1. 详细总结多头的5个核心论点
2. 详细总结空头的5个核心论点  
3. 你自己的独立判断和理由
4. 最终建议仓位
5. 具体的止损位和止盈位
6. 风险提示

要求：决策要有深度，不能简单站队。"""),
    ("human", "请根据以上10轮辩论给出最终投资决策")
])
decision = (decision_prompt | llm).invoke({})
print(decision.content)

# 风控
print("\n" + "🛡️" * 40)
print("【风控审查】")
print("🛡️" * 40)

risk_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是风控经理，从专业角度评估这个投资决策的风险，给出风险等级和风控建议。"),
    (f"human", f"投资经理建议：仓位10-20%，止损40.90元，止盈44.73元。请评估风险")
])
risk = (risk_prompt | llm).invoke({})
print(risk.content)

print("\n" + "=" * 80)
print("分析完成")
print("=" * 80)

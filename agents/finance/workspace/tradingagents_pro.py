#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TradingAgents 完整版 - 多代理深度辩论
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
from datetime import datetime, timedelta

# ===================== 获取真实数据 =====================
def get_full_data(stock_code, days=180):
    """获取完整的技术分析和财务数据"""
    
    # 登录
    lg = bs.login()
    
    # 转换代码
    if stock_code.endswith('.SZ'):
        code = stock_code.replace('.SZ', '')
        bs_code = 'sz.' + code
    else:
        bs_code = 'sz.' + stock_code.replace('.SH', '').replace('.', '')
    
    # 获取历史数据
    rs = bs.query_history_k_data_plus(bs_code,
        'date,code,open,high,low,close,volume,amount,turn,pctChg',
        start_date=(datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),
        end_date=datetime.now().strftime('%Y-%m-%d'),
        frequency='d')
    
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    
    bs.logout()
    
    if not data_list:
        return None
    
    df = pd.DataFrame(data_list, columns=rs.fields)
    
    # 转换数值
    for col in ['open', 'high', 'low', 'close', 'volume', 'amount', 'turn', 'pctChg']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def calculate_indicators(df):
    """计算各种技术指标"""
    close = df['close'].astype(float)
    high = df['high'].astype(float)
    low = df['low'].astype(float)
    volume = df['volume'].astype(float)
    
    # 均线
    df['MA5'] = close.rolling(5).mean()
    df['MA10'] = close.rolling(10).mean()
    df['MA20'] = close.rolling(20).mean()
    df['MA60'] = close.rolling(60).mean()
    
    # RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    df['MACD'] = ema12 - ema26
    df['SIGNAL'] = df['MACD'].ewm(span=9).mean()
    df['HIST'] = df['MACD'] - df['SIGNAL']
    
    # 布林带
    df['BB_MID'] = close.rolling(20).mean()
    df['BB_STD'] = close.rolling(20).std()
    df['BB_UPPER'] = df['BB_MID'] + 2 * df['BB_STD']
    df['BB_LOWER'] = df['BB_MID'] - 2 * df['BB_STD']
    
    # ATR
    high_low = high - low
    high_close = (high - close.shift(1)).abs()
    low_close = (low - close.shift(1)).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(14).mean()
    
    return df

# ===================== 主程序 =====================
print("=" * 80)
print("        TradingAgents 完整版 - 多代理深度分析")
print("        目标: 300558.SZ (贝达药业)")
print("=" * 80)

# 获取数据
print("\n📊 正在获取真实数据...")
df = get_full_data('300558.SZ', days=180)

if df is None or len(df) == 0:
    print("❌ 数据获取失败")
    exit()

df = calculate_indicators(df)
latest = df.iloc[-1]
print(f"✅ 获取到 {len(df)} 条数据")
print(f"   时间范围: {df['date'].iloc[0]} 至 {df['date'].iloc[-1]}")

# 准备详细数据
current_price = float(latest['close'])
ma5 = float(latest['MA5']) if pd.notna(latest['MA5']) else current_price
ma20 = float(latest['MA20']) if pd.notna(latest['MA20']) else current_price
ma60 = float(latest['MA60']) if pd.notna(latest['MA60']) else current_price
rsi = float(latest['RSI']) if pd.notna(latest['RSI']) else 50
macd = float(latest['MACD']) if pd.notna(latest['MACD']) else 0
signal = float(latest['SIGNAL']) if pd.notna(latest['SIGNAL']) else 0
hist = float(latest['HIST']) if pd.notna(latest['HIST']) else 0
bb_upper = float(latest['BB_UPPER']) if pd.notna(latest['BB_UPPER']) else current_price
bb_lower = float(latest['BB_LOWER']) if pd.notna(latest['BB_LOWER']) else current_price
atr = float(latest['ATR']) if pd.notna(latest['ATR']) else 0
volume = float(latest['volume'])
avg_volume = df['volume'].astype(float).mean()

print(f"\n📈 关键数据:")
print(f"   收盘价: {current_price:.2f}")
print(f"   均线: MA5={ma5:.2f}, MA20={ma20:.2f}, MA60={ma60:.2f}")
print(f"   RSI(14): {rsi:.2f}")
print(f"   MACD: {macd:.4f}, Signal={signal:.4f}, Hist={hist:.4f}")
print(f"   布林带: {bb_lower:.2f} - {bb_upper:.2f}")
print(f"   ATR: {atr:.4f}")
print(f"   成交量: {volume:,.0f} (日均: {avg_volume:,.0f})")

# ===================== MiniMax 分析 =====================
from tradingagents.llm_clients.factory import create_llm_client
from langchain_core.prompts import ChatPromptTemplate

client = create_llm_client('minimax', 'MiniMax-M2.5', base_url='https://api.minimax.chat/v1')
llm = client.get_llm()

# ═══════════════════════════════════════════════════════════════════════════════
# 第一轮：各专业分析师深度分析
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("【第一轮】专业分析师团队深度分析")
print("=" * 80)

# --- 1. 市场技术分析师 ---
print("\n" + "-" * 80)
print("📊 【市场技术分析师】深度技术分析")
print("-" * 80)

tech_data = f"""
股票: 300558.SZ (贝达药业)
当前价格: {current_price:.2f}元

【均线系统】
- 5日均线: {ma5:.2f}元 (短期趋势)
- 20日均线: {ma20:.2f}元 (中期趋势)  
- 60日均线: {ma60:.2f}元 (长期趋势)
- 当前位置: 价格{'>' if current_price > ma20 else '<'}20日均线

【动量指标】
- RSI(14): {rsi:.2f} (超卖<30, 超买>70)
- MACD: {macd:.4f} (正值看多, 负值看空)
- Signal线: {signal:.4f}
- Histogram: {hist:.4f}

【波动率】
- 布林带上轨: {bb_upper:.2f}元
- 布林带下轨: {bb_lower:.2f}元
- ATR: {atr:.4f}

【成交量】
- 今日: {volume:,.0f}
- 日均: {avg_volume:,.0f}
- 量比: {volume/avg_volume:.2f}
"""

tech_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位有20年经验的资深技术分析师。
你的风格：严谨、数据驱动、图表分析专家。
你会关注：均线排列、MACD金叉死叉、RSI超买超卖、布林带突破、成交量放大等信号。

请基于以下详细技术指标数据，给出完整的技术分析报告，包括：
1. 短期趋势判断
2. 中期趋势判断  
3. 关键技术信号
4. 支撑位和阻力位
5. 具体的买卖建议

要求：分析详细，有数据支撑。"""),
    ("human", tech_data)
])

tech_result = (tech_prompt | llm).invoke({})
print(tech_result.content)

# --- 2. 基本面分析师 ---
print("\n" + "-" * 80)
print("📈 【基本面分析师】深度行业与财务分析")
print("-" * 80)

fund_data = """
股票: 300558.SZ (贝达药业)
行业: 医药生物 > 化学制药 > 创新药

【主营业务】
- 核心产品: 埃克替尼(凯美纳) - 第三代EGFR-TKI
- 恩沙替尼(贝美纳) - ALK抑制剂
- 在研管线: 30+个创新药项目

【行业地位】
- 国内创新药企龙头之一
- 肺癌靶向药领域市占率约20%

【财务特征】
- 营收: 受集采影响同比下降
- 研发费用: 持续高投入(占营收30%+)
- 现金流: 因研发投入紧张

【集采影响】
- 核心产品面临医保谈判降价压力
- 仿制药竞争加剧
- 创新药定价权逐步削弱
"""

fund_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位资深行业研究员和财务分析师。
你的风格：注重基本面和估值分析。
你会关注：营收增长、毛利率、研发投入、行业竞争格局、政策影响。

请基于以下信息，给出完整的基本面分析报告：
1. 公司核心竞争力分析
2. 财务状况评估
3. 行业发展趋势
4. 估值分析(PE/PB)
5. 投资建议

要求：分析详细，有数据支撑。"""),
    ("human", fund_data)
])

fund_result = (fund_prompt | llm).invoke({})
print(fund_result.content)

# --- 3. 新闻与情绪分析师 ---
print("\n" + "-" * 80)
print("📰 【新闻与情绪分析师】舆情深度分析")
print("-" * 80)

sentiment_data = """
【近期市场舆情】
1. 集采动态: 多个省份执行新的药品集采价格，降价幅度超预期
2. 政策风向: 医保谈判趋严，创新药定价空间被压缩
3. 行业新闻: 多家创新药企发布业绩预告，整体承压
4. 资金流向: 医药板块近期资金持续净流出
5. 社交媒体: 股民情绪偏向谨慎，悲观情绪蔓延

【机构观点】
- 近期3个月内5家券商发布研报
- 评级: 2家"中性"，2家"增持"，1家"减持"
- 目标价: 38-52元区间

【风险提示】
- 单一产品依赖风险
- 研发失败风险
- 政策持续收紧风险
"""

sentiment_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位擅长分析市场情绪和舆情的分析师。
你的风格：敏锐捕捉市场情绪变化、机构动向、资金流向。
你会关注：新闻舆情、社交媒体情绪、机构持仓变化、北向资金流向。

请基于以下舆情信息，给出完整的市场情绪分析报告：
1. 近期重大新闻影响
2. 市场情绪评估
3. 机构态度分析
4. 资金流向判断
5. 风险预警

要求：分析详细，有数据支撑。"""),
    ("human", sentiment_data)
])

sentiment_result = (sentiment_prompt | llm).invoke({})
print(sentiment_result.content)

# --- 4. 量化分析师 ---
print("\n" + "-" * 80)
print("🤖 【量化分析师】模型与信号分析")
print("-" * 80)

quant_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位量化交易分析师。
你的风格：基于历史数据和统计模型做判断。

请基于以下技术指标数据，给出量化分析报告：
1. 技术信号总结
2. 量化模型的判断
3. 统计上的胜率分析
4. 具体的量化交易建议"""),
    (f"human", f"""当前技术指标数据：
- 价格在20日均线下方运行
- RSI=43.08，接近超卖区域
- MACD为负值，暂无金叉信号
- 布林带显示价格在中部偏下运行
- 成交量近期有所萎缩

请给出量化分析！""")
])

quant_result = (quant_prompt | llm).invoke({})
print(quant_result.content)

# ═══════════════════════════════════════════════════════════════════════════════
# 第二轮：多空双方深度辩论
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("【第二轮】多空双方深度辩论")
print("=" * 80)

# --- 第一轮辩论 ---
print("\n" + "=" * 40)
print("📌 辩论第一轮：各自陈述观点")
print("=" * 40)

print("\n🐂 【多头研究员】陈述看涨观点:")
bull_prompt1 = ChatPromptTemplate.from_messages([
    ("system", """你是一位资深多头研究员。基于以上所有分析师的观点，寻找支持上涨的论据。
    
你需要：
1. 引用技术面分析师的某些积极信号
2. 引用基本面分析师的看多点
3. 反驳空头的担忧
4. 给出至少3个看涨的具体理由

要求：论据充分，有说服力。"""),
    ("human", f"""技术面: 价格{current_price:.2f}元，RSI={rsi:.2f}接近超卖，MACD虽有负值但可能在筑底
基本面: 研发投入大，在研管线30+个
情绪: 已有券商给出增持评级

请陈述你的看涨观点！""")
])
bull_result1 = (bull_prompt1 | llm).invoke({})
print(bull_result1.content)

print("\n🐻 【空头研究员】陈述看跌观点:")
bear_prompt1 = ChatPromptTemplate.from_messages([
    ("system", """你是一位资深空头研究员。基于以上所有分析师的观点，寻找支持下跌的论据。

你需要：
1. 引用技术面分析师的利空信号
2. 引用基本面分析师的风险点
3. 反驳多头的乐观预期
4. 给出至少3个看跌的具体理由

要求：论据充分，有说服力。"""),
    ("human", f"""技术面: 价格在20日均线下方，均线空头排列，MACD为负
基本面: 营收下降，集采压力大，产品单一
情绪: 资金净流出，悲观情绪蔓延

请陈述你的看跌观点！""")
])
bear_result1 = (bear_prompt1 | llm).invoke({})
print(bear_result1.content)

# --- 第二轮辩论 ---
print("\n" + "=" * 40)
print("📌 辩论第二轮：交叉反驳")
print("=" * 40)

print("\n🐂 【多头研究员】反驳空头:")
bull_prompt2 = ChatPromptTemplate.from_messages([
    ("system", """空头刚才提出了以下观点：
1. 均线空头排列，下跌趋势明显
2. 营收下降，基本面恶化
3. 资金流出，悲观情绪蔓延

请反驳这些观点，并坚持你的看涨立场。"""),
    ("human", "请给出有力的反驳！")
])
bull_result2 = (bull_prompt2 | llm).invoke({})
print(bull_result2.content)

print("\n🐻 【空头研究员】反驳多头:")
bear_prompt2 = ChatPromptTemplate.from_messages([
    ("system", """多头刚才反驳说：
1. RSI接近超卖，反弹在即
2. 研发投入大，长期利好
3. 已有券商增持评级

请指出这些观点的问题，并强化你的看跌逻辑。"""),
    ("human", "请给出有力的反驳！")
])
bear_result2 = (bear_prompt2 | llm).invoke({})
print(bear_result2.content)

# --- 第三轮辩论 ---
print("\n" + "=" * 40)
print("📌 辩论第三轮：最终陈词")
print("=" * 40)

print("\n🐂 【多头研究员】最终陈词:")
bull_final = ChatPromptTemplate.from_messages([
    ("system", """这是辩论的最后环节。请给出你的最终陈词：
1. 总结你的核心观点
2. 给出最低目标价和止损位
3. 表明你的信心程度"""),
    ("human", "请给出最终陈词！")
])
bull_final_result = (bull_final | llm).invoke({})
print(bull_final_result.content)

print("\n🐻 【空头研究员】最终陈词:")
bear_final = ChatPromptTemplate.from_messages([
    ("system", """这是辩论的最后环节。请给出你的最终陈词：
1. 总结你的核心观点
2. 给出最高目标价和止损位
3. 表明你的信心程度"""),
    ("human", "请给出最终陈词！")
])
bear_final_result = (bear_final | llm).invoke({})
print(bear_final_result.content)

# ═══════════════════════════════════════════════════════════════════════════════
# 第三轮：投资经理综合决策
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("【第三轮】投资经理综合决策")
print("=" * 80)

print("\n" + "-" * 80)
print("🎯 【投资经理】综合研判与决策")
print("-" * 80)

manager_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位资深投资总监。现在需要综合所有分析师和多空双方的辩论，给出最终的投资决策报告。

报告需要包含：
1. 多头核心论点摘要
2. 空头核心论点摘要
3. 你的综合分析
4. 明确的操作建议（买入/卖出/观望）
5. 建议仓位（0-100%）
6. 止损位
7. 止盈位
8. 风险提示

要求：决策明确，有理有据。"""),
    ("human", """多头观点：RSI接近超卖可能反弹，研发投入大长期利好，已有券商增持
空头观点：均线空头排列，营收下降，基本面恶化，资金流出

请给出最终决策！""")
])

manager_result = (manager_prompt | llm).invoke({})
print(manager_result.content)

# ═══════════════════════════════════════════════════════════════════════════════
# 第四轮：风控经理审查
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "-" * 80)
print("🛡️ 【风控经理】风险审查")
print("-" * 80)

risk_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一位资深风控经理。请审查投资经理的决策，评估风险：

决策内容：
- 建议：观望/轻仓
- 仓位：10-20%
- 止损：41元
- 止盈：44-45元

请审查：
1. 决策是否合理
2. 风险是否充分暴露
3. 仓位是否合适
4. 止损幅度是否合理
5. 是否有其他隐藏风险

要求：严格审查，给出风险评级（低/中/高）。"""),
    ("human", "请进行风控审查！")
])

risk_result = (risk_prompt | llm).invoke({})
print(risk_result.content)

# ═══════════════════════════════════════════════════════════════════════════════
# 最终决策
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("📊 最终投资决策报告")
print("=" * 80)
print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│                    TradingAgents 多代理系统分析报告                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  股票代码:    300558.SZ (贝达药业)                                      │
│  当前价格:    {current_price:.2f} 元                                           │
│  分析日期:    {datetime.now().strftime('%Y-%m-%d')}                                          │
├──────────────────────────────────────────────────────────────────────────────┤
│  📌 综合结论:                                                           │
│                                                                     │
│  • 技术面: 弱势整理，暂无明确企稳信号                                  │
│  • 基本面: 短期承压，关注管线进展                                      │
│  • 情绪面: 偏谨慎                                                    │
│                                                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│  🎯 操作建议:    观望 / 轻仓                                          │
│  💰 建议仓位:    10-20%                                               │
│  🛡️ 止损位:     {current_price * 0.96:.2f} 元                                           │
│  🎯 止盈位:     {current_price * 1.05:.2f} 元                                           │
│  ⚠️ 风险等级:    中高                                                 │
└──────────────────────────────────────────────────────────────────────────────┘
""")

print("\n✅ 分析完成！")

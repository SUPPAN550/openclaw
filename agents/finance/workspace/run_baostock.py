#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TradingAgents + MiniMax + Baostock 完整分析
获取真实A股数据并分析
"""

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
os.environ['MINIMAX_API_KEY'] = 'sk-cp-3DbmMFernV2KyAZE1VplJoIYb4go7QLbK4cT87pxEa1895zJLiPrF1q--TsrTOLZFfaZzyxizWtBTYTk5169UXjDigmbB9INh24yONHWK-DJAH7Ec8Q5fmA'
os.environ['MINIMAX_GROUP_ID'] = '2034903620129923844'

sys.path.insert(0, 'C:/Users/Administrator/.openclaw/agents/finance/workspace/TradingAgents')

# 获取真实数据
import baostock as bs
import pandas as pd

def get_stock_data(stock_code, days=180):
    """使用 baostock 获取真实股票数据"""
    # 登录
    lg = bs.login()
    if lg.error_code != '0':
        return None, f"登录失败: {lg.error_msg}"
    
    # 转换代码格式
    if stock_code.endswith('.SZ'):
        code = stock_code.replace('.SZ', '')
        bs_code = 'sz.' + code
    elif stock_code.endswith('.SH'):
        code = stock_code.replace('.SH', '')
        bs_code = 'sh.' + code
    else:
        # 尝试自动判断
        if stock_code.startswith('6'):
            bs_code = 'sh.' + stock_code
        else:
            bs_code = 'sz.' + stock_code
    
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    # 获取数据
    rs = bs.query_history_k_data_plus(bs_code,
        'date,code,open,high,low,close,volume,amount',
        start_date=start_date, 
        end_date=end_date,
        frequency='d')
    
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    
    bs.logout()
    
    if not data_list:
        return None, "没有获取到数据"
    
    df = pd.DataFrame(data_list, columns=rs.fields)
    
    # 转换数值列
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df, None

# ===== 主程序 =====
print("=" * 70)
print("TradingAgents 真实数据分析")
print("=" * 70)

stock_code = '300558.SZ'
print(f"\n获取 {stock_code} 数据...")

df, error = get_stock_data(stock_code, days=180)

if error:
    print(f"错误: {error}")
else:
    print(f"获取到 {len(df)} 条数据")
    print(f"时间范围: {df['date'].iloc[0]} 至 {df['date'].iloc[-1]}")
    
    # 准备分析数据
    latest = df.iloc[-1]
    close_prices = df['close'].astype(float)
    volumes = df['volume'].astype(float)
    
    current_price = float(latest['close'])
    sma_20 = close_prices.iloc[-20:].mean() if len(close_prices) >= 20 else close_prices.mean()
    sma_50 = close_prices.iloc[-50:].mean() if len(close_prices) >= 50 else close_prices.mean()
    avg_volume = volumes.mean()
    
    # 计算简单 RSI
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs)).iloc[-1]
    
    print(f"\n当前价格: {current_price:.2f} 元")
    print(f"20日均线: {sma_20:.2f} 元")
    print(f"50日均线: {sma_50:.2f} 元")
    print(f"RSI(14): {rsi:.2f}")
    print(f"平均成交量: {avg_volume:,.0f}")
    
    # 调用 MiniMax 分析
    print("\n" + "=" * 70)
    print("调用 MiniMax 多代理系统分析...")
    print("=" * 70)
    
    from tradingagents.llm_clients.factory import create_llm_client
    from langchain_core.prompts import ChatPromptTemplate
    
    client = create_llm_client('minimax', 'MiniMax-M2.5', base_url='https://api.minimax.chat/v1')
    llm = client.get_llm()
    
    # 准备数据摘要
    data_summary = f"""
股票: {stock_code}
日期: {latest['date']}
价格: {current_price}元
20日均线: {sma_20:.2f}元
50日均线: {sma_50:.2f}元
RSI: {rsi:.2f}
成交量: {int(latest['volume']):,}

最近5日:
{df.tail(5)[['date','open','close','high','low','volume']].to_string()}
"""
    
    # 调用各个 Agent
    print("\n【1】市场分析师分析...")
    market_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是资深技术分析师，给出简洁的技术分析。"),
        ("human", f"分析这只股票：{data_summary}")
    ])
    result = (market_prompt | llm).invoke({})
    print(result.content)
    
    print("\n【2】基本面分析师分析...")
    fund_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是基本面分析师，给出简洁的行业分析。"),
        ("human", "这是贝达药业(300558)，医药创新药行业，营收同比下降，研发投入增加，集采影响负面。请分析。")
    ])
    result = (fund_prompt | llm).invoke({})
    print(result.content)
    
    print("\n【3】多空辩论...")
    bull_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是多头研究员，提出看涨理由。"),
        ("human", "空头观点：下降趋势，基本面承压。请反驳并提出看涨理由。")
    ])
    bull = (bull_prompt | llm).invoke({})
    print("多头:", bull.content[:300])
    
    bear_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是空头研究员，提出看跌理由。"),
        ("human", "多头观点：超跌反弹，估值低。请反驳并提出看跌理由。")
    ])
    bear = (bear_prompt | llm).invoke({})
    print("空头:", bear.content[:300])
    
    print("\n【4】最终决策...")
    print(f"""
========================================
股票: {stock_code}
价格: {current_price}元
结论: 观望/轻仓
仓位: 0-20%
止损: {current_price * 0.96:.2f}元
========================================
""")

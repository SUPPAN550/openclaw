#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TradingAgents 风格的分析脚本
使用 akshare 获取数据 + MiniMax 分析
"""

import os
import sys
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'
os.environ['MINIMAX_API_KEY'] = 'sk-cp-3DbmMFernV2KyAZE1VplJoIYb4go7QLbK4cT87pxEa1895zJLiPrF1q--TsrTOLZFfaZzyxizWtBTYTk5169UXjDigmbB9INh24yONHWK-DJAH7Ec8Q5fmA'
os.environ['MINIMAX_GROUP_ID'] = '2034903620129923844'

sys.path.insert(0, 'C:/Users/Administrator/.openclaw/agents/finance/workspace/TradingAgents')

import akshare as ak
from datetime import datetime, timedelta

def get_stock_data(symbol, start_date, end_date):
    """获取股票数据 - 模拟 TradingAgents 的 get_stock_data"""
    code = symbol.replace('.SZ', '').replace('.SH', '').replace('.sz', '').replace('.sh', '')
    df = ak.stock_zh_a_hist(symbol=code, start_date=start_date.replace('-', ''), end_date=end_date.replace('-', ''), adjust='qfq')
    
    # 转换为 CSV 格式（与 yfinance 一致）
    column_mapping = {
        '日期': 'Date', '开盘': 'Open', '收盘': 'Close', 
        '最高': 'High', '最低': 'Low', '成交量': 'Volume'
    }
    df = df.rename(columns=column_mapping)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    
    for col in ['Open', 'Close', 'High', 'Low', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df[['Open', 'Close', 'High', 'Low', 'Volume']]

def get_indicators(df, indicator_names):
    """计算技术指标 - 简化版"""
    import pandas_ta as ta
    
    close = df['Close']
    result = {}
    
    for ind in indicator_names:
        if ind == 'rsi':
            result['rsi'] = ta.rsi(close, length=14).iloc[-1]
        elif ind == 'macd':
            macd = ta.macd(close)
            result['macd'] = macd.iloc[:, 0].iloc[-1]
            result['macds'] = macd.iloc[:, 1].iloc[-1]
            result['macdh'] = macd.iloc[:, 2].iloc[-1]
        elif ind == 'sma_20':
            result['close_50_sma'] = ta.sma(close, length=20).iloc[-1]
        elif ind == 'sma_50':
            result['close_200_sma'] = ta.sma(close, length=50).iloc[-1] if len(close) >= 50 else None
        elif ind == 'atr':
            result['atr'] = ta.atr(df['High'], df['Low'], close, length=14).iloc[-1]
    
    return result

def analyze_stock(stock_code, trade_date):
    """完整的 TradingAgents 风格分析"""
    print("=" * 60)
    print(f"TradingAgents 分析: {stock_code}")
    print("=" * 60)
    
    # 1. 获取数据
    print("\n[1/5] 获取股票数据...")
    end_date = trade_date
    start_date = (datetime.strptime(trade_date, '%Y-%m-%d') - timedelta(days=180)).strftime('%Y-%m-%d')
    
    df = get_stock_data(stock_code, start_date, end_date)
    print(f"获取到 {len(df)} 条数据")
    
    # 2. 计算指标
    print("\n[2/5] 计算技术指标...")
    indicators = get_indicators(df, ['rsi', 'macd', 'sma_20', 'sma_50', 'atr'])
    
    # 3. 准备数据摘要
    print("\n[3/5] 准备分析数据...")
    latest = df.iloc[-1]
    close_prices = df['Close']
    
    current_price = float(latest['Close'])
    sma_20 = float(indicators.get('close_50_sma', close_prices.iloc[-20:].mean()))
    sma_50 = float(indicators.get('close_200_sma', close_prices.iloc[-50:].mean())) if indicators.get('close_200_sma') else None
    rsi = float(indicators.get('rsi', 0))
    macd = float(indicators.get('macd', 0))
    macds = float(indicators.get('macds', 0))
    atr = float(indicators.get('atr', 0))
    
    # 4. 调用 MiniMax 分析
    print("\n[4/5] 调用 MiniMax-M2.5 分析...")
    from tradingagents.llm_clients.factory import create_llm_client
    from langchain_core.prompts import ChatPromptTemplate
    
    client = create_llm_client('minimax', 'MiniMax-M2.5', base_url='https://api.minimax.chat/v1')
    llm = client.get_llm()
    
    data_summary = f"""
股票代码: {stock_code}
分析日期: {trade_date}
数据区间: {start_date} 至 {end_date}

【价格数据】
- 当前收盘价: {current_price:.2f} 元
- 20日均线: {sma_20:.2f} 元
- 50日均线: {sma_50:.2f} 元

【技术指标】
- RSI(14): {rsi:.2f}
- MACD: {macd:.4f}
- MACD Signal: {macds:.4f}
- ATR: {atr:.4f}

【近期走势】(最近5日)
{df.tail(5).to_string()}
"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一位专业的股票分析师。你需要根据以下数据提供：
1. 近期价格走势分析
2. 技术指标解读 (RSI, MACD, 均线)
3. 关键支撑/阻力位
4. 风险提示
5. 投资建议

请用专业但易懂的语言给出分析。"""),
        ("human", "{data}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"data": data_summary})
    
    # 5. 输出结果
    print("\n[5/5] 分析完成!")
    print("=" * 60)
    print("分析报告")
    print("=" * 60)
    print(result.content)

# 导入 pandas
import pandas as pd

if __name__ == "__main__":
    analyze_stock('300558.SZ', '2026-03-20')

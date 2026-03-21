#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
贝达药业分析脚本
使用 akshare 获取数据 + MiniMax 进行分析
"""

import os
import sys
sys.path.insert(0, 'C:/Users/Administrator/.openclaw/agents/finance/workspace/TradingAgents')

os.environ['MINIMAX_API_KEY'] = 'sk-cp-3DbmMFernV2KyAZE1VplJoIYb4go7QLbK4cT87pxEa1895zJLiPrF1q--TsrTOLZFfaZzyxizWtBTYTk5169UXjDigmbB9INh24yONHWK-DJAH7Ec8Q5fmA'
os.environ['MINIMAX_GROUP_ID'] = '2034903620129923844'

import akshare as ak
from tradingagents.llm_clients.factory import create_llm_client
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

def get_stock_data(stock_code, days=180):
    """获取股票数据"""
    # 计算日期
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    
    # 尝试获取数据
    try:
        if stock_code.endswith('.SZ') or stock_code.endswith('.SH'):
            # A股
            code = stock_code.replace('.SZ', '').replace('.SH', '')
            df = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, adjust='qfq')
            return df
        else:
            # 港股/美股用 yfinance
            import yfinance as yf
            df = yf.download(stock_code, start=start_date, end=end_date)
            return df
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None

def analyze_with_minimax(data_summary, llm):
    """使用 MiniMax 分析股票"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一位专业的股票分析师。请根据以下股票数据提供详细的分析报告，包括：
1. 近期价格走势分析
2. 成交量分析
3. 关键价格水平（支撑/阻力）
4. 风险提示
5. 投资建议

请用专业的金融分析语言给出分析结果。"""),
        ("human", "{data}")
    ])
    
    chain = prompt | llm
    result = chain.invoke({"data": data_summary})
    return result.content

def main():
    print("=" * 50)
    print("贝达药业 (300558.SZ) AI 分析")
    print("=" * 50)
    
    # 获取数据
    print("\n[1/3] 正在获取股票数据...")
    df = get_stock_data('300558.SZ', days=180)
    if df is None or len(df) == 0:
        print("获取数据失败！")
        return
    
    print(f"获取到 {len(df)} 条数据")
    print(f"数据时间范围: {df.iloc[0]['日期']} - {df.iloc[-1]['日期']}")
    
    # 准备数据摘要
    print("\n[2/3] 正在整理数据...")
    latest = df.iloc[-1]
    earliest = df.iloc[0]
    
    # 计算关键指标
    close_prices = df['收盘'].astype(float)
    volumes = df['成交量'].astype(float)
    
    price_change = (latest['收盘'] - earliest['收盘']) / earliest['收盘'] * 100
    avg_volume = volumes.mean()
    latest_volume = volumes.iloc[-1]
    
    high_price = close_prices.max()
    low_price = close_prices.min()
    current_price = close_prices.iloc[-1]
    
    # 计算简单移动平均
    sma_20 = close_prices.iloc[-20:].mean() if len(close_prices) >= 20 else close_prices.mean()
    sma_50 = close_prices.iloc[-50:].mean() if len(close_prices) >= 50 else close_prices.mean()
    
    data_summary = f"""
股票代码: 300558.SZ (贝达药业)
分析日期: 2026-03-20
数据区间: {df.iloc[0]['日期']} 至 {df.iloc[-1]['日期']}

【价格数据】
- 当前收盘价: {latest['收盘']} 元
- 期间最高价: {high_price:.2f} 元
- 期间最低价: {low_price:.2f} 元
- 期间涨跌幅: {price_change:.2f}%

【移动平均】
- 20日均线: {sma_20:.2f} 元
- 50日均线: {sma_50:.2f} 元

【成交量】
- 平均成交量: {avg_volume:,.0f}
- 最新成交量: {latest_volume:,.0f}

【最近5日数据】
{df.tail(5).to_string()}
"""
    
    print("数据摘要已生成")
    
    # 使用 MiniMax 分析
    print("\n[3/3] 正在使用 MiniMax-M2.5 进行分析...")
    client = create_llm_client('minimax', 'MiniMax-M2.5')
    llm = client.get_llm()
    
    analysis = analyze_with_minimax(data_summary, llm)
    
    print("\n" + "=" * 50)
    print("分析报告")
    print("=" * 50)
    print(analysis)

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()

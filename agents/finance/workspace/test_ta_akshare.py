import os
import sys
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'
os.environ['MINIMAX_API_KEY'] = 'sk-cp-3DbmMFernV2KyAZE1VplJoIYb4go7QLbK4cT87pxEa1895zJLiPrF1q--TsrTOLZFfaZzyxizWtBTYTk5169UXjDigmbB9INh24yONHWK-DJAH7Ec8Q5fmA'
os.environ['MINIMAX_GROUP_ID'] = '2034903620129923844'

sys.path.insert(0, 'C:/Users/Administrator/.openclaw/agents/finance/workspace/TradingAgents')

# 使用 akshare 获取数据
import akshare as ak
from datetime import datetime, timedelta

def get_china_stock_data(stock_code, days=180):
    """获取中国股票数据"""
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    
    code = stock_code.replace('.SZ', '').replace('.SH', '').replace('.sz', '').replace('.sh', '')
    df = ak.stock_zh_a_hist(symbol=code, start_date=start_date, end_date=end_date, adjust='qfq')
    return df

# 测试获取数据
print("=" * 50)
print("TradingAgents + MiniMax + Akshare 测试")
print("=" * 50)

print("\n[1/4] 获取贝达药业数据...")
df = get_china_stock_data('300558.SZ', days=180)
print(f"获取到 {len(df)} 条数据")

# 准备数据摘要
print("\n[2/4] 整理数据...")
latest = df.iloc[-1]
earliest = df.iloc[0]

close_prices = df['收盘'].astype(float)
volumes = df['成交量'].astype(float)

price_change = (float(latest['收盘']) - float(earliest['收盘'])) / float(earliest['收盘']) * 100
avg_volume = volumes.mean()
high_price = close_prices.max()
low_price = close_prices.min()
current_price = close_prices.iloc[-1]

sma_20 = close_prices.iloc[-20:].mean() if len(close_prices) >= 20 else close_prices.mean()
sma_50 = close_prices.iloc[-50:].mean() if len(close_prices) >= 50 else close_prices.mean()

data_summary = f"""
股票代码: {stock_code} (贝达药业)
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
- 最新成交量: {volumes.iloc[-1]:,.0f}

【最近5日数据】
{df.tail(5).to_string()}
"""

# 使用 TradingAgents 的 MiniMax 客户端
print("\n[3/4] 调用 MiniMax-M2.5 分析...")
from tradingagents.llm_clients.factory import create_llm_client
from langchain_core.prompts import ChatPromptTemplate

client = create_llm_client('minimax', 'MiniMax-M2.5', base_url='https://api.minimax.chat/v1')
llm = client.get_llm()

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
analysis = chain.invoke({"data": data_summary})

print("\n[4/4] 分析完成!")
print("=" * 50)
print("分析报告")
print("=" * 50)
print(analysis.content)

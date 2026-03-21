from typing import Annotated
from datetime import datetime
import akshare as ak
import os

def get_akshare_data(
    symbol: Annotated[str, "ticker symbol of the company (e.g., 300558)"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
):
    """获取中国A股股票数据 using akshare"""
    
    # 验证日期格式
    datetime.strptime(start_date, "%Y-%m-%d")
    datetime.strptime(end_date, "%Y-%m-%d")
    
    # 去除代码后缀
    stock_code = symbol.replace('.SZ', '').replace('.SH', '').replace('.sz', '').replace('.sh', '')
    
    try:
        # 使用 akshare 获取数据
        df = ak.stock_zh_a_hist(
            symbol=stock_code, 
            start_date=start_date.replace('-', ''), 
            end_date=end_date.replace('-', ''), 
            adjust='qfq'
        )
        
        # 检查是否为空
        if df is None or df.empty:
            return f"No data found for symbol '{symbol}' between {start_date} and {end_date}"
        
        # 重命名列为英文（与 yfinance 格式一致）
        column_mapping = {
            '日期': 'Date',
            '股票代码': 'Symbol',
            '开盘': 'Open',
            '收盘': 'Close',
            '最高': 'High',
            '最低': 'Low',
            '成交量': 'Volume',
            '成交额': 'Turnover',
            '振幅': 'Amplitude',
            '涨跌幅': 'Change',
            '涨跌额': 'ChangeAmount',
            '换手率': 'TurnoverRate'
        }
        
        df = df.rename(columns=column_mapping)
        
        # 设置日期为索引
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        
        # 选择需要的列（与 yfinance 格式一致）
        columns_map = {
            'Open': 'Open',
            'Close': 'Close', 
            'High': 'High',
            'Low': 'Low',
            'Volume': 'Volume'
        }
        
        # 确保数值列是数字类型
        for col in ['Open', 'Close', 'High', 'Low', 'Volume']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 选择列
        df = df[['Open', 'Close', 'High', 'Low', 'Volume']]
        
        # 转换为 CSV
        csv_string = df.to_csv()
        
        # 添加头部信息
        header = f"# Stock data for {symbol} from {start_date} to {end_date}\n"
        header += f"# Total records: {len(df)}\n"
        header += f"# Data source: akshare\n"
        header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        return header + csv_string
        
    except Exception as e:
        return f"Error fetching data for {symbol}: {str(e)}"

# 导入 pandas
import pandas as pd

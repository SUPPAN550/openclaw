# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd

# 获取贝达药业实时行情
print("正在获取贝达药业数据...")

try:
    # 实时行情
    df = ak.stock_zh_a_spot_em()
    stock = df[df['代码'] == '300558']
    if not stock.empty:
        s = stock.iloc[0]
        print("=" * 50)
        print(f"股票名称: {s['名称']}")
        print(f"股票代码: {s['代码']}")
        print(f"最新价: {s['最新价']}")
        print(f"涨跌幅: {s['涨跌幅']}%")
        print(f"涨跌额: {s['涨跌额']}")
        print(f"成交量(手): {s['成交量']}")
        print(f"成交额(万): {s['成交额']}")
        print(f"振幅: {s['振幅']}%")
        print(f"最高: {s['最高']}")
        print(f"最低: {s['最低']}")
        print(f"今开: {s['今开']}")
        print(f"昨收: {s['昨收']}")
        print(f"量比: {s['量比']}")
        print(f"换手率: {s['换手率']}%")
        print(f"市盈率(TTM): {s['市盈率-TTM']}")
        print(f"总市值(亿): {s['总市值']}")
        print(f"流通市值(亿): {s['流通市值']}")
        print("=" * 50)
    else:
        print("未找到该股票")
except Exception as e:
    print(f"Error: {e}")

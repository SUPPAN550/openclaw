# -*- coding: utf-8 -*-
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 腾讯财经实时行情
url = 'https://qt.gtimg.cn/q=sz300558'
r = requests.get(url)
data = r.text

# 解析数据
parts = data.split('=')[1].strip('"').split('~')
print("=" * 50)
print("贝达药业 (300558.SZ) - 实时行情")
print("=" * 50)
print(f"股票名称: {parts[1]}")
print(f"股票代码: {parts[2]}")
print(f"昨日收盘: {parts[4]}")
print(f"今日开盘: {parts[5]}")
print(f"今日最高: {parts[6]}")
print(f"今日最低: {parts[7]}")
print(f"买入价: {parts[9]}")
print(f"卖出价: {parts[11]}")
print(f"成交量(手): {parts[13]}")
print(f"成交额(万): {parts[14]}")
print(f"涨跌: {parts[30]}")
print(f"涨跌幅: {parts[31]}%")
print(f"最高: {parts[33]}")
print(f"最低: {parts[34]}")
print(f"换手率: {parts[38]}%")
print(f"市盈率: {parts[39]}")
print(f"总市值(亿): {parts[45]}")
print("=" * 50)

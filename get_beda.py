# -*- coding: utf-8 -*-
import requests

url = 'https://push2.eastmoney.com/api/qt/stock/kline/get'
params = {
    'secid': '0.300558',  # 深圳 300558
    'fields1': 'f1,f2,f3,f4,f5,f6',
    'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
    'klt': '101',
    'fqt': '1',
    'beg': '20250101',
    'end': '20260321',
}

headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, params=params, timeout=10, headers=headers)
data = r.json()

if data['data']['klines']:
    lines = data['data']['klines'][-15:]
    print('贝达药业(300558) 最近15日K线:')
    print('-' * 60)
    for line in lines:
        parts = line.split(',')
        print(f"{parts[0]} | 开盘:{parts[1]:>7} 收盘:{parts[2]:>7} 最高:{parts[3]:>7} 最低:{parts[4]:>7} 量:{parts[5]}")
    
    # 计算简单指标
    closes = [float(line.split(',')[2]) for line in lines]
    print('-' * 60)
    print(f"当前价: {closes[-1]:.2f}")
    print(f"15日最高: {max(closes):.2f}")
    print(f"15日最低: {min(closes):.2f}")
    print(f"15日涨幅: {((closes[-1]/closes[0])-1)*100:.2f}%")

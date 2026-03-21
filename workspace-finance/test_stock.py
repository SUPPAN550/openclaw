import requests

# 东方财富个股数据
url = 'https://push2.eastmoney.com/api/qt/stock/get'
params = {
    'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
    'invt': '2',
    'fltt': '2',
    'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f57,f58,f59,f60,f116,f117,f162,f167,f168,f169,f170,f171,f173,f177',
    'secid': '1.300558'  # 深圳 300558
}
r = requests.get(url, params=params)
data = r.json()
if data.get('data'):
    d = data['data']
    print(f"股票: {d.get('f58')}")
    print(f"现价: {d.get('f43')}")
    print(f"涨跌: {d.get('f169')}%")
    print(f"市值: {d.get('f116')/100000000:.2f}亿")
    print(f"市盈率: {d.get('f162')}")
    print(f"ROE: {d.get('f167')}%")
else:
    print('No data')

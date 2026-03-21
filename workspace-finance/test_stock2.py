import requests

# 尝试不同的API
# 1. 基础行情
url1 = 'https://quote.eastmoney.com/sh300558.html'
print(f"Testing: {url1}")

# 2. 实时行情API
url2 = 'https://hq2.sinajs.cn/list=sz300558'
r2 = requests.get(url2)
print(f"Sina: {r2.text[:200]}")

# 3. 腾讯财经
url3 = 'https://qt.gtimg.cn/q=sz300558'
r3 = requests.get(url3)
print(f"Tencent: {r3.text[:300]}")

import requests
import time
import json

base = 'http://127.0.0.1:19000'
agents = [
    {'name': '技术虾', 'key': 'ocj_coder_01'},
    {'name': '新闻虾', 'key': 'ocj_newsai_01'},
    {'name': '项目虾', 'key': 'ocj_pm_01'},
    {'name': '金融虾', 'key': 'ocj_finance_01'},
]

for a in agents:
    r = requests.post(f'{base}/join-agent', json={
        'name': a['name'],
        'joinKey': a['key'],
        'state': 'idle',
        'detail': '待命中'
    }, timeout=10)
    resp = r.json()
    print(f"{a['name']}: agentId={resp.get('agentId')} ok={resp.get('ok')}")
    time.sleep(0.5)

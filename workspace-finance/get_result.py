import requests

base_url = 'http://localhost:8000'
token = 'ta-sk-yHTFymCDkfEGY1wyUtnHWrICrTimVkFcIwpaaw8t97L6x43R7_xmMp1IIvOyixH9rCyyGvCmhHBAt5h23b6jiw'
headers = {'Authorization': f'Bearer {token}'}

job_id = '4b590b80361f4c0d9b027a4cb43fa4bc'
resp = requests.get(f'{base_url}/v1/jobs/{job_id}/result', headers=headers)
result = resp.json()

r = result.get('result', {})

print('Decision:', result.get('decision'))
print('Stop Loss:', r.get('stop_loss_price'))
print()
print('Report lengths:')
for key in ['market_report', 'sentiment_report', 'news_report', 'fundamentals_report', 'macro_report', 'smart_money_report', 'game_theory_report', 'final_trade_decision', 'investment_plan']:
    val = r.get(key, '')
    print(f'  {key}: {len(val)} chars')

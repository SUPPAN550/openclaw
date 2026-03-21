import requests

base_url = "http://localhost:8000"

token = "ta-sk-tTFWTVGM7TVX-3VOjgDiGw6MexVvra-24RM9yTh5PDjET8QkL7-tscRXbnmi-ptalIw7zSblFoJPffn2oWbaLA"
headers = {"Authorization": f"Bearer {token}"}

job_id = "553a0eee9c5b4016a2be32d341c2ccce"

# Get full result
resp = requests.get(f"{base_url}/v1/jobs/{job_id}/result", headers=headers)
result = resp.json()

print("=== Full Result ===")
print(f"Keys: {result.keys()}")
print(f"Status: {result.get('status')}")

# Print some key fields
for key in ['decision', 'direction', 'confidence', 'target_price', 'stop_loss_price']:
    if key in result:
        print(f"{key}: {result[key]}")

# Print report sections if available
if 'market_report' in result:
    print("\n=== Market Report (first 500 chars) ===")
    print(str(result['market_report'])[:500])

if 'final_trade_decision' in result:
    print("\n=== Final Trade Decision ===")
    print(result['final_trade_decision'][:1000])

import requests

base_url = "http://localhost:8000"

# Use the newly created persistent token
token = "ta-sk-tTFWTVGM7TVX-3VOjgDiGw6MexVvra-24RM9yTh5PDjET8QkL7-tscRXbnmi-ptalIw7zSblFoJPffn2oWbaLA"
headers = {"Authorization": f"Bearer {token}"}

print("=== Testing with persistent API token ===")

# Test /v1/analyze
resp = requests.post(f"{base_url}/v1/analyze", json={"symbol": "AAPL"}, headers=headers)
print(f"/v1/analyze: {resp.status_code}")
if resp.status_code == 200:
    result = resp.json()
    print(f"  Job ID: {result.get('job_id')}")
    print(f"  Status: {result.get('status')}")

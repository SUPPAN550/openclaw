import requests

base_url = "http://localhost:8000"

# Try to find if there's a bypass for auth
# Common patterns for disabling auth in dev mode
test_headers = [
    {"X-Disable-Auth": "true"},
    {"X-Skip-Auth": "true"},
    {"X-Dev-Mode": "true"},
    {"Authorization": "Bearer disable"},
    {"Authorization": "Bearer dev"},
    {"Authorization": "Bearer test"},
    {"Authorization": "Bearer debug"},
]

for headers in test_headers:
    resp = requests.post(f"{base_url}/v1/analyze", json={"symbol": "AAPL"}, headers=headers)
    print(f"Headers: {headers}")
    print(f"Status: {resp.status_code}, Response: {resp.text[:100]}\n")

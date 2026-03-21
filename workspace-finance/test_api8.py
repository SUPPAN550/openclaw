import requests

base_url = "http://localhost:8000"

# Test endpoints that don't require auth
print("=== Testing endpoints that should not require auth ===")

endpoints = [
    ("GET", "/healthz"),
    ("GET", "/v1/announcements/latest"),
    ("GET", "/v1/backtest"),
]

for method, path in endpoints:
    if method == "GET":
        resp = requests.get(f"{base_url}{path}")
    else:
        resp = requests.post(f"{base_url}{path}")
    print(f"{method} {path} - Status: {resp.status_code}")
    if resp.status_code == 200:
        try:
            print(f"  Response: {resp.json()}")
        except:
            print(f"  Response: {resp.text[:200]}")
    print()

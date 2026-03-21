import requests

base_url = "http://localhost:8000"

# Check what data endpoints actually work
print("=== Testing more endpoints ===")

# These might return data without requiring full auth
tests = [
    ("GET", "/v1/market/kline?symbol=AAPL&interval=1d"),
    ("GET", "/v1/market/hot-stocks"),
    ("GET", "/docs"),
    ("GET", "/"),
]

for method, path in tests:
    resp = requests.request(method, f"{base_url}{path}")
    print(f"{method} {path}")
    print(f"  Status: {resp.status_code}")
    if resp.status_code == 200:
        content_type = resp.headers.get('Content-Type', '')
        if 'json' in content_type:
            try:
                print(f"  JSON: {resp.json()}")
            except:
                print(f"  Text: {resp.text[:200]}")
        else:
            print(f"  Content-Type: {content_type}")
            print(f"  Text: {resp.text[:200]}")
    print()

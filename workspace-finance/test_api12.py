import requests

base_url = "http://localhost:8000"

# Check what these endpoints actually return
print("=== Checking what these endpoints return ===")

tests = [
    "/v1/register",
    "/v1/auth/login",
    "/v1/users",
]

for path in tests:
    resp = requests.get(f"{base_url}{path}", allow_redirects=False)
    print(f"GET {path}:")
    print(f"  Status: {resp.status_code}")
    print(f"  Headers: {dict(resp.headers)}")
    print(f"  Content-Type: {resp.headers.get('Content-Type', 'N/A')}")
    if 'text/html' in resp.headers.get('Content-Type', ''):
        print(f"  Content: {resp.text[:100]}...")
    print()

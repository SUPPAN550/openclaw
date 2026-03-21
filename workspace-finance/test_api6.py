import requests

base_url = "http://localhost:8000"

# Try different auth code request formats
print("=== Testing auth code formats ===")

# Try with different field names
for payload in [
    {"email": "admin@local"},
    {"email": "admin@local", "purpose": "login"},
    {"phone": "admin@local"},
    {"username": "admin@local"},
]:
    resp = requests.post(f"{base_url}/v1/auth/request-code", json=payload)
    print(f"Payload: {payload}")
    print(f"Status: {resp.status_code}, Response: {resp.text[:200]}\n")

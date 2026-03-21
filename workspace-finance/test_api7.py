import requests

base_url = "http://localhost:8000"

# Check config endpoint
print("=== Checking config ===")

# Without auth
resp = requests.get(f"{base_url}/v1/config")
print(f"GET /v1/config (no auth) - Status: {resp.status_code}")
print(f"Response: {resp.text[:500] if resp.text else 'empty'}")

# Try auth/me without auth
resp = requests.get(f"{base_url}/v1/auth/me")
print(f"\nGET /v1/auth/me (no auth) - Status: {resp.status_code}")
print(f"Response: {resp.text[:500] if resp.text else 'empty'}")

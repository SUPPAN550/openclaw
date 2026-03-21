import requests

base_url = "http://localhost:8000"

# Check auth endpoints
print("=== Testing auth flow ===")

# Request code (for email/phone auth)
resp = requests.post(f"{base_url}/v1/auth/request-code", json={"email": "admin@local"})
print(f"POST /v1/auth/request-code - Status: {resp.status_code}")
print(f"Response: {resp.text[:500]}")

# Check /healthz
resp = requests.get(f"{base_url}/healthz")
print(f"\nGET /healthz - Status: {resp.status_code}")
print(f"Response: {resp.text}")

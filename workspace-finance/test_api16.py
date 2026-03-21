import requests

base_url = "http://localhost:8000"

# Get a verification code first
print("=== Get access token ===")
resp = requests.post(
    f"{base_url}/v1/auth/request-code",
    json={"email": "admin@local.com"}
)
dev_code = resp.json().get("dev_code")

resp = requests.post(
    f"{base_url}/v1/auth/verify-code",
    json={"email": "admin@local.com", "code": dev_code}
)
auth_result = resp.json()
access_token = auth_result.get("access_token")
print(f"Got access token: {access_token[:50]}...")

# Now try the analyze endpoint with this token
print("\n=== Testing /v1/analyze with access token ===")
headers = {"Authorization": f"Bearer {access_token}"}
resp = requests.post(
    f"{base_url}/v1/analyze",
    json={"symbol": "AAPL"},
    headers=headers
)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text[:500]}")

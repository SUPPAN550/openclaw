import requests

base_url = "http://localhost:8000"

# Get a verification code first
print("=== Step 1: Get verification code ===")
resp = requests.post(
    f"{base_url}/v1/auth/request-code",
    json={"email": "admin@local.com"}
)
result = resp.json()
print(f"Response: {result}")
dev_code = result.get("dev_code")

# Step 2: Verify the code
print(f"\n=== Step 2: Verify code {dev_code} ===")
resp = requests.post(
    f"{base_url}/v1/auth/verify-code",
    json={"email": "admin@local.com", "code": dev_code}
)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text[:500]}")

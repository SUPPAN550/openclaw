import requests

base_url = "http://localhost:8000"

# Check email verification endpoints
print("=== Testing email verification endpoints ===")

# The database has email admin@local
# Let's see if we can get a verification code

# Check what the verify-code endpoint expects
import json

# First, try request-code with proper format
resp = requests.post(
    f"{base_url}/v1/auth/request-code",
    json={"email": "admin@local.com"}
)
print(f"request-code with .com: {resp.status_code} - {resp.text[:100]}")

resp = requests.post(
    f"{base_url}/v1/auth/request-code", 
    json={"email": "test@example.com"}
)
print(f"request-code with example.com: {resp.status_code} - {resp.text[:100]}")

# Try with different purposes
resp = requests.post(
    f"{base_url}/v1/auth/request-code",
    json={"email": "admin@local", "purpose": "register"}
)
print(f"request-code with purpose=register: {resp.status_code} - {resp.text[:100]}")

resp = requests.post(
    f"{base_url}/v1/auth/request-code",
    json={"email": "admin@local", "purpose": "login"}
)
print(f"request-code with purpose=login: {resp.status_code} - {resp.text[:100]}")

import requests
import json

base_url = "http://localhost:8000"

# Check all available paths from the schema
print("=== Looking for auth-related endpoints ===")

# Check for register or signup endpoints
tests = [
    "/v1/register",
    "/v1/signup", 
    "/v1/auth/register",
    "/v1/auth/signup",
    "/v1/auth/login",
    "/v1/login",
    "/v1/users",
    "/v1/user",
]

for path in tests:
    resp = requests.get(f"{base_url}{path}")
    print(f"GET {path}: {resp.status_code}")

# Also check POST variants
print("\n=== POST variants ===")
for path in tests:
    resp = requests.post(f"{base_url}{path}", json={})
    print(f"POST {path}: {resp.status_code} - {resp.text[:100]}")

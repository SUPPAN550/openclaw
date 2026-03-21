import requests
import json

# Test the API with authentication
base_url = "http://localhost:8000"

# First try without auth to see what endpoints require auth
print("=== Testing /v1/analyze without auth ===")
resp = requests.post(f"{base_url}/v1/analyze", json={"symbol": "AAPL"})
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text[:500]}")

print("\n=== Testing with Bearer token ===")
headers = {"Authorization": "Bearer sk-minimax-local-test"}
resp = requests.post(f"{base_url}/v1/analyze", json={"symbol": "AAPL"}, headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text[:500]}")

print("\n=== Testing with different token format ===")
headers = {"Authorization": "sk-minimax-local-test"}
resp = requests.post(f"{base_url}/v1/analyze", json={"symbol": "AAPL"}, headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text[:500]}")

print("\n=== Check API docs ===")
resp = requests.get(f"{base_url}/docs")
print(f"Status: {resp.status_code}")

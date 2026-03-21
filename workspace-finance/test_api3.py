import requests
import json

base_url = "http://localhost:8000"

# Test with the new token
print("=== Testing with ta-sk- token ===")
headers = {"Authorization": "Bearer ta-sk-local-test-token-123"}
resp = requests.post(f"{base_url}/v1/analyze", json={"symbol": "AAPL"}, headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text[:1000]}")

# Try without Bearer prefix
print("\n=== Testing without Bearer prefix ===")
headers = {"Authorization": "ta-sk-local-test-token-123"}
resp = requests.post(f"{base_url}/v1/analyze", json={"symbol": "AAPL"}, headers=headers)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text[:1000]}")

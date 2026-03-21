import requests

base_url = "http://localhost:8000"

# Try various auth approaches
print("=== Testing various auth approaches ===")

# Try API key in different headers
tests = [
    {"headers": {"X-API-Key": "ta-sk-local-test-token-123"}},
    {"headers": {"Api-Key": "ta-sk-local-test-token-123"}},
    {"headers": {"Authorization": "Token ta-sk-local-test-token-123"}},
    {"headers": {"Authorization": "Basic dXNlcjpwYXNz"}},  # user:pass base64
    {"json": {"token": "ta-sk-local-test-token-123"}},
    {"json": {"api_key": "ta-sk-local-test-token-123"}},
]

for i, test in enumerate(tests):
    headers = test.get("headers", {})
    json_data = test.get("json", {})
    
    resp = requests.post(
        f"{base_url}/v1/analyze",
        json={"symbol": "AAPL", **json_data},
        headers=headers
    )
    print(f"Test {i+1}: {headers or json_data}")
    print(f"  Status: {resp.status_code}, Response: {resp.text[:80]}\n")

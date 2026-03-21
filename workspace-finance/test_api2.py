import requests

base_url = "http://localhost:8000"

# Test data endpoints
print("=== Testing data endpoints ===")

# Get available data sources
resp = requests.get(f"{base_url}/api/v1/data/sources")
print(f"/api/v1/data/sources - Status: {resp.status_code}")
print(f"Response: {resp.text[:500] if resp.text else 'empty'}")

# Try market data
resp = requests.get(f"{base_url}/api/v1/market/AAPL")
print(f"\n/api/v1/market/AAPL - Status: {resp.status_code}")
print(f"Response: {resp.text[:500] if resp.text else 'empty'}")

# Try stock data
resp = requests.get(f"{base_url}/api/v1/stock/600519.SZ")
print(f"\n/api/v1/stock/600519.SZ - Status: {resp.status_code}")
print(f"Response: {resp.text[:500] if resp.text else 'empty'}")

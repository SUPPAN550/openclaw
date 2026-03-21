import requests
import time

base_url = "http://localhost:8000"

# Get a new token first
resp = requests.post(f"{base_url}/v1/auth/request-code", json={"email": "test@fix.com"})
dev_code = resp.json().get("dev_code")
resp = requests.post(f"{base_url}/v1/auth/verify-code", json={"email": "test@fix.com", "code": dev_code})
token = resp.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

# Create a persistent API token
resp = requests.post(f"{base_url}/v1/tokens", headers=headers, json={"name": "fixed-token"})
new_token = resp.json().get("token")
print(f"New token: {new_token}")

# Use the new token
headers = {"Authorization": f"Bearer {new_token}"}

# Test analysis
print("\n=== Submitting analysis for 300558.SZ ===")
resp = requests.post(f"{base_url}/v1/analyze", json={"symbol": "300558.SZ", "trade_date": "2026-03-21"}, headers=headers)
result = resp.json()
print(f"Response: {result}")

if "job_id" in result:
    job_id = result["job_id"]
    print(f"\nJob ID: {job_id}")
    print("Waiting for completion...")
    
    for i in range(90):
        time.sleep(10)
        resp = requests.get(f"{base_url}/v1/jobs/{job_id}", headers=headers)
        status_result = resp.json()
        status = status_result.get("status")
        print(f"  Check {i+1}: {status}")
        
        if status == "completed":
            print("\n=== Analysis Complete ===")
            # Get full result
            resp = requests.get(f"{base_url}/v1/jobs/{job_id}/result", headers=headers)
            full_result = resp.json()
            
            print(f"Decision: {full_result.get('decision')}")
            print(f"Direction: {full_result.get('direction')}")
            print(f"Confidence: {full_result.get('confidence')}")
            print(f"Target Price: {full_result.get('target_price')}")
            print(f"Stop Loss: {full_result.get('stop_loss_price')}")
            print(f"Risks: {full_result.get('risk_items')}")
            print(f"Key Metrics: {full_result.get('key_metrics')}")
            
            # Print final trade decision
            if 'result' in full_result and full_result['result']:
                r = full_result['result']
                if 'final_trade_decision' in r:
                    print(f"\nFinal Trade Decision:\n{r['final_trade_decision'][:1000]}...")
            break
        elif status == "failed":
            print(f"Error: {status_result.get('error')}")
            break

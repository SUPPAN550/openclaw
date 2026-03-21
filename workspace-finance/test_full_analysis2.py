import requests
import time

base_url = "http://localhost:8000"
token = "ta-sk-tTFWTVGM7TVX-3VOjgDiGw6MexVvra-24RM9yTh5PDjET8QkL7-tscRXbnmi-ptalIw7zSblFoJPffn2oWbaLA"
headers = {"Authorization": f"Bearer {token}"}

# Try with more explicit parameters
payload = {
    "symbol": "300558.SZ",
    "trade_date": "2026-03-21",
    "horizons": ["短线"]
}

print("=== Submitting new analysis ===")
resp = requests.post(f"{base_url}/v1/analyze", json=payload, headers=headers)
result = resp.json()
print(f"Response: {result}")

if "job_id" in result:
    job_id = result["job_id"]
    print(f"\nJob ID: {job_id}")
    print("Waiting for analysis to complete...")
    
    for i in range(60):
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
            print(f"Keys: {full_result.keys()}")
            
            # Print key fields
            for key in ['decision', 'direction', 'confidence', 'target_price', 'stop_loss_price']:
                if key in full_result:
                    print(f"{key}: {full_result[key]}")
            
            # Check for reports
            for report_key in ['market_report', 'final_trade_decision', 'decision']:
                if report_key in full_result:
                    print(f"\n{report_key}: {str(full_result[report_key])[:500]}")
            break
        elif status == "failed":
            print(f"Error: {status_result.get('error')}")
            break

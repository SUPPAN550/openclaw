import requests
import time

base_url = "http://localhost:8000"
token = "ta-sk-yHTFymCDkfEGY1wyUtnHWrICrTimVkFcIwpaaw8t97L6x43R7_xmMp1IIvOyixH9rCyyGvCmhHBAt5h23b6jiw"
headers = {"Authorization": f"Bearer {token}"}

# 配置短线+中线
payload = {
    "symbol": "300558.SZ",
    "trade_date": "2026-03-21",
    "horizons": ["短线", "中线"]
}

print("=== Submitting analysis with short + medium term ===")
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
            resp = requests.get(f"{base_url}/v1/jobs/{job_id}/result", headers=headers)
            full_result = resp.json()
            print(f"Keys: {full_result.keys()}")
            
            # Print key fields
            for key in ['decision', 'direction', 'confidence', 'target_price', 'stop_loss_price']:
                if key in full_result:
                    print(f"{key}: {full_result[key]}")
            break
        elif status == "failed":
            print(f"Error: {status_result.get('error')}")
            break

import requests
import time

base_url = "http://localhost:8000"

# Use the working persistent token
token = "ta-sk-tTFWTVGM7TVX-3VOjgDiGw6MexVvra-24RM9yTh5PDjET8QkL7-tscRXbnmi-ptalIw7zSblFoJPffn2oWbaLA"
headers = {"Authorization": f"Bearer {token}"}

# Test with a smaller subset of analysts first
selected_analysts = ["market", "sentiment"]

print(f"=== Testing with analysts: {selected_analysts} ===")
resp = requests.post(f"{base_url}/v1/analyze", json={"symbol": "AAPL", "selected_analysts": selected_analysts}, headers=headers)
print(f"Status code: {resp.status_code}")
if resp.status_code == 200:
    job_id = resp.json().get("job_id")
    print(f"Job ID: {job_id}")
    
    # Poll for result
    for i in range(30):
        resp = requests.get(f"{base_url}/v1/jobs/{job_id}", headers=headers)
        result = resp.json()
        status = result.get("status")
        print(f"  Status check {i+1}: {status}")
        
        if status == "completed":
            print(f"\n=== Analysis Complete! ===")
            print(f"Decision: {result.get('decision')}")
            print(f"Direction: {result.get('direction')}")
            print(f"Confidence: {result.get('confidence')}")
            break
        elif status == "failed":
            print(f"Error: {result.get('error')}")
            break
        
        time.sleep(5)
else:
    print(f"Error: {resp.status_code} - {resp.text}")

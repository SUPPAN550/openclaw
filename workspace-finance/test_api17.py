import requests
import time

base_url = "http://localhost:8000"

# Get access token
resp = requests.post(f"{base_url}/v1/auth/request-code", json={"email": "admin@local.com"})
dev_code = resp.json().get("dev_code")
resp = requests.post(f"{base_url}/v1/auth/verify-code", json={"email": "admin@local.com", "code": dev_code})
access_token = resp.json().get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}

# Get the job ID from before
job_id = "65428fd0422444fdb8cd993f949b7361"

# Check job status
print("=== Checking job status ===")
for i in range(5):
    resp = requests.get(f"{base_url}/v1/jobs/{job_id}", headers=headers)
    result = resp.json()
    print(f"Status check {i+1}: {result.get('status')}")
    if result.get('status') == 'completed':
        print(f"Job completed! Result: {result.get('decision')}")
        break
    elif result.get('status') == 'failed':
        print(f"Job failed: {result.get('error')}")
        break
    time.sleep(2)

# Also check if we can create a persistent API token
print("\n=== Creating persistent API token ===")
resp = requests.post(f"{base_url}/v1/tokens", headers=headers, json={"name": "my-persistent-token"})
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text[:500]}")

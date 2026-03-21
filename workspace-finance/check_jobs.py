import requests
import time

base_url = "http://localhost:8000"

# Use the persistent token
token = "ta-sk-tTFWTVGM7TVX-3VOjgDiGw6MexVvra-24RM9yTh5PDjET8QkL7-tscRXbnmi-ptalIw7zSblFoJPffn2oWbaLA"
headers = {"Authorization": f"Bearer {token}"}

# Check the most recent job
jobs_to_check = [
    "553a0eee9c5b4016a2be32d341c2ccce",  # Last test job
    "08ab8110b87f4b23afe827309435f3cc",
    "65428fd0422444fdb8cd993f949b7361",
]

for job_id in jobs_to_check:
    print(f"=== Checking job: {job_id} ===")
    resp = requests.get(f"{base_url}/v1/jobs/{job_id}", headers=headers)
    result = resp.json()
    print(f"Status: {result.get('status')}")
    if result.get('status') == 'completed':
        print(f"Decision: {result.get('decision')}")
        print(f"Direction: {result.get('direction')}")
        print(f"Confidence: {result.get('confidence')}")
        break
    elif result.get('status') == 'failed':
        print(f"Error: {result.get('error')}")
    print()

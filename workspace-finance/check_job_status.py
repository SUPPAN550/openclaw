import requests

base_url = "http://localhost:8000"
token = "ta-sk-tTFWTVGM7TVX-3VOjgDiGw6MexVvra-24RM9yTh5PDjET8QkL7-tscRXbnmi-ptalIw7zSblFoJPffn2oWbaLA"
headers = {"Authorization": f"Bearer {token}"}

# Check job status
job_id = "0a92b91047dd436db3d942835e369ccc"
resp = requests.get(f"{base_url}/v1/jobs/{job_id}", headers=headers)
result = resp.json()
print(f"Status: {result.get('status')}")
print(f"Full result: {result}")

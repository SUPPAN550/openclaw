import requests
import time

token = 'ta-sk-A_ezf4TQoSmYuEEYKswZHtMU1C-FP0_hCHoHecBfpbhUy69xQcpfA5P64md5nAOT3Bz0OhIbhDmmdKg0dCNtFA'
headers = {'Authorization': f'Bearer {token}'}
job_id = '109264420ffa441aa62de6db50aaccf6'

print("Checking job status...")
for i in range(60):
    time.sleep(10)
    r = requests.get(f'http://localhost:8000/v1/jobs/{job_id}', headers=headers)
    status = r.json().get('status')
    print(f'Check {i+1}: {status}')
    
    if status == 'completed':
        print('Analysis completed!')
        r2 = requests.get(f'http://localhost:8000/v1/jobs/{job_id}/result', headers=headers)
        result = r2.json()
        print(f"Keys: {result.keys()}")
        print(f"Decision: {result.get('decision')}")
        print(f"Direction: {result.get('direction')}")
        
        # Check for analyst reports
        if 'reports' in result:
            reports = result['reports']
            print(f"\n=== Analysts Summary ===")
            for analyst, report in reports.items():
                print(f"{analyst}: {str(report)[:100]}...")
        break
    elif status == 'failed':
        print(f"Error: {r.json().get('error')}")
        break

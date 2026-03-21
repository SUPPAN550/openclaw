import requests

base_url = "http://localhost:8000"

# Try to get the API schema
print("=== Getting API schema ===")
resp = requests.get(f"{base_url}/openapi.json")
if resp.status_code == 200:
    schema = resp.json()
    print("Endpoints:")
    for path, methods in schema.get('paths', {}).items():
        for method, details in methods.items():
            print(f"  {method.upper()} {path}")
            # Check for auth requirements
            if 'security' in details:
                print(f"    Auth: {details['security']}")

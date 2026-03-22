import requests

base_url = 'http://localhost:8000'
token = 'ta-sk-yHTFymCDkfEGY1wyUtnHWrICrTimVkFcIwpaaw8t97L6x43R7_xmMp1IIvOyixH9rCyyGvCmhHBAt5h23b6jiw'
headers = {'Authorization': f'Bearer {token}'}

# Check API docs for available params
resp = requests.get(f'{base_url}/openapi.json')
spec = resp.json()

# Look at analyze endpoint
analyze = spec.get('paths', {}).get('/v1/analyze', {})
request_body = analyze.get('post', {}).get('requestBody', {})
content = request_body.get('content', {}).get('application/json', {})
schema = content.get('schema', {})
print('Request body schema:')
props = schema.get('properties', {})
for name, info in props.items():
    print(f'  - {name}')

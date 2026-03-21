import subprocess
import re

result = subprocess.run(
    ["docker", "logs", "tradingagents", "--tail", "100"],
    capture_output=True,
    text=True
)

# Find error related to our job
lines = result.stdout.split('\n')
for i, line in enumerate(lines):
    if '41eabf65d933' in line or 'RuntimeError' in line or 'Error' in line:
        # Print context around the error
        start = max(0, i-5)
        end = min(len(lines), i+10)
        print('\n'.join(lines[start:end]))
        print('---')

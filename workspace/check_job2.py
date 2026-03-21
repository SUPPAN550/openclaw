# -*- coding: utf-8 -*-
import requests
import json

TOKEN = "ta-sk-hHDsjnHSyIci4Ebzis_bIVXloJGKW_IfF1p2HYFki0emVUESW-NbngffYCMKsLsMplmVYn2-xxrzpBuAGT1bZg"

# 检查第二个任务
job_id = "4d36b6c41d5b468daf58655861a9f46c"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

status_url = f"https://api.510168.xyz/v1/jobs/{job_id}"
r = requests.get(status_url, headers=headers, timeout=30)
status = r.json()
print(json.dumps(status, indent=2, ensure_ascii=False))

if status.get('status') == 'completed':
    result_url = f"https://api.510168.xyz/v1/jobs/{job_id}/result"
    result_r = requests.get(result_url, headers=headers, timeout=30)
    final = result_r.json()
    print("\n===== 分析结果 =====")
    print(json.dumps(final, indent=2, ensure_ascii=False))

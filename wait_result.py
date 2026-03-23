# -*- coding: utf-8 -*-
import requests
import json
import time

TOKEN = "ta-sk-hHDsjnHSyIci4Ebzis_bIVXloJGKW_IfF1p2HYFki0emVUESW-NbngffYCMKsLsMplmVYn2-xxrzpBuAGT1bZg"

job_id = "4d36b6c41d5b468daf58655861a9f46c"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print("等待分析完成...")

# 等待并轮询
for i in range(20):
    time.sleep(15)
    status_url = f"https://api.510168.xyz/v1/jobs/{job_id}"
    status_r = requests.get(status_url, headers=headers, timeout=30)
    status = status_r.json()
    print(f"轮询 {i+1}: {status.get('status')}")
    
    if status.get('status') == 'completed':
        # 获取完整结果
        result_url = f"https://api.510168.xyz/v1/jobs/{job_id}/result"
        result_r = requests.get(result_url, headers=headers, timeout=30)
        final = result_r.json()
        print("\n===== 贝达药业分析结果 =====")
        print(json.dumps(final, indent=2, ensure_ascii=False))
        break
    elif status.get('status') == 'failed':
        print("分析失败!")
        print(status.get('error'))
        break

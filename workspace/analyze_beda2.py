# -*- coding: utf-8 -*-
import requests
import json
import time

TOKEN = "ta-sk-hHDsjnHSyIci4Ebzis_bIVXloJGKW_IfF1p2HYFki0emVUESW-NbngffYCMKsLsMplmVYn2-xxrzpBuAGT1bZg"

# 提交分析任务 - 用代码
url = "https://api.510168.xyz/v1/analyze"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
data = {
    "symbol": "300558.SZ"
}

print("提交新任务: 300558.SZ")
r = requests.post(url, json=data, headers=headers, timeout=30)
result = r.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

if 'job_id' in result:
    job_id = result['job_id']
    print(f"新任务ID: {job_id}")
    
    # 等30秒
    print("等待30秒...")
    time.sleep(30)
    
    # 检查状态
    status_url = f"https://api.510168.xyz/v1/jobs/{job_id}"
    status_r = requests.get(status_url, headers=headers, timeout=30)
    status = status_r.json()
    print(f"状态: {status.get('status')}")
    
    if status.get('status') == 'completed':
        result_url = f"https://api.510168.xyz/v1/jobs/{job_id}/result"
        result_r = requests.get(result_url, headers=headers, timeout=30)
        final = result_r.json()
        print("\n===== 分析结果 =====")
        print(json.dumps(final, indent=2, ensure_ascii=False))

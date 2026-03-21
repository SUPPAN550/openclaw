# -*- coding: utf-8 -*-
import requests
import json

TOKEN = "ta-sk-hHDsjnHSyIci4Ebzis_bIVXloJGKW_IfF1p2HYFki0emVUESW-NbngffYCMKsLsMplmVYn2-xxrzpBuAGT1bZg"

job_id = "2511ecfc43a04fa89f82396729f504b7"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 检查任务状态
status_url = f"https://api.510168.xyz/v1/jobs/{job_id}"
r = requests.get(status_url, headers=headers, timeout=30)
status = r.json()
print(json.dumps(status, indent=2, ensure_ascii=False))

if status.get('status') == 'completed':
    # 获取完整结果
    result_url = f"https://api.510168.xyz/v1/jobs/{job_id}/result"
    result_r = requests.get(result_url, headers=headers, timeout=30)
    final = result_r.json()
    print("\n===== 分析结果 =====")
    print(json.dumps(final, indent=2, ensure_ascii=False))

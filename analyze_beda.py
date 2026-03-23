# -*- coding: utf-8 -*-
import requests
import json
import time
import sys

TOKEN = "ta-sk-hHDsjnHSyIci4Ebzis_bIVXloJGKW_IfF1p2HYFki0emVUESW-NbngffYCMKsLsMplmVYn2-xxrzpBuAGT1bZg"

print("开始分析贝达药业...", file=sys.stderr)

# 提交分析任务
url = "https://api.510168.xyz/v1/analyze"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
data = {
    "symbol": "贝达药业"
}

print("提交分析任务...", file=sys.stderr)

try:
    r = requests.post(url, json=data, headers=headers, timeout=30)
    print(f"Status: {r.status_code}", file=sys.stderr)
    result = r.json()
    print(json.dumps(result, indent=2, ensure_ascii=False), file=sys.stderr)
    
    if 'job_id' in result:
        job_id = result['job_id']
        print(f"任务ID: {job_id}", file=sys.stderr)
        
        # 轮询任务状态
        for i in range(20):
            time.sleep(15)
            status_url = f"https://api.510168.xyz/v1/jobs/{job_id}"
            status_r = requests.get(status_url, headers=headers, timeout=30)
            status = status_r.json()
            print(f"轮询 {i+1}: {status.get('status', 'unknown')}", file=sys.stderr)
            
            if status.get('status') == 'completed':
                # 获取完整结果
                result_url = f"https://api.510168.xyz/v1/jobs/{job_id}/result"
                result_r = requests.get(result_url, headers=headers, timeout=30)
                final = result_r.json()
                print("\n===== 分析结果 =====")
                print(json.dumps(final, indent=2, ensure_ascii=False))
                break
            elif status.get('status') == 'failed':
                print("分析失败!", file=sys.stderr)
                break
    else:
        print("提交失败", file=sys.stderr)
        
except Exception as e:
    print(f"错误: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()

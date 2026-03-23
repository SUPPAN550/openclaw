# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd
import sys

sys.stdout = open(r"C:\Users\Administrator\.openclaw\workspace\script_output.txt", "w", encoding="utf-8")
sys.stderr = open(r"C:\Users\Administrator\.openclaw\workspace\script_error.txt", "w", encoding="utf-8")

print("=== Fetching market data ===")

# 1. Market activity
try:
    df_activity = ak.stock_market_activity_legu()
    print("\nMarket Activity:")
    print(df_activity.to_string())
    
    rise = df_activity[df_activity['item'] == '上涨']['value'].values[0]
    fall = df_activity[df_activity['item'] == '下跌']['value'].values[0]
    flat = df_activity[df_activity['item'] == '平盘']['value'].values[0]
    limit_up = df_activity[df_activity['item'] == '涨停']['value'].values[0]
    limit_down = df_activity[df_activity['item'] == '跌停']['value'].values[0]
    activity = df_activity[df_activity['item'] == '活跃度']['value'].values[0]
    date = df_activity[df_activity['item'] == '统计日期']['value'].values[0]
    total = rise + fall + flat
    
    print(f"\nRise: {rise}, Fall: {fall}, Flat: {flat}, Total: {total}")
    print(f"Limit Up: {limit_up}, Limit Down: {limit_down}, Activity: {activity}, Date: {date}")
except Exception as e:
    print(f"Error activity: {e}")

# 2. Province trading volume
try:
    df_province = ak.stock_szse_area_summary()
    print("\nProvince Trading Volume (sorted):")
    df_sorted = df_province.sort_values('总交易额', ascending=False)
    print(df_sorted.to_string())
    
    # Save province data
    df_province.to_csv(r"C:\Users\Administrator\.openclaw\workspace\province_data.csv", index=False, encoding='utf-8-sig')
    print("\nProvince data saved.")
except Exception as e:
    print(f"Error province: {e}")

# 3. SSE summary
try:
    df_sse = ak.stock_sse_summary()
    print("\nSSE Summary:")
    print(df_sse.to_string())
except Exception as e:
    print(f"Error sse: {e}")

# 4. SZSE summary
try:
    df_szse = ak.stock_szse_summary()
    print("\nSZSE Summary:")
    print(df_szse.to_string())
except Exception as e:
    print(f"Error szse: {e}")

sys.stdout.close()
sys.stderr.close()

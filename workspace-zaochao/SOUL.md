# 鏃╂湞绠€鎶ュ畼 路 閽﹀ぉ鐩?

浣犵殑鍞竴鑱岃矗锛氭瘡鏃ユ棭鏈濆墠閲囬泦鍏ㄧ悆閲嶈鏂伴椈锛岀敓鎴愬浘鏂囧苟鑼傜殑绠€鎶ワ紝淇濆瓨渚涚殗涓婂尽瑙堛€?

## 鎵ц姝ラ锛堟瘡娆¤繍琛屽繀椤诲叏閮ㄥ畬鎴愶級

1. 鐢?web_search 鍒嗗洓绫绘悳绱㈡柊闂伙紝姣忕被鎼?5 鏉★細
   - 鏀挎不: "world political news" freshness=pd
   - 鍐涗簨: "military conflict war news" freshness=pd  
   - 缁忔祹: "global economy markets" freshness=pd
   - AI澶фā鍨? "AI LLM large language model breakthrough" freshness=pd

2. 鏁寸悊鎴?JSON锛屼繚瀛樺埌椤圭洰 `data/morning_brief.json`
   璺緞鑷姩瀹氫綅锛歚REPO = pathlib.Path(__file__).resolve().parent.parent`
   鏍煎紡锛?
   ```json
   {
     "date": "YYYY-MM-DD",
     "generatedAt": "HH:MM",
     "categories": [
       {
         "key": "politics",
         "label": "馃彌锔?鏀挎不",
         "items": [
           {
             "title": "鏍囬锛堜腑鏂囷級",
             "summary": "50瀛楁憳瑕侊紙涓枃锛?,
             "source": "鏉ユ簮鍚?,
             "url": "閾炬帴",
             "image_url": "鍥剧墖閾炬帴鎴栫┖瀛楃涓?,
             "published": "鏃堕棿鎻忚堪"
           }
         ]
       }
     ]
   }
   ```

3. 鍚屾椂瑙﹀彂鍒锋柊锛?
   ```bash
   python3 scripts/refresh_live_data.py  # 鍦ㄩ」鐩牴鐩綍涓嬫墽琛?
   ```

4. 鐢ㄩ涔﹂€氱煡鐨囦笂锛堝彲閫夛紝濡傛灉閰嶇疆浜嗛涔︾殑璇濓級

娉ㄦ剰锛?
- 鏍囬鍜屾憳瑕佸潎缈昏瘧涓轰腑鏂?
- 鍥剧墖URL濡傛棤娉曡幏鍙栧～绌哄瓧绗︿覆""
- 鍘婚噸锛氬悓涓€浜嬩欢鍙繚鐣欐渶鐩稿叧鐨勪竴鏉?
- 鍙彇24灏忔椂鍐呮柊闂伙紙freshness=pd锛?

---

## 馃摗 瀹炴椂杩涘睍涓婃姤

> 濡傛灉鏄棬鎰忎换鍔¤Е鍙戠殑绠€鎶ョ敓鎴愶紝蹇呴』鐢?`progress` 鍛戒护涓婃姤杩涘睍銆?

```bash
python3 scripts/kanban_update.py progress JJC-xxx "姝ｅ湪閲囬泦鍏ㄧ悆鏂伴椈锛屽凡瀹屾垚鏀挎不/鍐涗簨绫? "鏀挎不鏂伴椈閲囬泦鉁厊鍐涗簨鏂伴椈閲囬泦鉁厊缁忔祹鏂伴椈閲囬泦馃攧|AI鏂伴椈閲囬泦|鐢熸垚绠€鎶?
```


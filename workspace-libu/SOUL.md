# 绀奸儴 路 灏氫功

浣犳槸绀奸儴灏氫功锛岃礋璐ｅ湪灏氫功鐪佹淳鍙戠殑浠诲姟涓壙鎷?*鏂囨。銆佽鑼冦€佺敤鎴风晫闈笌瀵瑰娌熼€?*鐩稿叧鐨勬墽琛屽伐浣溿€?

## 涓撲笟棰嗗煙
绀奸儴鎺岀鍏哥珷浠埗锛屼綘鐨勪笓闀垮湪浜庯細
- **鏂囨。涓庤鑼?*锛歊EADME銆丄PI鏂囨。銆佺敤鎴锋寚鍗椼€佸彉鏇存棩蹇楁挵鍐?
- **妯℃澘涓庢牸寮?*锛氳緭鍑鸿鑼冨埗瀹氥€丮arkdown 鎺掔増銆佺粨鏋勫寲鍐呭璁捐
- **鐢ㄦ埛浣撻獙**锛歎I/UX 鏂囨銆佷氦浜掕璁″鏌ャ€佸彲璁块棶鎬ф敼杩?
- **瀵瑰娌熼€?*锛歊elease Notes銆佸叕鍛婅崏鎷熴€佸璇█缈昏瘧

褰撳皻涔︾渷娲惧彂鐨勫瓙浠诲姟娑夊強浠ヤ笂棰嗗煙鏃讹紝浣犳槸棣栭€夋墽琛岃€呫€?

## 鏍稿績鑱岃矗
1. 鎺ユ敹灏氫功鐪佷笅鍙戠殑瀛愪换鍔?
2. **绔嬪嵆鏇存柊鐪嬫澘**锛圕LI 鍛戒护锛?
3. 鎵ц浠诲姟锛岄殢鏃舵洿鏂拌繘灞?
4. 瀹屾垚鍚?*绔嬪嵆鏇存柊鐪嬫澘**锛屼笂鎶ユ垚鏋滅粰灏氫功鐪?

---

## 馃洜 鐪嬫澘鎿嶄綔锛堝繀椤荤敤 CLI 鍛戒护锛?

> 鈿狅笍 **鎵€鏈夌湅鏉挎搷浣滃繀椤荤敤 `kanban_update.py` CLI 鍛戒护**锛屼笉瑕佽嚜宸辫鍐?JSON 鏂囦欢锛?
> 鑷鎿嶄綔鏂囦欢浼氬洜璺緞闂瀵艰嚧闈欓粯澶辫触锛岀湅鏉垮崱浣忎笉鍔ㄣ€?

### 鈿?鎺ヤ换鍔℃椂锛堝繀椤荤珛鍗虫墽琛岋級
```bash
python3 scripts/kanban_update.py state JJC-xxx Doing "绀奸儴寮€濮嬫墽琛孾瀛愪换鍔"
python3 scripts/kanban_update.py flow JJC-xxx "绀奸儴" "绀奸儴" "鈻讹笍 寮€濮嬫墽琛岋細[瀛愪换鍔″唴瀹筣"
```

### 鉁?瀹屾垚浠诲姟鏃讹紙蹇呴』绔嬪嵆鎵ц锛?
```bash
python3 scripts/kanban_update.py flow JJC-xxx "绀奸儴" "灏氫功鐪? "鉁?瀹屾垚锛歔浜у嚭鎽樿]"
```

鐒跺悗鐢?`sessions_send` 鎶婃垚鏋滃彂缁欏皻涔︾渷銆?

### 馃毇 闃诲鏃讹紙绔嬪嵆涓婃姤锛?
```bash
python3 scripts/kanban_update.py state JJC-xxx Blocked "[闃诲鍘熷洜]"
python3 scripts/kanban_update.py flow JJC-xxx "绀奸儴" "灏氫功鐪? "馃毇 闃诲锛歔鍘熷洜]锛岃姹傚崗鍔?
```

## 鈿狅笍 鍚堣瑕佹眰
- 鎺ヤ换/瀹屾垚/闃诲锛屼笁绉嶆儏鍐?*蹇呴』**鏇存柊鐪嬫澘
- 灏氫功鐪佽鏈?4灏忔椂瀹¤锛岃秴鏃舵湭鏇存柊鑷姩鏍囩孩棰勮
- 鍚忛儴(libu_hr)璐熻矗浜轰簨/鍩硅/Agent绠＄悊

---

## 馃摗 瀹炴椂杩涘睍涓婃姤锛堝繀鍋氾紒锛?

> 馃毃 **鎵ц浠诲姟杩囩▼涓紝蹇呴』鍦ㄦ瘡涓叧閿楠よ皟鐢?`progress` 鍛戒护涓婃姤褰撳墠鎬濊€冨拰杩涘睍锛?*

### 绀轰緥锛?
```bash
# 寮€濮嬫挵鍐?
python3 scripts/kanban_update.py progress JJC-xxx "姝ｅ湪鍒嗘瀽鏂囨。缁撴瀯闇€姹傦紝纭畾澶х翰" "闇€姹傚垎鏋愷煍剕澶х翰璁捐|鍐呭鎾板啓|鎺掔増缇庡寲|鎻愪氦鎴愭灉"

# 鎾板啓涓?
python3 scripts/kanban_update.py progress JJC-xxx "澶х翰纭畾锛屾鍦ㄦ挵鍐欐牳蹇冪珷鑺? "闇€姹傚垎鏋愨渽|澶х翰璁捐鉁厊鍐呭鎾板啓馃攧|鎺掔増缇庡寲|鎻愪氦鎴愭灉"
```

### 鐪嬫澘鍛戒护瀹屾暣鍙傝€?
```bash
python3 scripts/kanban_update.py state <id> <state> "<璇存槑>"
python3 scripts/kanban_update.py flow <id> "<from>" "<to>" "<remark>"
python3 scripts/kanban_update.py progress <id> "<褰撳墠鍦ㄥ仛浠€涔?" "<璁″垝1鉁厊璁″垝2馃攧|璁″垝3>"
python3 scripts/kanban_update.py todo <id> <todo_id> "<title>" <status> --detail "<浜у嚭璇︽儏>"
```

### 馃摑 瀹屾垚瀛愪换鍔℃椂涓婃姤璇︽儏锛堟帹鑽愶紒锛?
```bash
# 瀹屾垚浠诲姟鍚庯紝涓婃姤鍏蜂綋浜у嚭
python3 scripts/kanban_update.py todo JJC-xxx 1 "[瀛愪换鍔″悕]" completed --detail "浜у嚭姒傝锛歕n- 瑕佺偣1\n- 瑕佺偣2\n楠岃瘉缁撴灉锛氶€氳繃"
```

## 璇皵
鏂囬泤绔锛屾帾杈炵簿鐐笺€備骇鍑虹墿娉ㄩ噸鍙鎬т笌鎺掔増缇庢劅銆?


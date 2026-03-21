# 灏氫功鐪?路 鎵ц璋冨害

浣犳槸灏氫功鐪侊紝浠?**subagent** 鏂瑰紡琚腑涔︾渷璋冪敤銆傛帴鏀跺噯濂忔柟妗堝悗锛屾淳鍙戠粰鍏儴鎵ц锛屾眹鎬荤粨鏋滆繑鍥炪€?

> **浣犳槸 subagent锛氭墽琛屽畬姣曞悗鐩存帴杩斿洖缁撴灉鏂囨湰锛屼笉鐢?sessions_send 鍥炰紶銆?*

## 鏍稿績娴佺▼

### 1. 鏇存柊鐪嬫澘 鈫?娲惧彂
```bash
python3 scripts/kanban_update.py state JJC-xxx Doing "灏氫功鐪佹淳鍙戜换鍔＄粰鍏儴"
python3 scripts/kanban_update.py flow JJC-xxx "灏氫功鐪? "鍏儴" "娲惧彂锛歔姒傝]"
```

### 2. 鏌ョ湅 dispatch SKILL 纭畾瀵瑰簲閮ㄩ棬
鍏堣鍙?dispatch 鎶€鑳借幏鍙栭儴闂ㄨ矾鐢憋細
```
璇诲彇 skills/dispatch/SKILL.md
```

| 閮ㄩ棬 | agent_id | 鑱岃矗 |
|------|----------|------|
| 宸ラ儴 | gongbu | 寮€鍙?鏋舵瀯/浠ｇ爜 |
| 鍏甸儴 | bingbu | 鍩虹璁炬柦/閮ㄧ讲/瀹夊叏 |
| 鎴烽儴 | hubu | 鏁版嵁鍒嗘瀽/鎶ヨ〃/鎴愭湰 |
| 绀奸儴 | libu | 鏂囨。/UI/瀵瑰娌熼€?|
| 鍒戦儴 | xingbu | 瀹℃煡/娴嬭瘯/鍚堣 |
| 鍚忛儴 | libu_hr | 浜轰簨/Agent绠＄悊/鍩硅 |

### 3. 璋冪敤鍏儴 subagent 鎵ц
瀵规瘡涓渶瑕佹墽琛岀殑閮ㄩ棬锛?*璋冪敤鍏?subagent**锛屽彂閫佷换鍔′护锛?
```
馃摦 灏氫功鐪伮蜂换鍔′护
浠诲姟ID: JJC-xxx
浠诲姟: [鍏蜂綋鍐呭]
杈撳嚭瑕佹眰: [鏍煎紡/鏍囧噯]
```

### 4. 姹囨€昏繑鍥?
```bash
python3 scripts/kanban_update.py done JJC-xxx "<浜у嚭>" "<鎽樿>"
python3 scripts/kanban_update.py flow JJC-xxx "鍏儴" "灏氫功鐪? "鉁?鎵ц瀹屾垚"
```

杩斿洖姹囨€荤粨鏋滄枃鏈粰涓功鐪併€?

## 馃洜 鐪嬫澘鎿嶄綔
```bash
python3 scripts/kanban_update.py state <id> <state> "<璇存槑>"
python3 scripts/kanban_update.py flow <id> "<from>" "<to>" "<remark>"
python3 scripts/kanban_update.py done <id> "<output>" "<summary>"
python3 scripts/kanban_update.py todo <id> <todo_id> "<title>" <status> --detail "<浜у嚭璇︽儏>"
python3 scripts/kanban_update.py progress <id> "<褰撳墠鍦ㄥ仛浠€涔?" "<璁″垝1鉁厊璁″垝2馃攧|璁″垝3>"
```

### 馃摑 瀛愪换鍔¤鎯呬笂鎶ワ紙鎺ㄨ崘锛侊級

> 姣忓畬鎴愪竴涓瓙浠诲姟娲惧彂/姹囨€绘椂锛岀敤 `todo` 鍛戒护甯?`--detail` 涓婃姤浜у嚭锛岃鐨囦笂鐪嬪埌鍏蜂綋鎴愭灉锛?

```bash
# 娲惧彂瀹屾垚
python3 scripts/kanban_update.py todo JJC-xxx 1 "娲惧彂宸ラ儴" completed --detail "宸叉淳鍙戝伐閮ㄦ墽琛屼唬鐮佸紑鍙戯細\n- 妯″潡A閲嶆瀯\n- 鏂板API鎺ュ彛\n- 宸ラ儴纭鎺ヤ护"
```

---

## 馃摗 瀹炴椂杩涘睍涓婃姤锛堝繀鍋氾紒锛?

> 馃毃 **浣犲湪娲惧彂鍜屾眹鎬昏繃绋嬩腑锛屽繀椤昏皟鐢?`progress` 鍛戒护涓婃姤褰撳墠鐘舵€侊紒**
> 鐨囦笂閫氳繃鐪嬫澘浜嗚В鍝簺閮ㄩ棬鍦ㄦ墽琛屻€佹墽琛屽埌鍝竴姝ヤ簡銆?

### 浠€涔堟椂鍊欎笂鎶ワ細
1. **鍒嗘瀽鏂规纭畾娲惧彂瀵硅薄鏃?* 鈫?涓婃姤"姝ｅ湪鍒嗘瀽鏂规锛岀‘瀹氭淳鍙戠粰鍝簺閮ㄩ棬"
2. **寮€濮嬫淳鍙戝瓙浠诲姟鏃?* 鈫?涓婃姤"姝ｅ湪娲惧彂瀛愪换鍔＄粰宸ラ儴/鎴烽儴/鈥?
3. **绛夊緟鍏儴鎵ц鏃?* 鈫?涓婃姤"宸ラ儴宸叉帴浠ゆ墽琛屼腑锛岀瓑寰呮埛閮ㄥ搷搴?
4. **鏀跺埌閮ㄥ垎缁撴灉鏃?* 鈫?涓婃姤"宸叉敹鍒板伐閮ㄧ粨鏋滐紝绛夊緟鎴烽儴"
5. **姹囨€昏繑鍥炴椂** 鈫?涓婃姤"鎵€鏈夐儴闂ㄦ墽琛屽畬鎴愶紝姝ｅ湪姹囨€荤粨鏋?

### 绀轰緥锛?
```bash
# 鍒嗘瀽娲惧彂
python3 scripts/kanban_update.py progress JJC-xxx "姝ｅ湪鍒嗘瀽鏂规锛岄渶娲惧彂缁欏伐閮?浠ｇ爜)鍜屽垜閮?娴嬭瘯)" "鍒嗘瀽娲惧彂鏂规馃攧|娲惧彂宸ラ儴|娲惧彂鍒戦儴|姹囨€荤粨鏋渱鍥炰紶涓功鐪?

# 娲惧彂涓?
python3 scripts/kanban_update.py progress JJC-xxx "宸叉淳鍙戝伐閮ㄥ紑濮嬪紑鍙戯紝姝ｅ湪娲惧彂鍒戦儴杩涜娴嬭瘯" "鍒嗘瀽娲惧彂鏂规鉁厊娲惧彂宸ラ儴鉁厊娲惧彂鍒戦儴馃攧|姹囨€荤粨鏋渱鍥炰紶涓功鐪?

# 绛夊緟鎵ц
python3 scripts/kanban_update.py progress JJC-xxx "宸ラ儴銆佸垜閮ㄥ潎宸叉帴浠ゆ墽琛屼腑锛岀瓑寰呯粨鏋滆繑鍥? "鍒嗘瀽娲惧彂鏂规鉁厊娲惧彂宸ラ儴鉁厊娲惧彂鍒戦儴鉁厊姹囨€荤粨鏋滒煍剕鍥炰紶涓功鐪?

# 姹囨€诲畬鎴?
python3 scripts/kanban_update.py progress JJC-xxx "鎵€鏈夐儴闂ㄦ墽琛屽畬鎴愶紝姝ｅ湪姹囨€绘垚鏋滄姤鍛? "鍒嗘瀽娲惧彂鏂规鉁厊娲惧彂宸ラ儴鉁厊娲惧彂鍒戦儴鉁厊姹囨€荤粨鏋溾渽|鍥炰紶涓功鐪侌煍?
```

## 璇皵
骞茬粌楂樻晥锛屾墽琛屽鍚戙€?


#!/usr/bin/env python3
"""
三省六部看板服务器 - Windows 完整版
"""
import json, pathlib, datetime, argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

HOME = pathlib.Path(r"C:\Users\Administrator\.openclaw")
TAIZI_DATA = HOME / "workspace-taizi" / "data"
OPENCLAW_CFG = HOME / "openclaw.json"

def read_json_utf8(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return None

def ts_age(ts_str):
    if not ts_str:
        return None
    try:
        s = ts_str.strip()
        # generatedAt is in local CST (Asia/Shanghai, UTC+8)
        dt = datetime.datetime.fromisoformat(s)
        now = datetime.datetime.now()
        return (now - dt).total_seconds()
    except Exception:
        return None

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(datetime.datetime.now().strftime("%H:%M:%S"), fmt % args)

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def taizi(self, filename, default=None):
        path = TAIZI_DATA / filename
        if path.exists():
            return read_json_utf8(path)
        return default

    def load_live_status(self):
        ls = self.taizi("live_status.json") or {
            "generatedAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "taskSource": "tasks.json",
            "officials": [],
            "tasks": [],
            "history": [],
            "metrics": {"officialCount": 0, "todayDone": 0, "totalDone": 0, "inProgress": 0, "blocked": 0},
            "health": {"syncOk": False, "syncLatencyMs": None, "missingFieldCount": 0},
        }
        gen = ls.get("generatedAt", "")
        age = ts_age(gen)
        ok = age is not None and age < 120
        ls["syncStatus"] = {"ok": ok, "syncLatencyMs": None}
        ls["health"] = {"syncOk": ok, "syncLatencyMs": None}
        return ls

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html", "/dashboard.html"):
            html = pathlib.Path(__file__).parent / "dashboard.html"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(html, "rb") as f:
                self.wfile.write(f.read())
            return

        if path == "/api/live-status":
            ls = self.load_live_status()
            gen = ls.get("generatedAt", "")
            age = ts_age(gen)
            ls["health"] = {"syncOk": age is not None and age < 120, "syncLatencyMs": None}
            self.send_json(ls)
            return

        elif path == "/api/agent-config":
            ac = self.taizi("agent_config.json") or {
                "generatedAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "agents": [], "knownModels": []
            }
            self.send_json(ac)

        elif path == "/api/officials-stats":
            ac = self.taizi("agent_config.json") or {}
            officials = ac.get("agents", [])
            stats = [{
                "id": o.get("id", ""),
                "name": o.get("name", ""),
                "label": o.get("label", ""),
                "emoji": o.get("emoji", "🏛️"),
                "role": o.get("role", o.get("label", "")),
                "merit_score": 0,
                "merit_rank": i+1,
                "tokens_in": 0,
                "tokens_out": 0,
                "cache_read": 0,
                "cache_write": 0,
                "heartbeat": {"status": "idle"},
                "status": "idle"
            } for i, o in enumerate(officials)]
            totals = {"tasks_done": 0, "cost_cny": 0.0}
            self.send_json({
                "generatedAt": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "officials": stats,
                "totals": totals,
                "top_official": officials[0].get("label", "") if officials else ""
            })

        elif path == "/api/model-change-log":
            self.send_json(self.taizi("model_change_log.json") or [])

        elif path == "/api/last-result":
            self.send_json(self.taizi("last_model_change_result.json") or {})

        elif path == "/api/morning-config":
            self.send_json({"enabled": False, "sources": []})

        elif path == "/api/morning-brief":
            self.send_json({"briefs": [], "lastUpdated": None})

        elif path == "/api/agents-status":
            cfg = read_json_utf8(OPENCLAW_CFG) or {}
            agents = cfg.get("agents", {}).get("list", [])
            ac = self.taizi("agent_config.json") or {}
            ac_agents = {a.get("id"): a for a in ac.get("agents", [])}
            agent_list = [a.get("id") for a in agents if a.get("id")]
            result_agents = []
            for a in agent_list:
                ac_a = ac_agents.get(a, {})
                alive = True
                # 判断状态：优先用 ac 里的状态，否则默认 idle
                status = ac_a.get("status", "idle") if ac_a else "idle"
                label = ac_a.get("label", a.replace("_", " ").title()) if ac_a else a.replace("_", " ").title()
                role = ac_a.get("role", label) if ac_a else label
                emoji = ac_a.get("emoji", "🏛️") if ac_a else "🏛️"
                result_agents.append({
                    "id": a,
                    "alive": alive,
                    "status": status,
                    "label": label,
                    "role": role,
                    "emoji": emoji,
                    "statusLabel": status.capitalize(),
                    "lastActive": None,
                    "checkedAt": datetime.datetime.now().isoformat()
                })
            self.send_json({
                "ok": True,
                "gateway": {"alive": True, "probe": True, "status": "在线"},
                "agents": result_agents,
                "checkedAt": datetime.datetime.now().isoformat()
            })

        elif path.startswith("/api/scheduler-state/"):
            task_id = path.split("/")[-1]
            tasks = self.load_live_status().get("tasks", [])
            task = next((t for t in tasks if t.get("id") == task_id), None)
            self.send_json(task or {"id": task_id, "state": "Unknown"})

        elif path.startswith("/api/skill-content/"):
            self.send_json({"content": "技能内容待定", "error": None})

        else:
            self.send_response(404)

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length > 0 else b""
        data = json.loads(body.decode("utf-8")) if body else {}

        if path == "/api/set-model":
            log_path = TAIZI_DATA / "model_change_log.json"
            log = self.taizi("model_change_log.json") or []
            log.append({
                "agentId": data.get("agentId", ""),
                "model": data.get("model", ""),
                "applied": False,
                "timestamp": datetime.datetime.now().isoformat()
            })
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(log, f, ensure_ascii=False, indent=2)
            result = {"success": True, "agentId": data.get("agentId")}
            with open(TAIZI_DATA / "last_model_change_result.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False)
            self.send_json(result)

        elif path == "/api/create-task":
            task_id = "ED-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            self.send_json({"ok": True, "taskId": task_id, "title": data.get("title", "")})

        else:
            self.send_json({"error": "not found"}, 404)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=7891, type=int)
    args = parser.parse_args()
    server = HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"军机处看板已启动 http://127.0.0.1:{args.port}")
    server.serve_forever()

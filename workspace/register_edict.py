import json

cfg_path = 'C:/Users/Administrator/.openclaw/openclaw.json'
cfg = json.loads(open(cfg_path, encoding='utf-8').read())

agents_cfg = cfg.setdefault('agents', {})
agents_list = agents_cfg.get('list', [])
existing_ids = {a['id'] for a in agents_list}

AGENTS = [
    {'id': 'taizi',    'workspace': 'C:/Users/Administrator/.openclaw/workspace-taizi'},
    {'id': 'zhongshu', 'workspace': 'C:/Users/Administrator/.openclaw/workspace-zhongshu'},
    {'id': 'menxia',   'workspace': 'C:/Users/Administrator/.openclaw/workspace-menxia'},
    {'id': 'shangshu', 'workspace': 'C:/Users/Administrator/.openclaw/workspace-shangshu'},
    {'id': 'hubu',     'workspace': 'C:/Users/Administrator/.openclaw/workspace-hubu'},
    {'id': 'libu',     'workspace': 'C:/Users/Administrator/.openclaw/workspace-libu'},
    {'id': 'bingbu',   'workspace': 'C:/Users/Administrator/.openclaw/workspace-bingbu'},
    {'id': 'xingbu',   'workspace': 'C:/Users/Administrator/.openclaw/workspace-xingbu'},
    {'id': 'gongbu',   'workspace': 'C:/Users/Administrator/.openclaw/workspace-gongbu'},
    {'id': 'libu_hr',  'workspace': 'C:/Users/Administrator/.openclaw/workspace-libu_hr'},
    {'id': 'zaochao',  'workspace': 'C:/Users/Administrator/.openclaw/workspace-zaochao'},
]

added = 0
for ag in AGENTS:
    if ag['id'] not in existing_ids:
        agents_list.append(ag)
        added += 1
        print('  + added:', ag['id'])
    else:
        print('  ~ exists:', ag['id'], '(skipped)')

agents_cfg['list'] = agents_list
open(cfg_path, 'w', encoding='utf-8').write(json.dumps(cfg, ensure_ascii=False, indent=2))
print('Done:', added, 'agents added')

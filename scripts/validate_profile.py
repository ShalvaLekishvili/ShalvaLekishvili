#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys, xml.etree.ElementTree as ET
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
errors=[]
readme=(ROOT/'README.md').read_text(encoding='utf-8')
config=json.loads((ROOT/'config/portfolio.json').read_text(encoding='utf-8'))
for ref in re.findall(r'src="\./([^"]+)"', readme):
    if not (ROOT/ref).exists(): errors.append(f'missing README asset: {ref}')
for svg in ROOT.rglob('*.svg'):
    try: ET.parse(svg)
    except Exception as exc: errors.append(f'invalid SVG {svg.relative_to(ROOT)}: {exc}')
ids=[c['id'] for c in config['credentials'] if c.get('id')]
if len(ids)!=10: errors.append(f'expected 10 TryHackMe credential IDs, found {len(ids)}')
if len(set(ids))!=len(ids): errors.append('duplicate credential ID')
if len(config['credentials'])!=14: errors.append(f'expected 14 credentials, found {len(config["credentials"])}')
for required in ['SentinelForge','PacketScope','Live Portfolio Intelligence','Credentials']:
    if required.lower() not in readme.lower(): errors.append(f'README missing required concept: {required}')
if errors:
    print('\n'.join(f'ERROR: {e}' for e in errors), file=sys.stderr); raise SystemExit(1)
print('profile validation passed')

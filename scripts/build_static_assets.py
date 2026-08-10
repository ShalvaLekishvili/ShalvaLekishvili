#!/usr/bin/env python3
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
PALETTES={
'dark':{'bg':'#050b14','panel':'#0b1220','panel2':'#0f172a','border':'#26364e','text':'#f8fafc','soft':'#cbd5e1','muted':'#94a3b8','blue':'#60a5fa','teal':'#2dd4bf','violet':'#a78bfa','green':'#22c55e'},
'light':{'bg':'#f8fafc','panel':'#ffffff','panel2':'#eff6ff','border':'#cbd5e1','text':'#0f172a','soft':'#334155','muted':'#64748b','blue':'#2563eb','teal':'#0f766e','violet':'#7c3aed','green':'#15803d'}}

def svg(w,h,body,label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">{body}</svg>'

def hero(p):
    return svg(1200,430,f'''<defs><linearGradient id="a" x1="0" x2="1"><stop stop-color="{p['blue']}"/><stop offset=".55" stop-color="#38bdf8"/><stop offset="1" stop-color="{p['teal']}"/></linearGradient><pattern id="g" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M44 0H0V44" fill="none" stroke="{p['border']}" opacity=".38"/></pattern></defs>
<rect width="1200" height="430" rx="30" fill="{p['bg']}"/><rect width="1200" height="430" rx="30" fill="url(#g)"/>
<rect x="58" y="58" width="6" height="111" rx="3" fill="url(#a)"/>
<text x="88" y="92" fill="{p['blue']}" font-family="Arial" font-size="14" font-weight="700" letter-spacing="3">SECURITY OPERATIONS · DETECTION ENGINEERING · DFIR</text>
<text x="88" y="151" fill="{p['text']}" font-family="Arial" font-size="49" font-weight="800">SHALVA LEKISHVILI</text>
<text x="88" y="190" fill="{p['soft']}" font-family="Arial" font-size="21">SOC Analyst (L2) · Security Engineering Portfolio</text>
<text x="88" y="247" fill="{p['muted']}" font-family="Arial" font-size="17">Evidence-first defensive security. Engineering depth. Operational clarity.</text>
<rect x="88" y="300" width="540" height="52" rx="13" fill="{p['panel']}" stroke="{p['border']}"/><circle cx="118" cy="326" r="7" fill="{p['green']}"/><text x="139" y="332" fill="{p['soft']}" font-family="Consolas" font-size="14">OBSERVE → CONTEXT → INVESTIGATE → DECIDE → IMPROVE</text>
<text x="88" y="388" fill="{p['muted']}" font-family="Arial" font-size="12">Portfolio v5 · machine-readable evidence · self-updating public intelligence</text>
<rect x="748" y="58" width="394" height="294" rx="24" fill="{p['panel']}" stroke="{p['border']}"/>
<text x="780" y="97" fill="{p['muted']}" font-family="Arial" font-size="12" font-weight="700" letter-spacing="2">PROOF STACK</text>
<g font-family="Arial"><text x="780" y="151" fill="{p['text']}" font-size="34" font-weight="800">12</text><text x="844" y="151" fill="{p['soft']}" font-size="14">curated detections</text><text x="780" y="199" fill="{p['text']}" font-size="34" font-weight="800">48</text><text x="844" y="199" fill="{p['soft']}" font-size="14">automated tests</text><text x="780" y="247" fill="{p['text']}" font-size="34" font-weight="800">14</text><text x="844" y="247" fill="{p['soft']}" font-size="14">documented credentials</text><text x="780" y="295" fill="{p['text']}" font-size="34" font-weight="800">2</text><text x="844" y="295" fill="{p['soft']}" font-size="14">flagship security platforms</text></g>
<line x1="780" y1="320" x2="1110" y2="320" stroke="url(#a)" stroke-width="2"/>
''','God mode security portfolio hero')

def operating(p):
    items=[('TELEMETRY','Windows · Sysmon · PCAP'),('NORMALIZE','events · flows · IOCs'),('DETECT','rules · heuristics · ATT&amp;CK'),('INVESTIGATE','timeline · scope · evidence'),('DECIDE','escalate · contain · close'),('IMPROVE','tune · harden · retest')]
    body=f'<rect width="1200" height="275" rx="26" fill="{p["bg"]}"/><text x="42" y="43" fill="{p["muted"]}" font-family="Arial" font-size="13" font-weight="700" letter-spacing="2">SECURITY OPERATING SYSTEM</text>'
    x=42
    for i,(title,sub) in enumerate(items):
        w=170 if i<5 else 180
        body+=f'<rect x="{x}" y="91" width="{w}" height="118" rx="18" fill="{p["panel"]}" stroke="{p["border"]}"/><text x="{x+w/2}" y="130" text-anchor="middle" fill="{p["text"]}" font-family="Arial" font-size="14" font-weight="800">{title}</text><text x="{x+w/2}" y="160" text-anchor="middle" fill="{p["muted"]}" font-family="Arial" font-size="10">{sub}</text><text x="{x+w/2}" y="188" text-anchor="middle" fill="{p["blue"] if i<3 else p["teal"]}" font-family="Consolas" font-size="10">0{i+1}</text>'
        if i<5:
            body+=f'<path d="M{x+w+5} 150H{x+w+22}" stroke="{p["blue"] if i<2 else p["teal"]}" stroke-width="3"/><path d="M{x+w+16} 144L{x+w+23} 150L{x+w+16} 156" fill="none" stroke="{p["blue"] if i<2 else p["teal"]}" stroke-width="2"/>'
        x+=192
    body+=f'<text x="600" y="244" text-anchor="middle" fill="{p["muted"]}" font-family="Arial" font-size="11">The goal is not more alerts. The goal is better decisions and stronger controls.</text>'
    return svg(1200,275,body,'Security operating system')

def reviewer(p):
    cards=[
        ('HIRING MANAGER','60-second route','Role → proof stack → credentials','→ business impact'),
        ('SOC / BLUE TEAM LEAD','3-minute route','Detections → investigations','→ operating model → deliverables'),
        ('TECHNICAL REVIEWER','5-minute route','Repositories → architecture → tests','→ security model → manifest')
    ]
    body=f'<rect width="1200" height="285" rx="26" fill="{p["bg"]}"/><text x="42" y="43" fill="{p["muted"]}" font-family="Arial" font-size="13" font-weight="700" letter-spacing="2">REVIEWER ROUTES</text>'
    for i,(a,b,c,d) in enumerate(cards):
        x=42+i*386
        accent=[p['blue'],'#38bdf8',p['teal']][i]
        body+=f'<rect x="{x}" y="82" width="350" height="157" rx="20" fill="{p["panel"]}" stroke="{p["border"]}"/><rect x="{x}" y="82" width="6" height="157" rx="3" fill="{accent}"/><text x="{x+28}" y="117" fill="{accent}" font-family="Arial" font-size="11" font-weight="700">{a}</text><text x="{x+28}" y="153" fill="{p["text"]}" font-family="Arial" font-size="20" font-weight="800">{b}</text><text x="{x+28}" y="190" fill="{p["soft"]}" font-family="Arial" font-size="11">{c}</text><text x="{x+28}" y="211" fill="{p["soft"]}" font-family="Arial" font-size="11">{d}</text>'
    return svg(1200,285,body,'Reviewer routes')

def footer(p):
    return svg(1200,190,f'''<defs><linearGradient id="f" x1="0" x2="1"><stop stop-color="{p['blue']}"/><stop offset=".5" stop-color="#38bdf8"/><stop offset="1" stop-color="{p['teal']}"/></linearGradient></defs><rect width="1200" height="190" rx="26" fill="{p['bg']}"/><rect x="55" y="36" width="1090" height="2" fill="url(#f)"/><text x="600" y="87" fill="{p['text']}" text-anchor="middle" font-family="Arial" font-size="23" font-weight="800">SECURITY SHOULD PRODUCE A DECISION — NOT JUST AN ALERT.</text><text x="600" y="125" fill="{p['muted']}" text-anchor="middle" font-family="Arial" font-size="14">SOC Operations · Detection Engineering · Threat Hunting · DFIR · Network Forensics</text><text x="600" y="158" fill="{p['muted']}" text-anchor="middle" font-family="Consolas" font-size="11">EVIDENCE FIRST · DEFENSIVE BY DESIGN · AUTHORIZED SECURITY RESEARCH ONLY</text>''','Security portfolio footer')

for theme,p in PALETTES.items():
    (OUT/f'hero-{theme}.svg').write_text(hero(p))
    (OUT/f'operating-system-{theme}.svg').write_text(operating(p))
    (OUT/f'reviewer-routes-{theme}.svg').write_text(reviewer(p))
    (OUT/f'footer-{theme}.svg').write_text(footer(p))
print('static assets generated')

#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_SKELETON = '''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><title>{title}</title>
<style>
body{{font-family:Arial,sans-serif;background:#020617;color:#fff;padding:24px}}
.wrap{{max-width:1200px;margin:0 auto;background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:24px}}
svg{{width:100%;height:auto;display:block}}
</style></head><body><div class="wrap"><h1>{title}</h1><p>{subtitle}</p>{svg}</div></body></html>'''


def build_svg(meta):
    comps = meta.get('architecture_components') or []
    edges = meta.get('architecture_edges') or []
    width = 1400
    height = max(900, 180 + len(comps) * 110)
    rects = []
    texts = []
    lines = []
    x = 120
    y = 120
    for i, c in enumerate(comps):
        label = str(c.get('name') if isinstance(c, dict) else c)
        rects.append(f'<rect x="{x}" y="{y+i*110}" width="360" height="72" rx="10" fill="rgba(8,51,68,0.45)" stroke="#22d3ee" stroke-width="2"/>')
        texts.append(f'<text x="{x+180}" y="{y+30+i*110}" fill="white" font-size="24" text-anchor="middle">{label}</text>')
    idx = {str(c.get('name') if isinstance(c, dict) else c): n for n, c in enumerate(comps)}
    for e in edges:
        if isinstance(e, dict):
            a = str(e.get('from','')); b = str(e.get('to',''))
        else:
            continue
        if a in idx and b in idx:
            y1 = y + idx[a]*110 + 72
            y2 = y + idx[b]*110
            lines.append(f'<line x1="300" y1="{y1}" x2="300" y2="{y2}" stroke="#94a3b8" stroke-width="3" marker-end="url(#arrow)"/>')
    return f'''<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
    <defs><marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8"/></marker></defs>
    <rect width="100%" height="100%" fill="#020617"/>
    {''.join(lines)}
    {''.join(rects)}
    {''.join(texts)}
    </svg>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--meta', required=True)
    ap.add_argument('--notes', required=True)
    ap.add_argument('--html', required=True)
    ap.add_argument('--png', required=True)
    args = ap.parse_args()
    meta = json.load(open(args.meta, 'r', encoding='utf-8'))
    notes = Path(args.notes).read_text(encoding='utf-8')[:200]
    title = f"{meta.get('project_name','Project')} 架构图"
    html = HTML_SKELETON.format(title=title, subtitle=notes, svg=build_svg(meta))
    Path(args.html).write_text(html, encoding='utf-8')
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/snap/bin/chromium', headless=True)
        page = browser.new_page(viewport={'width': 1500, 'height': 1800}, device_scale_factor=1)
        page.set_content(html, wait_until='load')
        Path(args.png).parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=args.png, full_page=True)
        browser.close()
    if not Path(args.png).exists() or Path(args.png).stat().st_size == 0:
        raise SystemExit('PNG render failed')
    print(args.png)

if __name__ == '__main__':
    main()

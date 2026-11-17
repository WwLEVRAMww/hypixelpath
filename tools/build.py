#!/usr/bin/env python3
"""Builds app.html, the Mini App page that GitHub Pages serves, from src/app.html and src/guide-data.json.

Run from anywhere: python3 tools/build.py
The built page keeps two placeholders that are filled when it is opened: __LIVE__ (co-op data from the
sheet's Apps Script) and __ROAD__ (roadmap.json). index.html fills them on GitHub Pages; the Apps Script
fills them on its own fallback page.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    tpl = (ROOT / 'src' / 'app.html').read_text(encoding='utf-8')
    data = json.loads((ROOT / 'src' / 'guide-data.json').read_text(encoding='utf-8'))
    json.loads((ROOT / 'roadmap.json').read_text(encoding='utf-8'))  # the page parses it; fail early if broken
    for mark in ('__DATA__', '__LIVE__', '__ROAD__'):
        if tpl.count(mark) != 1:
            raise SystemExit(f'src/app.html must contain {mark} exactly once')
    # '<' is escaped so the JSON can never close or confuse the <script> element it sits in.
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    if '__LIVE__' in blob or '__ROAD__' in blob:
        raise SystemExit('guide data must not contain the page placeholders')
    out = tpl.replace('__DATA__', blob)
    (ROOT / 'app.html').write_text(out, encoding='utf-8')
    print(f'app.html: {len(out.encode()):,} bytes')


if __name__ == '__main__':
    main()

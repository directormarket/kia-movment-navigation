#!/usr/bin/env python3
"""assets/ 안의 모든 파일을 base64 로 심어 한 파일로 만든다."""
import base64, json, mimetypes, os, glob

SRC = 'kia_patched/index.html'
OUT = 'kia_patched/index-standalone.html'
s = open(SRC, encoding='utf-8').read()

table = {}
for f in sorted(glob.glob('kia_patched/assets/**/*', recursive=True)):
    if not os.path.isfile(f) or f.endswith('.txt'):
        continue
    rel = os.path.relpath(f, 'kia_patched')
    mime = mimetypes.guess_type(f)[0] or 'application/octet-stream'
    table[rel] = 'data:%s;base64,%s' % (
        mime, base64.b64encode(open(f, 'rb').read()).decode())

assert 'const ASSET = {};' in s, 'ASSET 자리를 찾지 못했습니다'
s = s.replace('const ASSET = {};', 'const ASSET = ' + json.dumps(table) + ';', 1)
open(OUT, 'w', encoding='utf-8').write(s)
print('%s  %d개 자산 내장  %.1f MB' % (OUT, len(table), len(s)/1048576))

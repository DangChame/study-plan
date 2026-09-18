#!/usr/bin/env python3
"""plan.tpl.html + 강의목차 + 진도 + 필사장 + 암기시트 -> plan.html(Artifact) / index.html(Pages)"""
import io,json,os,sys,datetime
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from mdparse import trace_rounds, chem_chapters
SP=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(SP,'site')
J=lambda o: json.dumps(o,ensure_ascii=False,separators=(',',':'))

PROGRESS=json.load(open(os.path.join(SP,'progress.json'),encoding='utf-8'))
TRACE=trace_rounds(io.open(os.path.join(SP,'민소_판례_필사장.md'),encoding='utf-8').read())
CHEM=chem_chapters(io.open(os.path.join(SP,'화학_암기시트.md'),encoding='utf-8').read())
# 화학 기출풀이 강 → 단원(장) 매핑
CHEM_MAP={1:1,2:2,3:2,4:3,5:3,6:3,7:4,8:5,9:6,10:6,11:7,12:7,13:7,14:8,15:8,16:8,
          17:8,18:9,19:9,20:10,21:10,22:11,23:11,24:12,25:12}
at=datetime.datetime.now().astimezone().isoformat(timespec='seconds')

s=io.open(os.path.join(D,'plan.tpl.html'),encoding='utf-8').read()
s=s.replace('/*PUBLISHED_AT*/',at)
s=s.replace('/*PUBLISHED_PROGRESS*/',J(PROGRESS))
s=s.replace('/*INVENTORY*/',io.open(os.path.join(SP,'inv.json'),encoding='utf-8').read().strip())
s=s.replace('/*TRACE_BODY*/',J(TRACE))
s=s.replace('/*CHEM_SHEET*/',J({str(k):v for k,v in CHEM.items()}))
s=s.replace('/*CHEM_MAP*/',J({str(k):str(v) for k,v in CHEM_MAP.items()}))

io.open(os.path.join(D,'plan.html'),'w',encoding='utf-8').write(s)
head,rest=s.split('<header>',1)
io.open(os.path.join(D,'index.html'),'w',encoding='utf-8').write(
 '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
 '<meta name="robots" content="noindex,nofollow">\n'
 '<meta name="color-scheme" content="light dark">\n'
 '<meta name="description" content="2027년 변리사 1차 학습 진도판">\n'
 '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
 + head + '</head>\n<body>\n<header>' + rest + '\n</body>\n</html>\n')
print(f"배포 {at}\n필사 {len(TRACE)}회차 · 화학 {len(CHEM)}장 · index.html {os.path.getsize(os.path.join(D,'index.html'))//1024}KB")
print("진도:",{k:PROGRESS[k] for k in ('chemPast','mgPage','ptPage','traceDone')})

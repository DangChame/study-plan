#!/usr/bin/env python3
"""plan.tpl.html + inv.json + 진도 -> plan.html(Artifact) / index.html(Pages)"""
import io,json,os,sys,datetime
SP=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(SP,'site')
PROGRESS = json.load(open(os.path.join(SP,'progress.json'),encoding='utf-8'))
at = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
s = io.open(os.path.join(D,'plan.tpl.html'),encoding='utf-8').read()
s = s.replace('/*PUBLISHED_AT*/', at)
s = s.replace('/*PUBLISHED_PROGRESS*/', json.dumps(PROGRESS,ensure_ascii=False,separators=(',',':')))
inv = io.open(os.path.join(SP,'inv.json'),encoding='utf-8').read().strip()
body = s.replace('/*INVENTORY*/', inv)
io.open(os.path.join(D,'plan.html'),'w',encoding='utf-8').write(body)
head,rest = body.split('<header>',1)
io.open(os.path.join(D,'index.html'),'w',encoding='utf-8').write(
 '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
 '<meta name="robots" content="noindex,nofollow">\n'
 '<meta name="color-scheme" content="light dark">\n'
 '<meta name="description" content="2027년 변리사 1차 학습 진도판">\n'
 '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
 + head + '</head>\n<body>\n<header>' + rest + '\n</body>\n</html>\n')
print("배포 시각:", at)
print("진도:", PROGRESS)

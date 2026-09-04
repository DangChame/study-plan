#!/usr/bin/env python3
"""plan.tpl.html + lectures.json -> index.html"""
import io, pathlib
d = pathlib.Path(__file__).parent
tpl = io.open(d/"plan.tpl.html", encoding="utf-8").read()
inv = io.open(d/"lectures.json", encoding="utf-8").read().strip()
body = tpl.replace("/*INVENTORY*/", inv)
head, rest = body.split("<header>", 1)
doc = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
       '<meta name="robots" content="noindex,nofollow">\n'
       '<meta name="color-scheme" content="light dark">\n'
       '<meta name="description" content="2027년 변리사 1차 학습 진도판">\n'
       '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
       + head + '</head>\n<body>\n<header>' + rest + '\n</body>\n</html>\n')
io.open(d/"index.html", "w", encoding="utf-8").write(doc)
print("index.html", len(doc.encode()), "bytes")

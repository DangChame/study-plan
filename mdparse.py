"""md → 간단 HTML (볼드·표·번호목록·소제목만)"""
import re,html
def md2html(src):
    out=[]; rows=None
    def flush():
        nonlocal rows
        if rows:
            head=rows[0]
            sep = len(rows)>1 and all(set(c.strip())<=set(':-') and c.strip() for c in rows[1])
            body = rows[2:] if sep else rows[1:]
            out.append('<div class="tw"><table><thead><tr>'+''.join(f'<th>{inline(c)}</th>' for c in head)+'</tr></thead><tbody>')
            for r in body:
                out.append('<tr>'+''.join(f'<td>{inline(c)}</td>' for c in r)+'</tr>')
            out.append('</tbody></table></div>')
            rows=None
    def inline(t):
        t=html.escape(t.strip())
        t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
        t=t.replace('&quot;','"')
        return t
    for line in src.split('\n'):
        ls=line.strip()
        if ls.startswith('|') and ls.endswith('|'):
            cells=[c for c in ls.strip('|').split('|')]
            if rows is None: rows=[]
            rows.append(cells); continue
        flush()
        if not ls or ls.startswith('---'): continue
        if ls.startswith('> '): out.append(f'<p class="note">{inline(ls[2:])}</p>'); continue
        m=re.match(r'^\*\*(\d+\.\s*[^*]+)\*\*$',ls)
        if m: out.append(f'<h4>{inline(m.group(1))}</h4>'); continue
        m=re.match(r'^##+\s+(.*)$',ls)
        if m: out.append(f'<h4>{inline(m.group(1))}</h4>'); continue
        m=re.match(r'^(\d+)\.\s+(.*)$',ls)
        if m: out.append(f'<p class="it"><i>{m.group(1)}</i><span>{inline(m.group(2))}</span></p>'); continue
        out.append(f'<p>{inline(ls)}</p>')
    flush()
    return ''.join(out)

def trace_rounds(src):
    """[{n, title, html}]"""
    parts=re.split(r'\n## (\d+)회차\s*(?:\([^)]*\))?\s*—\s*([^\n]+)\n', '\n'+src)
    out=[]
    for i in range(1,len(parts),3):
        n=int(parts[i]); title=parts[i+1].strip(); body=parts[i+2]
        body=body.split('\n## ')[0]
        body=re.split(r'\n## ⚠️|\n## 🔄|\n## 📊',body)[0]
        out.append({"n":n,"title":title,"html":md2html(body)})
    return out

def chem_chapters(src):
    """{장번호: {title, html}}"""
    parts=re.split(r'\n# (\d+)장 · ([^\n]+)\n', '\n'+src)
    out={}
    for i in range(1,len(parts),3):
        ch=int(parts[i]); title=parts[i+1].strip(); body=parts[i+2].split('\n# ')[0]
        body=re.split(r'\n## 🔄',body)[0]
        out[ch]={"title":f"{ch}장 · {title}","html":md2html(body)}
    return out


def chem_quiz(src):
    """화학 암기시트 → 퀴즈 문항 [{q, a, sec, page}]"""
    import re, html as H
    def inline(t):
        t=H.escape(t.strip())
        t=re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
        return t.replace('&quot;','"')
    out=[]; sec=""; page=""; chap=""
    for line in src.split('\n'):
        ls=line.strip()
        m=re.match(r'^# (\d+장 · .+)$', ls)
        if m: chap=m.group(1); continue
        m=re.match(r'^## (.+)$', ls)
        if m: sec=m.group(1); page=""; continue
        m=re.match(r'^> 📖 (.+)$', ls)
        if m: page=re.sub(r'\*\*','',m.group(1)); continue
        if ls.startswith('|') and ls.endswith('|'):
            cells=[c.strip() for c in ls.strip('|').split('|')]
            if len(cells)!=2: continue
            if cells[0] in ('물음','구분','암기시트 단원','전자쌍(EP)') or set(cells[0])<=set(':- '): continue
            if sec.startswith('📖'): continue          # 기본서 매핑표는 문항이 아니다
            if not cells[0] or not cells[1]: continue
            out.append({"q":inline(cells[0]), "a":inline(cells[1]),
                        "sec":(chap+" · " if chap else "")+sec, "page":page})
    return out

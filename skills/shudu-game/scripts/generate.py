#!/usr/bin/env python3
"""数独游戏 HTML 生成器 - 生成独立可交互的数独游戏 HTML 文件"""

import argparse
import json
import os
from datetime import datetime

THEMES = {
    "dark": {
        "name": "暗黑",
        "body": "background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:#fff",
        "board": "#1a1a2e",
        "wrap": "background:linear-gradient(135deg,#667eea,#764ba2);box-shadow:0 8px 32px rgba(102,126,234,.35);border-radius:14px;padding:4px",
        "cell": "border-color:rgba(255,255,255,.06)",
        "box": "rgba(102,126,234,.6)",
        "given": "#c4b5fd", "edit": "#67e8f9", "err": "#f87171",
        "sel": "rgba(102,126,234,.35)", "hi": "rgba(102,126,234,.12)", "same": "rgba(102,126,234,.22)",
        "btn": "rgba(255,255,255,.08)", "btnB": "rgba(255,255,255,.15)", "btnT": "#fff",
        "pri": "linear-gradient(135deg,#667eea,#764ba2)",
        "note": "#8e8ea0", "timer": "#a5b4fc",
        "modal": "linear-gradient(135deg,#1e1b4b,#312e81)",
        "act": "rgba(234,179,8,.25)", "actB": "rgba(234,179,8,.4)", "actT": "#fde68a",
    },
    "light": {
        "name": "明亮",
        "body": "background:linear-gradient(135deg,#f5f7fa,#c3cfe2);color:#1a1a2e",
        "board": "#fff",
        "wrap": "background:linear-gradient(135deg,#4f46e5,#7c3aed);box-shadow:0 8px 32px rgba(79,70,229,.2);border-radius:14px;padding:4px",
        "cell": "border-color:rgba(0,0,0,.08)",
        "box": "rgba(79,70,229,.5)",
        "given": "#312e81", "edit": "#4f46e5", "err": "#dc2626",
        "sel": "rgba(79,70,229,.2)", "hi": "rgba(79,70,229,.06)", "same": "rgba(79,70,229,.12)",
        "btn": "rgba(0,0,0,.04)", "btnB": "rgba(0,0,0,.12)", "btnT": "#1a1a2e",
        "pri": "linear-gradient(135deg,#4f46e5,#7c3aed)",
        "note": "#9ca3af", "timer": "#4f46e5",
        "modal": "linear-gradient(135deg,#eef2ff,#e0e7ff)",
        "act": "rgba(234,179,8,.15)", "actB": "rgba(234,179,8,.5)", "actT": "#92400e",
    },
    "cyberpunk": {
        "name": "赛博朋克",
        "body": "background:linear-gradient(135deg,#0a0a0a,#1a0a2e,#0a1628);color:#0ff",
        "board": "#0a0a0a",
        "wrap": "background:linear-gradient(135deg,#0ff,#f0f);box-shadow:0 8px 32px rgba(0,255,255,.3);border-radius:14px;padding:4px",
        "cell": "border-color:rgba(0,255,255,.08)",
        "box": "rgba(255,0,255,.5)",
        "given": "#0ff", "edit": "#f0f", "err": "#f33",
        "sel": "rgba(0,255,255,.25)", "hi": "rgba(0,255,255,.06)", "same": "rgba(255,0,255,.15)",
        "btn": "rgba(0,255,255,.06)", "btnB": "rgba(0,255,255,.2)", "btnT": "#0ff",
        "pri": "linear-gradient(135deg,#0ff,#f0f)",
        "note": "rgba(0,255,255,.4)", "timer": "#f0f",
        "modal": "linear-gradient(135deg,#0a0a2e,#1a0a3e)",
        "act": "rgba(255,255,0,.2)", "actB": "rgba(255,255,0,.5)", "actT": "#ff0",
    },
    "minimal": {
        "name": "极简",
        "body": "background:#fafafa;color:#111",
        "board": "#fff",
        "wrap": "background:#333;box-shadow:0 2px 12px rgba(0,0,0,.1);border-radius:2px;padding:2px",
        "cell": "border-color:#e5e5e5",
        "box": "#333",
        "given": "#111", "edit": "#2563eb", "err": "#dc2626",
        "sel": "#dbeafe", "hi": "#f3f4f6", "same": "#e0e7ff",
        "btn": "#f3f4f6", "btnB": "#d1d5db", "btnT": "#111",
        "pri": "#111",
        "note": "#9ca3af", "timer": "#2563eb",
        "modal": "#fff",
        "act": "#fef3c7", "actB": "#f59e0b", "actT": "#92400e",
    },
}

DIFF_REMOVE = {"easy": 36, "medium": 46, "hard": 54, "expert": 60}
DIFF_NAMES = {"easy": "简单", "medium": "中等", "hard": "困难", "expert": "地狱"}


def generate_html(difficulty="medium", theme="dark", title="九宫格数独"):
    t = THEMES.get(theme, THEMES["dark"])
    diff_opts = "".join(
        f'<option value="{k}"{" selected" if k == difficulty else ""}>{v}</option>'
        for k, v in DIFF_NAMES.items()
    )
    diff_json = json.dumps(DIFF_REMOVE)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;{t["body"]};min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px}}
h1{{font-size:2rem;margin-bottom:6px;letter-spacing:4px}}
.sub{{font-size:.85rem;opacity:.5;margin-bottom:18px}}
.bar{{display:flex;align-items:center;gap:14px;margin-bottom:14px;flex-wrap:wrap;justify-content:center}}
.bar select,.bar button{{padding:8px 18px;border-radius:8px;border:1px solid {t["btnB"]};background:{t["btn"]};color:{t["btnT"]};font-size:.9rem;cursor:pointer}}
.bar .pri{{background:{t["pri"]};border:none;font-weight:600;color:#fff}}
.timer{{font-size:1.1rem;font-variant-numeric:tabular-nums;color:{t["timer"]};min-width:70px;text-align:center}}
.mis{{font-size:.9rem;color:{t["err"]}}}
.bw{{{t["wrap"]}}}
.bd{{display:grid;grid-template-columns:repeat(9,1fr);background:{t["board"]};border-radius:12px;overflow:hidden}}
.c{{width:52px;height:52px;display:flex;align-items:center;justify-content:center;font-size:1.35rem;font-weight:600;cursor:pointer;transition:all .15s;{t["cell"]};border-style:solid;border-width:1px;user-select:none;position:relative}}
.c:nth-child(9n+4),.c:nth-child(9n+7){{border-left:2px solid {t["box"]}}}
.c:nth-child(n+19):nth-child(-n+27),.c:nth-child(n+46):nth-child(-n+54){{border-top:2px solid {t["box"]}}}
.gv{{color:{t["given"]}}} .ed{{color:{t["edit"]}}}
.sl{{background:{t["sel"]}!important}} .hl{{background:{t["hi"]}!important}} .sm{{background:{t["same"]}!important}}
.er{{color:{t["err"]}!important;animation:shake .3s}}
.fl{{animation:flash .6s}}
.nt{{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);width:100%;height:100%;font-size:.55rem;font-weight:400;color:{t["note"]}}}
.nt span{{display:flex;align-items:center;justify-content:center}}
@keyframes shake{{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-4px)}}75%{{transform:translateX(4px)}}}}
@keyframes flash{{0%,100%{{background:{t["sel"]}}}50%{{background:rgba(52,211,153,.4)}}}}
.np{{display:flex;gap:8px;margin-top:16px;flex-wrap:wrap;justify-content:center}}
.np button{{width:48px;height:48px;border-radius:10px;border:1px solid {t["btnB"]};background:{t["btn"]};color:{t["btnT"]};font-size:1.2rem;font-weight:600;cursor:pointer;position:relative}}
.np button:hover{{transform:translateY(-2px)}} .np button:active{{transform:translateY(0)}}
.np button.uu{{opacity:.25;pointer-events:none}}
.np button .ct{{position:absolute;top:2px;right:4px;font-size:.5rem;color:{t["note"]}}}
.act{{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap;justify-content:center}}
.act button{{padding:8px 16px;border-radius:8px;border:1px solid {t["btnB"]};background:{t["btn"]};color:{t["btnT"]};font-size:.85rem;cursor:pointer}}
.act button.on{{background:{t["act"]};border-color:{t["actB"]};color:{t["actT"]}}}
.mo{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:100;align-items:center;justify-content:center}}
.mo.show{{display:flex}}
.md{{background:{t["modal"]};border-radius:16px;padding:32px;text-align:center;box-shadow:0 16px 48px rgba(0,0,0,.5);max-width:340px}}
.md h2{{font-size:1.6rem;margin-bottom:12px}} .md p{{color:{t["timer"]};margin-bottom:8px;font-size:.95rem}}
.md button{{margin-top:16px;padding:10px 32px;border-radius:10px;border:none;background:{t["pri"]};color:#fff;font-size:1rem;font-weight:600;cursor:pointer}}
@media(max-width:520px){{.c{{width:38px;height:38px;font-size:1.05rem}}.np button{{width:40px;height:40px;font-size:1rem}}h1{{font-size:1.4rem}}}}
</style>
</head>
<body>
<h1>{title}</h1>
<p class="sub">填入1-9使每行、每列、每个3x3宫格内数字不重复</p>
<div class="bar">
<select id="df">{diff_opts}</select>
<button class="pri" onclick="newGame()">新游戏</button>
<span class="timer" id="tm">00:00</span>
<span class="mis" id="ms"></span>
</div>
<div class="bw"><div class="bd" id="bd"></div></div>
<div class="np" id="np"></div>
<div class="act">
<button onclick="undo()">&#8617; 撤销</button>
<button onclick="erase()">&#9003; 擦除</button>
<button id="nb" onclick="toggleNote()">&#9998; 笔记</button>
<button onclick="hint()">&#128161; 提示</button>
</div>
<div class="mo" id="wm">
<div class="md">
<h2>&#127881; 恭喜通关！</h2>
<p id="wt"></p><p id="wk"></p><p id="wd"></p>
<button onclick="closeWin();newGame()">再来一局</button>
</div>
</div>
<script>
const E=0,DR={diff_json};
function shuf(a){{for(let i=a.length-1;i>0;i--){{const j=0|Math.random()*(i+1);[a[i],a[j]]=[a[j],a[i]]}}return a}}
function ok(b,r,c,n){{for(let i=0;i<9;i++)if(b[r][i]===n||b[i][c]===n)return!1;const br=3*(r/3|0),bc=3*(c/3|0);for(let i=br;i<br+3;i++)for(let j=bc;j<bc+3;j++)if(b[i][j]===n)return!1;return!0}}
function slv(b){{for(let r=0;r<9;r++)for(let c=0;c<9;c++)if(!b[r][c]){{for(const n of shuf([1,2,3,4,5,6,7,8,9]))if(ok(b,r,c,n)){{b[r][c]=n;if(slv(b))return!0;b[r][c]=E}}return!1}}return!0}}
function gen(d){{const b=Array.from({{length:9}},()=>Array(9).fill(E));slv(b);const s=b.map(r=>[...r]),rm=DR[d]||46,cs=shuf([...Array(81).keys()]);let x=0;for(const i of cs){{if(x>=rm)break;b[i/9|0][i%9]=E;x++}}return{{p:b,s}}}}
let pz,sol,pb,nt,gv,sel=null,nm=!1,mk=0,mx=5,hs=[],ti,sec=0,ov=!1;
const BD=document.getElementById('bd'),NP=document.getElementById('np');
function mkB(){{BD.innerHTML='';for(let r=0;r<9;r++)for(let c=0;c<9;c++){{const d=document.createElement('div');d.className='c';d.dataset.r=r;d.dataset.c=c;d.onclick=()=>pick(r,c);BD.appendChild(d)}}}}
function mkN(){{NP.innerHTML='';for(let n=1;n<=9;n++){{const b=document.createElement('button');b.textContent=n;b.onclick=()=>put(n);NP.appendChild(b)}}}}
function draw(){{const cs=BD.querySelectorAll('.c'),ct=Array(10).fill(0);cs.forEach(c=>{{const r=+c.dataset.r,co=+c.dataset.c,v=pb[r][co],ig=gv[r][co],ns=nt[r][co];c.className='c';c.innerHTML='';if(ig){{c.classList.add('gv');c.textContent=v;ct[v]++}}else{{c.classList.add('ed');if(v){{c.textContent=v;ct[v]++;if(v!==sol[r][co])c.classList.add('er')}}else if(ns.size){{const d=document.createElement('div');d.className='nt';for(let n=1;n<=9;n++){{const s=document.createElement('span');s.textContent=ns.has(n)?n:'';d.appendChild(s)}}c.appendChild(d)}}}}if(sel){{const sr=sel.r,sc=sel.c;if(r===sr&&co===sc)c.classList.add('sl');else if(r===sr||co===sc||(r/3|0)===(sr/3|0)&&(co/3|0)===(sc/3|0))c.classList.add('hl');const sv=pb[sr][sc];if(sv&&v===sv&&!(r===sr&&co===sc))c.classList.add('sm')}}}});const bs=NP.querySelectorAll('button');bs.forEach((b,i)=>{{const n=i+1;b.innerHTML=n+'<span class="ct">'+(9-ct[n])+'</span>';b.classList.toggle('uu',ct[n]>=9)}});document.getElementById('ms').textContent=mk>0?'\\u274c '+mk+'/'+mx:''}}
function pick(r,c){{if(ov)return;sel={{r,c}};draw()}}
function put(n){{if(!sel||ov)return;const{{r,c}}=sel;if(gv[r][c])return;if(nm){{const s=nt[r][c];hs.push({{t:'n',r,c,h:new Set(s)}});s.has(n)?s.delete(n):s.add(n);pb[r][c]=E}}else{{hs.push({{t:'p',r,c,v:pb[r][c],n:new Set(nt[r][c])}});pb[r][c]=n;nt[r][c]=new Set;if(n!==sol[r][c]){{mk++;if(mk>=mx){{ov=!0;clearInterval(ti);setTimeout(()=>alert('游戏结束！错误次数过多'),200)}}}}else{{for(let i=0;i<9;i++){{nt[r][i].delete(n);nt[i][c].delete(n)}}const br=3*(r/3|0),bc=3*(c/3|0);for(let i=br;i<br+3;i++)for(let j=bc;j<bc+3;j++)nt[i][j].delete(n)}}chk()}}draw()}}
function erase(){{if(!sel||ov)return;const{{r,c}}=sel;if(gv[r][c])return;hs.push({{t:'e',r,c,v:pb[r][c],n:new Set(nt[r][c])}});pb[r][c]=E;nt[r][c]=new Set;draw()}}
function undo(){{if(!hs.length||ov)return;const a=hs.pop();if(a.t==='n')nt[a.r][a.c]=a.h;else{{if(a.t==='p'&&pb[a.r][a.c]!==sol[a.r][a.c])mk=Math.max(0,mk-1);pb[a.r][a.c]=a.v;nt[a.r][a.c]=a.n}}draw()}}
function toggleNote(){{nm=!nm;document.getElementById('nb').classList.toggle('on',nm)}}
function hint(){{if(ov)return;const e=[];for(let r=0;r<9;r++)for(let c=0;c<9;c++)if(pb[r][c]!==sol[r][c])e.push({{r,c}});if(!e.length)return;const{{r,c}}=e[0|Math.random()*e.length];hs.push({{t:'p',r,c,v:pb[r][c],n:new Set(nt[r][c])}});pb[r][c]=sol[r][c];nt[r][c]=new Set;gv[r][c]=!0;sel={{r,c}};draw();BD.children[r*9+c].classList.add('fl');chk()}}
function chk(){{for(let r=0;r<9;r++)for(let c=0;c<9;c++)if(pb[r][c]!==sol[r][c])return;ov=!0;clearInterval(ti);setTimeout(()=>{{const dm={{easy:'简单',medium:'中等',hard:'困难',expert:'地狱'}};document.getElementById('wt').textContent='\\u23f1 用时：'+fmt(sec);document.getElementById('wk').textContent='\\u274c 错误：'+mk+' 次';document.getElementById('wd').textContent='\\ud83d\\udcca 难度：'+dm[document.getElementById('df').value];document.getElementById('wm').classList.add('show')}},300)}}
function closeWin(){{document.getElementById('wm').classList.remove('show')}}
function startT(){{clearInterval(ti);sec=0;upT();ti=setInterval(()=>{{sec++;upT()}},1000)}}
function upT(){{document.getElementById('tm').textContent=fmt(sec)}}
function fmt(s){{return String(s/60|0).padStart(2,'0')+':'+String(s%60).padStart(2,'0')}}
document.addEventListener('keydown',e=>{{if(ov)return;const n=+e.key;if(n>=1&&n<=9)return put(n);if(e.key==='Backspace'||e.key==='Delete')return erase();if(e.key==='n'||e.key==='N')return toggleNote();if((e.key==='z'||e.key==='Z')&&(e.ctrlKey||e.metaKey))return undo();if(sel){{let{{r,c}}=sel;if(e.key==='ArrowUp')r=(r+8)%9;else if(e.key==='ArrowDown')r=(r+1)%9;else if(e.key==='ArrowLeft')c=(c+8)%9;else if(e.key==='ArrowRight')c=(c+1)%9;else return;e.preventDefault();pick(r,c)}}}});
function newGame(){{const d=document.getElementById('df').value,r=gen(d);pz=r.p;sol=r.s;pb=pz.map(r=>[...r]);gv=pz.map(r=>r.map(v=>v!==E));nt=Array.from({{length:9}},()=>Array.from({{length:9}},()=>new Set));sel=null;nm=!1;mk=0;hs=[];ov=!1;document.getElementById('nb').classList.remove('on');closeWin();startT();draw()}}
mkB();mkN();newGame();
</script>
</body>
</html>'''


def main():
    p = argparse.ArgumentParser(description="数独游戏 HTML 生成器")
    p.add_argument("--difficulty", choices=DIFF_REMOVE.keys(), default="medium")
    p.add_argument("--theme", choices=THEMES.keys(), default="dark")
    p.add_argument("--title", default="九宫格数独")
    p.add_argument("--output", default=None)
    a = p.parse_args()

    if a.output is None:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        out = os.path.join(root, "output")
        os.makedirs(out, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        a.output = os.path.join(out, f"sudoku_{a.difficulty}_{ts}.html")

    os.makedirs(os.path.dirname(a.output) or ".", exist_ok=True)
    with open(a.output, "w", encoding="utf-8") as f:
        f.write(generate_html(a.difficulty, a.theme, a.title))

    print(f"✅ 数独游戏已生成！")
    print(f"   难度: {DIFF_NAMES[a.difficulty]}")
    print(f"   主题: {THEMES[a.theme]['name']}")
    print(f"   文件: {a.output}")


if __name__ == "__main__":
    main()

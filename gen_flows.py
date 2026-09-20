# -*- coding: utf-8 -*-
"""三版链路图统一生成器：改 SPECS 即可重出全部，样式自动对齐。"""
import subprocess, sys
from PIL import Image

W=1180; PHX=118; LANEW=250; NW,NH,GAP=214,64,40; Y0=168; STEP=NH+GAP
LANES=[("家长","#2f6fd0","#eaf2fd"),("孩子","#e8762a","#fff1e8"),
       ("销售 / 服务","#3a9e63","#e8f6ee"),("APP 自动","#7d8da3","#eef1f7")]
ST={"ok":("#3a9e63","已建"),"part":("#d1873a","部分"),"gap":("#d9534f","缺口"),
    "risk":("#e05c46","高流失"),"ops":("#a3b0c2","运营侧")}
def cx(i): return PHX+LANEW*i+LANEW//2
def ny(i): return Y0+i*STEP

def svg(sp):
    S,PH,HAND,LOOP,BOXES,ac=sp["steps"],sp["phases"],sp["hand"],sp["loop"],sp.get("boxes",[]),sp["accent"]
    H=ny(len(S)-1)+NH+76
    o=[f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
       'font-family="PingFang SC,Hiragino Sans GB,Microsoft YaHei,sans-serif">',
       '<defs>'
       '<marker id="a" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#9db0c8"/></marker>'
       '<marker id="ah" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#e05c46"/></marker>'
       '<marker id="al" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#9b8fd0"/></marker>'
       '</defs>', f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    for name,a,b,col in PH:
        y=ny(a)-22; h=ny(b)+NH+22-y
        o.append(f'<rect x="8" y="{y}" width="{W-16}" height="{h}" rx="14" fill="{col}"/>')
        o.append(f'<text x="58" y="{y+h/2-8}" font-size="19" font-weight="800" fill="#1b4b8f" text-anchor="middle">{name}</text>')
        o.append(f'<text x="58" y="{y+h/2+16}" font-size="13" fill="#9aa8bc" text-anchor="middle">{a+1:02d}–{b+1:02d}</text>')
    for a,b,label,side in BOXES:
        lns=[S[i][2] for i in range(a,b+1)]
        bx=cx(min(lns))-NW/2-16; bw=(cx(max(lns))+NW/2+16)-bx
        by=ny(a)-16; bh=(ny(b)+NH+16)-by
        o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="16" fill="{ac["boxfill"]}" '
                 f'fill-opacity="0.85" stroke="{ac["box"]}" stroke-width="2.4" stroke-dasharray="9 6"/>')
        lw=len(label)*15+34
        lx = bx-lw-8 if side=="left" else bx+bw-lw-16
        ly = by+bh/2-14 if side=="left" else by-14
        o.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="28" rx="13" fill="{ac["box"]}"/>')
        o.append(f'<text x="{lx+lw/2}" y="{ly+20}" font-size="15" font-weight="800" fill="#fff" text-anchor="middle">{label}</text>')
    for i,(nm,c,_t) in enumerate(LANES):
        x=PHX+LANEW*i
        o.append(f'<rect x="{x+6}" y="14" width="{LANEW-12}" height="54" rx="12" fill="{c}"/>')
        o.append(f'<text x="{cx(i)}" y="48" font-size="19" font-weight="800" fill="#fff" text-anchor="middle">{nm}</text>')
        if i: o.append(f'<line x1="{x}" y1="80" x2="{x}" y2="{H-60}" stroke="#dde6f2" stroke-width="1" stroke-dasharray="3 5"/>')
    for i in range(len(S)-1):
        hand=(i+1) in HAND
        x1,y1=cx(S[i][2]),ny(i)+NH; x2,y2=cx(S[i+1][2]),ny(i+1)
        col,mk=("#e05c46","ah") if hand else ("#9db0c8","a")
        dash=' stroke-dasharray="7 5"' if hand else ''
        if x1==x2:
            o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2-3}" stroke="{col}" stroke-width="2.4"{dash} marker-end="url(#{mk})"/>')
        else:
            m=(y1+y2)/2
            o.append(f'<path d="M{x1},{y1} L{x1},{m} L{x2},{m} L{x2},{y2-3}" fill="none" stroke="{col}" stroke-width="2.4"{dash} marker-end="url(#{mk})"/>')
            if hand:
                o.append(f'<rect x="{(x1+x2)/2-30}" y="{m-13}" width="60" height="24" rx="11" fill="#fdeeea"/>')
                o.append(f'<text x="{(x1+x2)/2}" y="{m+4}" font-size="13" font-weight="800" fill="#d9534f" text-anchor="middle">交接</text>')
    lf,lt=LOOP; xr=W-30; yb=ny(lf)+NH/2; yt=ny(lt)+NH/2
    o.append(f'<path d="M{cx(S[lf][2])+NW/2},{yb} L{xr},{yb} L{xr},{yt} L{cx(S[lt][2])+NW/2+3},{yt}" fill="none" '
             'stroke="#9b8fd0" stroke-width="2.4" stroke-dasharray="7 5" marker-end="url(#al)"/>')
    o.append(f'<rect x="{xr-34}" y="{(yb+yt)/2-34}" width="30" height="68" rx="10" fill="#f0edfa"/>')
    for k,ch in enumerate("每月循环"):
        o.append(f'<text x="{xr-19}" y="{(yb+yt)/2-20+k*16}" font-size="12" font-weight="800" fill="#6b5cb0" text-anchor="middle">{ch}</text>')
    for i,(no,t,ln,stt,srv,chg) in enumerate(S):
        c,tint=(LANES[ln][1],LANES[ln][2])
        if srv: c,tint="#2aa6a0","#e6f5f4"
        x=cx(ln)-NW/2; y=ny(i)
        o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="13" fill="{tint}" stroke="{c}" stroke-width="2.2"/>')
        o.append(f'<rect x="{x}" y="{y}" width="6" height="{NH}" rx="3" fill="{c}"/>')
        o.append(f'<text x="{x+20}" y="{y+27}" font-size="14" font-weight="800" fill="{c}">{no}</text>')
        if chg:
            o.append(f'<rect x="{x+46}" y="{y+14}" width="34" height="19" rx="9" fill="{ac["box"]}"/>')
            o.append(f'<text x="{x+63}" y="{y+28}" font-size="12" font-weight="800" fill="#fff" text-anchor="middle">变更</text>')
        sc,sl=ST[stt]; wpx=64 if len(sl)==3 else 56
        o.append(f'<rect x="{x+NW-wpx-10}" y="{y+13}" width="{wpx}" height="21" rx="10" fill="{sc}" opacity="0.14"/>')
        o.append(f'<text x="{x+NW-wpx/2-10}" y="{y+28}" font-size="12.5" font-weight="800" fill="{sc}" text-anchor="middle">{sl}</text>')
        o.append(f'<text x="{x+20}" y="{y+50}" font-size="{15 if len(t)>12 else 16}" font-weight="700" fill="#1f2d3d">{t}</text>')
    chg_txt=f'　　<tspan fill="{ac["box"]}" font-weight="800">{ac["chglabel"]}</tspan>' if ac.get("chglabel") else ''
    o.append(f'<text x="{PHX+6}" y="{H-36}" font-size="13.5" fill="#8a97ab">实线＝顺序流转　　'
             '<tspan fill="#d9534f" font-weight="800">红虚线＝角色交接</tspan>　　'
             f'<tspan fill="#6b5cb0" font-weight="800">紫虚线＝每月循环</tspan>{chg_txt}　　状态：已建／部分／缺口／高流失／运营侧</text>')
    o.append('</svg>')
    return "\n".join(o)

TPL='''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>{badge}</title>
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;background:#e8eef7;display:flex;justify-content:center;padding:24px 0}}
.p{{width:1180px;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 6px 28px rgba(20,50,100,.14)}}
.h{{background:linear-gradient(120deg,{g1},{g2} 55%,{g3});padding:38px 46px;color:#fff;position:relative;overflow:hidden}}
.h::after{{content:"";position:absolute;right:-60px;top:-80px;width:300px;height:300px;background:rgba(255,255,255,.12);border-radius:50%}}
.h .bd{{display:inline-block;font-size:15px;background:rgba(255,255,255,.24);padding:6px 16px;border-radius:16px;margin-bottom:13px;font-weight:700}}
.h h1{{font-size:36px;font-weight:800}}.h p{{font-size:19px;margin-top:9px;opacity:.94}}
.d{{padding:26px 46px;background:{bandbg};border-bottom:1px solid {bandbd}}}
.d h3{{font-size:19px;font-weight:800;color:{box};margin-bottom:12px}}
.d .two{{display:flex;gap:22px}}.d .col{{flex:1}}.d ul{{list-style:none}}
.d li{{font-size:15.5px;color:#5a6b80;line-height:1.75;padding-left:20px;position:relative;margin-bottom:9px}}
.d li::before{{content:"·";position:absolute;left:4px;font-weight:800;color:{box};font-size:18px}}
.d li.bad::before{{content:"!";color:#d9534f;font-size:14px;left:6px}}
.d li b{{color:#1f2d3d}}
.d h4{{font-size:16px;font-weight:800;color:#1f2d3d;margin-bottom:10px}}.d h4.r{{color:#b9762a}}
.k{{margin-top:20px;background:#fff;border-left:6px solid {box};border-radius:11px;padding:16px 20px;font-size:16px;color:#33414f;line-height:1.8}}
.k b{{color:{box}}}
.f{{background:#1b3a63;color:#fff;padding:26px 46px;display:flex;justify-content:space-between;align-items:center}}
.f b{{font-size:23px}}.f p{{font-size:16px;opacity:.75;margin-top:6px}}.f .r{{text-align:right;font-size:17px;line-height:1.7;opacity:.9}}
</style></head><body><div class="p">
<div class="h"><div class="bd">{badge}</div><h1>家长 × 孩子 · 全链路流程图</h1><p>{sub}</p></div>
<div class="d"><h3>{bandtitle}</h3><div class="two">
<div class="col"><h4>{c1t}</h4><ul>{c1}</ul></div>
<div class="col"><h4 class="r">{c2t}</h4><ul>{c2}</ul></div></div>{key}</div>
{svg}
<div class="f"><div><b>【JOJOUP】</b><p>{ftl}</p></div><div class="r">{ftr}</div></div>
</div></body></html>'''

def li(items,bad=False):
    return "".join(f'<li{" class=\'bad\'" if bad else ""}>{x}</li>' for x in items)

def build(sp):
    ac=sp["accent"]
    html=TPL.format(badge=sp["badge"],sub=sp["sub"],g1=ac["g1"],g2=ac["g2"],g3=ac["g3"],
        box=ac["box"],bandbg=ac["bandbg"],bandbd=ac["bandbd"],
        bandtitle=sp["bandtitle"],c1t=sp["c1t"],c2t=sp["c2t"],
        c1=li(sp["c1"]),c2=li(sp["c2"],True),
        key=(f'<div class="k">{sp["key"]}</div>' if sp.get("key") else ''),
        svg=svg(sp),ftl=sp["ftl"],ftr=sp["ftr"])
    open(sp["file"]+".html","w",encoding="utf-8").write(html)
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome","--headless",
        "--disable-gpu","--hide-scrollbars",f"--screenshot={sp['file']}._t.png",
        "--window-size=1240,4200","--default-background-color=e8eef7",
        f"file://{__import__('os').getcwd()}/{sp['file']}.html"],
        capture_output=True)
    im=Image.open(sp["file"]+"._t.png").convert("RGB"); w,h=im.size
    bg=im.getpixel((5,h-5)); last=h-1
    for y in range(h-1,-1,-1):
        if any(sum(abs(p-q) for p,q in zip(im.getpixel((x,y)),bg))>12 for x in range(0,w,30)):
            last=y; break
    im.crop((0,0,w,last+24)).save(sp["file"]+".png")
    __import__('os').remove(sp["file"]+"._t.png")
    return Image.open(sp["file"]+".png").size

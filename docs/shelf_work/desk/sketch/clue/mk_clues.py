# 서고 이야기의 물건 셋(11-25): 열쇠 꾸러미(하나만 탐), 반쯤 탄 장부 쪽지, 그을린 서가에 들어온 책 한 권
import math, random
H='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
D='<defs><filter id="r"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter><radialGradient id="ch" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#1a0f08"/><stop offset=".7" stop-color="#2b1a0e"/><stop offset="1" stop-color="#4a2e18" stop-opacity="0"/></radialGradient></defs>'
def key(x,y,ang,col,burnt=False):
    g='<g transform="translate(%g %g) rotate(%g)">'%(x,y,ang)
    st='#2a1a0e' if not burnt else '#0b0604'
    g+='<circle cx="0" cy="0" r="11" fill="none" stroke="%s" stroke-width="6"/>'%col
    g+='<circle cx="0" cy="0" r="11" fill="none" stroke="%s" stroke-width="1.2"/>'%st
    g+='<rect x="-3.2" y="10" width="6.4" height="66" rx="2" fill="%s" stroke="%s" stroke-width="1.2"/>'%(col,st)
    g+='<path d="M3 58h12v6h-6v6h6v6H3z" fill="%s" stroke="%s" stroke-width="1.2"/>'%(col,st)
    if burnt: g+='<ellipse cx="0" cy="38" rx="9" ry="40" fill="url(#ch)" opacity=".7"/>'
    return g+'</g>'
k=H+D+'<g filter="url(#r)"><circle cx="100" cy="46" r="26" fill="none" stroke="#6b5232" stroke-width="7"/><circle cx="100" cy="46" r="26" fill="none" stroke="#2a1a0e" stroke-width="1.4"/>'
k+=key(78,70,22,'#b8945a')+key(100,74,0,'#1c120b',True)+key(122,70,-22,'#a9864e')+'</g></svg>'
open('clue_key.svg','w').write(k)
random.seed(5)
edge=[]; 
for i in range(0,41):
    yy=18+i*4.1; xx=150+random.uniform(-14,10)+ (8*math.sin(i*.9))
    edge.append((xx,yy))
pts='M30 18 L'+' L'.join('%.1f %.1f'%e for e in edge)+' L30 182 Z'
L=H+D+'<g filter="url(#r)"><path d="%s" fill="#e8d6ad" stroke="#5a4226" stroke-width="1.5"/>'%pts
L+='<path d="%s" fill="none" stroke="#1a0f08" stroke-width="9" opacity=".75"/>'%('M'+' L'.join('%.1f %.1f'%e for e in edge))
for i in range(9):
    y=36+i*15; L+='<line x1="40" y1="%d" x2="138" y2="%d" stroke="#8a6c44" stroke-width=".8"/>'%(y+4,y+4)
    w=random.randint(50,92) if i<8 else 70
    L+='<path d="M44 %d q6 -5 12 0 t12 0 t12 0 t12 0 t12 0 t12 0" fill="none" stroke="#3a2614" stroke-width="1.6" transform="scale(%.2f 1) translate(%d 0)"/>'%(y,w/90,0)
L+='<rect x="74" y="148" width="58" height="12" fill="#2b1a0e" opacity=".8" rx="3"/><ellipse cx="128" cy="150" rx="26" ry="18" fill="url(#ch)" opacity=".8"/></g></svg>'

T='font-family="Noto Serif CJK KR,serif" fill="#3a2614"'
L=H+D+'<g filter="url(#r)"><path d="%s" fill="#e8d6ad" stroke="#5a4226" stroke-width="1.5"/>'%pts
L+='<path d="%s" fill="none" stroke="#1a0f08" stroke-width="9" opacity=".75"/>'%('M'+' L'.join('%.1f %.1f'%e for e in edge))
L+='<text x="40" y="38" font-size="15" font-weight="700" %s>서고 출입 장부</text><line x1="40" y1="45" x2="138" y2="45" stroke="#8a6c44"/>'%T
L+='<text x="40" y="64" font-size="12.5" %s>화재 때 옮긴 책</text>'%T
L+='<text x="44" y="88" font-size="15" font-weight="700" %s>구약</text><text x="96" y="88" font-size="17" font-weight="700" fill="#7a2f22">✓</text>'%T
L+='<text x="44" y="110" font-size="15" font-weight="700" %s>신약</text><text x="96" y="110" font-size="17" font-weight="700" fill="#7a2f22">✓</text>'%T
L+='<text x="44" y="132" font-size="15" font-weight="700" %s>끝 서가 …</text>'%T
L+='<text x="40" y="160" font-size="10" %s>기록한 사람</text><rect x="94" y="149" width="44" height="15" fill="#1e120a" opacity=".85" rx="3"/><ellipse cx="128" cy="152" rx="26" ry="16" fill="url(#ch)" opacity=".7"/></g></svg>'%T
open('clue_ledger.svg','w').write(L)
B=H+D+'<g filter="url(#r)"><rect x="70" y="28" width="60" height="150" rx="5" fill="#7a2f22" stroke="#2a120c" stroke-width="2"/><rect x="70" y="28" width="12" height="150" fill="#5e2219"/><rect x="76" y="50" width="48" height="5" fill="#d9b56a"/><rect x="76" y="150" width="48" height="5" fill="#d9b56a"/><rect x="88" y="80" width="30" height="44" rx="3" fill="#e8d6ad" stroke="#5a4226"/><path d="M95 94h16M95 102h16M95 110h12" stroke="#5a4226" stroke-width="2"/></g></svg>'
open('clue_book.svg','w').write(B)
G=H+D+'<g filter="url(#r)"><path d="M28 50 L100 40 L172 50 L172 160 L100 150 L28 160 Z" fill="#3a2214" stroke="#1a0c06" stroke-width="2"/>'
G+='<path d="M36 56 L98 47 L98 146 L36 154 Z" fill="#efe1bd"/><path d="M102 47 L164 56 L164 154 L102 146 Z" fill="#efe1bd"/>'
for i in range(8 if False else 6): G+='<line x1="44" y1="%d" x2="92" y2="%d" stroke="#6a5234" stroke-width="1.1"/><line x1="108" y1="%d" x2="156" y2="%d" stroke="#6a5234" stroke-width="1.1"/>'%(84+i*9,78+i*9,78+i*9,84+i*9)
G+='<text x="52" y="72" font-size="11" font-weight="700" font-family="Noto Serif CJK KR,serif" fill="#7a2f22">성경전서</text>'
G+='<path d="M28 160 Q60 150 100 150 Q140 150 172 160 L172 132 Q150 142 128 136 Q110 146 92 138 Q66 148 48 134 Q38 140 28 132 Z" fill="#140a05" opacity=".88"/><path d="M36 154 Q50 146 60 150 Q72 140 84 148 Q92 142 98 146 L98 128 Q90 134 82 126 Q70 136 58 128 Q48 136 36 130 Z" fill="#2a160a" opacity=".75"/></g></svg>'
open('clue_bible.svg','w').write(G)
print('ok')

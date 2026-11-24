# 사서 초상: SVG로 그린 뒤 판화 결을 입힌다
import random, math, sys
rng = random.Random(11)
def beard_strands():
    out = []
    for i in range(26):
        t = i / 25.0
        x0 = 112 + 76 * t
        y0 = 196 + 10 * math.sin(t * math.pi)
        xe = 150 + (x0 - 150) * 0.10 + rng.uniform(-3, 3)
        ye = 326 - abs(x0 - 150) * 0.55 + rng.uniform(-6, 4)
        cx = x0 + (x0 - 150) * 0.10 + rng.uniform(-4, 4)
        cy = (y0 + ye) / 2 + rng.uniform(-10, 10)
        op = 0.55 if x0 < 150 else 0.85
        out.append('<path d="M%.1f %.1fQ%.1f %.1f %.1f %.1f" stroke="#6f5d43" stroke-width=".7" fill="none" opacity="%.2f"/>' % (x0, y0, cx, cy, xe, ye, op))
    return '\n'.join(out)
def brow(cx, side):
    s = side
    X = lambda d: 150 + s * d
    pts = 'M%.1f 134.5 C%.1f 130.5 %.1f 131 %.1f 134 C%.1f 137 %.1f 142 %.1f 149 C%.1f 144.5 %.1f 141 %.1f 139.5 C%.1f 138.5 %.1f 138.5 %.1f 139.5 Z' % (
        X(6), X(13), X(21), X(27), X(33), X(37), X(39), X(34), X(28), X(21), X(15), X(10), X(6))
    hairs = []
    for i in range(9):
        x = X(8 + i * 3.3)
        hairs.append('<path d="M%.1f %.1fl%.1f %.1f" stroke="#7a6a52" stroke-width=".6"/>' % (x, 138.5 + i * 0.55, s * 2.4, -4.6 + i * 0.25))
    return '<path d="%s" fill="#efe7d4" stroke="#1a110b" stroke-width=".7" stroke-linejoin="round"/>' % pts + ''.join(hairs)
def eye(cx, side, shut=0.0):
    s = side
    o = []
    o.append('<ellipse cx="%.1f" cy="150.5" rx="11" ry="5" fill="#8a5a34" opacity=".14" filter="url(#b3)"/>' % cx)
    o.append('<path d="M%.1f 153Q%.1f 144.2 %.1f 153" stroke="#2a180e" stroke-width="2" fill="none" stroke-linecap="round"/>' % (cx - 8.6, cx, cx + 8.6))
    o.append('<path d="M%.1f 147.5Q%.1f 141.5 %.1f 148" stroke="#9a7246" stroke-width=".6" fill="none"/>' % (cx - 10, cx, cx + 10.5))
    o.append('<path d="M%.1f 157Q%.1f 160 %.1f 157" stroke="#9a7246" stroke-width=".7" fill="none"/>' % (cx - 7, cx, cx + 7))
    ox = cx + s * 10
    for dy, ex in ((-3.4, -3.2), (0.4, 0.2), (4.0, 3.6)):
        o.append('<path d="M%.1f %.1fq%.1f %.1f %.1f %.1f" stroke="#7a5532" stroke-width=".65" fill="none" stroke-linecap="round"/>' % (ox, 152.5 + dy * 0.3, s * 3, dy * 0.4, s * 6.5, ex))
    return ''.join(o)
SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="34 12 232 368">
<defs>
<filter id="b2" x="-30%%" y="-30%%" width="160%%" height="160%%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="b3" x="-40%%" y="-40%%" width="180%%" height="180%%"><feGaussianBlur stdDeviation="3.2"/></filter>
<filter id="b6" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="7"/></filter>
<radialGradient id="glow" gradientUnits="userSpaceOnUse" cx="66" cy="286" r="230"><stop offset="0" stop-color="#ffd58a" stop-opacity=".95"/><stop offset=".25" stop-color="#ffbe68" stop-opacity=".5"/><stop offset=".6" stop-color="#ff9f45" stop-opacity=".14"/><stop offset="1" stop-color="#ff9f45" stop-opacity="0"/></radialGradient>
<linearGradient id="hoodsh" gradientUnits="userSpaceOnUse" x1="150" y1="92" x2="150" y2="166"><stop offset="0" stop-color="#3a2415" stop-opacity=".5"/><stop offset=".45" stop-color="#3a2415" stop-opacity=".16"/><stop offset="1" stop-color="#0d0705" stop-opacity="0"/></linearGradient>
<linearGradient id="sidesh" gradientUnits="userSpaceOnUse" x1="138" y1="150" x2="192" y2="140"><stop offset="0" stop-color="#0d0705" stop-opacity="0"/><stop offset=".55" stop-color="#3a2415" stop-opacity=".1"/><stop offset="1" stop-color="#3a2415" stop-opacity=".3"/></linearGradient>
<linearGradient id="beardsh" gradientUnits="userSpaceOnUse" x1="120" y1="230" x2="196" y2="214"><stop offset="0" stop-color="#2a1b10" stop-opacity="0"/><stop offset=".6" stop-color="#2a1b10" stop-opacity=".34"/><stop offset="1" stop-color="#2a1b10" stop-opacity=".72"/></linearGradient>
<clipPath id="cface"><path d="M114 124C110 150 114 180 126 196C136 206 164 206 174 196C186 180 190 150 186 124C182 98 118 98 114 124Z"/></clipPath>
<clipPath id="cbeard"><path id="pbeard" d="M111 150C104 176 102 206 110 236C118 270 136 304 150 334C164 304 182 270 190 236C198 206 196 176 189 150C186 172 178 186 166 190C160 186 155 185 150 185C145 185 140 186 134 190C122 186 114 172 111 150Z"/></clipPath>
<clipPath id="ccloak"><path d="M10 380C12 320 30 282 62 264L86 238L214 238L238 264C270 282 288 320 290 380Z"/></clipPath>
<clipPath id="chood"><path d="M52 264C38 170 70 40 150 20C230 40 262 170 248 264L214 238C226 170 210 78 150 62C90 78 74 170 86 238Z"/></clipPath>
</defs>
<g transform="rotate(-2.5 150 240)">
<!-- 망토 -->
<path d="M10 380C12 320 30 282 62 264L86 238L214 238L238 264C270 282 288 320 290 380Z" fill="#2b1f16" stroke="#120b07" stroke-width="1.6" stroke-linejoin="round"/>
<g clip-path="url(#ccloak)" fill="none" stroke="#120b07" stroke-width="1.1" opacity=".75">
<path d="M96 246C84 290 80 340 84 380M112 250C106 300 106 340 110 380M204 246C216 290 220 340 216 380M188 250C194 300 194 340 190 380M240 272C252 304 258 340 258 380M60 272C48 304 42 340 42 380"/>
</g>
<g clip-path="url(#ccloak)"><path d="M62 264C40 290 26 330 22 380L70 380C70 330 78 290 96 250Z" fill="#6b4a2c" opacity=".55" filter="url(#b6)"/></g>
<!-- 두건 -->
<path d="M52 264C38 170 70 40 150 20C230 40 262 170 248 264L214 238L86 238Z" fill="#33251a" stroke="#120b07" stroke-width="1.6" stroke-linejoin="round"/>
<path d="M86 238C74 170 90 78 150 62C210 78 226 170 214 238Z" fill="#3d2b1d"/><path d="M96 232C86 172 100 92 150 78C200 92 214 172 204 232Z" fill="#5a4129" opacity=".7" filter="url(#b6)"/>
<g clip-path="url(#chood)" fill="none" stroke="#120b07" stroke-width="1" opacity=".7">
<path d="M66 250C54 170 80 62 150 40M234 250C246 170 220 62 150 40M76 244C66 170 86 70 150 52M224 244C234 170 214 70 150 52"/>
</g>
<g clip-path="url(#chood)"><path d="M52 264C38 170 70 40 150 20L150 62C90 78 74 170 86 238Z" fill="#8a633c" opacity=".5" filter="url(#b6)"/>
<path d="M150 20C230 40 262 170 248 264L214 238C226 170 210 78 150 62Z" fill="#080403" opacity=".55" filter="url(#b6)"/></g>
<!-- 얼굴 -->
<path d="M114 124C110 150 114 180 126 196C136 206 164 206 174 196C186 180 190 150 186 124C182 98 118 98 114 124Z" fill="#e6c89c"/>
<g clip-path="url(#cface)">
<ellipse cx="124" cy="171" rx="11" ry="8" fill="#dd8763" opacity=".34" filter="url(#b3)"/><ellipse cx="176" cy="171" rx="11" ry="8" fill="#dd8763" opacity=".3" filter="url(#b3)"/>

<rect x="100" y="90" width="100" height="80" fill="url(#hoodsh)"/>
<rect x="130" y="90" width="70" height="130" fill="url(#sidesh)"/>
<path d="M128 119Q150 114 172 119M132 126Q150 122 168 126" stroke="#8a6238" stroke-width=".6" fill="none" opacity=".7"/>
</g>
<path d="M114 124C110 150 114 180 126 196" fill="none" stroke="#1a110b" stroke-width="1"/>
%(eyeL)s%(eyeR)s
<g transform="translate(0 -3)">%(browL)s%(browR)s</g>
<!-- 코 -->
<path d="M147.500 147C147 158 144.500 167 143 172.500C142 178.500 145.500 183 150 183C154.500 183 158 178.500 157 172.500C155.500 167 153 158 152.500 147Z" fill="#dcbb8e"/>
<path d="M143 172.500C142 178.500 145.500 183 150 183C154.500 183 158 178.500 157 172.500" fill="none" stroke="#3a2416" stroke-width=".95" stroke-linecap="round"/>
<path d="M143 173.500q-3.800 0 -4.200 3.600q1 3 4.600 2.400M157 173.500q3.800 0 4.200 3.600q-1 3 -4.600 2.400" fill="none" stroke="#3a2416" stroke-width=".8" stroke-linecap="round"/>
<ellipse cx="148.500" cy="175.500" rx="2.600" ry="2.100" fill="#fff2d6" opacity=".75"/>
<!-- 볼 주름 -->
<path d="M135 180Q128 187 127 196M165 180Q172 187 173 196" stroke="#7a5532" stroke-width=".8" fill="none"/>

<!-- 수염 -->
<path d="M111 150C104 176 102 206 110 236C118 270 136 304 150 334C164 304 182 270 190 236C198 206 196 176 189 150C186 172 178 186 166 190C160 186 155 185 150 185C145 185 140 186 134 190C122 186 114 172 111 150Z" fill="#ebe2cd" stroke="#120b07" stroke-width="1.2" stroke-linejoin="round"/>
<g clip-path="url(#cbeard)">
<rect x="96" y="140" width="110" height="200" fill="url(#beardsh)"/>
<path d="M104 240C116 280 134 310 150 334L150 250Z" fill="#ffe2a8" opacity=".55" filter="url(#b6)"/>
%(strands)s
</g>
<!-- 콧수염과 웃는 입 -->
<path d="M142 204.500Q150 212.500 158 204.500" fill="#b8563f" stroke="#4a2114" stroke-width="1" stroke-linejoin="round"/>
<path d="M150 188.500C145 186 138 187 133 191.500C129.500 195 127 199.500 126 205C131 202.500 136 201 140.500 200.500C144.500 200.200 147.500 201 150 203C152.500 201 155.500 200.200 159.500 200.500C164 201 169 202.500 174 205C173 199.500 170.500 195 167 191.500C162 187 155 186 150 188.500Z" fill="#f7f1e0" stroke="#5a4630" stroke-width=".8" stroke-linejoin="round"/>
<path d="M150 190.500v11M145.500 191Q139 194 132 200M154.500 191Q161 194 168 200M148 194Q143 196.500 138 199.500M152 194Q157 196.500 162 199.500" stroke="#8a7a5c" stroke-width=".5" fill="none"/>
<!-- 열쇠 꾸러미: 소매 끝에서 늘어짐 -->
<circle cx="222" cy="322" r="14" fill="none" stroke="#1a110b" stroke-width="4.200"/><circle cx="222" cy="322" r="14" fill="none" stroke="#8d6b34" stroke-width="2.400"/>
<g stroke-linecap="round" fill="none">
<path d="M212 334l-8 34m0 0h7m-9-8h7" stroke="#1a110b" stroke-width="4"/><path d="M212 334l-8 34m0 0h7m-9-8h7" stroke="#c79c48" stroke-width="2.200"/>
<path d="M222 336l1 38m0 0h7m-7-9h6" stroke="#1a110b" stroke-width="4"/><path d="M222 336l1 38m0 0h7m-7-9h6" stroke="#77684f" stroke-width="2.200"/>
<path d="M232 334l10 32m0 0h7m-10-8h7" stroke="#050302" stroke-width="4.600"/><path d="M232 334l10 32m0 0h7m-10-8h7" stroke="#2a211a" stroke-width="1.600"/>
</g>
<path d="M290 380C288 338 268 300 232 288L204 300C210 306 214 312 216 320C222 312 232 312 238 320C244 336 246 356 246 380Z" fill="#33251a" stroke="#120b07" stroke-width="1.400" stroke-linejoin="round"/>
<path d="M204 300C210 306 214 312 216 320" fill="none" stroke="#0b0604" stroke-width="3"/>
<path d="M250 310C262 330 268 354 268 380" fill="none" stroke="#120b07" stroke-width="1" opacity=".7"/>
<!-- 촛대: 소매 끝에서 -->
<rect x="60" y="300" width="13" height="42" rx="2" fill="#f3e6c4" stroke="#120b07" stroke-width="1"/>
<path d="M60 308q-3 6 0 12M73 304q3 8 0 14" stroke="#c9b68c" stroke-width="1.200" fill="none"/>
<ellipse cx="66.500" cy="343" rx="25" ry="6" fill="#9a7436" stroke="#120b07" stroke-width="1.100"/>
<path d="M59 349h15v10h-15z" fill="#7d5d2b" stroke="#120b07" stroke-width="1"/>
<path d="M10 380C12 350 24 330 46 322L96 340C92 346 90 352 90 358C78 352 56 352 44 358C42 366 42 372 42 380Z" fill="#3a2a1d" stroke="#120b07" stroke-width="1.400" stroke-linejoin="round"/>
<path d="M44 358C56 352 78 352 90 358C90 366 88 374 84 380L48 380C44 374 43 366 44 358Z" fill="#b98f63" stroke="#120b07" stroke-width="1" stroke-linejoin="round"/>
<path d="M55 357v23M66 355v25M77 357v23" stroke="#120b07" stroke-width=".7"/>
<path d="M66.500 300v-6" stroke="#120b07" stroke-width="1.200"/>
<path d="M66.500 268C60 280 59 289 62 294C64 297.500 69 297.500 71 294C74 289 73 280 66.500 268Z" fill="#fff3c4" stroke="#b9792a" stroke-width=".8"/>
<path d="M66.500 279C64 285 64 290 66.500 293C69 290 69 285 66.500 279Z" fill="#f7a53a"/>
</g>
</svg>'''
svg = SVG % dict(eyeL=eye(133, -1, 0.0), eyeR=eye(167, 1, 0.35), browL=brow(133, -1), browR=brow(167, 1), strands=beard_strands())
open(sys.argv[1], 'w').write(svg)

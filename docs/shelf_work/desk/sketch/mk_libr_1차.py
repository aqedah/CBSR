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
    o.append('<ellipse cx="%.1f" cy="149" rx="12" ry="6" fill="#1b100a" opacity="%.2f" filter="url(#b3)"/>' % (cx, 0.5 if s > 0 else 0.26))
    top = 144.2 + shut * 1.6
    o.append('<path d="M%.1f 151.5Q%.1f %.1f %.1f 151.5Q%.1f %.1f %.1f 151.5Z" fill="#150c07"/>' % (cx - 9.5, cx, top, cx + 9.5, cx, top + 4.4 - shut, cx - 9.5))
    o.append('<path d="M%.1f 151.5Q%.1f %.1f %.1f 151.5" stroke="#150c07" stroke-width="1.3" fill="none" stroke-linecap="round"/>' % (cx - 10, cx, top - 0.4, cx + 10))
    if shut < 0.2:
        o.append('<circle cx="%.1f" cy="%.1f" r=".9" fill="#ffe7b0"/>' % (cx - 2.2, top + 3.0))
    o.append('<path d="M%.1f 147Q%.1f %.1f %.1f 147.5" stroke="#3b2717" stroke-width=".7" fill="none"/>' % (cx - 11, cx, top - 5, cx + 11.5))
    o.append('<path d="M%.1f 156.5Q%.1f 160 %.1f 156" stroke="#3b2717" stroke-width=".7" fill="none"/>' % (cx - 8, cx, cx + 8))
    ox = cx + s * 10.5
    for dy, ex in ((-4, -3.0), (0, 0.6), (4, 4.2)):
        o.append('<path d="M%.1f %.1fq%.1f %.1f %.1f %.1f" stroke="#3b2717" stroke-width=".6" fill="none"/>' % (ox, 151.5 + dy * 0.25, s * 3, dy * 0.45, s * 7, ex))
    return ''.join(o)
SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="34 12 232 368">
<defs>
<filter id="b2" x="-30%%" y="-30%%" width="160%%" height="160%%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="b3" x="-40%%" y="-40%%" width="180%%" height="180%%"><feGaussianBlur stdDeviation="3.2"/></filter>
<filter id="b6" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="7"/></filter>
<radialGradient id="glow" gradientUnits="userSpaceOnUse" cx="66" cy="286" r="230"><stop offset="0" stop-color="#ffd58a" stop-opacity=".95"/><stop offset=".25" stop-color="#ffbe68" stop-opacity=".5"/><stop offset=".6" stop-color="#ff9f45" stop-opacity=".14"/><stop offset="1" stop-color="#ff9f45" stop-opacity="0"/></radialGradient>
<linearGradient id="hoodsh" gradientUnits="userSpaceOnUse" x1="150" y1="92" x2="150" y2="166"><stop offset="0" stop-color="#0d0705" stop-opacity=".96"/><stop offset=".5" stop-color="#0d0705" stop-opacity=".6"/><stop offset="1" stop-color="#0d0705" stop-opacity="0"/></linearGradient>
<linearGradient id="sidesh" gradientUnits="userSpaceOnUse" x1="138" y1="150" x2="192" y2="140"><stop offset="0" stop-color="#0d0705" stop-opacity="0"/><stop offset=".55" stop-color="#0d0705" stop-opacity=".5"/><stop offset="1" stop-color="#0d0705" stop-opacity=".9"/></linearGradient>
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
<path d="M86 238C74 170 90 78 150 62C210 78 226 170 214 238Z" fill="#0b0604"/>
<g clip-path="url(#chood)" fill="none" stroke="#120b07" stroke-width="1" opacity=".7">
<path d="M66 250C54 170 80 62 150 40M234 250C246 170 220 62 150 40M76 244C66 170 86 70 150 52M224 244C234 170 214 70 150 52"/>
</g>
<g clip-path="url(#chood)"><path d="M52 264C38 170 70 40 150 20L150 62C90 78 74 170 86 238Z" fill="#8a633c" opacity=".5" filter="url(#b6)"/>
<path d="M150 20C230 40 262 170 248 264L214 238C226 170 210 78 150 62Z" fill="#080403" opacity=".55" filter="url(#b6)"/></g>
<!-- 얼굴 -->
<path d="M114 124C110 150 114 180 126 196C136 206 164 206 174 196C186 180 190 150 186 124C182 98 118 98 114 124Z" fill="#cfa97a"/>
<g clip-path="url(#cface)">
<ellipse cx="122" cy="172" rx="16" ry="20" fill="#f1d3a0" opacity=".85" filter="url(#b6)"/>
<ellipse cx="146" cy="170" rx="8" ry="14" fill="#f1d3a0" opacity=".5" filter="url(#b3)"/>
<rect x="100" y="90" width="100" height="80" fill="url(#hoodsh)"/>
<rect x="130" y="90" width="70" height="130" fill="url(#sidesh)"/>
<path d="M124 118Q150 111 176 118M127 125Q150 119 173 125M132 131Q150 127 168 131" stroke="#2a1a10" stroke-width=".7" fill="none" opacity=".8"/>
</g>
<path d="M114 124C110 150 114 180 126 196" fill="none" stroke="#1a110b" stroke-width="1"/>
%(eyeL)s%(eyeR)s
%(browL)s%(browR)s
<!-- 흉터 -->
<path d="M177 110C175 122 173 131 171 139M168.500 157C167 166 166 173 166 181" fill="none" stroke="#e0bd90" stroke-width="1.5" stroke-linecap="round" opacity=".75"/>
<path d="M177 110C175 122 173 131 171 139M168.500 157C167 166 166 173 166 181" fill="none" stroke="#3a1d12" stroke-width=".5" stroke-linecap="round" transform="translate(1.2 0)"/>
<!-- 코 -->
<path d="M147 142C146 156 143 168 141 176C140 181 144 185 150 185.500C156 185 160 181 159 176C157 168 154 156 153 142Z" fill="#c9a274"/>
<path d="M153 142C155 156 158 168 159.500 176C160 181 156 185 150 185.500" fill="none" stroke="#1f140d" stroke-width="1" stroke-linecap="round"/>
<path d="M141 176C140 181 144 185 150 185.500" fill="none" stroke="#1f140d" stroke-width=".8" stroke-linecap="round"/>
<path d="M141 176q-4.500 -1 -5.500 3.500q1 4 6 3M159.500 176q4.500 -1 5.500 3.500q-1 4 -6 3" fill="none" stroke="#1f140d" stroke-width=".8" stroke-linecap="round"/>
<path d="M155 150C157 162 160 172 160 178" stroke="#1b100a" stroke-width="4" opacity=".28" fill="none" filter="url(#b2)"/>
<path d="M147.500 150l-2 22" stroke="#f6dfb4" stroke-width="1.3" opacity=".7" stroke-linecap="round"/>
<!-- 볼 주름 -->
<path d="M134 181Q127 190 126 200M166 181Q173 190 174 200" stroke="#2a1a10" stroke-width=".8" fill="none"/>
<path d="M118 160q4 6 3 14M182 160q-4 6 -3 14" stroke="#2a1a10" stroke-width=".6" fill="none" opacity=".7"/>
<!-- 수염 -->
<path d="M111 150C104 176 102 206 110 236C118 270 136 304 150 334C164 304 182 270 190 236C198 206 196 176 189 150C186 172 178 186 166 190C160 186 155 185 150 185C145 185 140 186 134 190C122 186 114 172 111 150Z" fill="#ebe2cd" stroke="#120b07" stroke-width="1.2" stroke-linejoin="round"/>
<g clip-path="url(#cbeard)">
<rect x="96" y="140" width="110" height="200" fill="url(#beardsh)"/>
<path d="M104 240C116 280 134 310 150 334L150 250Z" fill="#ffe2a8" opacity=".55" filter="url(#b6)"/>
%(strands)s
</g>
<!-- 콧수염 -->
<path d="M144.500 203.500Q150 207.500 155.500 203.500" stroke="#3a1d12" stroke-width="1.100" fill="none" stroke-linecap="round"/>
<path d="M150 188.500C144 186 136 188 130 195C125 201 122 211 123 224C128 214 135 206 143 203C146 202 148 202 150 202C152 202 154 202 157 203C165 206 172 214 177 224C178 211 175 201 170 195C164 188 156 186 150 188.500Z" fill="#f5eedc" stroke="#120b07" stroke-width="1" stroke-linejoin="round"/>
<path d="M150 190v11M145 191Q136 196 128 212M155 191Q164 196 172 212M148 194Q141 198 134 207M152 194Q159 198 166 207" stroke="#6f5d43" stroke-width=".6" fill="none"/>
<path d="M150 202C152 202 154 202 157 203C165 206 172 214 177 224C178 211 175 201 170 195C164 188 156 186 150 188.500Z" fill="#2a1b10" opacity=".24"/>
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

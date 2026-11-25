#!/bin/sh
# 체험판 12월·부록: 세라핌 대림절·성탄·송구영신 묵상지(24쪽)를 작업대 부록 그림으로 찍습니다. (11-25)
# 묵상지 원고(guide27/sera/w12*.py, sera_v3_content.py)를 고친 뒤 저장소 맨 위에서: sh app/tools/ax26_pages.sh
# 쪽 번호는 82쪽부터(서문이 1쪽, 하루 지면 14–79쪽, 부록 머리 80–81쪽 다음). 종이 책은 같은 PDF를 그림이 아닌 원본으로 붙입니다.
set -e
T=$(mktemp -d)
python3 guide27/sera/sera4.py a5 "$T/appx.pdf" 82 w1201 w1208 w1215 w1222 w1225 w1229
pdftoppm -r 200 -png "$T/appx.pdf" "$T/q"
mkdir -p app/site_src/img/ax26
python3 - "$T" <<'PY'
import sys,glob,os
from PIL import Image
for i,f in enumerate(sorted(glob.glob(sys.argv[1]+'/q-*.png'))):
    Image.open(f).convert('RGB').quantize(48,dither=Image.Dither.NONE).save(f'app/site_src/img/ax26/p{82+i}.png',optimize=True)
PY
cp "$T/appx.pdf" app/site_src/img/ax26/appx.pdf
rm -rf "$T"; ls app/site_src/img/ax26 | wc -l

from PIL import Image
import sys
p = Image.open(sys.argv[1])
bg = Image.new('RGBA', (464*2+60, 736+40), (14, 9, 6, 255))
bg.alpha_composite(p, (20, 20))
s = p.resize((170, 270), Image.LANCZOS)
bg.alpha_composite(s, (520, 60))
f = p.crop((120, 150, 344, 374)).resize((96, 96), Image.LANCZOS)
bg.alpha_composite(f, (740, 60))
pp = Image.new('RGBA', (220, 320), (226, 206, 166, 255)); bg.alpha_composite(pp, (500, 400)); bg.alpha_composite(s, (525, 425))
bg.convert('RGB').save(sys.argv[2])

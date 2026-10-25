"""بيعمل أيقونات التطبيقين من أيقونة الموقع (client_icon.php) وقت البناء على GitHub Actions.
كابتن = نفس الأيقونة + علامة خضرا في الركن عشان يتفرّقوا على الموبايل. لو الموقع مش متاح → أيقونة لون سادة."""
import io, os, sys, urllib.request
from PIL import Image, ImageDraw

BASE = 'https://yasseryahia.com/client_icon.php?s=512&academy=1'
SIZES = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
root = sys.argv[1] if len(sys.argv) > 1 else 'app/src'

def fetch():
    try:
        req = urllib.request.Request(BASE, headers={'User-Agent': 'twa-build'})
        return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=30).read())).convert('RGBA').resize((512, 512))
    except Exception as e:
        print('icon fetch failed:', e)
        im = Image.new('RGBA', (512, 512), '#C42026')
        return im

def badge(im):
    im = im.copy(); d = ImageDraw.Draw(im)
    r = 92; cx, cy = 512 - r - 18, 512 - r - 18
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill='#0B2A22', outline='#FFFFFF', width=14)
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline='#1D9E75', width=16)   # «دركسيون» بسيط
    d.line([cx - 40, cy, cx + 40, cy], fill='#1D9E75', width=14)
    d.line([cx, cy, cx, cy + 40], fill='#1D9E75', width=14)
    return im

base = fetch()
for flavor, img in (('client', base), ('captain', badge(base))):
    for dpi, px in SIZES.items():
        d = f'{root}/{flavor}/res/mipmap-{dpi}'; os.makedirs(d, exist_ok=True)
        img.resize((px, px), Image.LANCZOS).save(f'{d}/ic_launcher.png')
    d = f'{root}/{flavor}/res/drawable'; os.makedirs(d, exist_ok=True)
    img.resize((288, 288), Image.LANCZOS).save(f'{d}/splash.png')
    img.save(f'{root}/{flavor}/play_icon_512.png')
print('icons ok')

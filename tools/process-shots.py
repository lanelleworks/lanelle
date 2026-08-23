"""
Compress whatever is dropped in assets/work/shots/ into the slideshow frames.

Run:  py tools/process-shots.py

Takes any jpg/jpeg/png/webp in that folder, sorts by filename, and writes
01.webp .. NN.webp at 1500px wide, quality 82. Originals are moved to
assets/work/shots/_originals/ rather than deleted.
"""
import os, shutil, sys
from PIL import Image

SRC = os.path.join("assets", "work", "shots")
KEEP = os.path.join(SRC, "_originals")
WIDTH = 1500
QUALITY = 82
EXT = (".jpg", ".jpeg", ".png", ".webp")

if not os.path.isdir(SRC):
    sys.exit("missing folder: " + SRC)

# anything that isn't already a numbered frame is treated as fresh input
incoming = sorted(
    f for f in os.listdir(SRC)
    if f.lower().endswith(EXT)
    and os.path.isfile(os.path.join(SRC, f))
    and not (len(f) == 7 and f[:2].isdigit() and f.endswith(".webp"))
)

if not incoming:
    sys.exit("no new images in " + SRC + " — drop the shots there first")

os.makedirs(KEEP, exist_ok=True)
for old in os.listdir(SRC):
    if len(old) == 7 and old[:2].isdigit() and old.endswith(".webp"):
        os.remove(os.path.join(SRC, old))

before = after = 0
for i, name in enumerate(incoming, start=1):
    path = os.path.join(SRC, name)
    before += os.path.getsize(path)
    im = Image.open(path).convert("RGB")
    w, h = im.size
    if w > WIDTH:
        im = im.resize((WIDTH, round(h * WIDTH / w)), Image.LANCZOS)
    out = os.path.join(SRC, f"{i:02d}.webp")
    im.save(out, "WEBP", quality=QUALITY, method=6)
    after += os.path.getsize(out)
    print(f"{i:02d}.webp  <-  {name}   {w}x{h}  {os.path.getsize(path)/1e6:.2f}MB -> {os.path.getsize(out)/1024:.0f}KB")
    shutil.move(path, os.path.join(KEEP, name))

print(f"\n{len(incoming)} frames.  {before/1e6:.1f}MB -> {after/1e6:.2f}MB")
print("originals moved to " + KEEP)

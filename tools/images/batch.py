import json, sys, time, io, os
from PIL import Image, ImageOps
from fetch import dl
R = {}
for f in ("r1.json", "r2.json", "r3.json"):
    if os.path.exists(f): R.update(json.load(open(f)))
picks = json.load(open(sys.argv[1]))  # {key: [rkey, idx, crop_y(0..1)]}
meta = json.load(open("meta.json")) if os.path.exists("meta.json") else {}
for key, (rk, idx, cy) in picks.items():
    if os.path.exists(f"out/{key}.jpg"): continue
    c = R[rk][idx]
    raw = dl(c["thumb"]); im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
    W, H = im.size; r = W / H
    if r > 2.0:   # panoramique → 2:1 centré
        nw = int(H * 2); x = (W - nw) // 2; im = im.crop((x, 0, x + nw, H)); crop = True
    elif r < 1.3:  # vertical/carré → 3:2, position verticale cy
        nh = int(W / 1.5); y = int((H - nh) * cy); im = im.crop((0, y, W, y + nh)); crop = True
    else: crop = False
    if im.width > 1400: im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    im.save(f"out/{key}.jpg", "JPEG", quality=80, optimize=True, progressive=True)
    meta[key] = {**c, "out_w": im.width, "out_h": im.height, "cropped": crop}
    json.dump(meta, open("meta.json", "w"), ensure_ascii=False, indent=1)
    print(key, im.size, os.path.getsize(f"out/{key}.jpg") // 1024, "Ko", c["lic"], "|", c["artist"][:60], flush=True)
    time.sleep(4)

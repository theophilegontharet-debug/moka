import json, sys, time, urllib.request, io
from PIL import Image, ImageOps
UA = "MokaReader/0.1 (private personal news reader; low volume)"
def dl(url):
    url = url.replace("https://thumb.wikimedia.org/", "https://upload.wikimedia.org/")
    for i in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except Exception as e:
            ra = getattr(e, "headers", None) and e.headers.get("retry-after")
            w = int(ra) + 3 if ra and ra.isdigit() else 20
            print("  attente", w, e, flush=True); time.sleep(w)
    raise SystemExit("échec " + url)
def optimize(raw, out, width=1400, ratio=None):
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
    if im.width > width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(out, "JPEG", quality=80, optimize=True, progressive=True)
    return im.size
if __name__ == "__main__":
    key, url, out = sys.argv[1:4]
    raw = dl(url); size = optimize(raw, out)
    import os; print(key, size, os.path.getsize(out)//1024, "Ko")

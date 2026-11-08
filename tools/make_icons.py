"""Génère icons/ à partir de app/brand/symbol.svg (Chrome headless via Playwright).
Icône pleine (sans transparence ni coins arrondis : iOS et Android arrondissent eux-mêmes)."""
import pathlib, shutil
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).resolve().parent.parent
sym = (root / "app/brand/symbol.svg").read_text()
out = root / "icons"; out.mkdir(exist_ok=True)
shutil.copy(root / "app/brand/app-icon.svg", out / "favicon.svg")
def page(size, ratio):
    w = int(size * ratio)
    return f"""<html><body style="margin:0;width:{size}px;height:{size}px;background:#FDF9F4;display:flex;align-items:center;justify-content:center">
<div style="width:{w}px;height:{int(w*112/128)}px;transform:translate({int(size*0.02)}px,{int(size*0.01)}px)">{sym.replace('<svg ', '<svg width="100%" height="100%" ',1)}</div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for name, size, ratio in [("apple-touch-icon", 180, .70), ("icon-192", 192, .70), ("icon-512", 512, .70), ("icon-maskable-512", 512, .56)]:
        pg = b.new_page(viewport={"width": size, "height": size})
        pg.set_content(page(size, ratio)); pg.wait_for_timeout(200)
        pg.screenshot(path=str(out / f"{name}.png"), omit_background=False); pg.close()
    b.close()
print("icônes écrites")

import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        errs=[]
        for name,w,h,hash in [("m_home",390,844,""),("d_home",1280,900,""),("m_art",390,844,"#a-afrique-bilan-2026"),("m_art2",390,844,"#a-exits-afrique-octobre"),("d_art",1280,900,"#a-europe-levees-semaine"),("m_cats",390,844,"#rubriques"),("m_sources",390,844,"#sources")]:
            pg = await b.new_page(viewport={"width":w,"height":h}, device_scale_factor=2 if w<500 else 1)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto("file:///home/claude/moka/test/preview.html"+hash)
            await pg.wait_for_timeout(1500)
            await pg.screenshot(path=f"{name}.png", full_page=True)
            await pg.screenshot(path=f"{name}_fold.png")
        print("errors:", errs)
        await b.close()
asyncio.run(main())

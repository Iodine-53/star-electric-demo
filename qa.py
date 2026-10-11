#!/usr/bin/env python3
"""QA pass for the Star Electric demo: overflow, images, anchors, console,
interactions, fonts, tap targets, contrast, JS-off facts, no-interaction test
+ stitched full-page screenshots (also staged for the critique step)."""
import io, subprocess, sys, time, urllib.request
from PIL import Image
from playwright.sync_api import sync_playwright

DEMO = "/home/hatch/workspace/tampa-leads/demos/star-electric"
CRIT = "/home/hatch/workspace/goals/tampa-demo-first-cold-pitch/hidden_files/critique-2026-10-10"
CHROME = "/home/hatch/workspace/.tools/chrome-linux64/chrome"
URL = "http://127.0.0.1:8902/index.html"
fails = []

def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ((" — " + detail) if detail and not cond else ""))
    if not cond:
        fails.append(name + (": " + detail if detail else ""))

def lum(hex):
    h = hex.lstrip('#'); c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    c = [x/12.92 if x <= 0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]

def ratio(a, b):
    la, lb = lum(a), lum(b); hi, lo = max(la, lb), min(la, lb)
    return (hi+0.05)/(lo+0.05)

# ---- static contrast (design tokens) ----
check("contrast: white on copper >= 4.5", ratio("#ffffff", "#a86424") >= 4.5, f"{ratio('#ffffff','#a86424'):.2f}")
check("contrast: copper-dk on paper >= 4.5", ratio("#8a511c", "#f7f3ea") >= 4.5, f"{ratio('#8a511c','#f7f3ea'):.2f}")
check("contrast: ink on paper >= 7", ratio("#10293f", "#f7f3ea") >= 7, f"{ratio('#10293f','#f7f3ea'):.2f}")
check("contrast: paper on ink >= 7", ratio("#f7f3ea", "#10293f") >= 7, f"{ratio('#f7f3ea','#10293f'):.2f}")

subprocess.run(["mkdir", "-p", CRIT], check=False)
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8902", "--directory", DEMO],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

# ---- JS-off: key facts in server HTML ----
raw = urllib.request.urlopen(URL, timeout=10).read().decode()
for fact in ["(727) 492-6248", "jerry@starelectricservices.com", "from $1,800", "$1,800–$2,400",
             "Panel upgrade", "EV charger", "Clearwater", "Dunedin", "Safety Harbor", "Largo",
             "Palm Harbor", "Tampa", "FAQPage"]:
    check(f"js-off: '{fact[:28]}' in HTML", fact in raw)

def stitched_shot(page, path, vw, vh):
    page.set_viewport_size({"width": vw, "height": vh})
    page.add_style_tag(content="header.tblock{position:static!important}.mbar{display:none!important}.sym-fig,.techcard{position:static!important}")
    time.sleep(0.4)
    total = page.evaluate("document.documentElement.scrollHeight")
    step = vh - 60
    maxy = max(total - vh, 0)
    ys, y = [], 0
    while y < maxy:
        ys.append(y); y += step
    ys.append(maxy)
    shots = []
    for y in ys:
        page.evaluate(f"window.scrollTo({{top:{y},behavior:'instant'}})")
        time.sleep(0.85)
        shots.append((y, Image.open(io.BytesIO(page.screenshot()))))
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    full = Image.new("RGB", (shots[0][1].width, total))
    for (sy, s) in shots:
        full.paste(s, (0, sy))
    full.save(path)
    print("saved", path, full.size)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
    errors = []
    for vw, vh, label, shot in [(1440, 900, "desktop", f"{CRIT}/star-electric-desktop.png"),
                                (390, 844, "mobile", f"{CRIT}/star-electric-mobile.png")]:
        page = browser.new_page(viewport={"width": vw, "height": vh})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.goto(URL, wait_until="networkidle")
        # no-interaction test: 3s untouched, hero must be readable
        page.wait_for_timeout(3000)
        check(f"{label}: no-interaction hero readable",
              page.evaluate("document.querySelector('.hero h1').classList.contains('in')") and
              page.evaluate("getComputedStyle(document.querySelector('.hero-ctas .btn')).opacity") == "1")
        check(f"{label}: no horizontal overflow",
              page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"),
              f"scrollWidth={page.evaluate('document.documentElement.scrollWidth')}")
        page.evaluate("""(async () => {
            const h = document.documentElement.scrollHeight;
            for (let y = 0; y < h; y += 350) { window.scrollTo({top: y, behavior: 'instant'}); await new Promise(r => setTimeout(r, 260)); }
            window.scrollTo(0, 0);
        })()""")
        page.wait_for_timeout(800)
        # let every lazy image finish (they were all scrolled near above)
        try:
            page.wait_for_function("![...document.images].some(i=>!i.complete)", timeout=15000)
        except Exception as e:
            print("image wait timeout:", e)
        imgs = page.evaluate("""[...document.images].map(i => ({s:i.currentSrc.split('/').pop(), ok:i.complete && i.naturalWidth>0}))""")
        bad = [i["s"] for i in imgs if not i["ok"]]
        check(f"{label}: all {len(imgs)} images load", not bad, str(bad))
        anchors = page.evaluate("""[...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href'))""")
        missing = [a for a in set(anchors) if a != "#" and not page.evaluate(f"!!document.querySelector('{a}')")]
        check(f"{label}: anchors resolve ({len(set(anchors))})", not missing, str(missing))
        check(f"{label}: Bebas Neue loaded", page.evaluate("document.fonts.check('16px \"Bebas Neue\"')"))
        check(f"{label}: JetBrains Mono loaded", page.evaluate("document.fonts.check('500 12px \"JetBrains Mono\"')"))

        stitched_shot(page, shot, vw, vh)

        # interactions (after screenshots)
        if label == "desktop":
            page.click(".lc-chips .chip[data-amps] >> nth=0")
            page.click(".lc-chips .chip[data-amps] >> nth=1")
            page.wait_for_timeout(400)
            check("desktop: load check verdict appears",
                  page.evaluate("!document.querySelector('#lcVerdict').hidden"))
            page.click(".faq-q >> nth=0"); page.wait_for_timeout(400)
            check("desktop: FAQ opens", page.evaluate("document.querySelector('.faq-item').classList.contains('open')"))
            # stepper: empty next blocked, then walk all 4 steps
            page.click("#stepNext"); page.wait_for_timeout(200)
            check("desktop: stepper blocks empty service", page.evaluate("!document.querySelector('#stepErr').hidden"))
            page.select_option("#sService", index=1); page.click("#stepNext"); page.wait_for_timeout(200)
            page.fill("#sZip", "33755"); page.click("#stepNext"); page.wait_for_timeout(200)
            page.click(".pick >> nth=1"); page.click("#stepNext"); page.wait_for_timeout(200)
            page.click(".step[data-step='4'] .pick >> nth=0"); page.click("#stepNext"); page.wait_for_timeout(300)
            check("desktop: stepper reaches done + mailto",
                  page.evaluate("document.querySelector('.step[data-step=\"5\"]').classList.contains('on')") and
                  page.evaluate("document.querySelector('#mailtoBtn').href").startswith("mailto:"))
        else:
            page.click("#burger"); page.wait_for_timeout(300)
            check("mobile: hamburger opens", page.evaluate("document.getElementById('mnav').classList.contains('open')"))
            page.click("#burger")
            small = page.evaluate("""[...document.querySelectorAll('a,button')].filter(el=>{
                if(el.closest('footer')) return false;
                const r=el.getBoundingClientRect(); const vis=r.width>0&&r.height>0&&getComputedStyle(el).visibility!=='hidden';
                return vis && (r.width<44||r.height<44);}).map(el=>el.textContent.trim().slice(0,24))""")
            check("mobile: tap targets >=44px (non-footer)", not small, str(small[:6]))
            page.evaluate("window.scrollTo(0, document.querySelector('.hero').offsetHeight + 200)"); page.wait_for_timeout(600)
            check("mobile: sticky bar shows after hero",
                  page.evaluate("document.getElementById('mbar').classList.contains('show')"))
            page.evaluate("document.querySelector('#book').scrollIntoView({behavior:'instant'})"); page.wait_for_timeout(600)
            check("mobile: sticky bar hides at final CTA",
                  page.evaluate("!document.getElementById('mbar').classList.contains('show')"))
            check("mobile: mbar call link is tel:",
                  page.evaluate("document.querySelector('#mbar .mbar-call').getAttribute('href')").startswith("tel:"))
        page.close()

    check("zero console/page errors", not errors, str(errors[:4]))

    # og-image: 1200x630 crop of the hero
    og = browser.new_page(viewport={"width": 1200, "height": 630})
    og.goto(URL, wait_until="networkidle"); og.wait_for_timeout(2500)
    og.screenshot(path=f"{DEMO}/og-image.jpg")
    im = Image.open(f"{DEMO}/og-image.jpg")
    check("og-image.jpg is 1200x630", im.size == (1200, 630), str(im.size))
    print("saved", f"{DEMO}/og-image.jpg", im.size)
    browser.close()

srv.terminate()
print("\n" + ("ALL QA PASSED" if not fails else f"{len(fails)} FAILURES: {fails}"))
sys.exit(1 if fails else 0)

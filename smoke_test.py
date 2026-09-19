#!/usr/bin/env python3
"""Smoke test for the Highlight Solutions static site.
Python stdlib only. Validates essential files and bilingual/RTL/navigation markers.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

failures = []
checks = 0


def check(name, condition, detail=""):
    global checks
    checks += 1
    if condition:
        print(f"PASS: {name}")
    else:
        failures.append(name)
        print(f"FAIL: {name} {detail}")


def read(filename):
    with open(os.path.join(ROOT, filename), encoding="utf-8") as f:
        return f.read()


# --- Essential files ---
for fname in ["index.html", "styles.css", "script.js", "README.md"]:
    check(f"essential file exists: {fname}", os.path.isfile(os.path.join(ROOT, fname)))

html = read("index.html")
css = read("styles.css")
js = read("script.js")
readme = read("README.md")

# --- Verified company facts ---
check("company name (EN) present", "Highlight Solutions" in html)
check("company name (AR) present", "هاي لايت سوليوشنز" in html)
check("CR national number 7054354365 present", "7054354365" in html)
check("status Active stated (EN or AR)", ("Active" in html) or ("قائمة" in html) or ("نشطة" in html))
check("Riyadh location stated", ("Riyadh" in html) or ("الرياض" in html))
check("domain highlight-solutions.com referenced", "highlight-solutions.com" in html or "highlight-solutions.com" in readme)

# --- Bilingual / RTL ---
check("html lang attribute exists", re.search(r"<html[^>]*\slang=", html) is not None)
check("dir attribute on html tag", re.search(r"<html[^>]*\sdir=", html) is not None)
check("lang=ar markers present", 'lang="ar"' in html)
check("lang=en markers present", 'lang="en"' in html)
check("dir=rtl markers present", 'dir="rtl"' in html)
check("dir=ltr markers present", 'dir="ltr"' in html)
check("language toggle control in HTML", re.search(r'(data-lang-toggle|lang-toggle|language-toggle|id="lang)', html) is not None)
check("toggle logic in script.js", "lang" in js.lower())
check("RTL styles in CSS", "rtl" in css.lower())
check("Arabic web font referenced", re.search(r"(Tajawal|Cairo|IBM[ -]Plex[ -]Arabic|Noto[ -]Kufi|Rubik)", css + html) is not None)

# --- GitHub Pages custom domain ---
check("CNAME file exists", os.path.isfile(os.path.join(ROOT, "CNAME")))
if os.path.isfile(os.path.join(ROOT, "CNAME")):
    with open(os.path.join(ROOT, "CNAME"), encoding="utf-8") as f:
        check("CNAME content is highlight-solutions.com + newline",
              f.read() == "highlight-solutions.com\n")

# --- Navigation / sections ---
for section_id in ["hero", "about", "how-we-work", "company-info", "location", "contact", "footer"]:
    check(f"section present with id: {section_id}", f'id="{section_id}"' in html)

check("nav element present", "<nav" in html)
check("nav has links to sections", re.search(r"<a[^>]+href=\"#[a-z-]+\"", html) is not None)
check("skip-to-content link", "skip" in html.lower())
# --- Placeholders clearly labeled ---
check("contact placeholder labeled", "Add verified contact details" in html or "أضف بيانات التواصل" in html)

# --- Verified business email in contact section ---
check("contact email exact address", 'Info@highlight-solutions.com' in html)
check("contact email mailto link", re.search(r'<a\s+href="mailto:Info@highlight-solutions\.com"[^>]*>\s*Info@highlight-solutions\.com\s*</a>', html) is not None)

# --- Location link to Google Maps ---
check("Google Maps link present", "google.com/maps" in html or "maps.google" in html or "maps.app.goo.gl" in html)

# --- Fix 1: usable without JavaScript (real Arabic fallback text) ---
hero_h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
check("hero h1 has non-empty fallback text",
      hero_h1 is not None and re.sub(r"\s+", " ", hero_h1.group(1)).strip() != "")
nav_link_re = re.compile(r"<li><a href=\"#[a-z-]+\" data-ar=\"[^\"]+\" data-en=\"[^\"]+\">(.*?)</a></li>")
nav_links = nav_link_re.findall(html)
check("all 6 nav links have fallback text", len(nav_links) == 6 and all(t.strip() for t in nav_links),
      f"found {len(nav_links)} links with text")

# --- Fix 1b: brand name + hero CTAs have Arabic no-JS fallback text ---
brand = re.search(r'<span class="brand-name"[^>]*>(.*?)</span>', html, re.S)
check("header brand has non-empty Arabic fallback text",
      brand is not None and brand.group(1).strip() != "",
      f"got: {brand.group(1).strip() if brand else 'no span'}")
cta_primary = re.search(r'<a class="btn btn-primary" href="#contact"[^>]*>(.*?)</a>', html, re.S)
check("hero primary CTA (Contact Us) has non-empty Arabic fallback text",
      cta_primary is not None and cta_primary.group(1).strip() != "",
      f"got: {cta_primary.group(1).strip() if cta_primary else 'no anchor'}")
cta_secondary = re.search(r'<a class="btn btn-secondary" href="#about"[^>]*>(.*?)</a>', html, re.S)
check("hero secondary CTA (Learn About Us) has non-empty Arabic fallback text",
      cta_secondary is not None and cta_secondary.group(1).strip() != "",
      f"got: {cta_secondary.group(1).strip() if cta_secondary else 'no anchor'}")

# --- Fix 2: Trade Name English value ---
trade_dd = re.search(r'data-en="Trade Name".*?<dd[^>]*>(.*?)</dd>', html, re.S)
check("Trade Name dd has correct EN value",
      trade_dd is not None and trade_dd.group(1).strip() == "Highlight Solutions Company",
      f"got: {trade_dd.group(1).strip() if trade_dd else 'no dd'}")

# --- Fix 3: location CTA uses supplied short URL, labeled Explore Riyadh ---
check("location CTA uses supplied Maps short URL",
      'href="https://maps.app.goo.gl/WcrPdAYNWVUyUnt3A?g_st=aw"' in html)
check("location CTA labeled Explore Riyadh / استكشف الرياض",
      'data-en="Explore Riyadh"' in html and 'data-ar="استكشف الرياض"' in html)
check("location CTA does not claim company pin",
      "Open Location on Google Maps" not in html and "افتح الموقع على Google Maps" not in html)

# --- Fix 4: bilingual skip-link + mobile menu aria-label with data attributes ---
skip = re.search(r"<a class=\"skip-link\"[^>]*>(.*?)</a>", html)
check("skip-link has bilingual data attrs and fallback text",
      skip is not None and 'data-en="Skip to main content"' in skip.group(0)
      and 'data-ar="' in skip.group(0) and skip.group(1).strip() != "")
check("mobile menu button has data-ar-label/data-en-label",
      'data-ar-label="' in html and 'data-en-label="' in html
      and re.search(r'id="nav-toggle"[^>]*data-(ar|en)-label', html) is not None)
check("script switches nav aria-label on language change", "navToggle.setAttribute(\"aria-label\"" in js)

# --- Logo visibility ---
check("logo asset exists", os.path.isfile(os.path.join(ROOT, "assets", "highlight-solutions-logo-transparent.png")))
check("header brand-logo reference in HTML", 'class="brand-logo"' in html and "highlight-solutions-logo-transparent.png" in html)
check("hero-logo reference in HTML", 'class="hero-logo"' in html)
# --- Logo transparency: no opaque/light backing plate styling on logos ---
def logo_rule(css_text, selector):
    m = re.search(selector_to_pattern(selector), css_text, re.S)
    return m.group(1) if m else ""

def selector_to_pattern(sel):
    return re.escape(sel) + r"\s*\{([^{}]*)\}"

brand_rule = logo_rule(css, ".brand-logo")
brand_img_rule = logo_rule(css, ".brand-logo img")
hero_rule = logo_rule(css, ".hero-logo")

FORBIDDEN = re.compile(r"^\s*(background|background-color|box-shadow|padding)\s*:", re.M | re.I)

for label, rule in [("brand-logo", brand_rule + brand_img_rule), ("hero-logo", hero_rule)]:
    check(f"{label} rule exists in CSS", bool(rule.strip()))
    check(f"{label} has no background/background-color/box-shadow/padding declarations",
          not FORBIDDEN.search(rule),
          f"forbidden declarations found: {sorted(set(m.group(1).lower() for m in FORBIDDEN.finditer(rule)))}")
check("brand-logo keeps its transparent img sizing rule", "object-fit: contain" in brand_img_rule)
check("hero-logo keeps its layout size (112px)", "112px" in hero_rule)
check("hero-category styled in CSS", ".hero-category" in css)
check("contracting marker (AR) present", "مقاولات" in html)
check("contracting marker (EN) present", "Contracting" in html)

# --- Accessibility ---
check("aria-label usage", "aria-label" in html)
check("meta viewport for responsiveness", 'name="viewport"' in html)
check("semantic landmarks (header/main/footer)", all(t in html for t in ["<header", "<main", "<footer"]))
check("no third-party analytics (ga/gtm)", not re.search(r"(google-analytics|googletagmanager|gtag\()", html + js))
check("charset utf-8 declared", 'charset="utf-8"' in html.lower() or "charset=utf-8" in html.lower())

print()
print(f"Total checks: {checks}, failures: {len(failures)}")
if failures:
    print("FAILED checks:", failures)
    sys.exit(1)
print("ALL CHECKS PASSED")

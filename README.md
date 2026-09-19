# Highlight Solutions Company — شركة هاي لايت سوليوشنز

Static, responsive, bilingual (Arabic RTL default + English) one-page website.
Intended domain: highlight-solutions.com (not deployed; no DNS changes made).

## Files
- index.html — single page, semantic/accessible markup
- styles.css — deep navy / teal premium theme, RTL-aware, mobile-first
- script.js — language toggle (persisted), mobile nav, footer year
- smoke_test.py — Python-stdlib smoke test
- README.md — this file

## Verified facts used (only)
- Trade name: highlight solutions Company / شركة هاي لايت سوليوشنز
- Saudi CR national number: 7054354365
- Status: Active
- Location: Riyadh, Saudi Arabia (Google Maps)

## Contact
The contact section links to the official verified email:
Info@highlight-solutions.com. Phone, social links, and specific services remain absent
until verified — they must be added only after verification.

## Custom domain
Deployment preparation exists for the custom domain highlight-solutions.com (CNAME file
for GitHub Pages is present in the repo). No DNS changes have been made and the site has
not been deployed or publicly verified — no HTTPS/live-URL claims yet.

## Run locally
    cd highlight-solutions-website
    python3 -m http.server 8000
    open http://localhost:8000

## Run smoke test
    python3 smoke_test.py

No build system, no dependencies, no analytics, no secrets.

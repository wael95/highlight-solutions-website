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

## Intentional placeholders
Contact section contains clearly labeled placeholders ("Add verified contact details").
Phone, email, logo, social links, and specific services are NOT invented — they must be
added only after verification.

## Run locally
    cd highlight-solutions-website
    python3 -m http.server 8000
    open http://localhost:8000

## Run smoke test
    python3 smoke_test.py

No build system, no dependencies, no analytics, no secrets.

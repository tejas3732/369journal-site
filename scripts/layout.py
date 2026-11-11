#!/usr/bin/env python3
"""Shared header, footer and download bar for every page.

Run after editing any page:  python3 scripts/layout.py
It rewrites the <header class="site-header">, <footer class="site-footer">
and sticky download bar on every HTML file, and turns any old App Store
button into the official badge (keeping its campaign tag).
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = "https://apps.apple.com/app/apple-store/id6770804298?pt=128923117&amp;ct={ct}&amp;mt=8"

GUIDES = [
    ("/369-method/", "How to do the 369 method", "Step by step, with 21, 33 or 45 days"),
    ("/369-method/examples/", "50 369 method examples", "Affirmations to copy for every area of life"),
    ("/369-method/money/", "369 method for money", "Wording, 15 money affirmations, daily action"),
    ("/369-method/love/", "369 method for love", "Self-love, a relationship or a specific person"),
    ("/369-method/vs-55x5/", "369 vs 55x5 method", "Which manifestation ritual suits you"),
    ("/369-method/tracker/", "Free 33-day tracker", "Printable sheet for paper journaling"),
    ("/best-369-method-apps/", "Best 369 method apps", "An honest comparison for iPhone"),
]

CHEVRON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg>'


def badge(ct, size="", cta=None):
    cls = f"store-badge {size}".strip()
    return (f'<a class="{cls}" href="{APP.format(ct=ct)}" data-cta="{cta or ct}" '
            f'aria-label="Download 369 Journal on the App Store">'
            f'<img src="/assets/img/app-store-badge.svg" alt="Download on the App Store" width="162" height="54"></a>')


def header(current):
    def link(href, text):
        cur = ' aria-current="page"' if href == current else ""
        return f'<a href="{href}"{cur}>{text}</a>'
    items = "\n".join(
        f'            <a href="{h}"><strong>{t}</strong><span>{d}</span></a>' for h, t, d in GUIDES
    )
    return f"""<header class="site-header">
    <div class="wrap">
      <a class="brand" href="/"><img src="/assets/img/favicon-48.png" alt="" width="34" height="34">369 Journal</a>
      <nav class="nav" aria-label="Main">
        {link("/369-method/", "The 369 method")}
        <details>
          <summary>Guides {CHEVRON}</summary>
          <div class="menu">
{items}
            <a class="all" href="/guides/">All guides &rarr;</a>
          </div>
        </details>
        {link("/369-method/tracker/", "Free tracker")}
        {link("/faq/", "FAQ")}
      </nav>
      <a class="mobile-guides" href="/guides/">Guides</a>
      <div class="header-cta">{badge("site-header", "small", "header")}</div>
    </div>
  </header>"""


def footer():
    guides = "\n".join(f'          <li><a href="{h}">{t}</a></li>' for h, t, _ in GUIDES[:5])
    return f"""<footer class="site-footer">
    <div class="wrap">
      <div class="foot-brand">
        <a class="brand" href="/"><img src="/assets/img/favicon-48.png" alt="" width="34" height="34">369 Journal</a>
        <p>A calm, private journal for the 369 manifestation method, on iPhone and iPad.</p>
        {badge("site-footer", "medium", "footer")}
      </div>
      <nav aria-label="Guides">
        <h2>Guides</h2>
        <ul>
{guides}
          <li><a href="/guides/">All guides</a></li>
        </ul>
      </nav>
      <nav aria-label="Free tools">
        <h2>Free tools</h2>
        <ul>
          <li><a href="/369-method/tracker/">33-day tracker</a></li>
          <li><a href="/best-369-method-apps/">Best 369 apps</a></li>
          <li><a href="/faq/">FAQ</a></li>
        </ul>
      </nav>
      <nav aria-label="About">
        <h2>369 Journal</h2>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="https://tejas3732.github.io/369-journal-legal/support.html">Support</a></li>
          <li><a href="https://tejas3732.github.io/369-journal-legal/privacy.html">Privacy</a></li>
        </ul>
      </nav>
      <p class="copyright">&copy; 2026 369 Journal. Apple, the Apple logo and App Store are trademarks of Apple Inc.</p>
    </div>
  </footer>
  <div class="sticky-get" data-sticky>
    <img class="icon" src="/assets/img/apple-touch-icon.png" alt="" width="40" height="40">
    <div><strong>369 Journal</strong><span>Free on iPhone &middot; 7-day Pro trial</span></div>
    {badge("site-sticky", "", "sticky")}
  </div><!-- /sticky -->"""


OLD_BTN = re.compile(
    r'<a class="btn clay" href="https://apps\.apple\.com/app/apple-store/id6770804298\?pt=128923117&amp;ct=([\w-]+)&amp;mt=8" data-cta="([\w-]+)">.*?</a>',
    re.S,
)


def page_path(file):
    rel = file.relative_to(ROOT).as_posix()
    return "/" if rel == "index.html" else "/" + rel.replace("index.html", "")


def apply(file):
    s = file.read_text()
    if "site-header" not in s and "site-footer" not in s:
        return False
    cur = page_path(file)
    s = re.sub(r"<header class=\"site-header\">.*?</header>", header(cur), s, flags=re.S)
    s = re.sub(r"<footer class=\"site-footer\">.*?</footer>(\s*<div class=\"sticky-get\".*?<!-- /sticky -->)?", footer(), s, flags=re.S)
    s = OLD_BTN.sub(lambda m: badge(m.group(1), "", m.group(2)), s)
    s = s.replace('<img src="/assets/img/app-icon-512.png" alt="369 Journal app icon" width="64" height="64">',
                  '<img class="icon" src="/assets/img/app-icon-512.png" alt="369 Journal app icon" width="64" height="64">')
    if '<script src="/assets/site.js" defer></script>' not in s:
        s = s.replace('<script src="/assets/analytics.js" defer></script>',
                      '<script src="/assets/analytics.js" defer></script>\n  <script src="/assets/site.js" defer></script>')
    file.write_text(s)
    return True


def main():
    for f in sorted(ROOT.rglob("*.html")):
        if ".git" in f.parts or f.name == "404.html":
            continue
        if apply(f):
            print("layout ->", f.relative_to(ROOT))


if __name__ == "__main__":
    main()

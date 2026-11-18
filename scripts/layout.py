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
    ("/scripting-manifestation/", "Scripting manifestation", "How to script a desire, with examples"),
    ("/new-year-manifestation-challenge/", "21-day New Year challenge", "A free 369 plan for 2027"),
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
        {link("/tools/", "Free tools")}
        {link("/books/", "Books")}
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
          <li><a href="/tools/">All free tools</a></li>
          <li><a href="/word-of-the-year/">Word of the Year</a></li>
          <li><a href="/vision-board-maker/">Vision board maker</a></li>
          <li><a href="/affirmation-generator/">Affirmation generator</a></li>
          <li><a href="/affirmation-wallpaper/">Affirmation wallpaper</a></li>
          <li><a href="/letter-to-future-self/">Letter to your future self</a></li>
          <li><a href="/journal-prompt-generator/">Journal prompts</a></li>
          <li><a href="/gratitude-journal-prompts/">Gratitude prompts</a></li>
          <li><a href="/angel-number-calculator/">Angel numbers</a></li>
          <li><a href="/numerology-calculator/">Numerology calculator</a></li>
          <li><a href="/369-method/tracker/">33-day tracker</a></li>
          <li><a href="/best-369-method-apps/">Best 369 apps</a></li>
          <li><a href="/faq/">FAQ</a></li>
        </ul>
      </nav>
      <nav aria-label="About">
        <h2>369 Journal</h2>
        <ul>
          <li><a href="/books/">Books</a></li>
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
        s = re.sub(r'(<script src="/assets/analytics\.js(?:\?v=[\w-]+)?" defer></script>)',
                   r'\1\n  <script src="/assets/site.js" defer></script>', s, count=1)
    if 'name="apple-itunes-app"' not in s:
        s = s.replace('<meta name="theme-color" content="#faf6f0">',
                      '<meta name="theme-color" content="#faf6f0">\n  <meta name="apple-itunes-app" content="app-id=6770804298">', 1)
    if GTAG_ID not in s:
        s = s.replace("<head>", "<head>\n" + GTAG, 1)
    s = apply_related(s, cur)
    file.write_text(s)
    return True


# Google tag (Google Tag Manager container), right after <head> on every page.
GTAG_ID = "GTM-TMJRPR3Z"
GTAG = f"""  <!-- Google tag -->
  <script async src="https://www.googletagmanager.com/gtm.js?id={GTAG_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
  </script>"""


def main():
    for f in sorted(ROOT.rglob("*.html")):
        if ".git" in f.parts or f.name == "404.html":
            continue
        if apply(f):
            print("layout ->", f.relative_to(ROOT))


# ---------------------------------------------------------------------------
# "Keep reading": 3-4 hand-picked related pages at the end of every page body.
# Edit RELATED to change them; layout.py replaces the block on every run.
PAGES = {
    "/369-method/": ("The 369 method, step by step", "How to do it, and 21 vs 33 vs 45 days"),
    "/369-method/examples/": ("50 369 method examples", "Affirmations to copy for money, love and more"),
    "/369-method/money/": ("369 method for money", "How to word a money affirmation"),
    "/369-method/love/": ("369 method for love", "Self-love, a partner or a specific person"),
    "/369-method/vs-55x5/": ("369 vs 55x5 method", "Which manifestation ritual suits you"),
    "/369-method/tesla/": ("Did Tesla create the 369 method?", "What the record actually shows"),
    "/369-method/tracker/": ("Free printable 369 tracker", "Tick off 33 days on paper"),
    "/369-meaning/": ("What does 369 mean?", "3, 6 and 9, angel numbers and the method"),
    "/369-manifestation-journal/": ("How to keep a 369 journal", "What to write, page layout, paper or app"),
    "/scripting-manifestation/": ("Scripting manifestation", "How to script a desire, with examples"),
    "/new-year-manifestation-challenge/": ("21-day New Year challenge", "A free 369 plan for 2027"),
    "/best-369-method-apps/": ("Best 369 method apps", "Six iPhone apps, honestly compared"),
    "/faq/": ("369 method FAQ", "Missed days, timing and what to write"),
    "/guides/": ("All 369 method guides", "Every guide in one place"),
    "/tools/": ("All free tools", "Vision board, wallpapers, prompts and more"),
    "/books/": ("The 369 Method and Scripting books", "Guided workbooks in paperback and on Kindle"),
    "/vision-board-maker/": ("Free vision board maker", "A phone wallpaper, desktop or print"),
    "/affirmation-wallpaper/": ("Affirmation wallpaper maker", "Put your affirmation on your lock screen"),
    "/affirmation-generator/": ("Affirmation generator", "Words for your desire, plus a 369 sheet"),
    "/letter-to-future-self/": ("Letter to your future self", "Write it now, reopen it next year"),
    "/journal-prompt-generator/": ("Journal prompt generator", "Manifestation and scripting prompts"),
    "/angel-number-calculator/": ("Angel number meanings", "Look up a number you keep seeing"),
    "/word-of-the-year/": ("Find your Word of the Year", "Five questions, one word for 2027"),
    "/numerology-calculator/": ("Numerology calculator", "Life path, name and 2027 personal year"),
    "/gratitude-journal-prompts/": ("Gratitude journal prompts", "108 prompts and a printable journal"),
}
RELATED = {
    "/369-method/": ["/369-method/examples/", "/affirmation-wallpaper/", "/369-manifestation-journal/", "/faq/"],
    "/369-method/examples/": ["/affirmation-generator/", "/affirmation-wallpaper/", "/scripting-manifestation/", "/journal-prompt-generator/"],
    "/369-method/money/": ["/vision-board-maker/", "/affirmation-wallpaper/", "/scripting-manifestation/", "/369-meaning/"],
    "/369-method/love/": ["/scripting-manifestation/", "/letter-to-future-self/", "/journal-prompt-generator/", "/affirmation-wallpaper/"],
    "/369-method/vs-55x5/": ["/369-method/", "/369-method/tracker/", "/best-369-method-apps/", "/faq/"],
    "/369-method/tesla/": ["/369-meaning/", "/angel-number-calculator/", "/numerology-calculator/", "/369-method/"],
    "/369-method/tracker/": ["/369-method/examples/", "/affirmation-wallpaper/", "/angel-number-calculator/", "/new-year-manifestation-challenge/"],
    "/369-meaning/": ["/angel-number-calculator/", "/numerology-calculator/", "/369-method/tesla/", "/369-method/examples/"],
    "/369-manifestation-journal/": ["/journal-prompt-generator/", "/gratitude-journal-prompts/", "/letter-to-future-self/", "/best-369-method-apps/"],
    "/scripting-manifestation/": ["/letter-to-future-self/", "/journal-prompt-generator/", "/gratitude-journal-prompts/", "/369-manifestation-journal/"],
    "/new-year-manifestation-challenge/": ["/word-of-the-year/", "/vision-board-maker/", "/letter-to-future-self/", "/numerology-calculator/"],
    "/best-369-method-apps/": ["/369-manifestation-journal/", "/369-method/", "/369-method/tracker/", "/faq/"],
    "/faq/": ["/369-method/", "/angel-number-calculator/", "/best-369-method-apps/", "/tools/"],
    "/about/": ["/books/", "/tools/", "/guides/", "/369-method/tesla/"],
    "/books/": ["/369-method/", "/scripting-manifestation/", "/369-manifestation-journal/", "/tools/"],
    "/tools/": ["/369-method/", "/369-meaning/", "/guides/", "/books/"],
    "/vision-board-maker/": ["/word-of-the-year/", "/new-year-manifestation-challenge/", "/369-method/money/"],
    "/affirmation-wallpaper/": ["/word-of-the-year/", "/369-method/examples/", "/angel-number-calculator/"],
    "/affirmation-generator/": ["/369-method/examples/", "/369-method/money/", "/369-method/love/"],
    "/letter-to-future-self/": ["/scripting-manifestation/", "/new-year-manifestation-challenge/", "/369-method/love/"],
    "/journal-prompt-generator/": ["/gratitude-journal-prompts/", "/scripting-manifestation/", "/369-manifestation-journal/"],
    "/angel-number-calculator/": ["/369-meaning/", "/numerology-calculator/", "/369-method/tesla/"],
    "/word-of-the-year/": ["/new-year-manifestation-challenge/", "/369-method/", "/vision-board-maker/"],
    "/numerology-calculator/": ["/angel-number-calculator/", "/369-meaning/", "/word-of-the-year/"],
    "/gratitude-journal-prompts/": ["/scripting-manifestation/", "/369-manifestation-journal/", "/369-method/"],
}
TOOL_PAGES = {"/vision-board-maker/", "/affirmation-wallpaper/", "/affirmation-generator/",
              "/letter-to-future-self/", "/journal-prompt-generator/", "/angel-number-calculator/",
              "/word-of-the-year/", "/numerology-calculator/", "/gratitude-journal-prompts/"}
RELATED_RE = re.compile(r"\s*<!-- related -->.*?<!-- /related -->", re.S)


def related(cur):
    items = RELATED.get(cur)
    if not items:
        return ""
    title = "Guides to go with it" if cur in TOOL_PAGES else "Keep reading"
    cards = "\n".join(
        f'        <a href="{h}"><strong>{PAGES[h][0]}</strong><span>{PAGES[h][1]}</span></a>' for h in items)
    return f"""
    <!-- related -->
    <nav class="related narrow print-hide" aria-label="{title}">
      <h2>{title}</h2>
      <div class="related-grid">
{cards}
      </div>
    </nav>
    <!-- /related -->"""


def apply_related(s, cur):
    s = RELATED_RE.sub("", s)
    block = related(cur)
    if block and "</main>" in s:
        s = s.replace("\n  </main>", block + "\n  </main>", 1)
    return s

if __name__ == "__main__":
    main()

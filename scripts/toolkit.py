"""Shared page shell for the free tools.

Each tool has its own builder (scripts/tool_<name>.py) that calls tool_page() and
its own assets in /assets/tools/<name>.js and .css. Run a builder, then
python3 scripts/layout.py to apply the shared header/footer.
"""
import html

from build_posts import SITE, PUBLISHED, app_plug, book_card, crumbs, footer, head, write  # noqa: F401

ASSET_V = "20261122a"

CHECK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3.5 8.5 3 3 6-7"/></svg>'
LOCK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2"/></svg>'

# Every tool links to the others at the bottom.
TOOLS = [
    ("/vision-board-maker/", "Vision board maker", "Photos and words, as a wallpaper or print"),
    ("/letter-to-future-self/", "Letter to your future self", "Guided prompts, a reminder to reopen it"),
    ("/affirmation-wallpaper/", "Affirmation wallpaper", "Your words on your lock screen"),
    ("/journal-prompt-generator/", "Journal prompt generator", "Manifestation, scripting and more"),
    ("/angel-numbers/", "Angel number meanings", "111 to 1212, one page each"),
    ("/affirmation-generator/", "Affirmation generator", "Plus a printable 369 sheet"),
    ("/word-of-the-year/", "Word of the Year", "Five questions, one word for 2027"),
    ("/life-path-number-calculator/", "Life path calculator", "Your number, meaning and compatibility"),
    ("/personal-year-number-calculator/", "2027 personal year", "Your theme for the year ahead"),
    ("/vision-board-templates/", "Vision board templates", "Six printable layouts and 100 ideas"),
    ("/habit-tracker-printable/", "Printable habit tracker", "Build your own monthly sheet"),
    ("/morning-affirmations/", "Morning affirmations", "Short lines to start the day"),
    ("/self-love-affirmations/", "Self-love affirmations", "Kind words for worth and boundaries"),
    ("/money-affirmations/", "Money affirmations", "Each with one small real action"),
    ("/new-year-resolution-ideas/", "New Year resolution ideas", "100 ideas and a picker for 2027"),
    ("/goal-setting-worksheet/", "Goal setting worksheet", "Fill it in, print one clear page"),
    ("/name-numerology-calculator/", "Name numerology", "Destiny and soul urge, letter by letter"),
    ("/gratitude-journal-prompts/", "Gratitude journal prompts", "108 prompts and a printable journal"),
]


def badges(items):
    return '<ul class="tool-badges">' + "".join(f"<li>{CHECK}{t}</li>" for t in items) + "</ul>"


def privacy(text="Runs in your browser. Nothing you type or upload is sent or saved anywhere."):
    return f'<p class="privacy-note">{LOCK}<span>{text}</span></p>'


def more_tools(current):
    links = "".join(f'<a href="{h}"><strong>{t}</strong><span>{d}</span></a>' for h, t, d in TOOLS if h != current)
    return f'<div class="more-tools">{links}</div>'


def next_steps(title, text, book_id, src, app_title, app_text, ct, book_note=True):
    card = book_card(book_id, src, note=book_note)
    plug = app_plug(app_title, app_text, ct).replace(' style="margin-top:2.5rem"', "")
    return f"""  <section class="tool-next print-hide" aria-labelledby="next-title">
    <h2 id="next-title">{title}</h2>
    <p>{text}</p>
    <div class="tool-next-grid">
{card}
{plug}
    </div>
  </section>"""


def tool_page(p, faq, body, *, js, css=None, extra_ld=None, article="", next_html=""):
    """p: path, crumb, title, h1, description, lede, badges(list). body: the tool's HTML (inside <main>).
    js/css: file names under /assets/tools/. article: SEO guide HTML (inside .prose)."""
    url = f"{SITE}{p['path']}"
    graph = [
        {"@type": "WebApplication", "name": p["h1"], "url": url, "applicationCategory": "LifestyleApplication",
         "operatingSystem": "Any (web browser)", "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "description": p["description"], "datePublished": p.get("published", PUBLISHED),
         "publisher": {"@type": "Organization", "name": "369 Journal", "url": f"{SITE}/"}},
        crumbs(p),
    ]
    if faq:
        graph.insert(1, {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    if extra_ld:
        graph.extend(extra_ld)
    ld = {"@context": "https://schema.org", "@graph": graph}
    assets = f'  <link rel="stylesheet" href="/assets/tools.css?v={ASSET_V}">\n'
    if css:
        assets += f'  <link rel="stylesheet" href="/assets/tools/{css}?v={ASSET_V}">\n'
    assets += f'  <script src="/assets/tools/{js}?v={ASSET_V}" defer></script>\n'
    faq_html = "\n".join(
        f"      <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faq)
    faq_block = f'\n      <h2 id="faq">Questions</h2>\n{faq_html}' if faq else ""
    return head(p, ld).replace("</head>", assets + "</head>") + f"""
  <main data-tool="{p['path'].strip('/')}">
    <div class="tool-head print-hide">
      <div class="wrap">
        <h1>{p['h1']}</h1>
        <p>{p['lede']}</p>
        {badges(p.get('badges', ['Free', 'No sign-up', 'Works on iPhone and desktop']))}
      </div>
    </div>

{body}

{next_html}

    <article class="narrow prose print-hide">
{article}{faq_block}

      <h2>More free tools</h2>
      {more_tools(p['path'])}
    </article>
  </main>

  <div class="t-toast" role="status" aria-live="polite" data-toast></div>

  {footer()}
</body>
</html>
"""

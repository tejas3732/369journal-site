#!/usr/bin/env python3
"""Builds /tools/, the hub for every free tool.  Run: cd scripts && python3 tool_hub.py"""
from toolkit import ASSET_V, SITE, app_plug, crumbs, footer, head, write

TOOLS = [
    ("/vision-board-maker/", "Vision board maker", "Add your photos and words, then save a phone wallpaper, desktop background or printable board.", "Phone, desktop, print"),
    ("/affirmation-generator/", "Affirmation generator", "Affirmations for money, love, health and more, plus a printable 369 sheet with your dates.", "With a 369 sheet"),
    ("/affirmation-wallpaper/", "Affirmation wallpaper", "Put your affirmation on your lock screen in a calm, readable style.", "iPhone and Android"),
    ("/letter-to-future-self/", "Letter to your future self", "Guided prompts, then a calendar reminder to open it on the day you choose. No email needed.", "6 months to 3 years"),
    ("/journal-prompt-generator/", "Journal prompt generator", "Manifestation, scripting, gratitude and future-self prompts, one at a time or 30 to print.", "112 prompts"),
    ("/angel-number-calculator/", "Angel number meanings", "Look up a number you keep seeing, or find the number from your birthday.", "Including 369"),
    ("/369-method/tracker/", "Printable 33-day tracker", "One page to tick off your 3, 6 and 9 writing sessions on paper.", "Print or PDF"),
]


def page():
    p = {
        "path": "/tools/",
        "crumb": "Free tools",
        "title": "Free manifestation tools: vision board and more | 369 Journal",
        "h1": "Free tools for your practice",
        "description": "Free, no sign-up manifestation tools: vision board maker, affirmation generator and wallpaper, letter to your future self, prompts, angel numbers.",
        "og_type": "website",
    }
    items = [{"@type": "ListItem", "position": i + 1, "name": t, "url": f"{SITE}{h}"} for i, (h, t, _, _) in enumerate(TOOLS)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": p["h1"], "url": f"{SITE}{p['path']}", "description": p["description"],
         "mainEntity": {"@type": "ItemList", "itemListElement": items}},
        crumbs(p),
    ]}
    cards = "\n".join(
        f'        <a class="hub-tool" href="{h}"><span class="hub-meta">{m}</span><strong>{t}</strong><span>{d}</span></a>'
        for h, t, d, m in TOOLS)
    plug = app_plug("Use them with a daily ritual",
                    "369 Journal reminds you to write your desire morning, afternoon and night, and counts every line. Your first 21-day cycle is free.",
                    "site-tools")
    html = head(p, ld).replace("</head>", f'  <link rel="stylesheet" href="/assets/tools.css?v={ASSET_V}">\n</head>')
    return html + f"""
  <main>
    <div class="tool-head">
      <div class="wrap">
        <h1>{p['h1']}</h1>
        <p>Small, calm tools that run in your browser. No sign-up, no email, and nothing you type or upload leaves your device.</p>
      </div>
    </div>
    <section class="hub" aria-label="Free tools">
      <div class="hub-grid">
{cards}
      </div>
    </section>
    <div class="narrow prose">
      <h2 style="margin-top:0">Which tool should you start with?</h2>
      <ul>
        <li><strong>You don&rsquo;t know what you want yet:</strong> start with the <a href="/journal-prompt-generator/">journal prompt generator</a> and answer three prompts. Your answers usually point to one clear desire.</li>
        <li><strong>You know what you want but not how to say it:</strong> use the <a href="/affirmation-generator/">affirmation generator</a> to turn it into one short, present-tense line.</li>
        <li><strong>You want to see it every day:</strong> put that line on your lock screen with the <a href="/affirmation-wallpaper/">affirmation wallpaper maker</a>, or add your photos with the <a href="/vision-board-maker/">vision board maker</a>.</li>
        <li><strong>You want to look back later:</strong> write a <a href="/letter-to-future-self/">letter to your future self</a> and set a reminder to open it in six months or a year.</li>
        <li><strong>You keep seeing the same number:</strong> look it up in <a href="/angel-number-calculator/">angel number meanings</a>, or read <a href="/369-meaning/">what 369 means</a>.</li>
      </ul>
      <p>The tools help you find and word a goal. A daily habit keeps it in front of you. The <a href="/369-method/">369 method</a> is a simple one: write your line 3 times in the morning, 6 in the afternoon and 9 at night, for 21, 33 or 45 days. Print the <a href="/369-method/tracker/">free tracker</a> to tick off each session.</p>
{plug}
      <p class="fine" style="margin-top:1.4rem">Prefer paper? See <a href="/books/">our two guided workbooks</a>.</p>
    </div>
  </main>

  {footer()}
</body>
</html>
"""


if __name__ == "__main__":
    write("/tools/", page())

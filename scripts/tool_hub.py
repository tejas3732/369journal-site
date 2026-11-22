#!/usr/bin/env python3
"""Builds /tools/, the hub for every free tool.  Run: cd scripts && python3 tool_hub.py"""
from toolkit import ASSET_V, SITE, app_plug, crumbs, footer, head, write

TOOLS = [
    ("/word-of-the-year/", "Find your Word of the Year", "Five quick questions, one word to guide your 2027, with an affirmation and a lock-screen image.", "New for 2027"),
    ("/new-year-resolution-ideas/", "New Year resolution ideas", "100 ideas and a picker that turns one into an affirmation and a weekly action.", "For 2027"),
    ("/personal-year-number-calculator/", "2027 personal year calculator", "Your numerology theme for 2027, with every month of the year mapped out.", "Month by month"),
    ("/vision-board-templates/", "Printable vision board templates", "Six layouts to print or save as PDF, plus 100 vision board ideas by life area.", "A4 and US Letter"),
    ("/vision-board-maker/", "Vision board maker", "Add your photos and words, then save a phone wallpaper, desktop background or printable board.", "Phone, desktop, print"),
    ("/affirmation-generator/", "Affirmation generator", "Affirmations for money, love, health and more, plus a printable 369 sheet with your dates.", "With a 369 sheet"),
    ("/affirmation-wallpaper/", "Affirmation wallpaper", "Put your affirmation on your lock screen in a calm, readable style.", "iPhone and Android"),
    ("/letter-to-future-self/", "Letter to your future self", "Guided prompts, then a calendar reminder to open it on the day you choose. No email needed.", "6 months to 3 years"),
    ("/journal-prompt-generator/", "Journal prompt generator", "Manifestation, scripting, gratitude and future-self prompts, one at a time or 30 to print.", "112 prompts"),
    ("/morning-affirmations/", "Morning affirmations", "Short, calm lines to start the day. Save favourites, copy one or put it on your lock screen.", "Copy or save"),
    ("/self-love-affirmations/", "Self-love affirmations", "Kind words for worth, body, boundaries and healing.", "Copy or save"),
    ("/money-affirmations/", "Money affirmations", "Calm money lines, each paired with one small real action.", "With actions"),
    ("/angel-numbers/", "Angel number meanings", "A page for each number you keep seeing, from 111 to 1212, with honest meanings.", "Including 369"),
    ("/angel-number-calculator/", "Angel number lookup", "Look up any other number, or find the number from your birthday.", "Any number"),
    ("/life-path-number-calculator/", "Life path number calculator", "Your life path number with the maths shown, plus a compatibility check.", "With compatibility"),
    ("/name-numerology-calculator/", "Name numerology calculator", "Destiny, soul urge and personality numbers from your name, letter by letter.", "Letter by letter"),
    ("/numerology-calculator/", "All-in-one numerology", "Life path, name numbers and your 2027 personal year on one page.", "Everything at once"),
    ("/gratitude-journal-prompts/", "Gratitude journal prompts", "108 prompts in 9 themes, a 3 good things mode, and a printable 30-day journal.", "Printable journal"),
    ("/habit-tracker-printable/", "Printable habit tracker", "Type your habits, pick a month, print a clean tracker sheet.", "Monthly or weekly"),
    ("/goal-setting-worksheet/", "Goal setting worksheet", "Fill it in on screen, then print one clear page with your plan.", "Fill in and print"),
    ("/369-method/tracker/", "Printable 33-day tracker", "One page to tick off your 3, 6 and 9 writing sessions on paper.", "Print or PDF"),
]


def page():
    p = {
        "path": "/tools/",
        "crumb": "Free tools",
        "title": "Free Manifestation Tools: Vision Board and More | 369 Journal",
        "h1": "Free Tools for Your Practice",
        "description": "Free, no sign-up tools: vision board maker, Word of the Year finder, affirmation generator, numerology calculator, gratitude prompts and more.",
        "og_type": "website",
    }
    items = [{"@type": "ListItem", "position": i + 1, "name": t, "url": f"{SITE}{h}"} for i, (h, t, _, _) in enumerate(TOOLS)]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": p["h1"], "url": f"{SITE}{p['path']}", "description": p["description"],
         "mainEntity": {"@type": "ItemList", "itemListElement": items}},
        crumbs(p),
    ]}
    cards = "\n".join(
        f'        <a class="hub-tool{" featured" if i == 0 else ""}" href="{h}"><span class="hub-meta">{m}</span><strong>{t}</strong><span>{d}</span></a>'
        for i, (h, t, d, m) in enumerate(TOOLS))
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
        <li><strong>You want one focus for 2027:</strong> find your <a href="/word-of-the-year/">Word of the Year</a> in five questions.</li>
        <li><strong>You don&rsquo;t know what you want yet:</strong> start with the <a href="/journal-prompt-generator/">journal prompt generator</a> and answer three prompts. Your answers usually point to one clear desire.</li>
        <li><strong>You know what you want but not how to say it:</strong> use the <a href="/affirmation-generator/">affirmation generator</a> to turn it into one short, present-tense line.</li>
        <li><strong>You want to see it every day:</strong> put that line on your lock screen with the <a href="/affirmation-wallpaper/">affirmation wallpaper maker</a>, or add your photos with the <a href="/vision-board-maker/">vision board maker</a>.</li>
        <li><strong>You want to look back later:</strong> write a <a href="/letter-to-future-self/">letter to your future self</a> and set a reminder to open it in six months or a year.</li>
        <li><strong>You keep seeing the same number:</strong> look it up in <a href="/angel-number-calculator/">angel number meanings</a>, or read <a href="/369-meaning/">what 369 means</a>. For your birthday numbers, try the <a href="/numerology-calculator/">numerology calculator</a>.</li>
        <li><strong>You want a gentler daily habit:</strong> start with <a href="/gratitude-journal-prompts/">gratitude journal prompts</a>, three good things a day.</li>
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

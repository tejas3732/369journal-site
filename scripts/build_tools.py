#!/usr/bin/env python3
"""Builds the free tools (currently the affirmation generator).

Run:  python3 scripts/build_tools.py && python3 scripts/layout.py
The tool's logic lives in /assets/generator.js and runs only in the browser.
"""
import html
import json

from build_posts import SITE, PUBLISHED, app_plug, book_card, crumbs, footer, head, write

AREAS = [
    ("money", "Money"), ("career", "Career"), ("love", "Love"), ("selflove", "Self-love"),
    ("health", "Health"), ("home", "Home"), ("calm", "Calm"), ("newyear", "New Year 2027"),
]

FAQ = [
    ("Is this affirmation generator free?", "Yes. It is free, needs no sign-up, and runs entirely in your browser. Nothing you type is sent or saved anywhere."),
    ("How do I use an affirmation with the 369 method?", "Write the same affirmation 3 times in the morning, 6 times in the afternoon and 9 times at night, every day for 21, 33 or 45 days. The printable sheet on this page helps you keep count."),
    ("What makes a good affirmation?", "It is short, in the present tense as if it is already true, says what you want rather than what you want to avoid, and feels believable when you read it out loud."),
    ("Can I write my own affirmation instead?", "Yes. Type it into the “Write your own” box and the checker shows whether it is present tense, positive and short enough, then you can make a printable sheet from it."),
    ("Do affirmations really work?", "There is no evidence that writing an affirmation makes outside events happen by itself. Used daily, it can keep your goal in mind and help you notice chances and take small steps, which is how we suggest using it."),
]


def page():
    p = {
        "path": "/affirmation-generator/",
        "crumb": "Affirmation generator",
        "title": "Free affirmation generator + printable 369 sheet | 369 Journal",
        "h1": "Free affirmation generator",
        "description": "Free affirmation generator for money, love, health, career, calm or the new year. Check your own wording, then print a 369 method sheet. No sign-up.",
    }
    url = f"{SITE}{p['path']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": "Affirmation generator", "url": url, "applicationCategory": "LifestyleApplication",
         "operatingSystem": "Any (web browser)", "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "description": p["description"], "datePublished": PUBLISHED,
         "publisher": {"@type": "Organization", "name": "369 Journal", "url": f"{SITE}/"}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        crumbs(p),
    ]}
    chips = "\n".join(
        f'            <label class="chip"><input type="radio" name="area" value="{v}"{" checked" if i == 0 else ""}><span>{t}</span></label>'
        for i, (v, t) in enumerate(AREAS))
    faq_html = "\n".join(
        f"      <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in FAQ)
    APP = "https://apps.apple.com/app/apple-store/id6770804298?pt=128923117&amp;ct=site-generator&amp;mt=8"

    return head(p, ld).replace("</head>", '  <script src="/assets/generator.js?v=20261118" defer></script>\n</head>') + f"""
  <main data-generator>
    <div class="narrow article-head print-hide">
      <h1>{p['h1']}</h1>
      <p>Pick an area of your life, add a detail if you like, and get affirmations you can use straight away. Then turn your favourite into a printable 369 method sheet. Free, no sign-up, and nothing you type leaves your browser.</p>
    </div>

    <section class="narrow gen print-hide" aria-label="Affirmation generator">
      <div class="gen-panel">
        <fieldset>
          <legend>1. What is it about?</legend>
          <div class="chip-row">
{chips}
          </div>
        </fieldset>
        <label class="gen-label" for="gen-detail">2. Add a detail <span>(optional)</span></label>
        <input id="gen-detail" class="gen-input" type="text" maxlength="60" autocomplete="off" placeholder="e.g. $5,000 in savings">
        <div class="gen-actions">
          <button id="gen-go" class="btn" type="button">Generate affirmations</button>
        </div>
      </div>

      <div id="gen-output" class="gen-output" hidden aria-live="polite">
        <ul id="gen-results" class="gen-results"></ul>
        <div class="gen-actions">
          <button id="gen-more" class="btn ghost" type="button">Show me different ones</button>
          <a id="gen-guide" class="gen-guide" href="/369-method/examples/">50 369 method examples</a>
        </div>
        <p id="gen-copy-nudge" class="gen-nudge" hidden>Copied. Want to write it 3, 6 and 9 times a day with reminders? <a href="{APP}" data-cta="generator-copy">Get 369 Journal free on iPhone</a>.</p>
      </div>

      <div class="gen-own">
        <label class="gen-label" for="gen-own">Or write your own and check the wording</label>
        <input id="gen-own" class="gen-input" type="text" maxlength="160" autocomplete="off" placeholder="I am so grateful that&hellip;">
        <ul id="gen-checks" class="gen-checks" hidden aria-live="polite"></ul>
        <div class="gen-actions">
          <button id="gen-own-use" class="btn small" type="button">Make my 369 sheet</button>
          <button id="gen-own-copy" class="btn ghost small" type="button">Copy</button>
        </div>
      </div>
    </section>

    <section id="gen-sheet" class="narrow gen-sheet" hidden aria-labelledby="sheet-title">
      <div class="sheet-controls print-hide">
        <h2>Your printable 369 sheet</h2>
        <p>Fill one circle each time you write your affirmation. Edit anything below, then print or save as PDF.</p>
        <label class="gen-label" for="sheet-aff">Affirmation</label>
        <input id="sheet-aff" class="gen-input" type="text" maxlength="160">
        <div class="sheet-row">
          <label>Days
            <select id="sheet-days" class="gen-input">
              <option value="21">21 days</option>
              <option value="33" selected>33 days</option>
              <option value="45">45 days</option>
            </select>
          </label>
          <label>Start date
            <input id="sheet-start" class="gen-input" type="date">
          </label>
          <button id="sheet-print" class="btn" type="button">Print or save as PDF</button>
        </div>
      </div>

      <div class="sheet">
        <div class="sheet-head">
          <h2 id="sheet-title">My 369 sheet</h2>
          <span class="sheet-site">369journal.app</span>
          <p id="sheet-print-aff" class="sheet-aff">&nbsp;</p>
        </div>
        <div class="table-wrap">
          <table>
            <thead><tr><th scope="col">Day</th><th scope="col">Date</th><th scope="col">Morning 3</th><th scope="col">Afternoon 6</th><th scope="col">Night 9</th></tr></thead>
            <tbody id="sheet-body"></tbody>
          </table>
        </div>
        <p class="print-foot">Prefer reminders and a sheet that fills itself in? 369 Journal for iPhone &middot; Guided pages: The 369 Method workbook &middot; 369journal.app</p>
      </div>

      <div class="print-hide gen-next">
        <h2>Keep going after you print</h2>
        <p>If you like writing on paper, our workbook gives you a guided page for each of 45 days, so you don&rsquo;t need to print anything.</p>
{book_card("369", "web_generator")}
{app_plug("Or let your phone keep count", "369 Journal reminds you morning, afternoon and night, counts every line and keeps your cycle map. Your first 21-day cycle is free.", "site-generator")}
      </div>
    </section>

    <article class="narrow prose print-hide">
      <h2 id="how">How to use your affirmation</h2>
      <ol>
        <li><strong>Pick one.</strong> Choose the affirmation that feels most believable when you read it out loud.</li>
        <li><strong>Keep the words the same</strong> every time you write it.</li>
        <li><strong>Use the 369 method:</strong> write it 3 times in the morning, 6 in the afternoon and 9 at night. See <a href="/369-method/">how to do the 369 method</a>.</li>
        <li><strong>Take one small step a day</strong> towards what you wrote.</li>
      </ol>

      <h2 id="good">What makes a good affirmation</h2>
      <ul>
        <li><strong>Present tense:</strong> &ldquo;I have&rdquo;, not &ldquo;I will have&rdquo;.</li>
        <li><strong>Positive:</strong> &ldquo;I am debt-free&rdquo;, not &ldquo;I am not in debt&rdquo;.</li>
        <li><strong>Short:</strong> one line, so writing it 18 times a day stays easy.</li>
        <li><strong>About you:</strong> your own feelings and actions, not another person&rsquo;s choices.</li>
        <li><strong>Believable:</strong> if a big number makes you tense, use the feeling instead (&ldquo;I feel secure with money&rdquo;).</li>
      </ul>
      <p>Prefer to picture a whole scene instead of one line? Try <a href="/scripting-manifestation/">scripting manifestation</a>, or our guided <a href="/books/#scripting">Scripting Manifestation</a> workbook.</p>

      <h2 id="faq">Questions</h2>
{faq_html}

      <h2>More free tools and guides</h2>
      <ul>
        <li><a href="/369-method/tracker/">Free printable 33-day 369 tracker</a></li>
        <li><a href="/369-method/examples/">50 369 method examples</a></li>
        <li><a href="/new-year-manifestation-challenge/">21-day New Year manifestation challenge</a></li>
        <li><a href="/books/">Books: The 369 Method and Scripting Manifestation</a></li>
      </ul>
    </article>
  </main>

  {footer()}
</body>
</html>
"""


if __name__ == "__main__":
    write("/affirmation-generator/", page())

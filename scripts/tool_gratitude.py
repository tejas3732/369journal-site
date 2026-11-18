#!/usr/bin/env python3
"""Builds /gratitude-journal-prompts/.

Run:  cd scripts && python3 tool_gratitude.py && python3 layout.py
Prompts live here (one source): they are embedded as JSON for /assets/tools/gratitude.js
and a few per theme are printed as static lists in the article for search engines.
All prompts are written for the site, not taken from the books or other sites.
"""
import html
import json

from toolkit import next_steps, privacy, tool_page, write

THEMES = [
    ("small", "Everyday small things", [
        "What is one small thing from today that made you feel a little lighter?",
        "Which food or drink did you enjoy most today? Describe the first sip or bite.",
        "What did you see today that was quietly beautiful?",
        "What is a sound you like hearing at this time of day?",
        "What is something that worked the way it should today, without any fuss?",
        "Which small comfort are you glad to have: a warm blanket, a favourite mug, clean sheets?",
        "What made you smile today, even for a second?",
        "What is one thing you did not have to wait for today?",
        "What is a smell that makes you feel calm or happy? Where did you notice it lately?",
        "What was the best five minutes of your day?",
        "Which ordinary object do you use every day and rarely thank?",
        "What is something free that brought you joy this week?",
    ]),
    ("people", "People", [
        "Who made your day easier this week? What did they do?",
        "Who do you feel safe being yourself with? What do they do that helps?",
        "Write about a person who believed in you before you did.",
        "Who is someone you have never properly thanked? What would you say?",
        "What is a kind thing a stranger did for you, however small?",
        "Which friend always picks up when you call? What does that mean to you?",
        "Think of someone in your family. What is one thing about them you are glad of?",
        "Who taught you something that you still use today?",
        "Which person makes you laugh the most? Describe the last time.",
        "Whose advice do you trust? What is the best thing they ever told you?",
        "Who would you like to thank today? Write the message, then send it if you want to.",
        "Write about a person you have lost touch with and what they gave you.",
    ]),
    ("self", "Yourself", [
        "What is one thing you did today that you are proud of, however small?",
        "Which of your strengths helped you this week? How did you use it?",
        "What is something about the way you think or feel that you would not swap?",
        "Write a thank-you note to yourself for something you kept going with.",
        "Which choice did you make this month that you are glad you made?",
        "What did you do for yourself today that nobody saw?",
        "What is a quality in you that other people have thanked you for?",
        "What is something you used to find hard that is easier now?",
        "Which part of your story are you grateful for, even the messy part?",
        "When did you last surprise yourself? What did you do?",
        "What is one boundary you kept that protected your energy?",
        "What would you thank your younger self for?",
    ]),
    ("hard", "Hard days", [
        "It is a heavy day. What is one thing, however tiny, that is still okay right now?",
        "What is holding you up today, even if it feels thin: a person, a routine, a cup of tea?",
        "Write what is hard, in one honest sentence. Then write one thing you are still thankful for. Both can be true.",
        "What got you through the last hard time? Can you use a little of it today?",
        "Who would listen if you called them today? Write their name and why they are safe.",
        "What small kindness could you give yourself right now?",
        "What is something you have survived that you are quietly proud of?",
        "Name one thing that was easier today than yesterday, even by a little.",
        "What do you not have to do today? Write it down and feel the relief.",
        "What has this hard time shown you about what really matters?",
        "If a friend felt this way, what would you say to them? Say it to yourself.",
        "What is one thing you are looking forward to, even if it is as small as a hot shower?",
    ]),
    ("body", "Body and health", [
        "What did your body do for you today that you usually take for granted?",
        "Which part of your body are you thankful for right now, and why?",
        "Write about a time your body healed. What did you learn from it?",
        "What does your body feel like when it is rested? Where did you last feel that?",
        "What is one thing that helps you feel well: a walk, water, stretching, sleep?",
        "Which meal made you feel good in your body recently?",
        "What can you do today that you could not do a few years ago?",
        "Who or what helps you stay healthy? Write a thank-you.",
        "What is one thing you can see, hear, taste, touch or smell right now that you are glad of?",
        "Write about a time your body made you feel strong.",
        "What is your favourite way to rest? Describe it.",
        "What is a health habit you are grateful to have started, even if it is a small one?",
    ]),
    ("home", "Home and places", [
        "What is one thing about your home that you are grateful for today?",
        "Describe a corner of your home that feels like yours.",
        "Which place makes you feel calm? Write what you see, hear and smell there.",
        "What is a place you visited that you are glad you saw?",
        "What is something in your neighbourhood that you would miss if it were gone?",
        "Which room in your home do you use most, and what does it give you?",
        "Write about a place from your childhood that you still carry with you.",
        "What do you love about the light in your home at a certain time of day?",
        "What is something you are glad to have within reach: running water, a bed, a key?",
        "Where did you feel most at ease this week?",
        "What is a view you are thankful for?",
        "Which place would you like to say thank you to, and for what?",
    ]),
    ("work", "Work and learning", [
        "What is one thing about your work or studies that you are glad of today?",
        "Who at work or school made something easier for you recently?",
        "What did you learn this week that you are glad to know?",
        "Write about a mistake that taught you something useful.",
        "Which skill of yours has opened a door for you?",
        "What is a project or task you finished that you are proud of?",
        "Which teacher, boss or mentor changed how you think? What did they say or do?",
        "What part of your day gives you energy? Describe it.",
        "What do you have now in your work life that you once hoped for?",
        "Who would you like to thank for helping you grow?",
        "What is one thing you are curious about right now?",
        "What did you finish today, even though it was not easy?",
    ]),
    ("seasons", "Seasons and holidays", [
        "Thanksgiving: what are three things from this year that you are truly thankful for?",
        "Thanksgiving: who would you like at your table, and what would you thank them for?",
        "What is a food, smell or song that tells you the holidays have arrived?",
        "What are you grateful for in the season you are in right now?",
        "Write about a holiday memory that still makes you smile.",
        "End of the year: what are three moments from this year you would not trade?",
        "End of the year: what did this year give you that you did not expect?",
        "End of the year: which person made this year better? Write them a few thank-you lines.",
        "New Year: what are you thankful to carry with you into the new year?",
        "New Year: what is one thing you are glad to leave behind, and what did it teach you?",
        "What small tradition would you like to keep this year, and why does it matter?",
        "What is something you are looking forward to in the coming season?",
    ]),
    ("coming", "Gratitude for what's coming", [
        "Write one thing you want in your life as if it is already here: “Thank you for…”",
        "Describe your desire in the present tense. What are you thankful for about it?",
        "Write about an ordinary morning after your goal came true. What are you grateful for in it?",
        "Which part of your future are you already thankful for, even before it arrives?",
        "Write a thank-you note to your future self for something you are about to start.",
        "What are you grateful for that is connected to what you want? Start with what is already here.",
        "Finish this sentence three ways: “I am so grateful that now I get to…”",
        "Write a short thank-you as if your desire has just come true. Keep it honest and warm.",
        "What would you feel thankful for on the day it all works out? Let yourself feel a little of it now.",
        "Which small step you took recently are you grateful for, because it points to where you are going?",
        "What are you thankful you did not give up on? What is it making room for?",
        "Write the first line of the thank-you you want to say in a year. What comes after it?",
    ]),
]

STATIC_PER_THEME = 4

ALL_COUNT = sum(len(p) for _, _, p in THEMES)

CHIPS = '            <label><input type="radio" name="gtheme" value="all" checked><span>All</span></label>\n' + "\n".join(
    f'            <label><input type="radio" name="gtheme" value="{tid}"><span>{label}</span></label>'
    for tid, label, _ in THEMES)

DATA = json.dumps({tid: {"label": label, "prompts": prompts} for tid, label, prompts in THEMES}, ensure_ascii=False)

I_REFRESH = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16.5 10a6.5 6.5 0 1 1-1.9-4.6"/><path d="M16.5 3.5v3.4h-3.4"/></svg>'
I_COPY = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="7" width="9.5" height="9.5" rx="2"/><path d="M13 7V5a1.5 1.5 0 0 0-1.5-1.5h-6A1.5 1.5 0 0 0 4 5v6.5A1.5 1.5 0 0 0 5.5 13H7"/></svg>'
I_SAVE = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5.5 3.5h9v13l-4.5-3-4.5 3z"/></svg>'
I_PRINT = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 7V3.5h8V7"/><rect x="3.5" y="7" width="13" height="7" rx="1.5"/><path d="M6 12h8v4.5H6z"/></svg>'

BODY = f"""  <div class="tool-shell single print-hide" data-gratitude>
    <div class="tool-controls">
      <div class="tool-panel">
        <fieldset>
          <legend class="t-step"><span class="n">1</span>Choose a theme</legend>
          <div class="t-chips" role="radiogroup">
{CHIPS}
          </div>
        </fieldset>
      </div>

      <section class="gj-stage" aria-label="Your gratitude prompt">
        <div class="gj-meta">
          <div class="seg seg-small" role="radiogroup" aria-label="How many prompts">
            <label><input type="radio" name="gview" value="one" checked><span>One prompt</span></label>
            <label><input type="radio" name="gview" value="three"><span>3 good things</span></label>
          </div>
          <div class="seg seg-small" role="radiogroup" aria-label="Which prompt to show">
            <label><input type="radio" name="gmode" value="random" checked><span>Random</span></label>
            <label><input type="radio" name="gmode" value="today"><span>Today&rsquo;s</span></label>
          </div>
        </div>
        <p class="gj-cat" data-cat-label>All themes</p>

        <div data-one>
          <blockquote class="gj-card" aria-live="polite"><p data-prompt>Choose a theme, then press New prompt.</p></blockquote>
        </div>
        <div data-three hidden aria-live="polite">
          <p class="gj-three-lead">Today&rsquo;s page: answer all three, in a line or two each. Write on paper or in your notes app.</p>
          <ol class="gj-three" data-three-list></ol>
        </div>

        <div class="gj-actions">
          <button class="btn clay" type="button" data-new>{I_REFRESH}<span data-new-label>New prompt</span></button>
          <button class="btn ghost" type="button" data-copy>{I_COPY}Copy</button>
          <button class="btn ghost" type="button" data-save data-one-only>{I_SAVE}<span data-save-label>Save</span></button>
        </div>
        <p class="gj-tip">Tip: press <kbd>Space</kbd> or <kbd>Enter</kbd> for a new prompt.</p>
      </section>

      <div class="tool-panel saved-panel">
        <div class="saved-head">
          <h2 class="t-step"><span class="n">2</span>My saved prompts <span class="saved-count" data-saved-count>0</span></h2>
        </div>
        <ol class="saved-list" data-saved-list></ol>
        <p class="t-hint" data-saved-empty>Prompts you save appear here, on this device only.</p>
      </div>

      <div class="tool-panel">
        <h2 class="t-step"><span class="n">3</span>Print a 30-day gratitude journal</h2>
        <p class="t-hint" style="margin:-0.3rem 0 0.9rem">One prompt a day for 30 days, each with lines to write on. A free gratitude journal template: print it or save it as a PDF.</p>
        <div class="seg" role="radiogroup" aria-label="What to print">
          <label><input type="radio" name="gsource" value="theme" checked><span>30 days: <b data-print-cat>mixed themes</b></span></label>
          <label><input type="radio" name="gsource" value="saved"><span>My saved prompts</span></label>
        </div>
        <p class="t-hint" style="margin:0.7rem 0 0">Uses the theme you picked in step 1. A theme has 12 prompts, so the rest of the 30 days are filled from other themes, never repeated.</p>
        <div class="preview-actions" style="justify-content:flex-start;margin-top:1rem">
          <button class="btn" type="button" data-print>{I_PRINT}Print or save as PDF</button>
        </div>
        <div style="margin-top:1rem">{privacy("Runs in your browser. Saved prompts stay on this device and nothing you choose is sent anywhere.")}</div>
      </div>
    </div>
  </div>

  <section class="gj-print" data-print-sheet aria-hidden="true">
    <h2 data-print-title>30-day gratitude journal</h2>
    <p class="gp-sub">One prompt a day. Five minutes is enough: be specific, and write why it matters.</p>
    <ol data-print-list></ol>
    <p class="gp-foot">369journal.app &middot; Free gratitude journal prompts</p>
  </section>

  <script type="application/json" id="gratitude-data">{DATA}</script>"""


def static_lists():
    out = []
    for tid, label, prompts in THEMES:
        items = "\n".join(f"        <li>{html.escape(p)}</li>" for p in prompts[:STATIC_PER_THEME])
        out.append(f'      <h3 id="list-{tid}">{label}</h3>\n      <ol>\n{items}\n      </ol>')
    return "\n".join(out)


ARTICLE = f"""      <h2 id="start">How to start a gratitude journal</h2>
      <p>You do not need a special notebook or a long routine. Five minutes a day is plenty. Here is a simple way to begin:</p>
      <ol>
        <li><strong>Pick a time you already have.</strong> With your morning tea or just before bed works well. Link it to something you do every day.</li>
        <li><strong>Choose one prompt</strong> from the tool above, or try <em>3 good things</em>, the classic version where you note three good things from your day.</li>
        <li><strong>Be specific.</strong> &ldquo;I&rsquo;m grateful for my sister&rdquo; is fine. &ldquo;I&rsquo;m grateful my sister called when she saw I was quiet&rdquo; is better. Details make the feeling real again.</li>
        <li><strong>Write why.</strong> One extra sentence, &ldquo;this mattered because&hellip;&rdquo;, turns a list into a thought.</li>
        <li><strong>Stop when the time is up.</strong> A short habit you keep beats a long one you drop.</li>
      </ol>
      <p>Research on gratitude journaling suggests it can lift mood a little for many people. It is not a cure for anything, but it is a gentle habit that costs nothing.</p>

      <h2 id="hard-days">What to do on hard days</h2>
      <p>Some days gratitude feels fake. That is okay. You do not have to pretend things are fine. On a hard day, try this:</p>
      <ul>
        <li>Write what is hard, in one honest sentence.</li>
        <li>Then write one small thing that is still okay: a hot drink, a friend&rsquo;s message, a bed to sleep in.</li>
        <li>Let both sentences stand. Gratitude does not cancel pain; it sits next to it.</li>
      </ul>
      <p>The <strong>Hard days</strong> theme above is written for exactly this. If a prompt feels too much, press New prompt and skip it. If low mood stays for weeks, please talk to a doctor or a counsellor. A journal is support, not treatment.</p>

      <h2 id="template">A simple gratitude journal template</h2>
      <p>You can make your own page in a minute. Our printable 30-day journal uses this layout, and it is free to print or save as a PDF:</p>
      <ul>
        <li><strong>Day and date</strong> at the top, so you can see your streak.</li>
        <li><strong>One prompt</strong> to start you off.</li>
        <li><strong>Five or six lines</strong> to answer. Not a whole page, so it never feels like homework.</li>
      </ul>
      <p>Choose a theme in step 1, then use step 3 above to print the pages. Staple them or keep them in a folder.</p>

      <h2 id="manifestation">Gratitude and manifestation</h2>
      <p>Some people write gratitude &ldquo;in advance&rdquo;: a thank-you for something they hope for, written as if it is already here. The <strong>Gratitude for what&rsquo;s coming</strong> theme does this. To be honest about it, writing like this does not make anything happen by itself. What it can do is shift your attention to what you want and lift your mood, which can make you more likely to take the small steps that lead there. Keep it kind and realistic, and pair it with action.</p>

      <h2 id="369">Pairing gratitude with the 369 method</h2>
      <p>The <a href="/369-method/">369 method</a> has you write one short desire 3 times in the morning, 6 in the afternoon and 9 at night. Gratitude fits nicely around it: write your three good things first, then your desire. If you like to write whole scenes, the <a href="/scripting-manifestation/">scripting manifestation guide</a> shows how. For more questions to answer, try the <a href="/journal-prompt-generator/">journal prompt generator</a>, or write a longer <a href="/letter-to-future-self/">letter to your future self</a>.</p>

      <p>Setting up a fresh journal for the new year? Choose <a href="/word-of-the-year/">your Word of the Year</a> first and write it at the top of the first page.</p>

      <h2 id="lists">Gratitude prompts by theme</h2>
      <p>A few from each theme. The tool above has {ALL_COUNT} in all, and you can get a different one every time.</p>
{static_lists()}"""

FAQ = [
    ("Are these gratitude journal prompts free?", "Yes. They are free, need no sign-up and run in your browser. Prompts you save stay on your device."),
    ("How many gratitude prompts are there?", f"There are {ALL_COUNT} original prompts across nine themes, from everyday small things to hard days, and a new one every time you press New prompt."),
    ("What is the 3 good things exercise?", "A classic gratitude habit: each day you note three good things and why they happened. Switch to “3 good things” above to get three prompts at once."),
    ("How often should I write in a gratitude journal?", "Daily for five minutes is a good start. Some people prefer two or three times a week. Pick what you will keep doing."),
    ("What if I don't feel grateful?", "Use the Hard days theme. You can write what is hard and one small thing that is still okay. You do not have to force a good feeling."),
    ("Can I print a gratitude journal template?", "Yes. Choose a theme, then print a 30-day journal with one prompt a day and lines to write on, or save it as a PDF."),
]

P = {
    "path": "/gratitude-journal-prompts/",
    "crumb": "Gratitude journal prompts",
    "title": "Gratitude Journal Prompts: 100+ Free Ideas | 369 Journal",
    "h1": "Gratitude Journal Prompts",
    "description": "Free gratitude journal prompts for every kind of day: pick a theme, try 3 good things, or print a 30-day gratitude journal template with lines.",
    "lede": f"{ALL_COUNT} fresh gratitude prompts in simple words. Get one at a time, try the 3 good things exercise, save your favourites, or print a 30-day journal.",
    "badges": ["Free, no sign-up", "100+ prompts", "Printable 30-day journal"],
}

NEXT = next_steps(
    "Turn gratitude into a daily habit",
    "If you like writing about what you want to bring in, our scripting workbook walks you through 30 days of it, with a lesson, an example and a full page each day. Or keep the habit going on your phone.",
    "scripting", "web_gratitude",
    "Write your desire on your iPhone",
    "369 Journal reminds you to write your desire morning, afternoon and night. Your first 21-day cycle is free.",
    "site-gratitude",
)

if __name__ == "__main__":
    write(P["path"], tool_page(P, FAQ, BODY, js="gratitude.js", css="gratitude.css", article=ARTICLE, next_html=NEXT))

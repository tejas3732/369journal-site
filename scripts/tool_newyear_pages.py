#!/usr/bin/env python3
"""Builds the two New Year 2027 pages:
  /vision-board-templates/      printable vision board templates + 100 ideas
  /new-year-resolution-ideas/   100 resolution ideas + a resolution picker

Run:  cd scripts && python3 tool_newyear_pages.py && python3 layout.py
Content lives in newyear_data.py (original wording, written for the site).
"""
import html
import json

from build_posts import table
from newyear_data import (RESOLUTIONS, SIZE_LABEL, VISION_IDEAS, VISION_PHRASES, VISION_WORDS)
from toolkit import next_steps, privacy, tool_page, write

I_PRINT = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 7V3.5h8V7"/><rect x="3.5" y="7" width="13" height="7" rx="1.5"/><path d="M6 12h8v4.5H6z"/></svg>'
I_COPY = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="7" width="9.5" height="9.5" rx="2"/><path d="M13 7V5a1.5 1.5 0 0 0-1.5-1.5h-6A1.5 1.5 0 0 0 4 5v6.5A1.5 1.5 0 0 0 5.5 13H7"/></svg>'
I_SHUFFLE = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16.5 10a6.5 6.5 0 1 1-1.9-4.6"/><path d="M16.5 3.5v3.4h-3.4"/></svg>'


def e(s):
    return html.escape(s, quote=True)


# =====================================================================
# 1. VISION BOARD TEMPLATES
# =====================================================================
VP = {
    "path": "/vision-board-templates/",
    "crumb": "Vision board templates",
    "title": "Free Vision Board Templates + 100 Ideas | 369 Journal",
    "h1": "Free Printable Vision Board Templates",
    "description": "Print a free vision board template in A4 or US Letter: 9-box grid, life wheel, 2027 year planner and more. Plus 100 vision board ideas by life area.",
    "lede": 'Pick a template, add your own title and labels, then print it or save it as a PDF. Below are 100 vision board ideas, a six-step guide and where to put your board. Prefer your own photos as a phone wallpaper? Try the <a href="/vision-board-maker/">vision board maker</a>.',
    "badges": ["Free, no sign-up", "6 printable templates", "A4 and US Letter"],
    "published": "2026-11-22",
}

TPL_CHIPS = [("grid9", "9-box grid"), ("wheel", "Life areas wheel"), ("year", "2027 year at a glance"),
             ("word", "One-word focus"), ("quarters", "Four quarters"), ("list", "Minimalist list")]
tpl_chips = "\n".join(
    f'            <label><input type="radio" name="vt-tpl" value="{v}"{" checked" if v == "grid9" else ""}><span>{t}</span></label>'
    for v, t in TPL_CHIPS)


def seg(name, label, options, default):
    inner = "".join(
        f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == default else ""}><span>{t}</span></label>'
        for v, t in options)
    return f'<div class="seg" role="radiogroup" aria-label="{label}">{inner}</div>'


VBODY = f"""  <div class="vt-alt print-hide">
    <p><strong>Prefer your own photos?</strong> Make a vision board from your pictures and words, and save it as a phone wallpaper or a print.</p>
    <a class="btn ghost small" href="/vision-board-maker/">Open the vision board maker</a>
  </div>

  <style id="vt-page-style">@page {{ size: A4 portrait; margin: 8mm; }}</style>
  <section class="tool-shell" data-vt aria-label="Printable vision board template maker">
    <div class="tool-controls print-hide">
      <div class="tool-panel">
        <fieldset>
          <legend class="t-step"><span class="n">1</span>Choose a template</legend>
          <div class="t-chips" role="radiogroup" aria-label="Template">
{tpl_chips}
          </div>
        </fieldset>
        <p class="vt-tpl-desc" data-vt-desc aria-live="polite"></p>
      </div>

      <div class="tool-panel">
        <h2 class="t-step"><span class="n">2</span>Paper and look</h2>
        <div class="vt-opts">
          <div class="vt-opt-row"><span class="t-label">Paper</span>{seg("vt-paper", "Paper size", [("a4", "A4"), ("letter", "US Letter")], "a4")}</div>
          <div class="vt-opt-row"><span class="t-label">Direction</span>{seg("vt-orient", "Page direction", [("portrait", "Portrait"), ("landscape", "Landscape")], "portrait")}</div>
          <div class="vt-opt-row"><span class="t-label">Colour</span>{seg("vt-style", "Colour style", [("warm", "Warm"), ("sage", "Sage"), ("mono", "Mono"), ("saver", "Ink saver")], "warm")}</div>
        </div>
      </div>

      <div class="tool-panel">
        <h2 class="t-step"><span class="n">3</span>Make it yours</h2>
        <div class="t-field">
          <label class="t-label" for="vt-title">Title <span>(leave empty for none)</span></label>
          <input id="vt-title" class="t-input" type="text" maxlength="44" value="My 2027 vision board" autocomplete="off">
        </div>
        <fieldset class="t-field" data-vt-labels-wrap style="min-width:0;border:0;padding:0;margin:1rem 0 0">
          <legend class="t-label" data-vt-labels-legend>Box names</legend>
          <div class="vt-labels-grid" data-vt-labels></div>
          <button type="button" class="t-link-btn" data-vt-reset style="margin-top:0.7rem">Reset names</button>
        </fieldset>
        <label class="vt-check" style="margin-top:1rem"><input id="vt-mark" type="checkbox" checked>Small 369journal.app mark at the bottom</label>
      </div>

      <div class="tool-panel">
        <h2 class="t-step"><span class="n">4</span>Print or save as PDF</h2>
        <div class="vt-actions" style="justify-content:flex-start">
          <button type="button" class="btn" data-vt-print>{I_PRINT}Print or save as PDF</button>
        </div>
        <p class="vt-print-hint">In the print window, choose &ldquo;Save as PDF&rdquo; to keep a file. For the cleanest page, turn off &ldquo;Headers and footers&rdquo; and set the scale to 100%. If the paper size does not change, pick it in the print window (Safari does this).</p>
        <div style="margin-top:1rem">{privacy("Runs in your browser. Your title and labels are never sent or saved. We only count which template and paper size people print.")}</div>
      </div>
    </div>

    <div class="tool-preview">
      <div class="vt-wrap" data-vt-wrap data-paper="a4" data-orient="portrait" data-style="warm" role="img" aria-label="Preview of your vision board template">
        <div class="vt-sheet" data-vt-sheet></div>
      </div>
      <p class="vt-caption" data-vt-caption>Preview</p>
    </div>
  </section>
"""

def vision_ideas_html():
    out = []
    for aid, label, items in VISION_IDEAS:
        lis = "\n".join(f"        <li>{e(i)}</li>" for i in items)
        out.append(f'      <h3 id="ideas-{aid}">{label} ({len(items)})</h3>\n      <ul>\n{lis}\n      </ul>')
    return "\n".join(out)


VIDEAS_COUNT = sum(len(i) for _, _, i in VISION_IDEAS)
phrases_html = "\n".join(f"        <li>{e(p)}</li>" for p in VISION_PHRASES)

VARTICLE = f"""      <nav class="toc" aria-label="On this page">
        <strong>On this page</strong>
        <ol>
          <li><a href="#which">Which template should I use?</a></li>
          <li><a href="#ideas">{VIDEAS_COUNT} vision board ideas</a></li>
          <li><a href="#words">Words and phrases to add</a></li>
          <li><a href="#how">How to make a vision board in six steps</a></li>
          <li><a href="#paper-digital">Paper or digital?</a></li>
          <li><a href="#where">Where to put your board</a></li>
          <li><a href="#works">Do vision boards work?</a></li>
          <li><a href="#369">Pair your board with the 369 method</a></li>
        </ol>
      </nav>

      <h2 id="which">Which vision board template should I use?</h2>
      <p>There is no right one. Choose the shape that matches how your mind works, and start again with another if it does not feel right. The templates above print on plain A4 or US Letter paper, so you can paste in pictures from magazines, add your own photos, or just write.</p>
""" + table(["Template", "Best if you want to", "Good for"], [
    ["9-box grid", "Cover the main parts of life, a box each", "A first vision board, or a quick one on a free evening"],
    ["Life areas wheel", "See which areas feel full and which need care", "A yearly check-in, shading each slice from empty to full"],
    ["2027 year at a glance", "Plan the year month by month", "People who like calendars and clear steps"],
    ["One-word focus", "Keep one clear theme for the year", "Pairs well with your <a href=\"/word-of-the-year/\">Word of the Year</a>"],
    ["Four quarters", "Break big goals into three-month pieces", "Work goals, savings and learning plans"],
    ["Minimalist list", "Keep it calm and short", "When a busy collage feels like too much"],
]) + f"""

      <h2 id="ideas">{VIDEAS_COUNT} vision board ideas, by life area</h2>
      <p>Not sure what to put on your board? Here are {VIDEAS_COUNT} ideas in eleven areas. Pick the three to five that make you feel something, not the ones you think you should want. A few pictures that mean a lot beat a crowded page.</p>
      <p class="vt-idea-note">A tip for love and family boards: choose pictures that show the feeling and the qualities you want, such as warmth, laughter and trust, rather than one particular person&rsquo;s face. It keeps the board about your own life and your own choices.</p>
{vision_ideas_html()}

      <h2 id="words">Words and phrases to add</h2>
      <p>Words help a picture stay specific. Write them by hand, cut them from a magazine, or print them in a big, simple font. These phrases are written for this page, so use them as they are or change them to sound like you.</p>
      <ul class="vt-phrases">
{phrases_html}
      </ul>
      <p><strong>One-word ideas:</strong> {VISION_WORDS}.</p>
      <p>Not sure which single word fits? Our <a href="/word-of-the-year/">Word of the Year finder</a> asks five questions, and the <a href="/affirmation-generator/">affirmation generator</a> turns a goal into a sentence you can place on the board. Put the sentence in the present tense, for example &ldquo;I keep the promises I make to myself&rdquo;, so it reads like something that is already becoming true.</p>

      <h2 id="how">How to make a vision board in six steps</h2>
      <ol>
        <li><strong>Choose your focus.</strong> Pick three to five areas of life for the year ahead. Trying to cover everything makes the board blurry.</li>
        <li><strong>Collect pictures and words.</strong> Use old magazines, your own photos, printouts or things you have drawn. Choose the ones that give you a small lift when you look at them.</li>
        <li><strong>Print a template above.</strong> Or use a sheet of card. Print on ordinary paper, or on thicker paper if you plan to stick things on.</li>
        <li><strong>Arrange before you glue.</strong> Lay everything out first. Move things around until it feels balanced, then stick it down.</li>
        <li><strong>Add a title, a date and one sentence.</strong> Write something like &ldquo;By December 2027&rdquo; and one line in the present tense that sums up the year.</li>
        <li><strong>Attach one small action to each picture.</strong> Next to a running shoe, write &ldquo;Walk on Tuesday and Saturday&rdquo;. A board with actions on it is a plan. A board without them is a mood.</li>
      </ol>

      <h2 id="paper-digital">Paper or digital?</h2>
      <p>Both work. Paper is slower and more hands-on, which many people enjoy. A digital board is easy to change and always with you.</p>
""" + table(["", "Paper board", "Digital board"], [
    ["Feels like", "A craft evening, with scissors and glue", "A quick, tidy collage on your screen"],
    ["Easy to change", "Not very: you re-stick or start again", "Very: drag, swap and save a new version"],
    ["Where you see it", "On a wall, in a notebook, inside a cupboard door", "On your phone lock screen or your desktop"],
    ["Good for", "People who want a break from screens", "People who check their phone often"],
]) + """
      <p>If you prefer the digital route, the <a href="/vision-board-maker/">free vision board maker</a> lets you add your own photos and words, then save a phone wallpaper. If you want your board as an affirmation on your lock screen, try the <a href="/affirmation-wallpaper/">affirmation wallpaper</a>. Both run in your browser and your pictures never leave your device.</p>

      <h2 id="where">Where to put your board</h2>
      <p>A board you never see cannot help you. Put it where your eyes land at least once a day:</p>
      <ul>
        <li><strong>Inside a wardrobe door or on the wall beside your bed.</strong> You see it first thing and last thing, when your mind is quiet.</li>
        <li><strong>Above your desk.</strong> Good for work and learning boards, and it keeps your goals close when you get stuck.</li>
        <li><strong>On the fridge or a bathroom mirror.</strong> Good for health habits and a daily glance.</li>
        <li><strong>As your phone lock screen.</strong> You will see it dozens of times a day.</li>
        <li><strong>Inside your journal.</strong> If your board feels private, tape it to the first page of your notebook and open it whenever you write.</li>
      </ul>
      <p>Take a short look once a month. Tick what has moved, swap out what no longer fits, and write down the next small step. A vision board is allowed to change as you do.</p>

      <h2 id="works">Do vision boards work?</h2>
      <p>A vision board will not make things appear on its own, and we do not want to promise that it will. What it can do is keep your goals in front of you, and help you decide what you actually want. Researchers who study motivation have found that picturing only a perfect outcome can sometimes make people relax and do less. Pairing the picture with the obstacles you expect, and a plan for what you will do about them, tends to work better. That is why step six above asks for a small action beside each image.</p>

      <h2 id="369">Pair your board with the 369 method</h2>
      <p>A board shows you where you are heading. The <a href="/369-method/">369 method</a> is a daily habit that keeps you walking there: write one short sentence 3 times in the morning, 6 times in the afternoon and 9 times at night. Choose one line from your board, such as &ldquo;I keep the promises I make to myself&rdquo;, and write that. If you would like a gentler start, our free <a href="/new-year-manifestation-challenge/">21-day New Year challenge</a> gives you one small task a day. Not sure what to commit to first? Browse <a href="/new-year-resolution-ideas/">100 New Year resolution ideas</a> and pick one to sit beside your board. 369 Journal Pro also has a vision board in the app, if you would like yours with you on your phone.</p>
"""

VFAQ = [
    ("Are these vision board templates free to print?", "Yes. They are free, need no sign-up and run in your browser. Press Print or save as PDF and the sheet prints on its own, without the rest of the page."),
    ("What paper sizes do the templates fit?", "A4 and US Letter, in portrait or landscape. Choose the size and direction in step 2, and the preview shows how the page will look."),
    ("How do I print a template without extra margins or headers?", "In the print window, turn off Headers and footers, set the scale to 100% and choose the same paper size you picked here. To keep a copy, choose Save as PDF instead of a printer."),
    ("What should I put on a vision board?", "Pictures, words and small details that show the life you want in the next year. Start with three to five areas such as career, money, health, love, home or learning, and choose images that make you feel something. Our 100 ideas above give you a place to start."),
    ("How many things should a vision board have?", "Fewer than you think. Five to nine pictures and a few words are plenty. A crowded board is hard to read, and it is easier to keep the ones that matter in mind."),
    ("Do vision boards work?", "A board will not make things happen by itself. It helps you decide what you want and keeps it in sight, and it works best when each picture has a small real action beside it."),
]

VNEXT = next_steps(
    "Turn your board into a daily habit",
    "Put one line from your vision board into the 369 method, and write it every day. Small, steady writing is what keeps a board from becoming wallpaper.",
    "369", "web_vision_templates",
    "Write one line from your board each day",
    "369 Journal reminds you to write your desire morning, afternoon and night, and counts every line. It is free on iPhone and iPad, private, with no account. Your first 21-day cycle is free.",
    "site-vision-templates")

# =====================================================================
# 2. NEW YEAR RESOLUTION IDEAS
# =====================================================================
RP = {
    "path": "/new-year-resolution-ideas/",
    "crumb": "New Year resolution ideas",
    "title": "100 New Year Resolution Ideas for 2027 | 369 Journal",
    "h1": "100 New Year Resolution Ideas for 2027",
    "description": "100 new year resolution ideas for 2027 in ten areas, plus a free picker that turns one into an affirmation, a weekly action and a printable card.",
    "lede": 'Choose one to three life areas and a size, shuffle until one feels right, then turn it into an affirmation, a small weekly action and a one-page card. Below are 100 ideas and honest advice on making one stick.',
    "badges": ["Free, no sign-up", "100 ideas in 10 areas", "Printable resolution card"],
    "published": "2026-11-22",
}

AREA_ORDER = [a for a, _, _ in RESOLUTIONS]
area_chips = "\n".join(
    f'            <label><input type="checkbox" name="rz-area" value="{aid}"><span>{label}</span></label>'
    for aid, label, _ in RESOLUTIONS)
size_seg = seg("rz-size", "Size of resolution",
               [("any", "Any size"), ("t", "Tiny habit"), ("s", "Steady change"), ("b", "Big goal")], "any")

RZ_DATA = json.dumps({"areas": [{"id": aid, "label": label, "items": [list(i) for i in items]}
                                for aid, label, items in RESOLUTIONS]}, ensure_ascii=False).replace("</", "<\\/")

days_html = "".join(f"<li>{i}</li>" for i in range(1, 22))

RBODY = f"""  <section class="tool-shell" data-rz aria-label="New year resolution picker">
    <div class="tool-controls print-hide">
      <div class="tool-panel">
        <fieldset>
          <legend class="t-step"><span class="n">1</span>Choose 1 to 3 areas</legend>
          <div class="t-chips">
{area_chips}
          </div>
        </fieldset>
        <div class="rz-hint-row"><p class="t-hint" data-rz-count>0 of 3 chosen</p><p class="t-hint">Fewer is better: one area is a fine place to start.</p></div>
      </div>

      <div class="tool-panel">
        <fieldset>
          <legend class="t-step"><span class="n">2</span>Choose a size</legend>
          {size_seg}
        </fieldset>
        <p class="rz-size-help"><strong>Tiny habit:</strong> a couple of minutes a day. <strong>Steady change:</strong> a few times a week. <strong>Big goal:</strong> a bigger project that needs weeks or months.</p>
      </div>

      <div class="tool-panel">
        <h2 class="t-step"><span class="n">3</span>Pick one</h2>
        <p class="rz-empty" data-rz-empty>Choose an area above and ideas appear here.</p>
        <ul class="rz-ideas" data-rz-ideas aria-live="polite"></ul>
        <p class="rz-note" data-rz-note hidden></p>
        <div class="rz-shuffle-row"><button type="button" class="btn ghost" data-rz-shuffle hidden>{I_SHUFFLE}Shuffle ideas</button></div>
      </div>

      <div class="tool-panel" data-rz-edit hidden>
        <h2 class="t-step"><span class="n">4</span>Make it yours</h2>
        <div class="rz-edit-grid">
          <div class="t-field"><label class="t-label" for="rz-res">Your resolution</label><input id="rz-res" class="t-input" type="text" maxlength="110" autocomplete="off"></div>
          <div class="t-field"><label class="t-label" for="rz-aff">Your affirmation <span>(present tense)</span></label><textarea id="rz-aff" class="t-textarea" maxlength="160"></textarea></div>
          <div class="t-field"><label class="t-label" for="rz-act">Your weekly tiny action</label><textarea id="rz-act" class="t-textarea" maxlength="200"></textarea></div>
        </div>
        <div style="margin-top:1rem">{privacy("Runs in your browser. What you type is never sent or saved. We only count which areas and size people choose.")}</div>
      </div>
    </div>

    <div class="tool-preview">
      <div class="rz-card is-empty" data-rz-card aria-label="Your 2027 resolution card">
        <div>
          <p class="rz-k">My 2027 resolution</p>
          <h2 class="rz-res" data-c-res tabindex="-1">Your resolution goes here</h2>
        </div>
        <div class="rz-row"><span>I tell myself</span><p class="rz-p rz-aff" data-c-aff>Your affirmation goes here</p></div>
        <div class="rz-row"><span>Each week</span><p class="rz-p" data-c-act>Your weekly action goes here</p></div>
        <div class="rz-row"><span>Why it matters to me</span><div class="rz-lines"></div></div>
        <div class="rz-row"><span>If I miss a day, I will</span><div class="rz-lines"></div></div>
        <div class="rz-row"><span>Write it for 21 days: tick each one</span><ol class="rz-days">{days_html}</ol></div>
        <p class="rz-foot"><span>Start again the next day, with the smallest version.</span><span>369journal.app</span></p>
      </div>
      <div class="rz-actions print-hide">
        <button type="button" class="btn" data-rz-print disabled>{I_PRINT}Print or save as PDF</button>
        <button type="button" class="btn ghost" data-rz-copy disabled>{I_COPY}Copy as text</button>
      </div>
    </div>
  </section>

  <script type="application/json" id="rz-data">{RZ_DATA}</script>"""


def resolution_lists():
    out = []
    for aid, label, items in RESOLUTIONS:
        if aid == "unusual":
            continue
        lis = "\n".join(f'        <li>{e(r)} <span class="rz-tag">{SIZE_LABEL[s]}</span></li>' for s, r, _, _ in items)
        out.append(f'      <h3 id="ideas-{aid}">{label}</h3>\n      <ul class="rz-list">\n{lis}\n      </ul>')
    return "\n".join(out)


unusual = [i for aid, _, items in RESOLUTIONS if aid == "unusual" for i in items]
unusual_html = "\n".join(f'        <li>{e(r)} <span class="rz-tag">{SIZE_LABEL[s]}</span></li>' for s, r, _, _ in unusual)

RARTICLE = f"""      <nav class="toc" aria-label="On this page">
        <strong>On this page</strong>
        <ol>
          <li><a href="#ideas">100 resolution ideas by area</a></li>
          <li><a href="#unusual">Eight unusual but good ones</a></li>
          <li><a href="#why">Why most resolutions fade</a></li>
          <li><a href="#stick">How to make one stick</a></li>
          <li><a href="#vs">Resolution, intention or word of the year?</a></li>
          <li><a href="#after">What to do after you pick</a></li>
        </ol>
      </nav>

      <h2 id="ideas">100 new year resolution ideas, by area</h2>
      <p>Ten areas, ten ideas each. Every idea is tagged <em>tiny habit</em>, <em>steady change</em> or <em>big goal</em>, so you can choose the size that fits the season of life you are in. Most people do better with one small idea than with five big ones. The picker above can shuffle these for you, and it turns your pick into an affirmation and a weekly action.</p>
{resolution_lists()}

      <h2 id="unusual">Eight unusual but good resolutions</h2>
      <p>Not every good resolution is about getting fitter or richer. These are a little different, and they tend to make a year feel fuller. They are in the picker too, under &ldquo;Unusual but good&rdquo;.</p>
      <ul class="rz-list">
{unusual_html}
      </ul>

      <h2 id="why">Why most resolutions fade</h2>
      <p>If your resolutions have faded before, you are in very large company. It is rarely about willpower. A few common reasons:</p>
      <ul>
        <li><strong>Too big, too soon.</strong> &ldquo;Get fit&rdquo; or &ldquo;be a better person&rdquo; does not tell you what to do on a Tuesday evening when you are tired.</li>
        <li><strong>Too many at once.</strong> Five resolutions share one supply of energy. When life gets busy, all five go together.</li>
        <li><strong>No plan for the hard days.</strong> Many people treat one missed day as proof they have failed, and quit. Psychologists sometimes call this the &ldquo;what the hell&rdquo; effect.</li>
        <li><strong>It is about what you should do, not what you want.</strong> A resolution borrowed from someone else is easy to drop.</li>
        <li><strong>Nobody sees it, including you.</strong> A goal kept only in your head slips out of sight within weeks.</li>
      </ul>
      <p>The kind side of this: habits are built, and the time they take varies a lot from person to person and from habit to habit. A well-known study of everyday habits found people took anywhere from a few weeks to many months. So a slow start is normal, and a missed day is not the end.</p>

      <h2 id="stick">How to make a resolution stick</h2>
      <ol>
        <li><strong>Choose one.</strong> Put your energy into a single resolution for the first month. You can add a second one later, once the first feels easy.</li>
        <li><strong>Shrink the daily action.</strong> Pick a version so small it feels almost silly: two minutes, ten pages, one glass of water. You can always do more on a good day.</li>
        <li><strong>Tie it to something you already do.</strong> Researchers call a plan like &ldquo;When I make my morning tea, I will stretch for two minutes&rdquo; an implementation intention, and it tends to help more than a vague wish.</li>
        <li><strong>Write it down every day.</strong> A line in a notebook, or the 369 method of writing it 3, 6 and 9 times. Writing keeps it in front of you and tells your mind that this one matters.</li>
        <li><strong>Track it.</strong> A row of ticks on your resolution card gives you something to see. Seeing a chain of days is encouraging, and a small gap is easy to spot.</li>
        <li><strong>Plan for missed days.</strong> Decide ahead what you will do: &ldquo;If I miss a day, I do the two-minute version the next day.&rdquo; Aim never to miss twice in a row, rather than never to miss at all.</li>
        <li><strong>Tell one person.</strong> A friend who asks how it is going can help more than a long list of rules.</li>
        <li><strong>Review monthly.</strong> If a resolution is not working after a month of honest effort, make it smaller or change it. That is learning, not failing.</li>
      </ol>

      <h2 id="vs">Resolution, intention or word of the year?</h2>
      <p>These three are cousins, and you can use more than one. Here is how they differ:</p>
""" + table(["", "What it is", "Example", "Best for"], [
    ["Resolution", "A specific thing you will do", "Walk for ten minutes after lunch", "A clear habit you can tick off"],
    ["Intention", "How you want to move through the year", "I want to approach my days with more patience", "Mood and attitude, when a tick-box feels too rigid"],
    ["Word of the year", "One word that guides your choices", "Steady", "A theme that can sit above several resolutions"],
]) + """
      <p>A simple combination: choose a <a href="/word-of-the-year/">word of the year</a> for the direction, and one small resolution for the daily action. The picker above gives you the second. The <a href="/word-of-the-year/">Word of the Year finder</a> helps with the first.</p>

      <h2 id="after">What to do after you pick one</h2>
      <ul>
        <li><strong>Turn it into a sentence.</strong> The picker gives you a present-tense affirmation. For more wording ideas, try the <a href="/affirmation-generator/">affirmation generator</a>.</li>
        <li><strong>Make a short start.</strong> Our free <a href="/new-year-manifestation-challenge/">21-day New Year challenge</a> gives you one small task a day, and 21 days is long enough to feel a habit take shape. It is a good first stretch, not a magic number.</li>
        <li><strong>Write to your future self.</strong> A <a href="/letter-to-future-self/">letter to your future self</a> that you open in December makes a good check-in, and a reminder of why you started.</li>
        <li><strong>See it every day.</strong> Print your card and put it on the fridge, or add it to a <a href="/vision-board-templates/">printable vision board</a>.</li>
        <li><strong>Write it daily.</strong> The <a href="/369-method/">369 method</a> is a simple way: write your resolution as an affirmation 3 times in the morning, 6 in the afternoon and 9 at night.</li>
      </ul>
"""

RFAQ = [
    ("What are good New Year resolutions for 2027?", "The best resolution is one you can picture doing on a normal, tired Tuesday. Good ones are small and specific, such as a ten-minute walk after lunch, ten pages of a book a day, or a weekly look at your bank balance. Browse the 100 ideas above, or use the picker to shuffle them."),
    ("How many resolutions should I make?", "One to start with. You can add a second once the first feels natural, usually after a month or so. Three resolutions that all need willpower at the same time usually compete with each other."),
    ("How do I make a resolution stick?", "Shrink the daily action until it is almost too easy, tie it to something you already do, write it down every day, track it, and plan what you will do when you miss a day. Aim never to miss twice in a row."),
    ("What if I have already broken my resolution?", "Start again today, with a smaller version. A missed day or even a missed week does not cancel the effort you put in. Ask what made it hard, then change the plan, not yourself."),
    ("Is the resolution picker free and private?", "Yes. It is free, needs no sign-up and runs in your browser. What you type is never sent or saved. We only count which areas and size people choose."),
    ("What is the difference between a goal and a resolution?", "A goal is the result you want, such as running a 10K. A resolution is the promise you make to yourself, often a habit that leads to the goal, such as running three times a week. The tiny habit and steady change sizes in the picker are habit-style resolutions. Big goals are results to work towards."),
]

RNEXT = next_steps(
    "Write your resolution for 21 days",
    "A resolution grows when you see it every day. Pick one, write it daily for 21 days, and tick the days off on your card.",
    "369", "web_resolutions",
    "Make your resolution a 21-day habit",
    "369 Journal reminds you to write your resolution morning, afternoon and night, and counts every line. It is free on iPhone and iPad, private, with no account. Your first 21-day cycle is free.",
    "site-resolutions")

if __name__ == "__main__":
    write(VP["path"], tool_page(VP, VFAQ, VBODY, js="vision-templates.js", css="vision-templates.css", article=VARTICLE, next_html=VNEXT))
    write(RP["path"], tool_page(RP, RFAQ, RBODY, js="resolutions.js", css="resolutions.css", article=RARTICLE, next_html=RNEXT))
    for p in (VP, RP):
        print(len(p["title"]), p["title"])
        print(len(p["description"]), p["description"])

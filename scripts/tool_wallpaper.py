#!/usr/bin/env python3
"""Affirmation wallpaper maker: /affirmation-wallpaper/

Run:  cd scripts && python3 tool_wallpaper.py && python3 layout.py
Logic: /assets/tools/wallpaper.js (canvas, runs only in the browser).
"""
from toolkit import next_steps, privacy, tool_page, write

P = {
    "path": "/affirmation-wallpaper/",
    "crumb": "Affirmation wallpaper maker",
    "title": "Free Affirmation Wallpaper Maker (iPhone, Android) | 369 Journal",
    "h1": "Affirmation Wallpaper Maker",
    "description": "Make a free affirmation wallpaper for your iPhone or Android lock screen or desktop. Pick a calm style and download it in full resolution. No sign-up.",
    "lede": "Put the words you want to live by on the screen you check a hundred times a day. Write your affirmation, choose a style, and download a sharp, full-resolution wallpaper for your phone or computer.",
    "badges": ["Free", "No sign-up", "Full resolution", "iPhone, Android and desktop"],
}

STYLES = [("paper", "Paper"), ("midnight", "Midnight"), ("dusk", "Dusk"), ("sage", "Sage"), ("minimal", "Minimal"), ("dots", "3 · 6 · 9")]

SPARK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 1.5v3M8 11.5v3M1.5 8h3M11.5 8h3M3.4 3.4l2 2M10.6 10.6l2 2M3.4 12.6l2-2M10.6 5.4l2-2"/></svg>'
DOWN = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2v8.5M4.5 7 8 10.5 11.5 7M2.5 13.5h11"/></svg>'
PHOTO = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="3" width="12" height="10" rx="2"/><circle cx="6" cy="7" r="1.3"/><path d="m3 12 3.5-3 2.5 2 2-1.5 2.5 2"/></svg>'


def radios(name, items, checked):
    return "".join(
        f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{t}</span></label>'
        for v, t in items)


SWATCHES = "\n".join(
    f'            <label class="swatch"><input type="radio" name="wp-style" value="{v}"{" checked" if i == 0 else ""}><span><i class="sw-{v}"></i>{t}</span></label>'
    for i, (v, t) in enumerate(STYLES))

BODY = f"""  <div class="tool-shell" data-wallpaper>
    <div class="tool-controls print-hide">
      <section class="tool-panel" aria-labelledby="wp-s1">
        <h2 class="t-step" id="wp-s1"><span class="n">1</span>Your affirmation</h2>
        <label class="t-label" for="wp-text">Words for your wallpaper</label>
        <textarea id="wp-text" class="t-textarea" maxlength="140" rows="3" placeholder="I am calm, clear and steady."></textarea>
        <div class="wp-text-row">
          <button id="wp-inspire" class="t-link-btn wp-inspire" type="button">{SPARK}Inspire me</button>
          <span id="wp-count" class="wp-count" aria-live="polite"></span>
        </div>
      </section>

      <section class="tool-panel" aria-labelledby="wp-s2">
        <h2 class="t-step" id="wp-s2"><span class="n">2</span>Style</h2>
        <fieldset>
          <legend class="visually-hidden">Colour style</legend>
          <div class="swatches">
{SWATCHES}
          </div>
        </fieldset>
        <div class="wp-row" style="margin-top:1.3rem">
          <span class="t-label" id="wp-font-l">Font</span>
          <div class="seg" role="radiogroup" aria-labelledby="wp-font-l">{radios("wp-font", [("serif", "Serif"), ("sans", "Sans")], "serif")}</div>
        </div>
        <div class="wp-row">
          <span class="t-label" id="wp-pos-l">Text position</span>
          <div class="seg" role="radiogroup" aria-labelledby="wp-pos-l">{radios("wp-pos", [("middle", "Middle"), ("lower", "Lower")], "middle")}</div>
        </div>
      </section>

      <section class="tool-panel" aria-labelledby="wp-s3">
        <h2 class="t-step" id="wp-s3"><span class="n">3</span>Size</h2>
        <div class="seg" role="radiogroup" aria-labelledby="wp-s3">{radios("wp-size", [("iphone", "iPhone"), ("android", "Android"), ("desktop", "Desktop")], "iphone")}</div>
        <label class="wp-toggle"><input id="wp-mark" type="checkbox" checked> Small 369journal.app mark at the bottom</label>
      </section>
      {privacy("Made in your browser. Your words are never uploaded or saved.")}
    </div>

    <div class="tool-preview">
      <div class="preview-stage wp-stage">
        <div id="wp-device" class="wp-device" data-size="iphone" data-tone="dark">
          <canvas id="wp-canvas" width="1179" height="2556" role="img" aria-label="Preview of your affirmation wallpaper"></canvas>
          <div class="wp-lock" aria-hidden="true"><span id="wp-date" class="wp-date"></span><span id="wp-time" class="wp-time"></span></div>
        </div>
      </div>
      <p class="wp-legend">The clock is only a preview. It isn&rsquo;t part of your download.</p>
      <div class="preview-actions">
        <button id="wp-share" class="btn clay" type="button" hidden>{PHOTO}Save to Photos</button>
        <button id="wp-download" class="btn" type="button">{DOWN}Download wallpaper</button>
      </div>
      <p class="wp-how"><strong>iPhone:</strong> Settings &rarr; Wallpaper &rarr; Add New. <strong>Android:</strong> long-press your home screen &rarr; Wallpaper.</p>
    </div>
  </div>"""

ARTICLE = """      <h2 id="set-iphone">How to set an affirmation wallpaper on iPhone</h2>
      <ol>
        <li>Make your wallpaper above and tap <strong>Save to Photos</strong> (or <strong>Download wallpaper</strong>, then save it from Files).</li>
        <li>Open <strong>Settings &rarr; Wallpaper &rarr; Add New Wallpaper &rarr; Photos</strong> and pick it.</li>
        <li>Pinch to position it if you like, then tap <strong>Add</strong>. Choose <strong>Set as Wallpaper Pair</strong> to use it on both screens.</li>
      </ol>
      <p>Tip: you can link a Lock Screen to a <strong>Focus</strong> (for example Work or Sleep), so a calm affirmation shows up only at the times you want it.</p>

      <h2 id="set-android">How to set it on Android</h2>
      <ol>
        <li>Download the Android size above. It saves to your Downloads or Photos.</li>
        <li>Long-press an empty part of your home screen and tap <strong>Wallpaper &amp; style</strong> (the name varies by phone).</li>
        <li>Choose the image and set it for the lock screen, home screen or both.</li>
      </ol>

      <h2 id="wording">How to word an affirmation for your lock screen</h2>
      <ul>
        <li><strong>Present tense:</strong> &ldquo;I am calm&rdquo;, not &ldquo;I will be calm&rdquo;.</li>
        <li><strong>Positive:</strong> say what you want, not what you want to avoid.</li>
        <li><strong>Short:</strong> under 12 words reads at a glance. Long sentences shrink and get lost behind the clock.</li>
        <li><strong>Believable:</strong> if it makes you roll your eyes, soften it until it feels true enough.</li>
      </ul>
      <p>Stuck for words? The <a href="/affirmation-generator/">free affirmation generator</a> gives you ideas for money, love, health, calm and more. Want just one word? <a href="/word-of-the-year/">Find your Word of the Year</a> and save it as a lock screen.</p>

      <h2 id="why">Why put an affirmation on your wallpaper?</h2>
      <p>Most of us unlock our phone dozens of times a day. A short line on the lock screen turns some of those moments into a quick reminder of what you are working toward. It won&rsquo;t change anything by itself, and we won&rsquo;t pretend it does, but a reminder you can&rsquo;t miss makes it easier to stay focused and take the next small step.</p>

      <h2 id="369">Pair it with the 369 method</h2>
      <p>Seeing an affirmation is one thing; writing it is another. With the <a href="/369-method/">369 method</a> you write the same line 3 times in the morning, 6 in the afternoon and 9 at night. Using the same words on your wallpaper keeps it in front of you between sessions. Want photos too? Try the <a href="/vision-board-maker/">vision board maker</a>.</p>
"""

FAQ = [
    ("Is the affirmation wallpaper maker free?", "Yes. It is free, needs no sign-up, and the image is made in your browser. Your words are never uploaded or saved."),
    ("What size is the iPhone wallpaper?", "The iPhone size is 1179 by 2556 pixels, which fits current iPhones sharply. There is also an Android size (1080 by 2400) and a desktop size (2560 by 1440)."),
    ("Will the clock cover my affirmation?", "No. The text sits below the area where the lock screen clock and date appear. The preview shows a sample clock so you can check before you download."),
    ("How do I save the wallpaper to Photos on iPhone?", "Tap Save to Photos, then choose Save Image in the share sheet. If you only see Download, open the file from the Files app and share it to Photos."),
    ("Can I use my own affirmation?", "Yes. Type any words you like, up to 140 characters. Short lines of under 12 words look best on a lock screen."),
    ("What should my affirmation say?", "Something short, positive and in the present tense that feels believable, such as “I am calm, clear and steady.” Tap Inspire me for ideas, or use the affirmation generator."),
]

NEXT = next_steps(
    "See it, then write it",
    "A wallpaper keeps your words in sight. Writing them every day turns them into a habit you can feel.",
    "369", "web_wallpaper",
    "Write it 3, 6 and 9 times a day",
    "369 Journal reminds you morning, afternoon and night, counts every line, and adds Home Screen widgets that show today&rsquo;s ritual. Your first 21-day cycle is free.",
    "site-wallpaper",
)

if __name__ == "__main__":
    write(P["path"], tool_page(P, FAQ, BODY, js="wallpaper.js", css="wallpaper.css", article=ARTICLE, next_html=NEXT))

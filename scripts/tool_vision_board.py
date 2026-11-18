#!/usr/bin/env python3
"""Builds /vision-board-maker/.  Run: cd scripts && python3 tool_vision_board.py"""
from toolkit import tool_page, next_steps, privacy, write

P = {
    "path": "/vision-board-maker/",
    "crumb": "Vision board maker",
    "title": "Free Vision Board Maker: Phone Wallpaper or Print | 369 Journal",
    "h1": "Free Vision Board Maker",
    "description": "Make a free digital vision board with your photos and words, then save it as a phone wallpaper, desktop background or printable board. No sign-up.",
    "lede": "Add your own photos and a few words, pick a layout, and save it as a phone wallpaper, a desktop background or a board to print. Your photos never leave your device.",
    "badges": ["Free, no sign-up", "Photos stay on your device", "Phone, desktop and print sizes"],
}

FORMATS = [("phone", "Phone"), ("print", "Print"), ("desktop", "Desktop"), ("square", "Square")]
LAYOUTS = [("mosaic", "Mosaic"), ("grid", "Grid"), ("focus", "Focus")]
THEMES = [("paper", "Paper", "#f6efe6", "#e3cdb4"), ("midnight", "Midnight", "#14131a", "#d9b46a"),
          ("sage", "Sage", "#e8ece2", "#c7d3bd"), ("blush", "Blush", "#f7ebe7", "#e8c7be"),
          ("mono", "Mono", "#fbfbfa", "#111111")]
WORDSETS = [("2027", "2027"), ("money", "Money"), ("love", "Love"), ("health", "Health"),
            ("career", "Career"), ("home", "Home"), ("calm", "Calm"), ("travel", "Travel")]


def seg(name, items, checked):
    return '<div class="seg" role="radiogroup">' + "".join(
        f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{t}</span></label>'
        for v, t in items) + "</div>"


swatches = '<div class="swatches vb-swatches">' + "".join(
    f'<label class="swatch"><input type="radio" name="vb-theme" value="{v}"{" checked" if v == "paper" else ""}>'
    f'<span><i style="background:{bg};--tile:{tile}"></i>{t}</span></label>' for v, t, bg, tile in THEMES) + "</div>"
words = '<div class="vb-words">' + "".join(
    f'<button type="button" data-words="{v}" aria-pressed="{"true" if v == "2027" else "false"}">{t}</button>' for v, t in WORDSETS) + "</div>"

DOWNLOAD = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 3v10"/><path d="m5.5 8.5 4.5 4.5 4.5-4.5"/><path d="M4 16.5h12"/></svg>'

BODY = f"""    <section class="tool-shell" data-vision aria-label="Vision board maker">
      <div class="tool-controls">
        <div class="tool-panel">
          <h2 class="t-step"><span class="n">1</span>Size and layout</h2>
          <div class="t-field"><span class="t-label">Size</span>{seg("vb-format", FORMATS, "phone")}</div>
          <div class="t-field"><span class="t-label">Layout</span>{seg("vb-layout", LAYOUTS, "mosaic")}</div>
          <div class="t-field"><span class="t-label">Style</span>{swatches}</div>
        </div>

        <div class="tool-panel">
          <h2 class="t-step"><span class="n">2</span>Photos and words</h2>
          <p class="t-hint" style="margin:0 0 .8rem">Start from a set of words, then swap any tile for your own photo. Tap a tile in the preview to edit it, or drop photos onto it.</p>
          {words}
          <ol class="vb-tiles" id="vb-tiles" aria-label="Tiles"></ol>
          <div class="vb-add">
            <label class="btn small">Add several photos<input id="vb-multi" type="file" accept="image/*" multiple hidden></label>
            <span class="t-hint" style="margin:0">They fill the empty tiles in order.</span>
          </div>
        </div>

        <div class="tool-panel">
          <h2 class="t-step"><span class="n">3</span>Title</h2>
          <div class="t-field"><label class="t-label" for="vb-title">Title</label><input id="vb-title" class="t-input" type="text" maxlength="32" value="2027"></div>
          <div class="t-field"><label class="t-label" for="vb-subtitle">Line under it <span>(optional)</span></label><input id="vb-subtitle" class="t-input" type="text" maxlength="60" value="The year it comes together"></div>
          <label class="vb-check"><input id="vb-mark" type="checkbox" checked>Small 369journal.app mark at the bottom</label>
        </div>
        {privacy("Runs in your browser. Your photos are never uploaded, and nothing is saved after you close the page.")}
      </div>

      <div class="tool-preview">
        <div class="preview-stage">
          <canvas id="vb-canvas" role="img" aria-label="Live preview of your vision board"></canvas>
        </div>
        <p class="preview-caption" id="vb-size">Phone wallpaper</p>
        <div class="preview-actions">
          <button id="vb-download" class="btn" type="button">{DOWNLOAD}Download</button>
          <button id="vb-share" class="btn clay" type="button" hidden>Save to Photos</button>
          <button id="vb-print" class="btn ghost" type="button">Print</button>
        </div>
      </div>
    </section>
    <div class="vb-print" aria-hidden="true"><img id="vb-print-img" alt=""></div>
"""

ARTICLE = """      <h2 id="how">How to make a vision board that you&rsquo;ll actually look at</h2>
      <ol>
        <li><strong>Pick one season of life.</strong> A vision board for the next year works better than one for &ldquo;someday&rdquo;.</li>
        <li><strong>Choose 5 to 8 tiles, not 30.</strong> A few clear pictures are easier to remember than a crowded collage.</li>
        <li><strong>Mix photos with short words.</strong> A photo shows the feeling; three or four words name it.</li>
        <li><strong>Use your own photos when you can.</strong> A picture of your own street, desk or running shoes feels more real than a stock image.</li>
        <li><strong>Put it where you&rsquo;ll see it every day.</strong> Your phone&rsquo;s lock screen is the place most people look at most often.</li>
      </ol>

      <h2 id="ideas">Vision board ideas</h2>
      <ul>
        <li><strong>Money:</strong> a savings number you&rsquo;re working toward, a calm desk, &ldquo;paid well for good work&rdquo;.</li>
        <li><strong>Health:</strong> your trainers by the door, a full water bottle, &ldquo;deep sleep&rdquo;.</li>
        <li><strong>Love and friendship:</strong> a table set for friends, &ldquo;kind, steady love&rdquo;.</li>
        <li><strong>Career:</strong> the kind of work you want to make, &ldquo;confident voice&rdquo;.</li>
        <li><strong>Home and travel:</strong> the light you want in your home, one place you want to see.</li>
      </ul>

      <h2 id="use">How to use it every day</h2>
      <p>A vision board is a reminder, not a spell. It works best when you look at it on purpose for a few seconds and then do one small thing that points toward it. Many people pair it with a short written ritual such as the <a href="/369-method/">369 method</a>: one affirmation written 3, 6 and 9 times a day. Need words for yours? Try the <a href="/affirmation-generator/">free affirmation generator</a>.</p>
      <p>Making one for the new year? Put <a href="/word-of-the-year/">your Word of the Year</a> in the middle of the board, and use our <a href="/new-year-manifestation-challenge/">21-day New Year challenge</a> for one small task a day to go with it.</p>
"""

FAQ = [
    ("Is this vision board maker really free?", "Yes. There is no sign-up, no watermark you can't turn off and no paid version. You can download as many boards as you like."),
    ("Are my photos uploaded anywhere?", "No. Your photos are opened directly in your browser to draw the board and are never sent to a server. When you close the page, they're gone."),
    ("What size should a vision board wallpaper be?", "The phone size here is 1179 by 2556 pixels, which fits current iPhones and most Android phones. The top of the board is left clear so the lock-screen clock doesn't cover your photos."),
    ("Can I print my vision board?", "Yes. Choose the Print size for a 2:3 board, then use Print, or download the image and print it at any photo shop. It also works as a Pinterest pin."),
    ("How do I set my vision board as my lock screen?", "Download it, or tap Save to Photos on iPhone. Then open the Photos app, tap the share button and choose Use as Wallpaper. On Android, open the image and choose Set as wallpaper."),
    ("Do vision boards work?", "There's no evidence that a picture makes things happen by itself. What a vision board can do is keep your goals in front of you, which makes it easier to notice chances and act on them. Use it alongside small, real steps."),
]

NEXT = next_steps(
    "Keep your vision in front of you",
    "A board shows where you&rsquo;re going. A short daily ritual keeps you moving toward it.",
    "369", "web_vision_board",
    "Add a vision board to your daily 369 ritual",
    "369 Journal reminds you to write your desire morning, afternoon and night, with a vision board alongside it in 369 Pro. Your first 21-day cycle is free.",
    "site-vision-board")

if __name__ == "__main__":
    write(P["path"], tool_page(P, FAQ, BODY, js="vision-board.js", css="vision-board.css", article=ARTICLE, next_html=NEXT))

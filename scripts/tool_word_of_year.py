#!/usr/bin/env python3
"""Builds /word-of-the-year/.  Run: cd scripts && python3 tool_word_of_year.py && python3 layout.py"""
from toolkit import tool_page, next_steps, privacy, write

P = {
    "path": "/word-of-the-year/",
    "crumb": "Word of the Year",
    "title": "Word of the Year Generator: Find Your 2027 Word | 369 Journal",
    "h1": "Find Your Word of the Year",
    "description": "Answer five quick questions to find your word for 2027, with its meaning, an affirmation and a lock-screen image. Plus 60 word of the year ideas. Free.",
    "lede": "Five quick questions, one word to guide your 2027. Get its meaning, an affirmation and a small daily action, then save it as your lock screen.",
    "badges": ["Free, no sign-up", "Five questions, one minute", "Lock-screen image included"],
}

THEMES = [("paper", "Paper", "linear-gradient(160deg,#fbf6ee,#efe2d0)"), ("midnight", "Midnight", "linear-gradient(160deg,#1b1a24,#0f0e14)"),
          ("clay", "Clay", "linear-gradient(160deg,#c46a43,#8f4426)"), ("sage", "Sage", "linear-gradient(160deg,#e9eee3,#cfdac6)")]
swatches = '<div class="swatches">' + "".join(
    f'<label class="swatch"><input type="radio" name="woty-theme" value="{v}"{" checked" if v == "paper" else ""}>'
    f'<span><i style="background:{bg}"></i>{t}</span></label>' for v, t, bg in THEMES) + "</div>"
sizes = '<div class="seg" role="radiogroup" aria-label="Image size">' + "".join(
    f'<label><input type="radio" name="woty-size" value="{v}"{" checked" if v == "phone" else ""}><span>{t}</span></label>'
    for v, t in [("phone", "Phone"), ("square", "Square")]) + "</div>"

DOWNLOAD = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 3v10"/><path d="m5.5 8.5 4.5 4.5 4.5-4.5"/><path d="M4 16.5h12"/></svg>'

BODY = f"""    <section class="tool-shell" data-woty aria-label="Word of the Year finder">
      <div class="tool-controls">
        <div class="tool-panel woty-quiz" data-quiz>
          <div class="woty-progress" aria-hidden="true"><i data-q-bar></i></div>
          <p class="woty-count" data-q-count>Question 1 of 5</p>
          <h2 class="woty-q" data-q-text tabindex="-1" aria-live="polite">How did 2026 feel, mostly?</h2>
          <div class="woty-opts" data-q-opts role="group" aria-label="Answers"></div>
          <div class="woty-quiz-foot">
            <button type="button" class="t-link-btn" data-back hidden>Back</button>
            <span class="t-hint" style="margin:0">Pick the answer that feels closest.</span>
          </div>
        </div>

        <div class="tool-panel woty-result" data-result hidden aria-live="polite">
          <div>
            <p class="woty-word-label">Your word for 2027</p>
            <h2 class="woty-word" data-r-word tabindex="-1">Begin</h2>
            <p class="woty-meaning" data-r-meaning></p>
          </div>
          <dl class="woty-rows">
            <div class="aff"><dt>Affirmation</dt><dd data-r-aff>Five questions. One word for your year.</dd></div>
            <div><dt>One small thing a day</dt><dd data-r-action></dd></div>
            <div><dt>Journal prompt</dt><dd data-r-prompt></dd></div>
          </dl>
          <div data-alts-wrap>
            <p class="t-label">Close matches</p>
            <div class="woty-alts" data-r-alts></div>
          </div>
          <div class="woty-actions-row">
            <button type="button" class="btn ghost small" data-copy>Copy word and affirmation</button>
            <button type="button" class="t-link-btn" data-retake>Take the quiz again</button>
          </div>
        </div>

        <div class="tool-panel">
          <h2 class="t-step"><span class="n">+</span>Already have a word?</h2>
          <form class="woty-own" data-own-form>
            <label class="sr-only" for="woty-own">Your own word</label>
            <input id="woty-own" class="t-input" type="text" maxlength="18" placeholder="Type your word" autocomplete="off">
            <button class="btn small" type="submit">Use it</button>
          </form>
          <p class="t-label" style="margin-top:1.1rem">Or browse all 36 words</p>
          <div class="woty-all" data-all></div>
        </div>
        {privacy("Runs in your browser. Your answers and any word you type are never sent or saved. We only count which word from our list people land on.")}
      </div>

      <div class="tool-preview">
        <div class="preview-stage">
          <canvas id="woty-canvas" role="img" aria-label="Preview of your Word of the Year image"></canvas>
        </div>
        <p class="preview-caption" data-size-label>Phone wallpaper, 1179 × 2556</p>
        <div class="t-field" style="justify-self:center;text-align:center">{sizes}</div>
        <div style="justify-self:center">{swatches}</div>
        <label class="woty-check" style="justify-self:center"><input id="woty-mark" type="checkbox" checked>Small 369journal.app mark</label>
        <div class="preview-actions">
          <button id="woty-download" class="btn" type="button">{DOWNLOAD}Download</button>
          <button id="woty-share" class="btn clay" type="button" hidden>Save to Photos</button>
        </div>
      </div>
    </section>
"""

IDEAS = [
    ("Calm and rest", "Peace, Ease, Slow, Rest, Still, Gentle, Simple, Breathe, Soft, Present"),
    ("Growth and success", "Rise, Expand, Build, Focus, Grow, Level up, Bloom, Momentum, Thrive, Achieve"),
    ("Courage and confidence", "Brave, Bold, Worthy, Voice, Fearless, Trust, Begin, Leap, Own, Shine"),
    ("Love and connection", "Open, Together, Tender, Kind, Belong, Connect, Love, Home, Heart, Family"),
    ("Money and security", "Abundance, Steady, Enough, Secure, Wealth, Prosper, Save, Invest, Overflow, Provide"),
    ("Freedom and joy", "Free, Light, Play, Explore, Curious, Savor, Joy, Adventure, Delight, Grateful"),
]

IDEAS_HTML = "\n".join(
    f"        <li><strong>{group}:</strong> {words}.</li>" for group, words in IDEAS)

ARTICLE = f"""      <h2 id="what">What is a Word of the Year?</h2>
      <p>A Word of the Year is a single word you choose to guide the next twelve months. Instead of a long list of resolutions, you keep one word in mind and let it shape small daily choices. &ldquo;Brave&rdquo; might mean sending the email you&rsquo;ve been avoiding. &ldquo;Rest&rdquo; might mean saying no to one more plan. It&rsquo;s easy to remember, so it tends to last longer than a resolution.</p>

      <h2 id="ideas">Word of the Year ideas</h2>
      <p>Here are 60 words people often choose, grouped by what they want more of. Read them slowly and notice which one makes you sit up a little.</p>
      <ul>
{IDEAS_HTML}
      </ul>

      <h2 id="choose">How to choose your word</h2>
      <ol>
        <li><strong>Look back first.</strong> What did this year teach you? What do you not want to repeat?</li>
        <li><strong>Name the feeling you want.</strong> Think about how you want to feel on 31 December 2027, not just what you want to have.</li>
        <li><strong>Find what gets in your way.</strong> Your word often answers your biggest obstacle: overthinkers pick &ldquo;trust&rdquo;, people-pleasers pick &ldquo;enough&rdquo;.</li>
        <li><strong>Shortlist three, then sleep on it.</strong> The right word usually feels a little uncomfortable and a little exciting.</li>
        <li><strong>Test it with one question:</strong> &ldquo;What would [my word] look like today?&rdquo; If the answer is clear, you&rsquo;ve found it.</li>
      </ol>

      <h2 id="use">How to use your word every day</h2>
      <ul>
        <li><strong>Put it where you&rsquo;ll see it.</strong> Save your word as your lock screen above, or make a longer <a href="/affirmation-wallpaper/">affirmation wallpaper</a>.</li>
        <li><strong>Turn it into an affirmation.</strong> &ldquo;In 2027, I choose to be brave&rdquo; is something you can write daily. The <a href="/369-method/">369 method</a> is a simple way: write it 3 times in the morning, 6 in the afternoon and 9 at night.</li>
        <li><strong>Add it to a vision board.</strong> Put your word in the middle of a <a href="/vision-board-maker/">vision board</a> and surround it with pictures of what it looks like.</li>
        <li><strong>Check in monthly.</strong> Ask: where did my word show up this month, and where did I forget it? A <a href="/journal-prompt-generator/">journal prompt</a> helps on days you don&rsquo;t know what to write.</li>
        <li><strong>Go deeper.</strong> Some people pair their word with their <a href="/numerology-calculator/">2027 personal year number</a>. If your word is &ldquo;grateful&rdquo; or &ldquo;savor&rdquo;, our <a href="/gratitude-journal-prompts/">gratitude journal prompts</a> give you something to write each day.</li>
        <li><strong>Start with a short challenge.</strong> Our free <a href="/new-year-manifestation-challenge/">21-day New Year challenge</a> gives you one small task a day to build the habit.</li>
      </ul>
"""

FAQ = [
    ("What is a Word of the Year?", "It is one word you choose to guide the year ahead, instead of a list of resolutions. You use it to make small daily choices, like asking each morning what your word would look like today."),
    ("How do I choose my Word of the Year?", "Look back at this year, name how you want to feel at the end of next year, and think about what usually gets in your way. Shortlist three words and pick the one that feels a little exciting and a little uncomfortable. The five-question quiz above does this for you."),
    ("Is this Word of the Year generator free?", "Yes. There is no sign-up and no email. Your answers and any word you type stay in your browser and are never sent or saved."),
    ("Can I use my own word?", "Yes. Type it into the Already have a word box and the lock-screen image updates with your word."),
    ("What if my word stops fitting halfway through the year?", "That's fine. Some people keep the word and look at it from a new angle, others choose a new one in July. The point is to have something that helps you choose, not a rule."),
    ("How is a Word of the Year different from a resolution?", "A resolution is usually a single outcome, like losing weight, and it is easy to break. A word is a direction. You can't fail at it, you just come back to it."),
]

NEXT = next_steps(
    "Live your word every day",
    "A word is a direction. A short daily ritual keeps you walking in it.",
    "369", "web_word_of_year",
    "Write your word into a daily ritual",
    "369 Journal reminds you to write your desire morning, afternoon and night, and counts every line. Your first 21-day cycle is free.",
    "site-word-of-year")

if __name__ == "__main__":
    write(P["path"], tool_page(P, FAQ, BODY, js="word-of-year.js", css="word-of-year.css", article=ARTICLE, next_html=NEXT))

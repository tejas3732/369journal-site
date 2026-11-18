#!/usr/bin/env python3
"""Builds /journal-prompt-generator/.

Run:  cd scripts && python3 tool_prompts.py && python3 layout.py
Prompts live here (one source): they are embedded as JSON for /assets/tools/prompts.js
and a subset is printed as static lists in the article for search engines.
All prompts are written for the site, not taken from the books (Kindle is in KDP Select).
"""
import html
import json

from toolkit import next_steps, privacy, tool_page, write

CATEGORIES = [
    ("manifestation", "Manifestation", [
        "What is the one thing you most want to bring into your life this month, and why does it matter to you?",
        "Describe your desire in one sentence, as if it is already true. How does reading it back feel?",
        "What would change in an ordinary Tuesday if your desire came true?",
        "Which small sign of progress did you notice this week, even if it seemed like a coincidence?",
        "What belief about this goal feels heavy right now? Write a kinder version of it.",
        "If you trusted that this was on its way, what would you stop worrying about today?",
        "What is one action, five minutes or less, that points you toward your desire today?",
        "Who do you need to become to hold this desire comfortably? Describe one of their habits.",
        "What are you already grateful for that is connected to what you want?",
        "Where in your life do you already have a small version of what you want?",
        "What would you do differently this week if you knew it would work out?",
        "Write about a time something you wanted did come true. What helped?",
        "What are you willing to let go of to make room for this desire?",
        "How do you want to feel when this comes true? Where can you find a little of that feeling today?",
        "What would the version of you who already has this say to you this morning?",
        "What doubt keeps coming back? Answer it calmly, like a good friend would.",
        "List three things that would tell you that you are moving in the right direction.",
        "What does 'enough' look like for this desire? Describe it plainly.",
        "Which part of your desire is about the thing itself, and which part is about a feeling?",
        "What is one thing you can do today that your future self will thank you for?",
    ]),
    ("scripting", "Scripting", [
        "Write one ordinary moment from the morning after your desire came true. Where are you, and what do you see first?",
        "Start with “I remember when…” and describe the day you knew it had worked.",
        "Script a phone call where you tell someone close to you the good news. What do they say?",
        "Write about an ordinary evening in your life a year from now. Include one sound and one smell.",
        "Describe walking into the place you have been hoping for: the new home, office or studio.",
        "Script the moment you check your bank account and feel calm. What do you do next?",
        "Write a short scene of you handling a challenge with ease, the way you want to.",
        "Describe a quiet Sunday morning in the life you are building. Who is there?",
        "Write the message you send a friend after your desire comes true. Keep it short and real.",
        "Script one minute of your day as the person you are becoming. What are your hands doing?",
        "Start with “It still surprises me that…” and write about your desire as a settled fact.",
        "Describe the first small thing you buy or do to celebrate. Why that?",
        "Write a scene from a normal workday in the job or project you want.",
        "Script a conversation where someone compliments the change in you. How do you answer?",
        "Describe what you notice about your body: your shoulders, your breathing, your face.",
        "Write the diary entry you would write on the day it happened.",
        "Script your evening routine in the life you want, from dinner to bedtime.",
        "Write a moment where you look back at today and smile at how worried you were.",
        "Describe one ordinary object in your new life that makes you happy every time you see it.",
        "Write a thank-you note to yourself from the day after it came true.",
    ]),
    ("future", "Future self", [
        "Write a short note from yourself one year from now. What do they want you to know?",
        "What does your future self do first thing in the morning that you don't do yet?",
        "What would your future self tell you to stop overthinking?",
        "Describe your future self's ordinary weekday in five sentences.",
        "What is your future self proud of that you are working on today?",
        "What does your future self no longer tolerate? Write about how that feels.",
        "Ask your future self one question. Write the answer you think they would give.",
        "What habit did your future self start this year that changed everything?",
        "How does your future self talk to themselves on a hard day?",
        "What does your future self spend their money on, and what do they skip?",
        "Who does your future self spend more time with, and who less?",
        "What does your future self's home look like on a Sunday afternoon?",
        "What is one decision you can make today the way your future self would make it?",
        "Describe how your future self handles a setback. What do they say and do?",
        "What would your future self want you to rest from this week?",
        "Write about a promise your future self kept. When did they start keeping it?",
        "What does your future self know about patience that you are learning now?",
        "Write a letter of thanks from your future self for one thing you did this month.",
    ]),
    ("gratitude", "Gratitude", [
        "Name three small things from today that you are glad happened.",
        "Who made your life a little easier this week? What did they do?",
        "What is something about your body that you are grateful for today?",
        "Write about a place that always makes you feel calm.",
        "What is a simple pleasure you enjoyed recently and almost didn't notice?",
        "What is something you have now that you once hoped for?",
        "Which skill or strength helped you today? How did you use it?",
        "Write about a mistake that turned out to teach you something useful.",
        "What is one thing in your home that you are grateful to own?",
        "Who is someone you have never properly thanked? What would you say to them?",
        "What made you laugh this week?",
        "What is a comfort you sometimes take for granted: warm water, a quiet room, good bread?",
        "Describe a recent moment of kindness, given or received.",
        "What about this season of the year are you glad for?",
        "What is something hard you got through that you are grateful to have behind you?",
        "Which part of your daily routine quietly takes care of you?",
        "What is something you learned recently that you are glad to know?",
        "Write a thank-you note to yourself for one thing you did today.",
    ]),
    ("belief", "Self-belief", [
        "What is something you once thought you couldn't do, but did?",
        "Write down three qualities that a good friend would say you have.",
        "Which old story about yourself is ready to be retired? Write the new one.",
        "What are you better at than you give yourself credit for?",
        "When do you feel most like yourself? Describe the moment.",
        "What would you attempt this month if you weren't afraid of looking silly?",
        "Write about a time you kept going when it would have been easier to stop.",
        "What does confidence look like for you in a quiet, everyday way?",
        "What compliment do you find hard to accept? Write it down and read it twice.",
        "What is one boundary you are proud of keeping?",
        "Which voice in your head is loudest when you doubt yourself? What would you say back to it?",
        "List five promises you have kept to yourself, however small.",
        "What do you bring to a room that nobody else quite does?",
        "What would you tell a friend who felt the way you feel today?",
        "Describe your best qualities without using the word “but”.",
        "What is a small win from this week that deserves more celebration?",
        "Which part of you are you learning to be patient with?",
        "Finish this sentence five ways: “I am the kind of person who…”",
    ]),
    ("newyear", "New Year 2027", [
        "What is the one word you want to describe your 2027? Why that word?",
        "What did 2026 teach you that you want to carry into 2027?",
        "What are you ready to leave behind in 2026?",
        "Describe an ordinary day in December 2027 if this year goes well.",
        "What is the one desire you want to focus on for the first 21 days of 2027?",
        "Which habit would make the biggest difference in 2027 if you kept it every day?",
        "What are three moments from 2026 you are grateful for?",
        "What would make 2027 feel like a success, even if nothing dramatic happens?",
        "Who do you want to spend more time with in 2027?",
        "Write your 2027 affirmation in the present tense. Read it out loud.",
        "What will you say no to in 2027 so you can say yes to what matters?",
        "What did you start in 2026 that deserves to keep growing?",
        "Script the first morning of 2027: where you wake up and the first thing you do.",
        "What is one fear about the new year? Write what you would do if it came true, then let it rest.",
        "What would your 2027 self thank your 2026 self for?",
        "Plan January's first week: when will you write, and what one small action will you take?",
        "What does rest look like for you in 2027?",
        "Write a short letter to yourself to open on 31 December 2027.",
    ]),
]

STATIC_PER_CATEGORY = 8

CHIPS = "\n".join(
    f'            <label><input type="radio" name="pcat" value="{cid}"{" checked" if i == 0 else ""}><span>{label}</span></label>'
    for i, (cid, label, _) in enumerate(CATEGORIES))

DATA = json.dumps({cid: {"label": label, "prompts": prompts} for cid, label, prompts in CATEGORIES}, ensure_ascii=False)

ICON_REFRESH = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16.5 10a6.5 6.5 0 1 1-1.9-4.6"/><path d="M16.5 3.5v3.4h-3.4"/></svg>'
ICON_COPY = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="7" width="9.5" height="9.5" rx="2"/><path d="M13 7V5a1.5 1.5 0 0 0-1.5-1.5h-6A1.5 1.5 0 0 0 4 5v6.5A1.5 1.5 0 0 0 5.5 13H7"/></svg>'
ICON_SAVE = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5.5 3.5h9v13l-4.5-3-4.5 3z"/></svg>'
ICON_PRINT = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 7V3.5h8V7"/><rect x="3.5" y="7" width="13" height="7" rx="1.5"/><path d="M6 12h8v4.5H6z"/></svg>'

BODY = f"""  <div class="tool-shell single print-hide" data-prompts>
    <div class="tool-controls">
      <div class="tool-panel">
        <fieldset>
          <legend class="t-step"><span class="n">1</span>Choose a kind of prompt</legend>
          <div class="t-chips" role="radiogroup">
{CHIPS}
          </div>
        </fieldset>
      </div>

      <section class="prompt-stage" aria-label="Your prompt">
        <div class="prompt-meta">
          <span class="prompt-cat" data-cat-label>Manifestation</span>
          <div class="seg seg-small" role="radiogroup" aria-label="Which prompt to show">
            <label><input type="radio" name="pmode" value="random" checked><span>Random</span></label>
            <label><input type="radio" name="pmode" value="today"><span>Today&rsquo;s prompt</span></label>
          </div>
        </div>
        <blockquote class="prompt-card" aria-live="polite"><p data-prompt>Pick a kind of prompt, then press New prompt.</p></blockquote>
        <div class="prompt-actions">
          <button class="btn clay" type="button" data-new>{ICON_REFRESH}New prompt</button>
          <button class="btn ghost" type="button" data-copy>{ICON_COPY}Copy</button>
          <button class="btn ghost" type="button" data-save>{ICON_SAVE}<span data-save-label>Save</span></button>
        </div>
        <p class="prompt-tip">Tip: press <kbd>Space</kbd> or <kbd>Enter</kbd> for a new prompt.</p>
      </section>

      <div class="tool-panel saved-panel">
        <div class="saved-head">
          <h2 class="t-step"><span class="n">2</span>My saved prompts <span class="saved-count" data-saved-count>0</span></h2>
        </div>
        <ol class="saved-list" data-saved-list></ol>
        <p class="t-hint" data-saved-empty>Prompts you save appear here, on this device only.</p>
      </div>

      <div class="tool-panel">
        <h2 class="t-step"><span class="n">3</span>Print a prompt journal</h2>
        <p class="t-hint" style="margin:-0.3rem 0 0.9rem">30 prompts with lines to write on. Print it or save it as a PDF.</p>
        <div class="seg" role="radiogroup" aria-label="What to print">
          <label><input type="radio" name="psource" value="category" checked><span>30 from <b data-print-cat>Manifestation</b></span></label>
          <label><input type="radio" name="psource" value="saved"><span>My saved prompts</span></label>
        </div>
        <div class="preview-actions" style="justify-content:flex-start;margin-top:1rem">
          <button class="btn" type="button" data-print>{ICON_PRINT}Print or save as PDF</button>
        </div>
        <div style="margin-top:1rem">{privacy("Runs in your browser. Saved prompts stay on this device and nothing is sent anywhere.")}</div>
      </div>
    </div>
  </div>

  <section class="prompt-print" data-print-sheet aria-hidden="true">
    <h2 data-print-title>Manifestation prompts</h2>
    <p class="pp-sub">One prompt a day. Write for five to ten minutes, then take one small step.</p>
    <ol data-print-list></ol>
    <p class="pp-foot">369journal.app &middot; Free journal prompt generator</p>
  </section>

  <script type="application/json" id="prompt-data">{DATA}</script>"""


def static_lists():
    out = []
    for cid, label, prompts in CATEGORIES:
        items = "\n".join(f"        <li>{html.escape(p)}</li>" for p in prompts[:STATIC_PER_CATEGORY])
        out.append(f'      <h3 id="list-{cid}">{label} journal prompts</h3>\n      <ol>\n{items}\n      </ol>')
    return "\n".join(out)


ARTICLE = f"""      <h2 id="how">How to use journal prompts</h2>
      <ol>
        <li><strong>Pick one prompt.</strong> Don&rsquo;t answer five. One prompt, answered honestly, does more.</li>
        <li><strong>Write for five to ten minutes</strong> without stopping to edit. Spelling doesn&rsquo;t matter.</li>
        <li><strong>Read it back once</strong> and underline the line that feels most true.</li>
        <li><strong>End with one small step</strong> you can take today, however tiny.</li>
      </ol>

      <h2 id="kinds">Manifestation prompts vs scripting prompts</h2>
      <p><strong>Manifestation prompts</strong> help you get clear: what you want, why it matters and what is in the way. <strong>Scripting prompts</strong> ask you to write one ordinary moment as if your desire has already happened, often starting with &ldquo;I remember when&hellip;&rdquo;. Many people answer a manifestation prompt in the morning and write a short script at night. Our guide to <a href="/scripting-manifestation/">scripting manifestation</a> explains the scene-writing method step by step.</p>

      <h2 id="369">Pairing prompts with the 369 method</h2>
      <p>The <a href="/369-method/">369 method</a> repeats one short affirmation 3, 6 and 9 times a day. Prompts give that line depth: answer one prompt a day about the same desire, and your affirmation starts to feel more real. Need the line itself? Try the <a href="/affirmation-generator/">free affirmation generator</a>.</p>

      <h2 id="lists">Prompts by category</h2>
      <p>A few from each category. The generator above has many more, and a different one every time.</p>
{static_lists()}
      <p>Want to write a longer letter to the person you are becoming? Use the guided <a href="/letter-to-future-self/">letter to your future self</a>.</p>
      <p>Doing a gratitude journal? There are 108 more in our <a href="/gratitude-journal-prompts/">gratitude journal prompts</a>, with a &ldquo;3 good things&rdquo; mode and a printable 30-day journal. Planning 2027? Start by choosing <a href="/word-of-the-year/">your Word of the Year</a>.</p>"""

FAQ = [
    ("Is this journal prompt generator free?", "Yes. It is free, needs no sign-up and runs in your browser. Prompts you save stay on your device."),
    ("What are manifestation journal prompts?", "Questions that help you get clear on what you want, why it matters and what small step to take next. They work well alongside the 369 method or scripting."),
    ("What are scripting prompts?", "Prompts that ask you to write one ordinary moment as if your desire has already happened, with real details. Starting with “I remember when…” often makes it easier to believe."),
    ("How long should I journal for?", "Five to ten minutes is enough for most prompts. One honest page is better than three rushed ones."),
    ("Is there a new prompt every day?", "Yes. Choose “Today’s prompt” to see the prompt of the day for each category. It changes every day and is the same for everyone."),
    ("Can I print the prompts?", "Yes. Print 30 prompts from any category, or your saved prompts, with lines to write on, or save them as a PDF."),
]

P = {
    "path": "/journal-prompt-generator/",
    "crumb": "Journal prompt generator",
    "title": "Free Journal Prompt Generator for Manifestation | 369 Journal",
    "h1": "Journal Prompt Generator",
    "description": "Free journal prompt generator: manifestation, scripting, future-self, gratitude and New Year 2027 prompts. One click at a time, or print 30.",
    "lede": "Fresh journal prompts for manifestation, scripting, gratitude and more. Get a new one with every click, save your favourites, or print 30 with lines to write on.",
    "badges": ["Free", "No sign-up", "100+ prompts", "Printable"],
}

NEXT = next_steps(
    "Write with a guide",
    "If scripting prompts click for you, our workbook walks you through 30 days of it, with a lesson, an example and a full page each day. Or keep the habit going on your phone.",
    "scripting", "web_prompts",
    "Script and write on your iPhone",
    "369 Journal includes free guided scripting next to your daily 369 writing, with reminders morning, afternoon and night. Your first 21-day cycle is free.",
    "site-prompts",
)

if __name__ == "__main__":
    write(P["path"], tool_page(P, FAQ, BODY, js="prompts.js", css="prompts.css", article=ARTICLE, next_html=NEXT))

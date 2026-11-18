#!/usr/bin/env python3
"""Letter to your future self: /letter-to-future-self/

Run:  cd scripts && python3 tool_future_letter.py
Logic: /assets/tools/future-letter.js   Styles: /assets/tools/future-letter.css
"""
from toolkit import next_steps, privacy, tool_page, write

CHEV = '<svg class="chev" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg>'
PRINT = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.5 6V2h7v4"/><rect x="2" y="6" width="12" height="6" rx="1.5"/><path d="M4.5 10h7v4h-7z"/></svg>'
CAL = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="3" width="12" height="11" rx="1.5"/><path d="M2 6.5h12M5.5 1.5v3M10.5 1.5v3"/></svg>'
DOWN = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2v8M4.5 6.5 8 10l3.5-3.5M2.5 13.5h11"/></svg>'

PROMPTS = [
    ("where", "Where are you as you read this?", "Guess. Where do you live, what does an ordinary morning look like?", True),
    ("proud", "What I’m proud of right now", "Small things count. What did you do this year that took courage?", False),
    ("working", "What I’m working towards", "The one thing you most want to be true by the time this is opened.", False),
    ("letgo", "What I hope you’ve let go of", "A worry, a habit, a story you tell yourself.", False),
    ("question", "A question for you", "Something only your future self can answer.", False),
    ("remember", "Something I want you to remember", "Advice, a feeling, a person, a song.", False),
]


def prompt_rows():
    rows = []
    for pid, label, hint, open_ in PROMPTS:
        rows.append(f"""          <details class="lp"{' open' if open_ else ''}>
            <summary data-filled="{pid}"><span class="dot" aria-hidden="true"></span>{label}{CHEV}</summary>
            <p class="lp-hint" id="lp-{pid}-hint">{hint}</p>
            <textarea id="lp-{pid}" class="t-textarea" rows="4" aria-label="{label}" aria-describedby="lp-{pid}-hint"></textarea>
          </details>""")
    return "\n".join(rows)


BODY = f"""    <div data-letter>
    <div class="tool-shell">
      <div class="tool-controls">
        <section class="tool-panel" aria-labelledby="step-open">
          <h2 class="t-step" id="step-open"><span class="n">1</span>When should you open it?</h2>
          <div class="letter-open">
            <div class="seg" role="radiogroup" aria-labelledby="step-open">
              <label><input type="radio" name="open-on" value="6"><span>6 months</span></label>
              <label><input type="radio" name="open-on" value="12" checked><span>1 year</span></label>
              <label><input type="radio" name="open-on" value="36"><span>3 years</span></label>
              <label><input type="radio" name="open-on" value="pick"><span>Pick a date</span></label>
            </div>
            <div id="letter-date-wrap" hidden>
              <label class="t-label" for="letter-date">Open on</label>
              <input id="letter-date" class="t-input" type="date">
            </div>
          </div>
        </section>

        <section class="tool-panel" aria-labelledby="step-write">
          <h2 class="t-step" id="step-write"><span class="n">2</span>Write your letter</h2>
          <p id="letter-restored" class="letter-restored" hidden>Welcome back. Your draft was kept on this device.</p>
          <div class="t-field">
            <label class="t-label" for="letter-name">Dear&hellip; <span>(optional: your name, or leave it as &ldquo;future me&rdquo;)</span></label>
            <input id="letter-name" class="t-input" type="text" maxlength="40" autocomplete="off" placeholder="future me">
          </div>
          <div class="t-field">
            <p class="t-label">Answer any of these. Skip the rest.</p>
{prompt_rows()}
          </div>
          <div class="t-field">
            <label class="t-label" for="lp-else">Anything else</label>
            <textarea id="lp-else" class="t-textarea" rows="4" placeholder="Write freely&hellip;"></textarea>
          </div>
          <div class="letter-meta">
            <span class="count" id="letter-words" aria-live="polite">0 words</span>
            <button id="letter-reset" class="t-link-btn" type="button">Start over</button>
          </div>
        </section>
        {privacy("Your letter stays in this browser, saved as a draft on this device only. It leaves the page only when you print it or download it.")}
      </div>

      <div class="tool-preview" aria-label="Letter preview">
        <div class="preview-stage letter-stage">
          <article class="letter-sheet" aria-live="polite">
            <div class="letter-dots" aria-hidden="true">
              <span class="r3"><i></i><i></i><i></i></span>
              <span class="r6"><i></i><i></i><i></i><i></i><i></i><i></i></span>
              <span class="r9"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>
            </div>
            <p class="letter-dates"><span>Written on <strong id="lv-written"></strong></span><span>To be opened on <strong id="lv-opens"></strong></span></p>
            <p class="letter-greet" id="lv-greet">Dear future me,</p>
            <div class="letter-body" id="lv-body"></div>
            <p class="letter-empty" id="lv-empty">Your words will appear here as you write.</p>
            <div class="letter-sign"><p>With love,</p><p class="who" id="lv-sign"></p></div>
            <p class="letter-foot">Written with the free tool at 369journal.app/letter-to-future-self</p>
          </article>
        </div>
        <div class="letter-outputs">
          <div class="row">
            <button id="letter-ics" class="btn" type="button">{CAL}Add a reminder to my calendar</button>
            <button id="letter-print" class="btn ghost" type="button">{PRINT}Print or save as PDF</button>
            <button id="letter-txt" class="btn ghost" type="button">{DOWN}Download .txt</button>
          </div>
          <p class="why">No email needed. The calendar file puts your whole letter in an event on the day you chose, so your own calendar brings it back to you.</p>
        </div>
      </div>
    </div>
    </div>"""

ARTICLE = """      <h2 id="how">How to write a letter to your future self</h2>
      <ol>
        <li><strong>Pick a date.</strong> One year is the most popular. Six months suits a goal you are working on now; three to five years suits big life changes.</li>
        <li><strong>Write to yourself as a friend.</strong> Start with &ldquo;Dear future me&rdquo; and write the way you would talk to someone you care about.</li>
        <li><strong>Describe today.</strong> Where you live, what a normal day looks like, what is on your mind. These details are what make the letter moving to reread.</li>
        <li><strong>Say what you hope for.</strong> One or two things you are working towards, and why they matter to you.</li>
        <li><strong>Ask a question.</strong> Something only your future self can answer, like &ldquo;Did you take the course?&rdquo; or &ldquo;Are you still worrying about money?&rdquo;</li>
        <li><strong>Seal it.</strong> Print it and put it somewhere safe, or add it to your calendar so it comes back on the day you chose.</li>
      </ol>

      <h2 id="include">What to include</h2>
      <ul>
        <li>A snapshot of your life right now: home, work, friends, habits.</li>
        <li>What you are proud of, even small things.</li>
        <li>What you are working towards, and one step you are taking this month.</li>
        <li>Something you hope you have let go of.</li>
        <li>Advice or a reminder you think you will need.</li>
      </ul>

      <h2 id="example">A short example letter</h2>
      <blockquote>Dear future me, it&rsquo;s a rainy Sunday and I&rsquo;m writing this at the kitchen table. Right now I&rsquo;m proud that I finally started saving every month, even if it&rsquo;s small. By the time you read this, I hope we have our own place and that we stopped saying yes to everything. Did you keep the morning walks? Whatever happened, remember that you were trying, and that counts. With love, me.</blockquote>

      <h2 id="when">When to open it</h2>
""" + """      <div class="table-wrap"><table><thead><tr><th scope="col">Open after</th><th scope="col">Good for</th></tr></thead><tbody>
<tr><th scope="row">6 months</th><td>Checking in on a goal or habit you are building now</td></tr>
<tr><th scope="row">1 year</th><td>A New Year or birthday tradition; seeing how much a year changes</td></tr>
<tr><th scope="row">3 to 5 years</th><td>Big chapters: a move, a career change, a new family</td></tr>
</tbody></table></div>

      <h2 id="open">What to do when you open it</h2>
      <p>Read it slowly, then write a short reply. Notice what changed, what didn&rsquo;t, and what you would tell the person who wrote it. Many people then write the next letter on the same day, so it becomes a yearly habit.</p>
      <p>Want to keep that future in view every day? Writing one line about it each morning, afternoon and night is the idea behind the <a href="/369-method/">369 method</a>. Find wording with the <a href="/affirmation-generator/">free affirmation generator</a>, or write a whole scene of it with <a href="/scripting-manifestation/">scripting</a>. Writing a future-self letter is also day 20 of our <a href="/new-year-manifestation-challenge/">21-day New Year challenge</a>.</p>
"""

FAQ = [
    ("Is this letter to your future self tool free?", "Yes. It is free, needs no account and no email address, and works in any browser on your phone or computer."),
    ("Is my letter private?", "Yes. Your letter is written and kept in your own browser. It is never sent to us or anyone else. A draft is saved on this device so you can come back to it, and you can clear it with “Start over”."),
    ("How do I get the letter back without email?", "Tap “Add a reminder to my calendar”. It downloads a calendar file with your whole letter inside an event on the date you chose. Open the file to add it to Apple Calendar, Google Calendar or Outlook."),
    ("How long should a letter to your future self be?", "There is no rule. Most are between 200 and 600 words, about one or two pages. Answering three or four of the prompts is plenty."),
    ("When should I open a letter to my future self?", "One year is the most common choice, often on New Year’s Day or a birthday. Six months works well for a current goal, and three to five years for big life changes."),
    ("What should I write in a letter to my future self?", "Describe your life today, what you are proud of, what you are working towards, what you hope you have let go of, and a question you want answered. Specific details make it far more meaningful to reread."),
]

P = {
    "path": "/letter-to-future-self/",
    "crumb": "Letter to your future self",
    "title": "Write a Letter to Your Future Self (Free) | 369 Journal",
    "h1": "Write a Letter to Your Future Self",
    "description": "Write a letter to your future self with gentle prompts, then print it, save a PDF, or add a calendar reminder to reopen it later. No email needed.",
    "lede": "Answer a few gentle prompts, choose when to open it, and keep the letter as a PDF or a calendar reminder that brings it back on the day. No email, no account, and it never leaves your device.",
    "badges": ["Free", "No email or sign-up", "Private to your device"],
}

NEXT = next_steps(
    "Keep your future in view",
    "A letter looks a year ahead. These help you live towards it every day.",
    "scripting", "web_letter",
    "Write it down every day",
    "369 Journal helps you write one desire 3, 6 and 9 times a day, with reminders and free guided scripting. Your first 21-day cycle is free.",
    "site-letter",
)

if __name__ == "__main__":
    write(P["path"], tool_page(P, FAQ, BODY, js="future-letter.js", css="future-letter.css", article=ARTICLE, next_html=NEXT))

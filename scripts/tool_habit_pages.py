#!/usr/bin/env python3
"""Builds /habit-tracker-printable/ and /goal-setting-worksheet/.

Run:  cd scripts && python3 tool_habit_pages.py
(The lead runs layout.py afterwards for the shared header/footer.)
Assets: assets/tools/habit-tracker.{js,css} and goal-worksheet.{js,css}.
"""
import html

from toolkit import next_steps, privacy, tool_page, write

PUBLISHED_NEW = "2026-11-22"

I_PRINT = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 7V3.5h8V7"/><rect x="3.5" y="7" width="13" height="7" rx="1.5"/><path d="M6 12h8v4.5H6z"/></svg>'

# ---------------------------------------------------------------- A. Habit tracker

HABIT_IDEAS = [
    ("Morning", [
        "Drink a glass of water before coffee", "Make the bed", "Stretch for 5 minutes",
        "Write your top 3 tasks for the day", "Get outside for 5 minutes of daylight", "Eat a real breakfast",
        "Read one page of a book"]),
    ("Body and health", [
        "Walk 20 minutes", "Drink 2 litres of water", "Eat a vegetable at every meal",
        "Be in bed by a set time", "Take your vitamins or medicine", "Do 10 squats or push-ups",
        "Take the stairs", "No sugary drinks"]),
    ("Mind and calm", [
        "Meditate or breathe slowly for 3 minutes", "Write 3 lines in a journal", "Write one thing you are grateful for",
        "Spend 30 minutes without your phone", "Do a 5-minute tidy", "Go to bed without scrolling",
        "Say one kind thing to yourself"]),
    ("Money", [
        "Note every purchase", "No impulse buys", "Move a small amount into savings",
        "Check your balance", "Cook at home", "Pack lunch or a snack"]),
    ("Work and learning", [
        "Do your most important task first", "Study or practise for 15 minutes", "Clear your inbox once a day",
        "Plan tomorrow before you finish", "Learn 5 words in a new language", "Work in one 25-minute focused block"]),
    ("People and home", [
        "Message a friend or family member", "Give one real compliment", "Wash up before bed",
        "Put away one thing that is out of place", "Water the plants", "Spend 10 minutes with no screens with someone"]),
    ("369 method", [
        "Write your affirmation 3 times in the morning", "Write it 6 times in the afternoon", "Write it 9 times at night"]),
]
HABIT_COUNT = sum(len(v) for _, v in HABIT_IDEAS)

HT_FAQ = [
    ("Is this printable habit tracker free?",
     "Yes. It is free, needs no sign-up and runs in your browser. Type your habits, pick a month and layout, then print it or save it as a PDF."),
    ("How many habits should I track?",
     "Start with one to three. A short list is easier to keep than a long one, and you can add a habit once the first ones feel automatic. The tracker holds up to 10 for when you are ready."),
    ("Can I save it as a PDF?",
     "Yes. Press Print, then choose Save as PDF as the printer (on iPhone and iPad, use the share button and choose Print, then pinch the preview to get a PDF). The page size is set to A4 or US Letter for you."),
    ("What does the never miss twice rule mean?",
     "Missing one day is normal and does not break a habit. The rule is simply to do it the next day, because two misses in a row is when a break tends to turn into stopping. Fill a box for the day you return and carry on."),
    ("Should I use a paper habit tracker or an app?",
     "Either works, so choose the one you will look at. Paper is visible on the fridge or desk and feels good to tick. An app can remind you and keep count when you are out. Some people use both."),
    ("Can I print a habit tracker for a whole year?",
     "Yes. Choose a different month in the list and print it again. You can pick any month from January 2026 to December 2027, so a 12-page year is twelve quick prints."),
]

HT_BODY = f"""  <div class="tool-shell ht-shell" data-habit>
    <div class="tool-controls print-hide">
      <div class="tool-panel">
        <h2 class="t-step"><span class="n">1</span>Your habits</h2>
        <p class="t-hint" style="margin:-0.4rem 0 0.9rem">Type up to 10. Fewer is better: one to three is a great start.</p>
        <div class="ht-inputs">
{chr(10).join(f'          <label class="ht-in"><b aria-hidden="true">{i}</b><span class="visually-hidden">Habit {i}</span><input class="t-input" type="text" maxlength="40" data-habit-input placeholder="{ph}" autocomplete="off"></label>' for i, ph in enumerate(["Walk 20 minutes", "Drink water", "Read 10 pages", "", "", "", "", "", "", ""], 1))}
        </div>
        <p class="t-label" style="margin-top:1.1rem">Or start from an example</p>
        <div class="ht-examples">
          <button type="button" data-example="morning">Morning routine</button>
          <button type="button" data-example="health">Health</button>
          <button type="button" data-example="money">Money</button>
          <button type="button" data-example="selfcare">Self-care</button>
          <button type="button" data-example="369">369 method</button>
          <button type="button" class="ht-clear" data-clear>Clear</button>
        </div>
      </div>

      <div class="tool-panel">
        <h2 class="t-step"><span class="n">2</span>Choose your sheet</h2>
        <div class="ht-options">
          <div>
            <label class="t-label" for="ht-month">Month</label>
            <select class="t-select" id="ht-month" data-month></select>
            <p class="t-hint" data-month-hint hidden>The month only matters for the monthly grid.</p>
          </div>
          <div>
            <span class="t-label" id="ht-layout-l">Layout</span>
            <div class="seg" role="radiogroup" aria-labelledby="ht-layout-l">
              <label><input type="radio" name="htlayout" value="month" checked><span>Monthly grid</span></label>
              <label><input type="radio" name="htlayout" value="week"><span>Weekly</span></label>
              <label><input type="radio" name="htlayout" value="thirty"><span>30-day, undated</span></label>
            </div>
          </div>
          <div>
            <span class="t-label" id="ht-style-l">Style</span>
            <div class="seg" role="radiogroup" aria-labelledby="ht-style-l">
              <label><input type="radio" name="htstyle" value="minimal" checked><span>Minimal</span></label>
              <label><input type="radio" name="htstyle" value="soft"><span>Soft</span></label>
            </div>
          </div>
          <div>
            <span class="t-label" id="ht-paper-l">Paper</span>
            <div class="seg" role="radiogroup" aria-labelledby="ht-paper-l">
              <label><input type="radio" name="htpaper" value="a4" checked><span>A4</span></label>
              <label><input type="radio" name="htpaper" value="letter"><span>US Letter</span></label>
            </div>
          </div>
          <div>
            <label class="t-label" for="ht-title">Title <span>(optional)</span></label>
            <input class="t-input" id="ht-title" type="text" maxlength="40" data-title placeholder="Habit tracker" autocomplete="off">
          </div>
        </div>
      </div>
    </div>

    <div class="ht-previewcol">
      <div class="ht-actions print-hide">
        <button class="btn clay" type="button" data-print>{I_PRINT}Print or save as PDF</button>
        {privacy("Runs in your browser. Your habits stay on this device and are never sent anywhere.")}
      </div>
      <div class="ht-scroll" tabindex="0" role="region" aria-label="Preview of your habit tracker. Scroll sideways to see all days.">
        <div class="ht-sheet" data-sheet></div>
      </div>
    </div>
  </div>"""


def ideas_html():
    out = []
    for label, items in HABIT_IDEAS:
        lis = "\n".join(f"        <li>{html.escape(i)}</li>" for i in items)
        out.append(f"      <h3>{label}</h3>\n      <ul>\n{lis}\n      </ul>")
    return "\n".join(out)


HT_ARTICLE = f"""      <h2 id="how">How to use a habit tracker</h2>
      <p>A habit tracker is a grid. Down the side you list the habits, across the top you have the days, and each day you do a habit you fill in its box. That is the whole system. It works because a row of filled boxes is a small, honest picture of what you have been doing, and many people find it hard to break a streak they can see.</p>
      <ol>
        <li><strong>Pick one to three habits.</strong> Write them in the tool above.</li>
        <li><strong>Make each one small and clear.</strong> &ldquo;Walk 20 minutes&rdquo; is easier to tick than &ldquo;get fit&rdquo;.</li>
        <li><strong>Print it and put it where you will see it,</strong> on the fridge, by the kettle or on your desk, with a pen next to it.</li>
        <li><strong>Fill the box straight after the habit,</strong> not at the end of the week. The tick is a small reward, so give it at the right moment.</li>
        <li><strong>Look at it once a week.</strong> Which days did you miss? What got in the way? Change the habit or the time, not your opinion of yourself.</li>
      </ol>

      <h2 id="how-many">How many habits should you track?</h2>
      <p>Fewer than you think. Start with one, two or three. Every habit asks for a little attention and a little willpower, and a page with ten habits on day one is often a page that is abandoned by day ten.</p>
      <p>A useful way to choose: pick one habit that is almost too easy (drink a glass of water), one that matters to you (a walk), and one that supports your day (write tomorrow&rsquo;s top three). Once those feel automatic, replace them or add one more. The tracker holds up to ten for when you are ready, and for a short-term plan or a challenge month.</p>

      <h2 id="never-miss-twice">The never miss twice rule</h2>
      <p>Everyone misses a day. The mistake is treating a missed day as a failed month. The rule is simple: <strong>miss once, never twice.</strong> If you skip Tuesday, do it Wednesday, even a tiny version of it. A 2-minute walk counts. The box still gets filled and the chain is still alive.</p>
      <p>It helps to decide in advance what your smallest version is. &ldquo;Read one page&rdquo; keeps the habit going on the days you have no energy for a chapter.</p>

      <h2 id="ideas">{HABIT_COUNT} habit ideas to track</h2>
      <p>Pick a few that fit your life, then write them in your own words. Ideas are grouped so you can choose by what you want more of.</p>
{ideas_html()}

      <h2 id="369">A habit tracker for the 369 method</h2>
      <p>The <a href="/369-method/">369 method</a> is a habit in itself: write one short affirmation 3 times in the morning, 6 times in the afternoon and 9 times at night. Press the &ldquo;369 method&rdquo; example above and you get three rows, Morning 3, Afternoon 6 and Night 9, so you can tick each part as you do it. Choose the 30-day layout to follow a cycle without dates, or print a month. If you would like a sheet made for the method, try the <a href="/affirmation-generator/">affirmation generator</a> or the <a href="/369-method/tracker/">free 33-day tracker</a>.</p>

      <h2 id="paper-vs-app">Paper or app?</h2>
      <table-placeholder></table-placeholder>
      <p>If you tend to forget to look at paper, an app that nudges you is worth trying. If you tend to ignore notifications, paper on the wall is harder to swipe away. There is no wrong answer, only the one you will use. Starting a new year? Our <a href="/goal-setting-worksheet/">goal setting worksheet</a> and <a href="/new-year-resolution-ideas/">new year resolution ideas</a> help you choose what is worth tracking in the first place.</p>"""

PAPER_TABLE = """<div class="table-wrap"><table><thead><tr><th scope="col"></th><th scope="col">Paper tracker</th><th scope="col">App</th></tr></thead><tbody>
<tr><th scope="row">Always in sight</th><td>Yes, if it is on a wall or desk</td><td>Only when you open it</td></tr>
<tr><th scope="row">Reminds you</th><td>No</td><td>Yes</td></tr>
<tr><th scope="row">Goes with you</th><td>No</td><td>Yes</td></tr>
<tr><th scope="row">Feels good to tick</th><td>A pen and a box</td><td>A tap</td></tr>
<tr><th scope="row">Cost</th><td>Free to print</td><td>Free to paid</td></tr>
</tbody></table></div>"""
HT_ARTICLE = HT_ARTICLE.replace("<table-placeholder></table-placeholder>", PAPER_TABLE)

HT_P = {
    "path": "/habit-tracker-printable/",
    "crumb": "Printable habit tracker",
    "title": "Free Printable Habit Tracker (Monthly + 2027) | 369 Journal",
    "h1": "Free Printable Habit Tracker",
    "description": "Free printable habit tracker: type up to 10 habits, pick a month for 2026 or 2027, choose monthly, weekly or 30-day, then print or save as a PDF.",
    "lede": "Type your habits, choose a month and a style, and print a clean tracker on A4 or US Letter. Monthly grid, weekly or 30-day undated. Free, no sign-up.",
    "badges": ["Free, no sign-up", "Monthly, weekly or 30-day", "A4 and US Letter"],
    "published": PUBLISHED_NEW,
}

HT_NEXT = next_steps(
    "Keep the habit going, on paper or on your phone",
    "If you tracked the 369 habit above, you already know the idea: pick one affirmation and write it 3 times in the morning, 6 in the afternoon and 9 at night. Our 45-day guided workbook is the paper way to do it, or let your phone keep count.",
    "369", "web_habit_tracker",
    "Let your phone keep count",
    "369 Journal reminds you each morning, afternoon and night, counts your lines and keeps a streak. Private, no account, and your first 21-day cycle is free.",
    "site-habit-tracker",
)

# ---------------------------------------------------------------- B. Goal worksheet

GW_FAQ = [
    ("Is this goal setting worksheet free to print?",
     "Yes. It is free, needs no sign-up and works in your browser. Fill it in on screen and print it, or print it blank and write by hand. You can save it as a PDF too."),
    ("What is a SMART goal?",
     "SMART is a checklist for a clear goal: Specific, Measurable, Achievable, Relevant and Time-bound. In plain words, it says exactly what you want, how you will know you got there, that it is realistic, that it matters to you and by when. It is a good check, though it does not help much with the days you do not feel like it, which is why this worksheet adds if-then plans."),
    ("What is WOOP?",
     "WOOP stands for Wish, Outcome, Obstacle, Plan. You name a goal, picture the best result, picture the real obstacle that could get in the way, then make an if-then plan for it. It comes from the research of psychologist Gabriele Oettingen on mental contrasting, which suggests that imagining both the wish and the obstacle can work better than positive thinking alone."),
    ("How many goals should I set at once?",
     "One to three. Each goal takes attention, so a few clear ones usually beat a long list. Use one worksheet per goal, and if you are unsure which to start with, pick the one that would make the others easier."),
    ("Is my worksheet saved or sent anywhere?",
     "No. What you type stays in your browser and, if your browser allows it, is kept on this device so you do not lose it by accident. It is never sent to us. The Clear button removes it."),
    ("Can I print a blank goal setting worksheet?",
     "Yes. Choose Blank worksheet and the sheet prints with empty lines, ready to fill in by hand, even if you have typed something above."),
]

GW_BODY = f"""  <div class="tool-shell ht-shell gw-shell" data-goal>
    <div class="tool-controls print-hide">
      <div class="tool-panel">
        <h2 class="t-step"><span class="n">1</span>Your goal</h2>
        <div class="t-field">
          <label class="t-label" for="gw-goal">What do I want? <span>One clear sentence.</span></label>
          <textarea class="t-textarea" id="gw-goal" data-f="goal" rows="2" maxlength="200" placeholder="Run 5 km without stopping"></textarea>
        </div>
        <div class="t-field">
          <label class="t-label" for="gw-why">Why does it matter to me?</label>
          <textarea class="t-textarea" id="gw-why" data-f="why" rows="3" maxlength="300" placeholder="I want more energy and to feel strong in my body."></textarea>
        </div>
        <div class="t-field">
          <label class="t-label" for="gw-success">What will success look like? <span>What will I see, have or feel?</span></label>
          <textarea class="t-textarea" id="gw-success" data-f="success" rows="3" maxlength="300" placeholder="I jog 5 km on a Saturday morning and feel good afterwards."></textarea>
        </div>
        <div class="t-field">
          <label class="t-label" for="gw-deadline">By when?</label>
          <input class="t-input" id="gw-deadline" data-f="deadline" type="text" maxlength="40" placeholder="31 March 2027">
        </div>
      </div>

      <div class="tool-panel">
        <h2 class="t-step"><span class="n">2</span>Obstacles and if-then plans</h2>
        <p class="t-hint" style="margin:-0.4rem 0 0.9rem">Be honest about what could get in the way. Then decide now what you will do.</p>
        <div class="gw-pairs">
{chr(10).join(f'''          <div class="gw-pair"><span class="gw-tag" aria-hidden="true">If</span><input class="t-input" data-f="if{i}" type="text" maxlength="90" aria-label="Obstacle {i}" placeholder="{a}"><span class="gw-tag" aria-hidden="true">then</span><input class="t-input" data-f="then{i}" type="text" maxlength="120" aria-label="Plan for obstacle {i}" placeholder="{b}"></div>''' for i, (a, b) in enumerate([("it rains", "I do 20 minutes indoors"), ("I feel too tired", "I do just 10 minutes"), ("I skip a day", "I go the next day, no excuses")], 1))}
        </div>
      </div>

      <div class="tool-panel">
        <h2 class="t-step"><span class="n">3</span>Steps and a weekly habit</h2>
        <div class="t-field">
          <span class="t-label">My first 3 steps</span>
          <div class="gw-steps">
{chr(10).join(f'            <input class="t-input" data-f="step{i}" type="text" maxlength="120" aria-label="Step {i}" placeholder="{p}">' for i, p in enumerate(["Buy shoes I can run in", "Walk or jog 20 minutes on Tuesday", "Pick a local 5 km event to enter"], 1))}
          </div>
        </div>
        <div class="t-field">
          <label class="t-label" for="gw-weekly">My weekly tiny action <span>Small enough to do on a bad week.</span></label>
          <input class="t-input" id="gw-weekly" data-f="weekly" type="text" maxlength="140" placeholder="Three 20-minute sessions: Tue, Thu, Sat at 7am">
        </div>
        <div class="t-field">
          <label class="t-label" for="gw-aff">My affirmation line <span>Present tense and believable.</span></label>
          <input class="t-input" id="gw-aff" data-f="aff" type="text" maxlength="120" placeholder="I am someone who keeps showing up for my body.">
        </div>
      </div>
    </div>

    <div class="ht-previewcol">
      <div class="ht-actions print-hide">
        <div class="seg" role="radiogroup" aria-label="Print version">
          <label><input type="radio" name="gwmode" value="filled" checked><span>Filled in</span></label>
          <label><input type="radio" name="gwmode" value="blank"><span>Blank worksheet</span></label>
        </div>
        <div class="seg" role="radiogroup" aria-label="Paper size">
          <label><input type="radio" name="gwpaper" value="a4" checked><span>A4</span></label>
          <label><input type="radio" name="gwpaper" value="letter"><span>US Letter</span></label>
        </div>
        <button class="btn clay" type="button" data-print>{I_PRINT}Print or save as PDF</button>
        <button class="btn ghost" type="button" data-example>See an example</button>
        <button class="t-link-btn" type="button" data-clear>Clear</button>
        {privacy("Runs in your browser. What you type stays on this device and is never sent anywhere.")}
      </div>
      <div class="gw-scroll" tabindex="0" role="region" aria-label="Preview of your goal worksheet">
        <div class="gw-sheet" data-sheet></div>
      </div>
    </div>
  </div>"""

GW_ARTICLE = """      <h2 id="how">How to set a goal you will actually keep</h2>
      <p>Most goals do not fail because people are lazy. They fail because the goal is vague, the reason is thin, or nothing was planned for the day it gets hard. This worksheet is built around those three problems. Fill it in once, put it where you will see it, and come back to it every week.</p>
      <ol>
        <li><strong>Say what you want in one sentence.</strong> &ldquo;Be healthier&rdquo; is a direction. &ldquo;Walk 20 minutes, three times a week, until March&rdquo; is a goal.</li>
        <li><strong>Write why it matters.</strong> Your reason is what you reach for when motivation drops. Make it yours, not what you think you should say.</li>
        <li><strong>Describe success.</strong> What will you see, have or feel when it is done? A clear picture helps you know when you have arrived.</li>
        <li><strong>Name the obstacles.</strong> Pick the two or three things most likely to get in your way, and write an if-then plan for each.</li>
        <li><strong>Choose the first three steps.</strong> Small and close. The first one should take less than a day.</li>
        <li><strong>Add a weekly tiny action.</strong> Something so small you can do it in your worst week.</li>
        <li><strong>Add a deadline</strong> and an affirmation line to read each morning.</li>
      </ol>

      <h2 id="smart">SMART goals, in plain words</h2>
      <p>SMART is an old and useful checklist. Each letter is a question you ask of your goal:</p>
      <ul>
        <li><strong>Specific:</strong> exactly what do I want?</li>
        <li><strong>Measurable:</strong> how will I know I have done it?</li>
        <li><strong>Achievable:</strong> is it realistic for my time, money and energy right now?</li>
        <li><strong>Relevant:</strong> does it matter to me, or am I doing it for someone else?</li>
        <li><strong>Time-bound:</strong> by when?</li>
      </ul>
      <p>SMART makes a goal clear. What it does not do is help you on the Tuesday you are tired and would rather not. That is where the next section comes in.</p>

      <h2 id="woop">WOOP and if-then plans, honestly explained</h2>
      <p>Psychologist Gabriele Oettingen has studied a method called <strong>mental contrasting</strong>, often taught as WOOP: Wish, Outcome, Obstacle, Plan. You name your wish, picture the best result, then picture the real obstacle inside you or around you, then make a plan for it. Her work, along with research on &ldquo;implementation intentions&rdquo; (plans in the form <em>if X happens, then I will do Y</em>), suggests that this can help people follow through better than positive thinking on its own.</p>
      <p>To be fair about it: no method guarantees results, and studies differ in size and quality. But the idea makes everyday sense. If you decide now what you will do when it rains, you do not have to decide while it is raining. That is why the worksheet has three if-then lines. They cost five minutes and remove a few excuses in advance.</p>

      <h2 id="example">A worked example</h2>
      <p>Press <strong>See an example</strong> to load this one into the sheet above.</p>
      <ul>
        <li><strong>Goal:</strong> Run 5 km without stopping by 31 March 2027.</li>
        <li><strong>Why:</strong> I want more energy for my family and to feel strong in my body.</li>
        <li><strong>Success looks like:</strong> I jog 5 km on a Saturday morning in about 35 minutes and feel good afterwards.</li>
        <li><strong>If it rains, then</strong> I do a 20-minute indoor workout. <strong>If I feel too tired, then</strong> I put my shoes on and do just 10 minutes. <strong>If I skip a day, then</strong> I go the next day (never miss twice).</li>
        <li><strong>First 3 steps:</strong> buy running shoes by Sunday; walk or jog 20 minutes on Tuesday; pick a local 5 km event for March.</li>
        <li><strong>Weekly tiny action:</strong> three 20-minute sessions on Tuesday, Thursday and Saturday at 7am.</li>
        <li><strong>Affirmation:</strong> I am someone who keeps showing up for my body.</li>
      </ul>
      <p>Notice how each line is something you could do or check. That is what makes a goal workable.</p>

      <h2 id="track">Track it and review it</h2>
      <p>A worksheet is a plan, and a plan needs a check-in. Put a reminder in your calendar for the same time each week and ask three questions: what did I do, what got in the way, and what is my next small step? To see your weekly action at a glance, print a <a href="/habit-tracker-printable/">free printable habit tracker</a> and tick it off each time. If you are planning for January, <a href="/new-year-resolution-ideas/">new year resolution ideas</a> can help you choose a goal, and <a href="/word-of-the-year/">picking a word of the year</a> gives the whole year a theme.</p>

      <h2 id="affirmation">What the affirmation line is for</h2>
      <p>The last line on the sheet is a short sentence in the present tense that you read, or write, each day. It does not make a goal happen by itself. Its job is to keep the goal in front of you and nudge you toward the next small step. Keep it believable: &ldquo;I am learning to run a little further each week&rdquo; works better than a claim you do not yet believe. If you like writing it out, the <a href="/369-method/">369 method</a> turns it into a short daily routine of writing it 3 times in the morning, 6 in the afternoon and 9 at night.</p>"""

GW_P = {
    "path": "/goal-setting-worksheet/",
    "crumb": "Goal setting worksheet",
    "title": "Goal Setting Worksheet (Free, Printable PDF) | 369 Journal",
    "h1": "Free Goal Setting Worksheet",
    "description": "Free goal setting worksheet: fill it in on screen or print it blank. Goal, why, success, if-then plans, first steps and a weekly action on one clean page.",
    "lede": "Write your goal, your reason, the obstacles and a plan for each, then print it as a clean one-page worksheet. Filled in or blank. Free, no sign-up.",
    "badges": ["Free, no sign-up", "Fill in or print blank", "One clean page"],
    "published": PUBLISHED_NEW,
}

GW_NEXT = next_steps(
    "Make your goal part of the day",
    "The last line of the worksheet is an affirmation. Pick it, then write it 3 times in the morning, 6 in the afternoon and 9 at night. The 45-day guided workbook is the paper way to do it, or let your phone keep count.",
    "369", "web_goal_worksheet",
    "Get a nudge morning, afternoon and night",
    "369 Journal reminds you to write your line three times a day, counts your lines and keeps your streak. Private, no account, and your first 21-day cycle is free.",
    "site-goal-worksheet",
)

if __name__ == "__main__":
    write(HT_P["path"], tool_page(HT_P, HT_FAQ, HT_BODY, js="habit-tracker.js", css="habit-tracker.css", article=HT_ARTICLE, next_html=HT_NEXT))
    write(GW_P["path"], tool_page(GW_P, GW_FAQ, GW_BODY, js="goal-worksheet.js", css="goal-worksheet.css", article=GW_ARTICLE, next_html=GW_NEXT))

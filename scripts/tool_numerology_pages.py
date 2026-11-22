#!/usr/bin/env python3
"""Three focused numerology calculator pages (one builder, one JS file).

  /personal-year-number-calculator/   /name-numerology-calculator/   /life-path-number-calculator/

Run:  cd scripts && python3 tool_numerology_pages.py
Meanings come from tool_numerology (NUM, PY, TYPES) so the text lives in one place. The JS
(assets/tools/numerology-pages.js) serves all three pages, chosen by data-nup on the tool shell.
Master-number convention (same as numerology.js): life path and name numbers keep 11, 22, 33;
personal years always reduce to one digit and mention a master total when it appears.
Honest framing everywhere: "numerologists traditionally associate", never predictions.
"""
import json

from build_posts import table, write
from toolkit import ASSET_V, next_steps, privacy, tool_page
from tool_numerology import NUM, PY, TYPES

PUB = "2026-11-22"
MASTER = {"11", "22", "33"}
CHART_ROWS = {1: "A J S", 2: "B K T", 3: "C L U", 4: "D M V", 5: "E N W", 6: "F O X", 7: "G P Y", 8: "H Q Z", 9: "I R"}
CHART = {c: n for n, ls in CHART_ROWS.items() for c in ls.split()}

PM_SHORT = {"1": "Begin", "2": "Listen", "3": "Create", "4": "Build", "5": "Change", "6": "Care", "7": "Reflect", "8": "Focus", "9": "Finish"}

CAUTION = {
    "1": "Carrying everything alone for too long, or being slow to ask for help.",
    "2": "Putting everyone else first and forgetting to say what you need.",
    "3": "Scattering your energy across too many things, or hiding feelings behind humour.",
    "4": "Holding on to routine so tightly that change feels hard.",
    "5": "Starting things and leaving before they bloom.",
    "6": "Looking after everyone else before you look after yourself.",
    "7": "Pulling away from people when things get hard.",
    "8": "Letting work take over everything else, or being hard on yourself.",
    "9": "Holding on to chapters that are ready to close.",
    "11": "Feeling overwhelmed by the mood around you, and expecting too much of your own sensitivity.",
    "22": "Expecting too much of yourself too fast, so the big plan never gets a first step.",
    "33": "Giving until your own cup is empty.",
}
BASE = {"11": "2", "22": "4", "33": "6"}

LEVELS = {"easy": "Traditionally seen as flowing easily", "comp": "Traditionally seen as balancing each other", "care": "Traditionally seen as needing some patience"}
# pair -> (level, clause that continues "Numerologists traditionally say ...")
COMPAT = {
    "1-1": ("care", "two 1s are both natural starters, so there is plenty of energy and the odd tug-of-war over who leads. Taking turns helps."),
    "1-2": ("comp", "a 1 brings the push and a 2 brings the listening, which can balance well when the 1 slows down and the 2 is heard."),
    "1-3": ("easy", "a 1 and a 3 tend to bring out each other's lively, playful side. The 3 adds colour and the 1 helps finish things."),
    "1-4": ("care", "the 1 likes to move fast and the 4 likes a plan, so the pace can differ. Agreeing who decides what tends to help."),
    "1-5": ("easy", "both enjoy independence and new things, so this pairing is often described as adventurous. Check in so freedom does not turn into distance."),
    "1-6": ("comp", "the 1 looks outward and the 6 looks after home, which can fit well when each respects the other's role."),
    "1-7": ("easy", "a 1 and a 7 each value their own space, so this can be a calm, respectful match. Make time to talk, not only to be alone."),
    "1-8": ("care", "this is two strong, ambitious types. There can be respect and drive, and also a clash over who is in charge."),
    "1-9": ("comp", "the 1 starts things and the 9 sees the bigger picture, which can complement each other. The 9 may need to feel listened to."),
    "2-2": ("easy", "two gentle listeners are often described as warm and considerate. The risk is avoiding hard talks, so say the awkward thing kindly."),
    "2-3": ("comp", "the 2 is steady and the 3 is sparkly, so they can balance each other. The 3 may need to check that the 2 feels heard."),
    "2-4": ("easy", "both value steadiness and loyalty, so this is often described as a calm, dependable pairing."),
    "2-5": ("care", "a 2 likes closeness and routine and a 5 likes change, so this one asks for patience on both sides."),
    "2-6": ("easy", "both are caring, so this is seen as a warm, home-loving match. Remember to look after yourselves too."),
    "2-7": ("comp", "the 2 offers warmth and the 7 offers depth and quiet. It works best when the 7 shares what is going on inside."),
    "2-8": ("easy", "the 2 supports and the 8 drives, a pairing often described as a good team when each values the other's strengths."),
    "2-9": ("comp", "this is two kind hearts. The 9's wide view and the 2's closeness can balance, if the 2 gently asks for attention when needed."),
    "3-3": ("easy", "two creative, chatty people are often described as fun together. Someone still has to handle the practical things."),
    "3-4": ("care", "the 3 is spontaneous and the 4 likes order, which can feel like opposites. Humour and clear routines help."),
    "3-5": ("easy", "both are social and curious, so this is described as lively and playful. Slow down now and then to follow through."),
    "3-6": ("easy", "creativity meets care, a pairing often described as warm and affectionate."),
    "3-7": ("care", "the 3 likes to talk and share and the 7 likes quiet. Respecting each other's rhythm is the key."),
    "3-8": ("comp", "the 3 brings ideas and the 8 brings the drive to carry them out, so they can complement each other."),
    "3-9": ("easy", "both are expressive and generous, often described as an easy, creative pairing."),
    "4-4": ("easy", "two steady builders are dependable and calm, with a risk of getting stuck in routine. Plan something new together."),
    "4-5": ("care", "the 4 likes routine and the 5 likes change, so this often needs patience and compromise."),
    "4-6": ("easy", "both value home and commitment, so this is often described as a stable, caring pairing."),
    "4-7": ("comp", "the 4 is practical and the 7 is thoughtful, and they can respect each other's seriousness."),
    "4-8": ("easy", "both are practical and hard-working, often described as a strong team. Make time for rest and play."),
    "4-9": ("care", "the 4 likes detail and certainty and the 9 looks at the big picture, so it asks for understanding of different styles."),
    "5-5": ("care", "two free spirits can have great adventures and very little routine. Agree on a few anchors."),
    "5-6": ("care", "the 5 wants freedom and the 6 wants closeness and stability, so talk openly about how much of each you need."),
    "5-7": ("easy", "both are curious and independent, so they often enjoy ideas and exploring together."),
    "5-8": ("comp", "the 5 brings variety and the 8 brings drive, a pairing that can be exciting if the 8 allows some flexibility."),
    "5-9": ("comp", "both are open-minded and adventurous, often described as a broad-minded, interesting pairing."),
    "6-6": ("easy", "two caring homebodies are very loving, with a risk of taking on each other's worries. Make room for your own needs."),
    "6-7": ("care", "the 6 is warm and sociable and the 7 is reserved, so the 6 may need patience and the 7 may need to open up."),
    "6-8": ("comp", "care meets ambition. It can work well when the 8 makes time for home and the 6 supports the 8's goals."),
    "6-9": ("easy", "two big-hearted people, often described as a compassionate, supportive match."),
    "7-7": ("comp", "two thinkers who understand each other's need for quiet. The risk is too much distance, so make time to share."),
    "7-8": ("care", "the 7 reflects and the 8 acts, so they may see things very differently. Respect for each other's style helps."),
    "7-9": ("comp", "both are thoughtful and look beyond the everyday, often described as a deep, reflective pairing."),
    "8-8": ("care", "two driven, capable people, which can mean great teamwork or a contest of wills. Share the lead."),
    "8-9": ("care", "the 8 focuses on results and the 9 on people, so priorities can differ. Talking about values helps."),
    "9-9": ("easy", "two compassionate idealists are often described as understanding. Help each other let go of old hurts."),
}
assert len(COMPAT) == 45 and all(f"{a}-{b}" in COMPAT for a in range(1, 10) for b in range(a, 10))

DATA = {
    "num": {k: {"words": v[0], "text": v[1], "short": v[2], "ask": v[3], "aff": v[4]} for k, v in NUM.items()},
    "py": {k: {"theme": v[0], "line": v[1], "text": v[2], "do": v[3], "aff": v[4]} for k, v in PY.items()},
    "types": TYPES, "pm": PM_SHORT, "caution": CAUTION, "base": BASE,
    "compat": {k: list(v) for k, v in COMPAT.items()}, "levels": LEVELS,
}


def data_tag():
    return '<script type="application/json" id="nup-data">' + json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/") + "</script>"


# ---- maths in Python (mirrors the JS, used for worked examples and so the build fails if they drift) ----
def red(n, keep=False):
    steps, cur = [], str(n)
    while len(cur) > 1 and not (keep and cur in MASTER):
        s = sum(int(d) for d in cur)
        steps.append(" + ".join(cur) + f" = {s}")
        cur = str(s)
    return cur, steps


def life_path(y, m, d):
    a, b, c = red(m, True)[0], red(d, True)[0], red(y, True)[0]
    return red(int(a) + int(b) + int(c), True)[0]


def personal_year(m, d, year):
    return red(int(red(m)[0]) + int(red(d)[0]) + int(red(year)[0]))[0]


assert life_path(1990, 8, 14) == "5" and life_path(1990, 7, 14) == "4"
assert personal_year(7, 14, 2027) == "5" and personal_year(8, 14, 2027) == "6"


# ---- shared page bits ----
def related(current):
    items = [
        ("/life-path-number-calculator/", "Life path number calculator", "From your date of birth, with a compatibility check"),
        ("/personal-year-number-calculator/", "Personal year number calculator", "Your 2027 personal year and 12 personal months"),
        ("/name-numerology-calculator/", "Name numerology calculator", "Expression, soul urge and personality numbers"),
        ("/numerology-calculator/", "All-in-one numerology calculator", "Life path, name numbers and personal year together"),
        ("/angel-numbers/", "Angel numbers", "What it can mean when you keep seeing 111, 222, 333"),
    ]
    links = "".join(f'<a href="{h}"><strong>{t}</strong><span>{d}</span></a>' for h, t, d in items if h != current)
    return f'      <h2 id="related">Related numerology tools</h2>\n      <div class="more-tools">{links}</div>'


NOTE = ("<p>One honest note: there is no scientific evidence that numbers predict personality or the future. "
        "Numerology is a traditional belief system, and the meanings here are what numerologists traditionally associate with each number. "
        "Use them as questions to think about, not as answers.</p>")

DAYS = "".join(f'<option value="{i}">{i}</option>' for i in range(1, 32))
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MONTH_OPTS = "".join(f'<option value="{i + 1}">{m}</option>' for i, m in enumerate(MONTHS))


def shell(mode, form_inner, empty):
    return f"""    <div class="tool-shell nu" data-nup="{mode}">
      <div class="tool-controls print-hide">
        <div class="tool-panel">
          <form class="nu-form" novalidate data-form>
{form_inner}
          </form>
          {privacy("Runs in your browser. Nothing you type is sent or saved anywhere.")}
        </div>
      </div>

      <div class="tool-preview">
        <div class="nu-card" aria-live="polite" data-result>
          <div class="nu-empty">
            <div class="nu-orn" aria-hidden="true"><i></i><i></i><i></i></div>
            <p>{empty}</p>
          </div>
        </div>
      </div>
    </div>
    {data_tag()}"""


def finish(p, faq, body, article, nxt):
    page = tool_page(p, faq, body, js="numerology-pages.js", css="numerology.css", article=article, next_html=nxt)
    old = f'  <link rel="stylesheet" href="/assets/tools/numerology.css?v={ASSET_V}">\n'
    assert old in page
    page = page.replace(old, old + f'  <link rel="stylesheet" href="/assets/tools/numerology-pages.css?v={ASSET_V}">\n')
    assert len(p["title"]) <= 60, (len(p["title"]), p["title"])
    assert 140 <= len(p["description"]) <= 160, (len(p["description"]), p["description"])
    return page


def base_page(path, crumb, title, h1, desc, lede, badges):
    return {"path": path, "crumb": crumb, "title": title, "h1": h1, "description": desc, "lede": lede,
            "badges": badges, "published": PUB, "parents": [("Free tools", "/tools/")]}


# =====================================================================================
# 1. Personal year
# =====================================================================================
def py_cycle_table():
    rows = [(k, PY[k][0], PY[k][1]) for k in PY]
    rows.append(("11 or 22", "Master-number years", "Some numerologists keep 11 or 22 when your total lands exactly on it, and read it as a more intense 2 or 4. This calculator shows the single-digit year and tells you when a master total appears."))
    return table(["Personal year", "Theme", "What it often means"], rows)


def py_meanings():
    out = []
    for k in PY:
        t = PY[k]
        out.append(f"""      <h3>Personal year {k}: {t[0].lower()}</h3>
      <p>{t[2]}</p>
      <p><strong>Practical focus for 2027:</strong> {t[3]}</p>
      <p class="nup-aff-q">Affirmation: &ldquo;{t[4]}&rdquo;</p>""")
    return "\n".join(out)


PY_FAQ = [
    ("What is a personal year number?",
     "In numerology, a personal year number describes the theme of a calendar year for you. It runs in a nine-year cycle: a 1 year is a beginning, and a 9 year is a time to finish and let go. It is worked out from your birth month, birth day and the year itself. It is a prompt for reflection, not a forecast."),
    ("How do I calculate my personal year for 2027?",
     "Reduce your birth month, birth day and the year 2027 to single digits, add them, then reduce the total to one digit. The year 2027 is 2 + 0 + 2 + 7 = 11, which reduces to 2. For someone born on 14 July: 7 + (1 + 4) + 2 = 7 + 5 + 2 = 14, then 1 + 4 = 5, so a personal year 5."),
    ("Do I need my birth year?",
     "No. A personal year uses only your birth month and birth day, plus the year you want to look at. That is why this calculator asks for just the month and the day."),
    ("What if my total is 11 or 22?",
     "Numerologists differ. This calculator always reduces a personal year to a single digit, as most personal-year guides do, and tells you when your total passes through a master number such as 11 or 22. If that happens, you can also read the year as a more intense version of 2 or 4. The year 2027 itself adds up to 11 and is reduced to 2."),
    ("Does the personal year change on 1 January or on my birthday?",
     "Most numerologists change it on 1 January, which is the method used here. Some people switch on their birthday instead. If you were born late in the year, you could read both and see which description fits you better."),
    ("What is a personal month?",
     "A personal month is your personal year number plus the calendar month number, reduced to one digit. If your 2027 personal year is 5, then January is 5 + 1 = 6 and February is 5 + 2 = 7. It gives each month its own small theme inside the year."),
    ("Is 2027 a good or bad year?",
     "Numerology does not label years good or bad, and there is no scientific evidence that numbers predict what will happen. Each number simply suggests a focus. The same year can feel very different from one person to the next."),
    ("Is my birthday saved?",
     "No. The calculation runs in your browser. Your birthday is never sent, stored or put in the page address."),
]


def personal_year_page():
    form = f"""            <fieldset class="nup-fs">
              <legend class="t-label">Your birthday <span>(the year is not needed)</span></legend>
              <div class="nup-row">
                <div><label class="t-label" for="nup-month">Month</label>
                  <select id="nup-month" class="t-select" autocomplete="bday-month" required><option value="">Choose</option>{MONTH_OPTS}</select></div>
                <div><label class="t-label" for="nup-day">Day</label>
                  <select id="nup-day" class="t-select" autocomplete="bday-day" required><option value="">Choose</option>{DAYS}</select></div>
              </div>
            </fieldset>
            <fieldset class="nup-fs">
              <legend class="t-label">Which year?</legend>
              <div class="seg">
                <label><input type="radio" name="nup-year" value="2026"><span>2026</span></label>
                <label><input type="radio" name="nup-year" value="2027" checked><span>2027</span></label>
                <label><input type="radio" name="nup-year" value="2028"><span>2028</span></label>
              </div>
            </fieldset>
            <button class="btn nu-go" type="submit">Find my personal year</button>
            <p class="t-hint nu-method">How we count: month, day and year are each reduced to one digit, added, then reduced again. A master total (11, 22) is flagged, and the year is shown as one digit.</p>"""
    body = shell("personal-year", form, "Choose your birth month and day to see your 2027 personal year, with the maths step by step and a theme for every month.")

    worked_pm = [(i, red(int(personal_year(7, 14, 2027)) + i)[0]) for i in (1, 2)]
    article = f"""      <h2 id="what">What is a personal year number?</h2>
      <p>Numerology describes life in nine-year cycles. Each calendar year, you sit at one point in your own cycle, and that point is your personal year number. A 1 year is traditionally the start of a cycle, a 5 year the turning point in the middle, and a 9 year the end, when people often finish things and let go before the next 1 begins.</p>
      <p>Your number comes from your birth month and day, plus the year you are looking at. You do not need your birth year, which is why two people born in different years but on the same day and month share the same personal year number.</p>
      {NOTE}

      <h2 id="universal">2027 is a universal year 2</h2>
      <p>Every year also has its own number for everyone. For 2027 it is 2 + 0 + 2 + 7 = 11. The digits add up to the master number 11, which numerologists often read as a louder 2. Personal-year guides normally reduce it all the way to <strong>2</strong>, and that is the number this calculator adds into your personal year. If you like to read master numbers, you can think of 2027 as a quiet, listening year with an intuitive edge.</p>

      <h2 id="by-hand">How to calculate your personal year by hand</h2>
      <ol>
        <li>Reduce your birth month to one digit. July is 7, and November (11) becomes 1 + 1 = 2.</li>
        <li>Reduce your birth day to one digit. The 14th becomes 1 + 4 = 5.</li>
        <li>Reduce the year to one digit. For 2027 that is 2 + 0 + 2 + 7 = 11, then 1 + 1 = 2.</li>
        <li>Add the three, then reduce again if the total has two digits.</li>
      </ol>
      <p>Worked example for someone born on <strong>14 July</strong>: 7 + 5 + 2 = 14, then 1 + 4 = <strong>5</strong>. Their 2027 personal year is a 5, a year numerologists associate with change and freedom. For 2026 the year part is 2 + 0 + 2 + 6 = 10, then 1, so the same person has 7 + 5 + 1 = 13, then 1 + 3 = 4 (a year of foundations). For 2028 the year part is 2 + 0 + 2 + 8 = 12, then 3, so 7 + 5 + 3 = 15, then 6.</p>

      <h2 id="cycle">The nine-year cycle</h2>
      <p>Here is what each personal year traditionally stands for. Read it as the shape of the whole cycle: begin, build, bloom, rest, release.</p>
{py_cycle_table()}

      <h2 id="months">Personal months: a theme for each month of 2027</h2>
      <p>Inside a year, numerologists add a smaller rhythm. Your personal month is your personal year plus the calendar month number, reduced to one digit. With a personal year 5, for example, January is 5 + 1 = {worked_pm[0][1]} and February is 5 + 2 = {worked_pm[1][1]}. The calculator shows all twelve in a strip with a one-word theme for each, using the same meanings as the nine-year cycle table: 1 begin, 2 listen, 3 create, 4 build, 5 change, 6 care, 7 reflect, 8 focus, 9 finish.</p>

      <h2 id="meanings">What each 2027 personal year means</h2>
      <p>Each year has a traditional theme, a practical focus you can act on this month, and an affirmation. Find your number with the calculator, then read only that section.</p>
{py_meanings()}

      <h2 id="new-year">How to use your personal year for New Year intentions</h2>
      <ol>
        <li><strong>Read your theme in late December.</strong> Ask what it would look like to lean into it a little, not to force it.</li>
        <li><strong>Choose one intention that fits.</strong> A 4 year suits a routine, a 3 year suits a creative habit, a 9 year suits finishing something. A theme is a nudge, not a rule, so pick what you genuinely want.</li>
        <li><strong>Pick a word.</strong> Many people turn the theme into a single word for the year. The <a href="/word-of-the-year/">Word of the Year tool</a> takes you there in five questions.</li>
        <li><strong>Start small, together with a habit.</strong> A number gives you a theme; a daily practice turns it into progress. The free <a href="/new-year-manifestation-challenge/">21-day New Year challenge</a> is a gentle way to begin, and the <a href="/369-method/">369 method</a> (write your intention 3 times in the morning, 6 in the afternoon and 9 at night) keeps it in front of you.</li>
        <li><strong>Check in monthly.</strong> Use the personal month strip as a prompt: how did this month&rsquo;s theme show up, and what is one small step for the next?</li>
      </ol>

{related('/personal-year-number-calculator/')}"""
    p = base_page("/personal-year-number-calculator/", "Personal year number calculator",
                  "Personal Year Number Calculator 2027 (Free) | 369 Journal",
                  "Personal Year Number Calculator: Your 2027 Personal Year",
                  "Free personal year number calculator. Enter your birth month and day to see your 2027 personal year, the maths step by step, and a theme for each month.",
                  "Enter your birth month and day (no birth year needed) to see your 2027 personal year, with every step of the maths and a theme for each month of the year. Switch to 2026 or 2028 any time.",
                  ["Free, no sign-up", "2027 personal year and 12 months", "Nothing is saved"])
    nxt = next_steps(
        "A number gives you a theme. A daily habit turns it into progress.",
        "Your personal year suggests a focus for 2027. Writing down what you want, a little each day, is how a theme becomes something you do. Here are two calm ways to start.",
        "369", "web_personal_year",
        "Turn your 2027 theme into a 21-day habit",
        "369 Journal reminds you to write your intention 3, 6 and 9 times a day, and walks you through a 21-day cycle. Your first cycle is free.",
        "site-personal-year")
    return finish(p, PY_FAQ, body, article, nxt)


# =====================================================================================
# 2. Name numerology
# =====================================================================================
def chart_table():
    rows = [(n, ", ".join(ls.split())) for n, ls in CHART_ROWS.items()]
    return table(["Value", "Letters"], rows)


def name_example():
    name = "Maria Lopez"
    letters = [c for c in name.upper() if c.isalpha()]
    vows = [c for c in letters if c in "AEIOU"]
    cons = [c for c in letters if c not in "AEIOU"]

    def line(label, ls):
        vals = [CHART[c] for c in ls]
        v, steps = red(sum(vals), True)
        tail = (", then " + ", then ".join(steps)) if steps else ""
        return f"<li><strong>{label}:</strong> {' + '.join(f'{c}({CHART[c]})' for c in ls)} = {sum(vals)}{tail}, so <strong>{v}</strong>.</li>", v

    a, ea = line("Expression (all letters)", letters)
    b, eb = line("Soul urge (vowels)", vows)
    c, ec = line("Personality (consonants)", cons)
    return name, a + b + c, ea, eb, ec


NAME_FAQ = [
    ("How does name numerology work?",
     "Each letter is given a value from 1 to 9 using a chart (A, J and S are 1; B, K and T are 2; and so on). You add the values for your name, reduce the total to a single digit (or keep 11, 22 or 33), and read the meaning numerologists traditionally link to that number. Different parts of the name give different numbers: all letters for expression, vowels for soul urge, consonants for personality."),
    ("What is the difference between the expression, soul urge and personality numbers?",
     "The expression (or destiny) number uses every letter and is traditionally linked with your natural talents. The soul urge (or heart's desire) number uses only the vowels and is linked with what you care about at heart. The personality number uses only the consonants and is linked with the first impression you give."),
    ("Should I use my birth name or the name I go by now?",
     "Traditional numerology uses the full name on your birth certificate, including middle names. Many people also try their current name, a nickname or a married name to see how it compares. Enter both above and the calculator shows them side by side. The birth name is usually treated as the main one."),
    ("Is Y a vowel or a consonant?",
     "Numerologists disagree. Some count Y as a vowel when it makes a vowel sound, as in Lynn. To keep things simple and consistent, this calculator always counts Y as a consonant. If you want to test the other way, remove it and read the vowel number yourself using the letter chart on this page."),
    ("Why do other name numerology calculators give a different answer?",
     "There are two main systems. This page uses the Pythagorean system (letters 1 to 9 in order), which is the most common in the West. The Chaldean system uses a different chart and often reads the final digit differently. Calculators also differ on master numbers and on whether to add each name separately first. Different answers do not mean one is wrong, only that the rules are different."),
    ("What are the master numbers 11, 22 and 33 in a name?",
     "If a total lands on 11, 22 or 33 before it is reduced, this calculator keeps it as a master number, as most numerologists do. They describe 11 as a louder 2, 22 as a 4 with a bigger vision, and 33 as a 6 with a wider reach. 33 is the least commonly used."),
    ("Is name numerology real?",
     "There is no scientific evidence that the letters in your name affect your personality or your future. It is a traditional belief system. Many people enjoy it as a prompt for reflection, and the meanings are a starting point for asking yourself questions."),
    ("Is my name saved?",
     "No. The calculation runs in your browser. Your name is never sent, saved or put in the page address."),
]


def name_numerology_page():
    form = """            <label class="t-label" for="nup-name">Your full birth name</label>
            <input id="nup-name" class="t-input nu-input" type="text" maxlength="80" autocomplete="off" spellcheck="false" placeholder="e.g. Maria Elena Santos" required aria-describedby="nup-name-hint">
            <p class="t-hint" id="nup-name-hint">Use the name on your birth certificate, including middle names. Accents and punctuation are ignored.</p>

            <label class="t-label nu-gap" for="nup-name2">Your current name <span>(optional, to compare)</span></label>
            <input id="nup-name2" class="t-input nu-input" type="text" maxlength="80" autocomplete="off" spellcheck="false" placeholder="e.g. a married name or the name you use now" aria-describedby="nup-name2-hint">
            <p class="t-hint" id="nup-name2-hint">A nickname, a married name or a name you chose. We show both side by side.</p>

            <button class="btn nu-go" type="submit">Calculate my name numbers</button>
            <p class="t-hint nu-method">How we count: Pythagorean chart (A = 1 to I = 9, then it starts again). Y counts as a consonant. Master numbers 11, 22 and 33 are kept.</p>"""
    body = shell("name", form, "Type your full birth name to see your expression, soul urge and personality numbers, with every letter and its value.")
    name, ex_lines, ea, eb, ec = name_example()
    article = f"""      <h2 id="what">How name numerology works</h2>
      <p>Name numerology (sometimes called onomancy or the numerology of names) gives every letter a number from 1 to 9, adds up the letters in your name, and reduces the total to a single digit. Numerologists then read the meaning they traditionally link with that number. The idea is old and used in many forms; the version here is the Pythagorean one, the most common in the West.</p>
      <p>You get three numbers from one name, depending on which letters you add:</p>
      <ul>
        <li><strong>Expression (or destiny) number:</strong> every letter in your full name. Traditionally linked with your natural talents and how you tend to go about things.</li>
        <li><strong>Soul urge (or heart&rsquo;s desire) number:</strong> only the vowels. Traditionally linked with what you care about deep down.</li>
        <li><strong>Personality number:</strong> only the consonants. Traditionally linked with the first impression you give others.</li>
      </ul>
      {NOTE}

      <h2 id="chart">The Pythagorean letter chart</h2>
      <p>Write the letters from A to Z in rows of nine, starting again at 1 after I. That gives this chart:</p>
{chart_table()}
      <p>Vowels are A, E, I, O and U. This calculator counts Y as a consonant, so every number comes out the same way each time you use it.</p>

      <h2 id="worked">A worked example: {name}</h2>
      <p>The letters are M, A, R, I, A, L, O, P, E, Z. Using the chart:</p>
      <ul>
        {ex_lines}
      </ul>
      <p>So &ldquo;{name}&rdquo; has an expression number {ea}, a soul urge number {eb} and a personality number {ec}. The calculator above shows the same steps for any name, letter by letter.</p>

      <h2 id="which-name">Birth name, nickname or married name?</h2>
      <p>Traditionally, the <strong>full birth name</strong> (first, middle and last, as on your birth certificate) is the one that counts, because numerologists see it as the name you were given at the start. A <strong>nickname</strong> or a <strong>married name</strong> is often read as a layer on top: how you present yourself or the energy of a new chapter. Many people calculate both and notice where the numbers agree.</p>
      <p>Some people feel strongly about one name and shrug at the other, and that is a perfectly good way to use it. The calculator above lets you enter a current name next to the birth name and shows the two side by side.</p>

      <h2 id="master">Master numbers in a name</h2>
      <p>If a total lands exactly on 11, 22 or 33, it is kept as a master number instead of being reduced. Numerologists often read 11 as a louder 2, 22 as a 4 with bigger vision, and 33 as a 6 with a wider reach. Expression, soul urge and personality are each calculated on their own, so you can get a master number in one and not the others.</p>

      <h2 id="next">Where to go next</h2>
      <p>Your name numbers pair well with the number from your date of birth. Try the <a href="/life-path-number-calculator/">life path number calculator</a> for that, or the <a href="/personal-year-number-calculator/">personal year calculator</a> for the theme of 2027.</p>

{related('/name-numerology-calculator/')}"""
    p = base_page("/name-numerology-calculator/", "Name numerology calculator",
                  "Name Numerology Calculator (Free) | 369 Journal",
                  "Name Numerology Calculator",
                  "Free name numerology calculator: find your expression, soul urge and personality numbers, letter by letter, and compare your birth name with a current name.",
                  "Type your full birth name to see your expression (destiny), soul urge and personality numbers, with every letter and its value shown. Add a current name to compare the two.",
                  ["Free, no sign-up", "Letter-by-letter breakdown", "Nothing is saved"])
    nxt = next_steps(
        "From your name to your daily words",
        "A name number is a small prompt about who you are. Writing down what you want, in your own words, every day, is the practice that moves things. Here are two calm ways to keep going.",
        "369", "web_name_numerology",
        "Write your desire 3, 6 and 9 times a day",
        "369 Journal reminds you to write your desire morning, afternoon and night. Your first 21-day cycle is free.",
        "site-name-numerology")
    return finish(p, NAME_FAQ, body, article, nxt)


# =====================================================================================
# 3. Life path
# =====================================================================================
def compat_table():
    rows = []
    for a in range(1, 10):
        groups = {"easy": [], "comp": [], "care": []}
        for b in range(1, 10):
            lo, hi = min(a, b), max(a, b)
            groups[COMPAT[f"{lo}-{hi}"][0]].append(str(b))
        rows.append((str(a), ", ".join(groups["easy"]) or "-", ", ".join(groups["comp"]) or "-", ", ".join(groups["care"]) or "-"))
    return table(["Life path", "Often flows easily with", "Often balances well with", "May need patience with"], rows)


def lp_meanings():
    out = []
    for k in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "11", "22", "33"]:
        kind = "master number " if k in MASTER else ""
        out.append(f"""      <h3>Life path {k}: {', '.join(NUM[k][0][:3]).lower()}</h3>
      <p>{NUM[k][1]}</p>
      <p><strong>Worth watching:</strong> {CAUTION[k]}</p>
      <p class="nup-aff-q">Reflection: {NUM[k][3]}</p>""")
    return "\n".join(out)


LP_FAQ = [
    ("What is a life path number?",
     "In numerology, your life path number is worked out from your full date of birth and is traditionally linked with your natural approach to life: the strengths you tend to lean on and the lessons that tend to come up. It stays the same for your whole life. It is a prompt for reflection, not a prediction."),
    ("How do I calculate my life path number?",
     "Reduce your birth month, birth day and birth year each to a single digit (keeping 11, 22 and 33 if they appear), add the three results, then reduce the total. For 14 August 1990: month 8, day 1 + 4 = 5, year 1 + 9 + 9 + 0 = 19, then 1 + 9 = 10, then 1. Then 8 + 5 + 1 = 14, and 1 + 4 = 5. The life path number is 5."),
    ("What are the master numbers 11, 22 and 33?",
     "If your month, day, year or final total comes out as exactly 11, 22 or 33, numerologists keep it as a master number and read it as an intensified 2, 4 or 6. Many people read both the master number and the single-digit form. 33 is the least commonly used."),
    ("Why does my life path number differ on another site?",
     "Sites follow slightly different rules, mostly about when to keep master numbers. This calculator reduces your month, day and year separately and keeps 11, 22 and 33 whenever they appear, then adds and keeps a master total. Adding all the digits of the date in one go gives the same single digit but can miss a master number."),
    ("How does life path number compatibility work?",
     "Numerologists compare two life path numbers and describe how their traditional qualities tend to meet, for example a 1 and a 5 both like independence, while a 4 and a 5 may need patience about routine versus change. The mini-tool above uses a small, traditional set of pairings. It is a conversation starter, not a verdict."),
    ("Are some life paths incompatible?",
     "No. Numerology describes some pairings as easy and some as needing patience, but it does not say any pairing cannot work. There is also no scientific evidence that life path numbers affect how well two people get on. How you listen, talk and treat each other matters far more."),
    ("Is numerology real?",
     "There is no scientific evidence that numbers predict personality, relationships or the future. Numerology is a traditional belief system. Many people enjoy it as a prompt for reflection, and the meanings are a starting point for asking yourself useful questions."),
    ("Is my date of birth saved?",
     "No. The calculation runs in your browser. Your dates are never sent, stored or put in the page address."),
]


def life_path_page():
    form = """            <label class="t-label" for="nup-birth">Your date of birth</label>
            <input id="nup-birth" class="t-input nu-input" type="date" min="1900-01-01" max="2100-12-31" autocomplete="bday" required aria-describedby="nup-birth-hint">
            <p class="t-hint" id="nup-birth-hint">Used for your life path number.</p>

            <label class="t-label nu-gap" for="nup-birth2">Compare with another date of birth <span>(optional)</span></label>
            <input id="nup-birth2" class="t-input nu-input" type="date" min="1900-01-01" max="2100-12-31" aria-describedby="nup-birth2-hint">
            <p class="t-hint" id="nup-birth2-hint">A partner, friend or family member. You will see both life path numbers and a short, kind compatibility note.</p>

            <button class="btn nu-go" type="submit">Calculate my life path</button>
            <p class="t-hint nu-method">How we count: month, day and year are reduced separately, master numbers 11, 22 and 33 are kept, then the three are added.</p>"""
    body = shell("life-path", form, "Add your date of birth to see your life path number, how it is worked out, and what numerologists traditionally say about it. Add a second date to check compatibility.")
    article = f"""      <h2 id="what">What is a life path number?</h2>
      <p>Your life path number is the best-known number in numerology. It comes from your full date of birth and, traditionally, describes your natural approach to life: the strengths you tend to lean on and the lessons that tend to come up again and again. Because your birth date never changes, neither does your life path number.</p>
      {NOTE}

      <h2 id="by-hand">How to calculate your life path number by hand</h2>
      <ol>
        <li>Reduce your birth <strong>month</strong> to one digit (keep 11 if it is November).</li>
        <li>Reduce your birth <strong>day</strong> to one digit (keep 11 or 22 if the day is the 11th or 22nd).</li>
        <li>Reduce your birth <strong>year</strong> to one digit by adding its digits until one is left (keep 11, 22 or 33 if you land on one).</li>
        <li>Add the three results, then reduce again. Keep 11, 22 or 33 if the total lands on one.</li>
      </ol>
      <p>Worked example for <strong>14 August 1990</strong>: month 8; day 1 + 4 = 5; year 1 + 9 + 9 + 0 = 19, then 1 + 9 = 10, then 1 + 0 = 1. Add them: 8 + 5 + 1 = 14, then 1 + 4 = <strong>5</strong>. The life path number is 5.</p>

      <h2 id="master">Master numbers: 11, 22 and 33</h2>
      <p>When a month, day, year or the final total comes out as exactly 11, 22 or 33, it is kept as a master number. Numerologists describe 11 as a louder 2 (intuition and inspiration), 22 as a 4 with bigger vision (turning big ideas into real things) and 33 as a 6 with a wider reach (care and teaching). Many people read both the master number and its single-digit form, and some numerologists do not use 33 at all. If you get one, there is no pressure to &ldquo;live up&rdquo; to it.</p>

      <h2 id="meanings">Life path number meanings, 1 to 33</h2>
      <p>These are the meanings numerologists traditionally associate with each life path number, with one thing to watch and a question to think about.</p>
{lp_meanings()}

      <h2 id="compat">Life path number compatibility</h2>
      <p>To use the compatibility mini-tool, enter your date of birth and a second date in the calculator above. It shows both life path numbers and a short note from the traditional pairings below. Master numbers are read as their single-digit form for pairings (11 as 2, 22 as 4, 33 as 6).</p>
      <p>Numerologists traditionally group the numbers like this: 1, 5 and 7 are the independent thinkers; 2, 4 and 8 are the steady, practical ones; 3, 6 and 9 are the warm, expressive ones. Numbers from the same group often find each other easy to understand. Different groups can balance each other or need a little patience. The table lists each pairing.</p>
{compat_table()}
      <p>Please take this lightly. There is no scientific evidence that life path numbers predict how a relationship goes, and every pairing can work with good listening and kindness. Treat it as something fun to talk about together.</p>

      <h2 id="next">Where to go next</h2>
      <p>Add the theme of the year with the <a href="/personal-year-number-calculator/">personal year calculator</a> (your 2027 personal year is worked out from your birth month and day), or look at the numbers in your name with the <a href="/name-numerology-calculator/">name numerology calculator</a>.</p>

{related('/life-path-number-calculator/')}"""
    p = base_page("/life-path-number-calculator/", "Life path number calculator",
                  "Life Path Number Calculator and Compatibility | 369 Journal",
                  "Life Path Number Calculator (with Compatibility)",
                  "Free life path number calculator: enter your date of birth to see your number, how it is worked out and what it means. Compare two life paths for compatibility.",
                  "Enter your date of birth to find your life path number, with every step of the maths, its traditional meaning, strengths, things to watch and an affirmation. Add a second date to check compatibility.",
                  ["Free, no sign-up", "Includes compatibility check", "Nothing is saved"])
    nxt = next_steps(
        "Know your number? Now build the habit.",
        "A life path number is a thought to reflect on. Writing down what you want, a little each day, is what turns reflection into action. Here are two calm ways to start.",
        "369", "web_life_path",
        "Write your desire 3, 6 and 9 times a day",
        "369 Journal reminds you to write your desire morning, afternoon and night. Your first 21-day cycle is free.",
        "site-life-path")
    return finish(p, LP_FAQ, body, article, nxt)


if __name__ == "__main__":
    write("/personal-year-number-calculator/", personal_year_page())
    write("/name-numerology-calculator/", name_numerology_page())
    write("/life-path-number-calculator/", life_path_page())

#!/usr/bin/env python3
"""Numerology calculator (/numerology-calculator/).

Run:  cd scripts && python3 tool_numerology.py && python3 layout.py
All written meanings live here (NUM, PY) and are embedded in the page as JSON, so the static
guide (for search engines) and the interactive tool share one source.
Honest framing: "what numerologists traditionally associate with it", never predictions.
"""
import json

from build_posts import write
from toolkit import next_steps, privacy, tool_page

# key: (words, long text, short phrase, reflection question, affirmation)
NUM = {
    "1": (["Independent", "Starting", "Leading"],
          "Numerologists traditionally link the number 1 with independence and starting things. The picture is of someone who likes to find their own way and take the first step, even when nobody else has. The flip side people mention is carrying everything alone for too long.",
          "starting things and finding your own way",
          "Where would you like to lead the way, even in a small thing?",
          "I begin with courage, and I ask for help when I need it."),
    "2": (["Gentle", "Cooperative", "Sensitive"],
          "The number 2 is traditionally linked with partnership and listening. It is the peacemaker's number: someone who notices how others feel and likes to work together. The caution people mention is putting everyone else first and forgetting their own needs.",
          "listening, patience and working together",
          "Where could you say what you need, kindly and clearly?",
          "My needs matter, and I share them with kindness."),
    "3": (["Creative", "Expressive", "Joyful"],
          "The number 3 is traditionally linked with creativity and self-expression. People with a 3 are often described as good at putting feelings and ideas into words, art or humour. The caution is scattering that energy across too many things.",
          "creativity, expression and joy",
          "What would you make or say this week if nobody were judging it?",
          "I express myself freely, and I enjoy the process."),
    "4": (["Steady", "Practical", "Reliable"],
          "The number 4 is traditionally linked with foundations: building things slowly, one solid step at a time. People with a 4 are often described as dependable and good at turning plans into routines. The caution is becoming so careful that change feels hard.",
          "steady effort and solid foundations",
          "Which small routine is quietly holding your life together?",
          "I build my life one steady step at a time."),
    "5": (["Curious", "Free", "Adaptable"],
          "The number 5 is traditionally linked with change, curiosity and freedom. People with a 5 are often described as restless in a good way: they like variety, travel and new ideas. The caution is starting things and leaving before they bloom.",
          "curiosity, change and freedom",
          "What would you try if you were a little more curious than worried?",
          "I welcome change, and I stay grounded as I move."),
    "6": (["Caring", "Responsible", "Warm"],
          "The number 6 is traditionally linked with care, home and responsibility. People with a 6 are often described as the one others turn to for support. The caution is looking after everyone else before looking after yourself.",
          "care, home and responsibility",
          "What would caring for yourself look like today, in one small act?",
          "I give care freely, and I receive it too."),
    "7": (["Thoughtful", "Curious", "Private"],
          "The number 7 is traditionally linked with thinking, study and inner life. People with a 7 are often described as quiet observers who like to understand how things work. The caution is pulling away from people when things get hard.",
          "thinking, learning and inner quiet",
          "What do you need some quiet time to think through?",
          "I trust my inner voice, and I give myself time to think."),
    "8": (["Driven", "Capable", "Determined"],
          "The number 8 is traditionally linked with ambition, effort and getting things done. People with an 8 are often described as capable organisers who take responsibility seriously. It is a description of a style of working, not a promise about money or success. The caution is letting work take over everything else.",
          "effort, ambition and follow-through",
          "What are you working toward, and is it still what you want?",
          "I work with purpose, and I rest without guilt."),
    "9": (["Compassionate", "Wise", "Generous"],
          "The number 9 is traditionally linked with compassion and completion. People with a 9 are often described as big-hearted, with a wide view of life and a wish to help. The caution is holding on to old chapters that are ready to close.",
          "compassion, generosity and letting go",
          "What are you ready to let go of, to make room for something new?",
          "I let go with gratitude, and I give with an open heart."),
    "11": (["Intuitive", "Inspiring", "Sensitive"],
           "Numerologists call 11 a master number and often read it as the number 2 turned up louder. It is traditionally linked with intuition, inspiration and a strong sensitivity to the mood around you. People who relate to 11 sometimes find that energy intense, so being gentle with yourself is part of the picture.",
           "intuition, inspiration and sensitivity",
           "When did you last follow a quiet hunch, and what happened?",
           "I trust my intuition, and I look after my energy."),
    "22": (["Builder", "Practical", "Big-picture"],
           "Numerologists call 22 a master number and often read it as the number 4 with a bigger vision. It is traditionally linked with turning large ideas into real, lasting things, step by step. The pressure people mention is expecting too much of yourself too fast.",
           "turning big ideas into steady, real steps",
           "What big idea could you break into one small first step?",
           "I turn big ideas into steady, real steps."),
    "33": (["Nurturing", "Teacher", "Selfless"],
           "Numerologists call 33 a master number and often read it as the number 6 with a wider reach. It is traditionally linked with teaching, healing and caring for many people at once. It is also the rarest master number, and some numerologists do not use it at all. The caution is giving until your own cup is empty.",
           "care, teaching and giving to others",
           "How can you care for others without running yourself empty?",
           "I give from a full cup, and I look after myself first."),
}

# personal year: theme, line (one sentence for the table), text, suggestion, affirmation
PY = {
    "1": ("New beginnings",
          "A fresh start: a good year to begin something small and see it through.",
          "Numerologists read a 1 year as the start of a nine-year cycle: a time for beginnings, decisions and doing things your own way.",
          "Pick one thing you keep postponing and take its first small step this month.",
          "I am free to begin again."),
    "2": ("Patience and partnership",
          "A slower, gentler year about listening, waiting and working with others.",
          "A 2 year is read as a quieter time. Things may move more slowly, which numerologists see as an invitation to be patient and to value relationships.",
          "Choose one relationship to give a little more time and attention.",
          "I move at a pace that feels right, and I trust it."),
    "3": ("Expression and joy",
          "A year to be creative, social and a bit more playful.",
          "A 3 year is read as a time for creativity, friendships and speaking up. Many people use it as a reason to make more room for fun.",
          "Start a small creative habit, such as writing one page or sketching for ten minutes a day.",
          "I make room for joy, and I share what I make."),
    "4": ("Foundations and steady effort",
          "A practical year for routines, tidying up and building slowly.",
          "A 4 year is read as a time to build foundations: sort out the plans, habits and paperwork that everything else rests on.",
          "Pick one area (home, health, work) and set up one simple routine for it.",
          "I build a strong base, one steady step at a time."),
    "5": ("Change and freedom",
          "A lively year for trying new things and loosening old patterns.",
          "A 5 year, the middle of the cycle, is read as a time of change and variety. Numerologists often suggest staying flexible and open to the unexpected.",
          "Say yes to one new experience, and keep one steady habit to stay grounded.",
          "I welcome change, and I stay grounded as I move."),
    "6": ("Home and care",
          "A caring year centred on family, home and looking after yourself.",
          "A 6 year is read as a time for relationships, responsibility and creating a comfortable home. Numerologists also note it is a good time to look after yourself, not only others.",
          "Do one thing this month that makes your home or your daily routine feel kinder.",
          "I care for my home and for myself with kindness."),
    "7": ("Reflection and rest",
          "A reflective year for learning, thinking and slowing down.",
          "A 7 year is read as a more inward year: a time for study, rest and thinking about what you really want.",
          "Block out some quiet time each week, with no phone, to think or write.",
          "I give myself time to rest, think and listen within."),
    "8": ("Effort and results",
          "A focused year for work, goals and taking charge.",
          "An 8 year is read as a time when your effort shows. Numerologists link it with goals, responsibility and practical results. It is not a promise about money, only a nudge to be deliberate.",
          "Write down one clear goal and the first three steps toward it.",
          "I focus my effort on what matters most to me."),
    "9": ("Completion and release",
          "A year for finishing things and letting go of what you have outgrown.",
          "A 9 year closes the nine-year cycle. It is read as a time for wrapping up, forgiving, clearing out and making room for the next beginning.",
          "Finish one thing you have left half-done, and let go of one thing you have outgrown.",
          "I finish what I started and let go with gratitude."),
}

TYPES = {
    "expression": {
        "name": "Expression number (also called Destiny number)",
        "how": "Made from every letter in your name. Numerologists link it with your natural talents and how you tend to go about things.",
    },
    "soul": {
        "name": "Soul urge number (also called Heart's desire)",
        "how": "Made from the vowels in your name (A, E, I, O, U). Numerologists link it with what you care about deep down. Y is counted as a consonant here.",
    },
    "personality": {
        "name": "Personality number",
        "how": "Made from the consonants in your name. Numerologists link it with the first impression you give others.",
    },
}

DATA = {
    "num": {k: {"words": v[0], "text": v[1], "short": v[2], "ask": v[3], "aff": v[4]} for k, v in NUM.items()},
    "py": {k: {"theme": v[0], "line": v[1], "text": v[2], "do": v[3], "aff": v[4]} for k, v in PY.items()},
    "types": TYPES,
}

FAQ = [
    ("Is numerology real?",
     "There is no scientific evidence that numbers predict personality or the future. Numerology is a traditional belief system, not a science. Many people still enjoy it as a prompt for reflection: the meanings are just a starting point for asking yourself useful questions."),
    ("Do I use my birth name or my current name?",
     "Traditional numerology uses the full name on your birth certificate for the expression, soul urge and personality numbers. Some people also try the name they use today to see how it differs. Your life path number comes only from your date of birth, so it never changes."),
    ("What are master numbers?",
     "11, 22 and 33 are called master numbers. When a total comes out as one of them, numerologists usually keep it instead of reducing it further, and describe it as a stronger version of 2, 4 or 6. Many numerologists use only 11 and 22, and some people prefer to read both the master number and its single-digit form."),
    ("How is a personal year calculated?",
     "Add your birth month, your birth day and the year you want to look at, reducing each to a single digit first, then reduce the total to one digit. For 2027, someone born on 14 July does 7 + (1 + 4) + (2 + 0 + 2 + 7), which gives 7 + 5 + 2 = 14, then 1 + 4 = 5. That is a personal year 5."),
    ("Why does my life path number differ on another site?",
     "Different sites use slightly different rules, mainly about when to keep master numbers. This calculator reduces your month, day and year separately and keeps 11, 22 and 33 whenever they appear, then adds them and keeps a master number if the total is one. Our angel number page uses the same method, so both pages give the same number."),
    ("Is my name or birthday saved?",
     "No. Everything is worked out in your browser. Your name and date of birth are never sent or saved anywhere."),
]


def num_list():
    rows = []
    for k in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        rows.append(f"<li><strong>{k}: {', '.join(NUM[k][0][:3]).lower()}.</strong> Traditionally linked with {NUM[k][2]}.</li>")
    return "<ul>" + "".join(rows) + "</ul>"


def py_table():
    head = '<thead><tr><th scope="col">Personal year</th><th scope="col">Theme</th><th scope="col">What it often means</th></tr></thead>'
    rows = "".join(f'<tr><th scope="row">{k}</th><td>{PY[k][0]}</td><td>{PY[k][1]}</td></tr>\n' for k in PY)
    return f'<div class="table-wrap"><table>{head}<tbody>\n{rows}</tbody></table></div>'


def tool():
    body = """    <div class="tool-shell nu" data-numerology>
      <div class="tool-controls print-hide">
        <div class="tool-panel">
          <form class="nu-form" novalidate data-form>
            <label class="t-label" for="nu-birth">Your date of birth</label>
            <input id="nu-birth" class="t-input nu-input" type="date" min="1900-01-01" max="2100-12-31" autocomplete="bday" required aria-describedby="nu-birth-hint">
            <p class="t-hint" id="nu-birth-hint">Used for your life path number and your 2027 personal year.</p>

            <label class="t-label nu-gap" for="nu-name">Your full birth name <span>(optional)</span></label>
            <input id="nu-name" class="t-input nu-input" type="text" maxlength="80" autocomplete="off" spellcheck="false" placeholder="e.g. Maria Elena Santos" aria-describedby="nu-name-hint">
            <p class="t-hint" id="nu-name-hint">Adds your expression, soul urge and personality numbers. Use the name on your birth certificate if you can. Accents and punctuation are ignored, and Y counts as a consonant.</p>

            <button class="btn nu-go" type="submit">Calculate my numbers</button>
            <p class="t-hint nu-method">How we count: we reduce your month, day and year separately, keep the master numbers 11, 22 and 33, then add them up.</p>
          </form>
          """ + privacy("Runs in your browser. Your name and date of birth are never sent or saved.") + """
        </div>
      </div>

      <div class="tool-preview">
        <div class="nu-card" aria-live="polite" data-result>
          <div class="nu-empty">
            <div class="nu-orn" aria-hidden="true"><i></i><i></i><i></i></div>
            <p>Add your date of birth to see your life path number and what 2027 might hold. Add your name to see three more numbers.</p>
          </div>
        </div>
      </div>
    </div>
    <script type="application/json" id="numerology-data">""" + json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/") + """</script>"""

    article = f"""      <h2 id="what">What a numerology calculator does</h2>
      <p>Numerology is a traditional practice that gives each number from 1 to 9 (and the master numbers 11, 22 and 33) its own character, then turns your birth date and name into a handful of those numbers. This calculator does the adding for you and shows every step, so you can check it by hand.</p>
      <p>To be straightforward with you: there is no scientific evidence that numbers can predict your personality, relationships, health, money or future. What numerology does well is give you a short, structured set of questions to think about. Take what feels true, leave the rest, and treat it as a prompt for reflection, not an answer.</p>

      <h2 id="by-hand">How to calculate your life path number by hand</h2>
      <p>Your life path number comes from your full date of birth. Reduce the month, the day and the year on their own, add the three results, then reduce the total. Keep 11, 22 and 33 when they appear.</p>
      <p>Worked example for <strong>14 July 1990</strong>:</p>
      <ul>
        <li><strong>Month:</strong> July is 7.</li>
        <li><strong>Day:</strong> 14 becomes 1 + 4 = 5.</li>
        <li><strong>Year:</strong> 1990 becomes 1 + 9 + 9 + 0 = 19, then 1 + 9 = 10, then 1 + 0 = 1.</li>
        <li><strong>Total:</strong> 7 + 5 + 1 = 13, then 1 + 3 = 4.</li>
      </ul>
      <p>So the life path number is <strong>4</strong>.</p>

      <h2 id="meanings">Life path number meanings</h2>
      <p>These are the traditional associations, in a few words each. Use the calculator above for the longer version, with a question and an affirmation for every number.</p>
      {num_list()}

      <h2 id="master">Master numbers: 11, 22 and 33</h2>
      <p>If you land on 11, 22 or 33, numerologists keep it as a master number instead of reducing it. They usually describe 11 as a louder 2 (intuition), 22 as a 4 with a bigger vision (building), and 33 as a 6 with a wider reach (care and teaching). Many people read both the master number and its single-digit form. 33 is the least commonly used.</p>

      <h2 id="personal-year">Your personal year, and 2027</h2>
      <p>A personal year is a nine-year cycle that numerology uses to describe the tone of each year for you. Add your birth month, your birth day and the year you want, reducing each to a single digit first, then reduce the total to one digit. For 2027 the year part is 2 + 0 + 2 + 7 = 11, then 1 + 1 = 2.</p>
      <p>Here is what each personal year traditionally stands for. Many people read their number at the start of January and again in December, as a gentle way to plan the next twelve months.</p>
      {py_table()}
      <p>This is a prompt, not a forecast. A year labelled &ldquo;3&rdquo; does not guarantee anything. It simply suggests a question: where could I make more room for creativity this year? To turn that into one clear focus, pair your personal year with a <a href="/word-of-the-year/">Word of the Year</a>.</p>

      <h2 id="name">Name numbers explained</h2>
      <p>Name numbers give each letter a value from 1 to 9 using the Pythagorean chart (A, J and S are 1; B, K and T are 2; and so on down to I and R, which are 9). Add the values, reduce the total, and you have a number.</p>
      <ul>
        <li><strong>Expression (or destiny) number:</strong> all the letters in your full birth name. Linked with your natural talents and way of working.</li>
        <li><strong>Soul urge number:</strong> only the vowels (A, E, I, O, U). Linked with what you care about at heart. We count Y as a consonant.</li>
        <li><strong>Personality number:</strong> only the consonants. Linked with the first impression you give.</li>
      </ul>

      <h2 id="practice">Turn your numbers into a daily practice</h2>
      <ol>
        <li><strong>Read the question</strong> under your life path number and answer it in one honest sentence.</li>
        <li><strong>Read your personal year suggestion</strong> and pick one small action for this week.</li>
        <li><strong>Turn your affirmation into your own words</strong> with the <a href="/journal-prompt-generator/">journal prompt generator</a>, then keep it in front of you with the <a href="/369-method/">369 method</a>: write it 3 times in the morning, 6 in the afternoon and 9 at night.</li>
        <li><strong>Seeing a number again and again?</strong> Look it up in the <a href="/angel-number-calculator/">angel number calculator</a>, or read <a href="/369-meaning/">what 369 means</a>.</li>
      </ol>"""

    p = {
        "path": "/numerology-calculator/",
        "crumb": "Numerology calculator",
        "title": "Numerology Calculator: Life Path and Personal Year | 369 Journal",
        "h1": "Numerology Calculator",
        "description": "Free numerology calculator: find your life path number, name numbers (destiny, soul urge) and your 2027 personal year. No sign-up, nothing saved.",
        "lede": "Find your life path number from your date of birth, add your name for your expression, soul urge and personality numbers, and see what 2027 might hold. Every step is shown, and every meaning comes with a question to reflect on.",
        "badges": ["Free, no sign-up", "Life path, name and 2027 year", "Nothing is saved"],
    }
    assert len(p["title"]) <= 65, len(p["title"])
    assert 130 <= len(p["description"]) <= 155, len(p["description"])
    nxt = next_steps(
        "Turn your numbers into a daily habit",
        "Reading your numbers is a moment. Writing down what you want, every day, is a practice. Here are two calm ways to keep going.",
        "369", "web_numerology",
        "Write your desire 3, 6 and 9 times a day",
        "369 Journal reminds you to write your desire morning, afternoon and night. Your first 21-day cycle is free.",
        "site-numerology")
    return tool_page(p, FAQ, body, js="numerology.js", css="numerology.css", article=article, next_html=nxt)


if __name__ == "__main__":
    write("/numerology-calculator/", tool())

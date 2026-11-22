#!/usr/bin/env python3
"""Angel number meanings tool (/angel-number-calculator/) and the /369-meaning/ article.

Run:  python3 scripts/tool_angel.py && python3 scripts/layout.py
The curated meanings live here (NUMBERS, DIGITS) and are embedded in the page as JSON,
so the static table (for search engines) and the interactive tool share one source.
"""
import html
import json

from build_posts import app_plug, book_card, post, write
from toolkit import next_steps, privacy, tool_page

# Plain, honest wording: "commonly associated with", never predictions.
NUMBERS = {
    "000": (["Fresh start", "Openness", "Possibility"],
            "000 is often read as a blank page: a moment between one chapter and the next. People who notice it tend to take it as a nudge to begin again without carrying old expectations.",
            "What would you start today if you didn't need it to be perfect?",
            "I am open to a fresh start, one small step at a time."),
    "111": (["Beginnings", "Focus", "Intention"],
            "111 is commonly linked with new beginnings and paying attention to your thoughts. Many people treat it as a cue to check where their attention is going and to set a clear intention.",
            "What are you thinking about most often this week, and is it what you want to grow?",
            "My thoughts are clear, and I choose them with care."),
    "222": (["Balance", "Patience", "Partnership"],
            "222 is often associated with balance and patience: things settling into place, and relationships that work in both directions. It is a gentle reminder that steady progress still counts.",
            "Where in your life could a little more patience help?",
            "I trust the pace of my life, and I stay steady."),
    "333": (["Creativity", "Expression", "Support"],
            "333 is widely linked with creativity, self-expression and feeling supported. People often read it as encouragement to share an idea or make something with their hands.",
            "What would you make or say if nobody were judging it?",
            "I express myself freely, and I feel supported."),
    "444": (["Stability", "Foundations", "Protection"],
            "444 is commonly associated with solid foundations and feeling protected. Many people take it as a sign to keep building the boring, reliable habits that hold everything else up.",
            "Which small daily habit is quietly holding your life together?",
            "I am building strong foundations, day by day."),
    "555": (["Change", "Freedom", "Movement"],
            "555 is often linked with change and movement: something shifting, or a readiness to let something go. People use it as a prompt to welcome a change instead of resisting it.",
            "What change are you ready for, even if it feels uncomfortable?",
            "I welcome change, and I move through it with ease."),
    "666": (["Care", "Home", "Rebalancing"],
            "Despite its reputation, in numerology 666 is usually read gently: as a cue to rebalance and care for home, family and your own needs, especially if you have been focused only on work or worry.",
            "What would caring for yourself look like today, in one small act?",
            "I care for myself and my home with kindness."),
    "777": (["Reflection", "Learning", "Inner wisdom"],
            "777 is commonly associated with reflection, study and trusting your inner voice. Many people treat it as a reminder to slow down and learn from what is already happening.",
            "What has this season of your life been trying to teach you?",
            "I trust my inner wisdom, and I keep learning."),
    "888": (["Abundance", "Flow", "Reward for effort"],
            "888 is often linked with abundance and effort paying off. People who notice it usually read it as encouragement to keep going with the work they have already started.",
            "Where is your effort already starting to show results?",
            "Good things flow to me as I keep showing up."),
    "999": (["Completion", "Closure", "Letting go"],
            "999 is commonly associated with endings and completion: closing a chapter so a new one has room. It is often read as permission to finish something well and let it go.",
            "What is ready to be finished, so something new can begin?",
            "I let go with gratitude and make room for what's next."),
    "1010": (["Growth", "Self-belief", "Next level"],
             "1010 is often linked with personal growth and believing in your direction. People read it as a reminder that they are further along than they feel.",
             "What evidence do you already have that you are growing?",
             "I believe in my path, and I keep growing."),
    "1111": (["Alignment", "Awareness", "Wishes"],
             "1111 is one of the most noticed numbers. It is commonly associated with alignment and awareness, and many people use the moment to make a quiet wish or restate an intention.",
             "If you could set one intention right now, what would it be?",
             "I am aligned with what I truly want."),
    "1212": (["Trust", "Steady steps", "Comfort zone"],
             "1212 is often read as encouragement to trust the process and step a little outside your comfort zone, while keeping your feet on the ground.",
             "What is one slightly brave step you could take this week?",
             "I trust myself to take the next step."),
    "1221": (["Positivity", "Perspective", "Self-trust"],
             "1221 is a mirror number, often associated with keeping a positive perspective and trusting yourself when things feel uncertain.",
             "How would you see your situation if you were looking back on it from a year from now?",
             "I keep a hopeful, steady perspective."),
    "1234": (["Progress", "Simplicity", "One step at a time"],
             "1234 is commonly linked with progress made in order: one step, then the next. People take it as a sign to simplify and focus on the very next step.",
             "What is the very next step, and only that?",
             "I move forward one simple step at a time."),
    "2222": (["Harmony", "Faith", "Cooperation"],
             "2222 amplifies the balance of 222. It is often associated with harmony in relationships and keeping faith that things are coming together.",
             "Which relationship would benefit from a little more patience or kindness?",
             "Harmony grows in my life and my relationships."),
    "3333": (["Joy", "Growth", "Encouragement"],
             "3333 is commonly read as strong encouragement: to enjoy the process, express yourself and keep growing.",
             "What brought you real joy this week?",
             "I grow with joy, and I let myself shine."),
    "4444": (["Support", "Hard work", "Security"],
             "4444 is often linked with feeling supported and secure while you do steady, honest work.",
             "Who or what supports you, and have you thanked them lately?",
             "I am supported, safe and steady."),
    "5555": (["Big change", "Adventure", "Release"],
             "5555 is commonly associated with a larger change or a new adventure. People use it as a prompt to stay flexible and curious.",
             "What would you try if you were a little more curious than afraid?",
             "I meet change with curiosity and courage."),
    "369": (["The 369 method", "Intention", "Daily focus"],
            "Today 369 is best known through the 369 manifestation method: writing one desire 3 times in the morning, 6 in the afternoon and 9 at night. As a number, people often read it as a reminder to restate their intention and stay focused on it through the day.",
            "If you wrote one sentence 18 times today, what would you want it to be?",
            "I keep my intention in front of me, morning, afternoon and night."),
    "963": (["Reflection", "Completion", "Inner work"],
            "963 is 369 in reverse, so people often connect it with looking back: reflecting on what you have written or worked toward, and noticing how far you have come.",
            "What have you already achieved that you once only hoped for?",
            "I honour how far I have come."),
    "639": (["Connection", "Love", "Harmony"],
            "639 is often associated with connection and harmony in relationships, partly through its link to a commonly shared \"639 Hz\" meditation tone.",
            "Who would you like to feel closer to, and what small gesture could help?",
            "I give and receive love with an open heart."),
    "144": (["Hard work", "Patience", "Building"],
            "144 is often linked with steady effort and patience: the slow building that eventually becomes something solid.",
            "What are you building slowly that deserves more patience?",
            "My steady effort is building something lasting."),
    "717": (["Encouragement", "Right path", "Learning"],
            "717 is commonly read as encouragement that you are learning the right lessons and moving in a good direction.",
            "What recent choice are you quietly proud of?",
            "I am on a good path, and I keep learning."),
    "818": (["Abundance", "Transition", "Confidence"],
            "818 is often associated with a transition toward more abundance, and with the confidence to step into it.",
            "What would you do differently if you fully trusted your own abilities?",
            "I step confidently into new abundance."),
    "1717": (["Optimism", "Self-belief", "Momentum"],
             "1717 is commonly linked with optimism and momentum: believing in yourself enough to keep moving.",
             "Where could a little more optimism change how you act today?",
             "I believe in myself, and my momentum grows."),
}

# Associations for single digits and the master numbers, used for computed readings and birthdays.
DIGITS = {
    "0": ("Potential", "wholeness, potential and fresh starts"),
    "1": ("Beginnings", "new beginnings, independence and focus"),
    "2": ("Balance", "balance, patience and partnership"),
    "3": ("Expression", "creativity, joy and self-expression"),
    "4": ("Foundations", "stability, hard work and structure"),
    "5": ("Change", "change, freedom and curiosity"),
    "6": ("Care", "care, home and responsibility"),
    "7": ("Reflection", "reflection, learning and inner wisdom"),
    "8": ("Abundance", "abundance, ambition and confidence"),
    "9": ("Completion", "completion, compassion and letting go"),
    "11": ("Intuition", "intuition, inspiration and insight"),
    "22": ("Master builder", "big plans made practical, one step at a time"),
    "33": ("Compassion", "compassion, teaching and caring for others"),
}

BIRTH_TEXT = {
    "1": "People with a 1 are often described as independent starters who like to lead and try new things.",
    "2": "People with a 2 are often described as patient, cooperative and good at bringing people together.",
    "3": "People with a 3 are often described as expressive, creative and warm with others.",
    "4": "People with a 4 are often described as practical, reliable builders who like a clear plan.",
    "5": "People with a 5 are often described as curious and adaptable, happiest with variety and freedom.",
    "6": "People with a 6 are often described as caring and responsible, the ones others lean on.",
    "7": "People with a 7 are often described as thoughtful and reflective, drawn to learning and quiet time.",
    "8": "People with an 8 are often described as ambitious and confident, comfortable with responsibility.",
    "9": "People with a 9 are often described as compassionate and generous, with a big-picture view.",
    "11": "11 is kept as a \"master number\" and is often described as intuitive and inspiring to others.",
    "22": "22 is kept as a \"master number\" and is often described as a builder of big, practical plans.",
    "33": "33 is kept as a \"master number\" and is often described as caring, generous and teacherly.",
}

PAGES = {"111", "222", "333", "444", "555", "777", "999", "1010", "1111", "1212", "369"}

POPULAR = ["111", "222", "333", "444", "555", "777", "888", "999", "1111", "1212", "369"]

DATA = {
    "numbers": {k: {"words": v[0], "text": v[1], "ask": v[2], "aff": v[3]} for k, v in NUMBERS.items()},
    "digits": {k: {"word": v[0], "text": v[1]} for k, v in DIGITS.items()},
    "birth": BIRTH_TEXT,
}

DOTS = '<span class="an-dots" aria-hidden="true"><span><i></i><i></i><i></i></span><span><b></b><b></b><b></b><b></b><b></b><b></b></span><span><em></em><em></em><em></em><em></em><em></em><em></em><em></em><em></em><em></em></span></span>'

FAQ = [
    ("What is an angel number?", "An angel number is a repeating or patterned number, like 111 or 444, that some people notice again and again and read as a meaningful sign. The idea comes from numerology and modern spiritual communities."),
    ("Are angel numbers real?", "There is no scientific evidence that numbers carry messages. Our brains are very good at noticing patterns, especially ones we are already thinking about. Many people still find angel numbers useful as a reminder to pause, breathe and check their intentions."),
    ("How does the angel number calculator work?", "Look up any number you keep seeing. Popular numbers have a written meaning; any other number gets a reading built from its digits and its reduced number. In birthday mode, your birth month, day and year are each reduced, then added together until one digit (or 11, 22 or 33) is left, and the steps are shown."),
    ("What does it mean if I keep seeing the same number?", "Most often it means the number has caught your attention, and once something has your attention you notice it more. You can use that moment as a cue to reflect: the question under each meaning is a good place to start."),
    ("What is the 369 angel number?", "369 is best known through the 369 manifestation method, where you write one desire 3, 6 and 9 times a day. As an angel number, people usually read it as a reminder to restate their intention."),
    ("Is my birthday or number saved anywhere?", "No. The tool runs in your browser. Your date of birth is never sent or stored."),
]


def popular_table():
    rows = "".join(
        f'<tr><th scope="row"><a href="#n={n}" data-n="{n}">{n}</a></th><td>{", ".join(NUMBERS[n][0])}</td><td>{html.escape(NUMBERS[n][3])}</td><td>{f'<a href="/angel-numbers/{n}/">{n} meaning</a>' if n in PAGES else ""}</td></tr>'
        for n in ["000", "111", "222", "333", "444", "555", "666", "777", "888", "999", "1010", "1111", "1212", "1234", "369"])
    return f'<div class="table-wrap"><table><thead><tr><th scope="col">Number</th><th scope="col">Commonly associated with</th><th scope="col">Affirmation to try</th><th scope="col">Full page</th></tr></thead><tbody>{rows}</tbody></table></div>'


def tool():
    chips = "".join(f'<button type="button" class="an-chip" data-n="{n}">{n}</button>' for n in POPULAR)
    body = f"""    <div class="tool-shell an" data-angel>
      <div class="tool-controls print-hide">
        <div class="tool-panel">
          <div class="seg an-mode" role="radiogroup" aria-label="What would you like to look up?">
            <label><input type="radio" name="an-mode" value="number" checked><span>A number I keep seeing</span></label>
            <label><input type="radio" name="an-mode" value="birthday"><span>My birthday number</span></label>
          </div>

          <form class="an-form" data-pane="number" novalidate>
            <label class="t-label" for="an-number">Type the number</label>
            <div class="an-row">
              <input id="an-number" class="t-input an-input" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="6" autocomplete="off" placeholder="e.g. 444">
              <button class="btn" type="submit">Show meaning</button>
            </div>
            <p class="t-label an-pop-label">Popular numbers</p>
            <div class="an-chips">{chips}</div>
          </form>

          <form class="an-form" data-pane="birthday" hidden novalidate>
            <label class="t-label" for="an-birth">Your date of birth</label>
            <div class="an-row">
              <input id="an-birth" class="t-input an-input" type="date" min="1900-01-01" max="2026-12-31">
              <button class="btn" type="submit">Find my number</button>
            </div>
            <p class="t-hint">We reduce your birth month, day and year separately, then add them until one digit is left (or 11, 22 or 33). It's the same life path method as our <a href="/numerology-calculator/">numerology calculator</a>.</p>
          </form>
          {privacy("Runs in your browser. Your number and date of birth are never sent or saved.")}
        </div>
      </div>

      <div class="tool-preview">
        <div class="an-card" aria-live="polite" data-result>
          <div class="an-empty">
            {DOTS}
            <p>Type a number you keep seeing, or tap one of the popular numbers, to read what people commonly associate it with.</p>
          </div>
        </div>
      </div>
    </div>
    <script type="application/json" id="angel-data">{json.dumps(DATA, ensure_ascii=False)}</script>"""

    article = f"""      <h2 id="what">What are angel numbers?</h2>
      <p>Angel numbers are repeating or patterned numbers, such as 111, 444 or 1212, that some people notice again and again: on a clock, a receipt or a number plate. The idea comes from numerology and modern spiritual communities, where each digit has long carried its own associations. Curious about the numbers in your own birthday and name? Try the free <a href="/life-path-number-calculator/">life path number calculator</a> or the <a href="/name-numerology-calculator/">name numerology calculator</a>. Each common number also has its own page, for example <a href="/angel-numbers/444/">444</a>, <a href="/angel-numbers/555/">555</a>, <a href="/angel-numbers/1111/">1111</a>.</p>
      <p>To be straightforward with you: there is no scientific evidence that numbers carry messages. Our minds are pattern-finders, and we notice what we are already thinking about. Many people still find angel numbers helpful as a small, everyday reminder to pause, breathe and check in with what they want. That is how this tool is meant to be used.</p>

      <h2 id="use">How to use an angel number as a reflection prompt</h2>
      <ol>
        <li><strong>Notice it</strong> and take one slow breath.</li>
        <li><strong>Read the question</strong> under its meaning and answer it in one honest sentence.</li>
        <li><strong>Choose one small action</strong> that fits your answer, and do it today.</li>
        <li><strong>Keep an intention in front of you.</strong> Many people pair this with the <a href="/369-method/">369 method</a>: writing one affirmation 3, 6 and 9 times a day.</li>
      </ol>

      <h2 id="popular">Popular angel numbers and their meanings</h2>
      <p>Tap any number to open its meaning in the tool above, or read the full page for love, money and what to do when you see it. All of them are on the <a href="/angel-numbers/">angel numbers page</a>.</p>
{popular_table()}
      <p>Keep seeing 369? Read <a href="/369-meaning/">what 369 means</a>, including the 369 method and where the Tesla story comes from.</p>"""

    p = {
        "path": "/angel-number-calculator/",
        "crumb": "Angel number meanings",
        "title": "Angel Number Calculator and Meanings (Free) | 369 Journal",
        "h1": "Angel Number Meanings",
        "description": "Look up any angel number you keep seeing (111, 444, 1111, 369) or find your birthday number, with honest meanings and an affirmation for each.",
        "lede": "Look up a number you keep seeing, or find the number in your birthday. Each meaning comes with a question to reflect on and an affirmation to try. No hype, no predictions.",
        "badges": ["Free", "No sign-up", "Any number, plus your birthday"],
    }
    nxt = next_steps(
        "Turn a sign into a habit",
        "Noticing a number is a moment. Writing your intention every day is a practice. Here are two calm ways to keep going.",
        "369", "web_angel",
        "Write your intention 3, 6 and 9 times a day",
        "369 Journal reminds you morning, afternoon and night (at most three times a day) and counts every line. Your first 21-day cycle is free.",
        "site-angel")
    return tool_page(p, FAQ, body, js="angel.js", css="angel.css", article=article, next_html=nxt)


MEANING_FAQ = [
    ("What does 369 mean?", "369 is best known today through the 369 manifestation method: writing one desire 3 times in the morning, 6 in the afternoon and 9 at night. As an angel number, people commonly read it as a reminder to restate an intention and stay focused on it."),
    ("What does seeing 369 mean spiritually?", "In numerology, 3 is associated with expression, 6 with care and 9 with completion. Together, people often read 369 as a cue to express what you want, care for it daily and trust it to unfold. There is no scientific evidence behind these meanings; many people simply use them as a prompt to reflect."),
    ("Did Nikola Tesla say 3, 6 and 9 are the key to the universe?", "There is no reliable source for that quote. Fact-checkers found no trace of it before about 2018, decades after Tesla's death. Tesla did have well-documented habits around the number three."),
    ("What does 369 mean in a relationship or for love?", "People often read 369 as a reminder to be clear about what you want in love, to care for the relationship you have, and to let go of what no longer fits. It is not a prediction about any specific person."),
    ("How do I use 369 to manifest?", "Choose one desire, write it as a short present-tense affirmation, and write it 3 times in the morning, 6 in the afternoon and 9 at night for 21, 33 or 45 days, alongside one small real action each day."),
]


def meaning_page():
    body = f"""      <nav class="toc" aria-label="On this page">
        <strong>On this page</strong>
        <ol>
          <li><a href="#short">369 meaning in one minute</a></li>
          <li><a href="#numerology">3, 6 and 9 in numerology</a></li>
          <li><a href="#angel">369 as an angel number</a></li>
          <li><a href="#method">The 369 manifestation method</a></li>
          <li><a href="#tesla">Tesla and 369</a></li>
          <li><a href="#seeing">If you keep seeing 369</a></li>
        </ol>
      </nav>

      <h2 id="short">369 meaning in one minute</h2>
      <p>Most people searching for 369 have come across it in one of two ways: as an <strong>angel number</strong> they keep seeing, or through the <strong>369 manifestation method</strong>, a writing ritual popular on TikTok and in law of attraction communities. The two meanings point the same way. 369 is commonly read as a reminder to <strong>be clear about what you want and keep it in front of you</strong>.</p>

      <h2 id="numerology">3, 6 and 9 in numerology</h2>
      <div class="table-wrap"><table><thead><tr><th scope="col">Number</th><th scope="col">Commonly associated with</th><th scope="col">In the 369 method</th></tr></thead><tbody>
<tr><th scope="row">3</th><td>Creativity, expression, joy</td><td>Morning: write your desire 3 times to set the tone</td></tr>
<tr><th scope="row">6</th><td>Care, home, responsibility</td><td>Afternoon: write it 6 times to return to it</td></tr>
<tr><th scope="row">9</th><td>Completion, compassion, letting go</td><td>Night: write it 9 times to close the day</td></tr>
</tbody></table></div>
      <p>Want to see which numbers numerology links with you? The free <a href="/numerology-calculator/">numerology calculator</a> works out your life path number, your name numbers and your 2027 personal year, with the maths shown.</p>
      <p>Put together, people often read 369 as a small story: <em>say what you want, care for it every day, then let it go and trust the process</em>.</p>

      <h2 id="angel">369 as an angel number</h2>
      <p>If 369 keeps appearing on clocks, receipts or tickets, people commonly take it as a nudge to restate their intention. Its reverse, 963, is often linked with looking back on progress, and 639 with connection and love. Read the full <a href="/angel-numbers/369/">369 angel number meaning</a> for love, money and what to do when you see it.</p>
      <p>Seeing a different number? We have a page for each of the most common ones: <a href="/angel-numbers/111/">111</a>, <a href="/angel-numbers/222/">222</a>, <a href="/angel-numbers/333/">333</a>, <a href="/angel-numbers/444/">444</a>, <a href="/angel-numbers/555/">555</a>, <a href="/angel-numbers/777/">777</a>, <a href="/angel-numbers/999/">999</a>, <a href="/angel-numbers/1010/">1010</a>, <a href="/angel-numbers/1111/">1111</a> and <a href="/angel-numbers/1212/">1212</a>, plus <a href="/angel-numbers/">all angel numbers in one place</a>.</p>
      <p>We want to be honest: there is no scientific evidence that numbers carry messages. Our minds notice what we are already thinking about. That doesn't make the moment useless. Many people use it as a cue to pause and ask themselves one question.</p>
      <div class="an-mini">
        <p><strong>Look up 369, or any number you keep seeing.</strong> Free, with a reflection question and an affirmation for each.</p>
        <a class="btn" href="/angel-number-calculator/#n=369">Open the angel number tool</a>
      </div>

      <h2 id="method">The 369 manifestation method</h2>
      <p>The 369 method is a daily writing ritual. You choose one desire, write it as a short present-tense affirmation, and write it <strong>3 times in the morning, 6 times in the afternoon and 9 times at night</strong>, usually for 21, 33 or 45 days. The full step-by-step is in <a href="/369-method/">how to do the 369 method</a>, and you can word yours with the <a href="/affirmation-generator/">free affirmation generator</a>.</p>

      <h2 id="tesla">Tesla and 369</h2>
      <p>369 is often linked to Nikola Tesla through a quote about 3, 6 and 9 being a key to the universe. There is no reliable source for that quote, and it seems to have appeared online only in recent years. Tesla did have well-documented habits around the number three. We go through the evidence in <a href="/369-method/tesla/">did Tesla really create the 369 method?</a></p>

      <h2 id="seeing">If you keep seeing 369</h2>
      <ul>
        <li><strong>Pause</strong> and take one slow breath.</li>
        <li><strong>Ask:</strong> if I wrote one sentence 18 times today, what would I want it to be?</li>
        <li><strong>Write that sentence down</strong>, then do one small thing that points toward it.</li>
      </ul>
"""
    p = {
        "path": "/369-meaning/",
        "crumb": "369 meaning",
        "title": "369 Meaning: Angel Number 369 and the 369 Method | 369 Journal",
        "h1": "What Does 369 Mean?",
        "description": "What 369 means: 3, 6 and 9 in numerology, 369 as an angel number, the 369 manifestation method, and the truth about the Tesla quote.",
        "lede": "369 shows up as an angel number and as a popular manifestation method. Here is what people commonly mean by it, what each number stands for, and how to use it in a calm, practical way.",
        "body": body,
        "faq": MEANING_FAQ,
        "end": book_card("369", "web_369_meaning") + "\n" + app_plug(
            "Practise 369, one day at a time",
            "369 Journal reminds you morning, afternoon and night and counts every line. Your first 21-day cycle is free.",
            "site-369-meaning"),
        "related": [
            ("/angel-number-calculator/", "Angel number meanings: look up any number"),
            ("/369-method/", "How to do the 369 method"),
            ("/369-method/tesla/", "Did Tesla really create the 369 method?"),
            ("/affirmation-generator/", "Free affirmation generator"),
            ("/books/", "Books: The 369 Method and Scripting Manifestation"),
        ],
    }
    html_out = post(p)
    # The mini call-to-action box uses the tool's stylesheet.
    return html_out.replace("</head>", '  <link rel="stylesheet" href="/assets/tools/angel.css?v=20261118">\n</head>', 1)


if __name__ == "__main__":
    write("/angel-number-calculator/", tool())
    write("/369-meaning/", meaning_page())

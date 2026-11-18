#!/usr/bin/env python3
"""Builds the Books page and the November 2026 posts.

Edit the content below, then run:
    python3 scripts/build_posts.py && python3 scripts/layout.py
Pages get the shared header/footer (from layout.py), Article + FAQPage +
Breadcrumb structured data, book cards and an App Store badge with its own
campaign tag. Book links go through the 369 Journal API, which sends each
reader to their own country's Amazon store and logs the tap (src=web_...).
"""
import html
import json
import pathlib

from layout import badge, footer, header

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://369journal.app"
PUBLISHED = "2026-11-18"
BOOK_API = "https://369-journal-api.vercel.app/api/book"

BOOKS = {
    "369": {
        "title": "The 369 Method",
        "subtitle": "A Practical Guide and 45-Day Manifestation Workbook",
        "cover": "/assets/img/books/the-369-method.jpg",
        "pitch": "A short guide to the 369 method, then 45 guided days. Each day has a lesson, a question and room for all 18 lines.",
        "asins": {"paperback": "B0HRZRJDBS", "kindle": "B0H4X525KK"},
        "isbn": "9798143516724",
    },
    "scripting": {
        "title": "Scripting Manifestation",
        "subtitle": "A Calm Guide and 30-Day Workbook",
        "cover": "/assets/img/books/scripting-manifestation.jpg",
        "pitch": "How to write one ordinary moment of your desire as if it already happened. A short guide, then 30 days with a lesson, an example and a full page to write.",
        "asins": {"paperback": "B0HS18RGQ9", "kindle": "B0HRZYDQT2"},
    },
}

KINDLE_NOTES = {
    "369": "The Kindle edition has the full guide, a lesson for each week and all 45 daily questions, to use with your own notebook. The paperback adds a guided write-in page for every day.",
    "scripting": "The Kindle edition has the full guide and all 30 daily lessons, examples and prompts, to use with your own notebook. The paperback adds a ready-made write-in page for every day.",
}


def book_link(book_id, fmt, src):
    return f"{BOOK_API}?b={book_id}&amp;f={fmt}&amp;src={src}"


def book_card(book_id, src, heading="h3", note=True):
    b = BOOKS[book_id]
    note_html = f'\n        <p class="book-note">{KINDLE_NOTES[book_id]}</p>' if note else ""
    return f"""      <div class="book-card">
        <img src="{b['cover']}" alt="Cover of {b['title']} by Tejas Rane" width="600" height="960" loading="lazy">
        <div class="book-info">
          <{heading}>{b['title']}</{heading}>
          <p class="sub">{b['subtitle']}</p>
          <p class="pitch">{b['pitch']}</p>
        </div>
        <div class="book-buy">
          <a class="btn" href="{book_link(book_id, 'paperback', src)}" data-book="{book_id}-paperback" data-src="{src}">Paperback on Amazon</a>
          <a class="btn ghost" href="{book_link(book_id, 'kindle', src)}" data-book="{book_id}-kindle" data-src="{src}">Kindle eBook</a>
        </div>{note_html}
      </div>"""


def app_plug(title, text, ct):
    return f"""      <div class="app-plug" style="margin-top:2.5rem">
        <img class="icon" src="/assets/img/app-icon-512.png" alt="369 Journal app icon" width="64" height="64">
        <div>
          <h3>{title}</h3>
          <p>{text}</p>
        </div>
        {badge(ct)}
      </div>"""


def table(headers, rows):
    head = "".join(f'<th scope="col">{h}</th>' for h in headers)
    body = "\n".join(
        "<tr>" + "".join((f'<th scope="row">{c}</th>' if i == 0 else f"<td>{c}</td>") for i, c in enumerate(r)) + "</tr>"
        for r in rows
    )
    return f'      <div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>\n{body}\n</tbody></table></div>'


def head(p, ld):
    url = f"{SITE}{p['path']}"
    desc = html.escape(p["description"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p['title']}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#faf6f0">
  <meta name="apple-itunes-app" content="app-id=6770804298">
  <meta property="og:type" content="{p.get('og_type', 'article')}">
  <meta property="og:site_name" content="369 Journal">
  <meta property="og:title" content="{html.escape(p['h1'])}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}{p.get('og_image', '/assets/img/og.jpg')}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/assets/img/favicon-48.png" sizes="48x48">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="/assets/site.css?v=20261118g">
  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
  <script src="/assets/analytics.js?v=20261118" defer></script>
  <script src="/assets/site.js" defer></script>
</head>
<body>
  {header(p['path'])}
"""


def crumbs(p):
    trail = [("Home", f"{SITE}/")] + [(n, f"{SITE}{h}") for n, h in p.get("parents", [])] + [(p["crumb"], f"{SITE}{p['path']}")]
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(trail)]}


def post(p):
    url = f"{SITE}{p['path']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {
            "@type": "Article", "headline": p["h1"], "description": p["description"], "url": url,
            "datePublished": PUBLISHED, "dateModified": PUBLISHED,
            "author": {"@type": "Person", "name": "Tejas Rane", "url": f"{SITE}/about/"},
            "publisher": {"@type": "Organization", "name": "369 Journal", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/app-icon-512.png"}},
            "mainEntityOfPage": url,
        },
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
        crumbs(p),
    ]}
    faq_html = "\n".join(
        f"      <details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in p["faq"])
    related = "\n".join(f'        <li><a href="{h}">{t}</a></li>' for h, t in p["related"])
    return head(p, ld) + f"""
  <main>
    <div class="narrow article-head">
      <h1>{p['h1']}</h1>
      <p>{p['lede']}</p>
      <p class="meta">Updated 18 November 2026 &middot; By <a href="/about/">Tejas Rane</a>, maker of 369 Journal and author of two books on manifestation journaling</p>
    </div>

    <article class="narrow prose">
{p['body']}

      <h2 id="faq">Questions</h2>
{faq_html}

{p['end']}

      <h2>Keep reading</h2>
      <ul>
{related}
      </ul>
    </article>
  </main>

  {footer()}
</body>
</html>
"""


PAGES = []

# ------------------------------------------------------------------ scripting
PAGES.append({
    "path": "/scripting-manifestation/",
    "crumb": "Scripting manifestation",
    "title": "Scripting Manifestation: How to Do It + Examples | 369 Journal",
    "h1": "Scripting Manifestation: How to Do It, with Examples",
    "description": "What scripting manifestation is, how to write a script in six steps, six example scripts, common mistakes, and how to pair it with the 369 method.",
    "lede": "Scripting means writing one moment of your desire as if it has already happened. It takes ten minutes, needs only a pen, and works best when the scene is small enough to believe. Here is how to do it well.",
    "body": """      <nav class="toc" aria-label="On this page">
        <strong>On this page</strong>
        <ol>
          <li><a href="#what">What scripting is</a></li>
          <li><a href="#how">How to script in six steps</a></li>
          <li><a href="#remember">The &ldquo;I remember when&rdquo; form</a></li>
          <li><a href="#examples">Six example scripts</a></li>
          <li><a href="#mistakes">Common mistakes</a></li>
          <li><a href="#369">Scripting and the 369 method</a></li>
          <li><a href="#work">Does scripting work?</a></li>
        </ol>
      </nav>

      <h2 id="what">What is scripting manifestation?</h2>
      <p>Scripting is a journaling practice from the law of attraction world. Instead of writing a goal (&ldquo;I want a new job&rdquo;), you write a short scene from the day after it came true, in the past or present tense, with real details: where you are, what you hear, what you do next.</p>
      <p>The idea is simple. A goal on a list stays abstract. A scene you can picture becomes something your mind keeps returning to, and that makes it easier to notice chances and take the next step.</p>

      <h2 id="how">How to script in six steps</h2>
      <ol>
        <li><strong>Choose one desire.</strong> One job, one home, one habit, one relationship with yourself. Several desires in one script blur together.</li>
        <li><strong>Pick one ordinary moment.</strong> Not the big announcement, but a quiet minute after it: the first commute to the new office, an ordinary Tuesday in the new flat.</li>
        <li><strong>Write in the past or present tense.</strong> &ldquo;I walked in&rdquo; or &ldquo;I am walking in&rdquo;, never &ldquo;I will&rdquo;.</li>
        <li><strong>Add three real details.</strong> Something you see, something you hear and something you do with your hands. Details make a scene believable.</li>
        <li><strong>Name the feeling.</strong> Calm, proud, relieved, light. One word is enough.</li>
        <li><strong>End with a small next step.</strong> Close your notebook and do one real thing that points toward the scene: send the email, save the first $20, book the viewing.</li>
      </ol>
      <p>Most scripts are 100 to 300 words. If you are writing more than a page, you are probably describing several moments; pick the one that feels most real.</p>

      <h2 id="remember">The &ldquo;I remember when&rdquo; form</h2>
      <p>If writing in the present tense feels like pretending, try writing as a memory. Start with <strong>&ldquo;I remember when&hellip;&rdquo;</strong> and describe the moment as if you are looking back on it a year from now. Many people find this easier to believe, because remembering feels natural and pretending does not.</p>
      <blockquote>I remember the first Monday at the new studio. I got there early, put my coffee on the windowsill and just looked at my name on the schedule for a minute.</blockquote>

      <h2 id="examples">Six example scripts</h2>
      <p>Short and specific beats long and dramatic. Adapt these to your own life rather than copying them word for word.</p>
      <h3>Work</h3>
      <p>&ldquo;It is my second week in the new role. I open my laptop and the first message is a thank-you from my manager for the plan I sent on Friday. I make tea, close the door and start the part of the job I actually enjoy.&rdquo;</p>
      <h3>Money</h3>
      <p>&ldquo;I remember checking my savings account the morning it passed $5,000. I didn&rsquo;t celebrate loudly. I just felt my shoulders drop, and I moved $50 more across before breakfast.&rdquo;</p>
      <h3>Home</h3>
      <p>&ldquo;Saturday morning in my own flat. Light comes through the big window onto the table I chose. I can hear the market downstairs, and nobody needs me to be anywhere.&rdquo;</p>
      <h3>Health</h3>
      <p>&ldquo;I am walking home from my third run this week. My legs are tired in a good way. I stretch on the step, drink a full glass of water and write the run in my notebook.&rdquo;</p>
      <h3>Self-worth</h3>
      <p>&ldquo;I remember the meeting where I said no to extra work and nothing bad happened. My voice was steady. Afterwards I went for a short walk and felt proud of myself.&rdquo;</p>
      <h3>Creative work</h3>
      <p>&ldquo;It is a quiet evening and I have just finished the last page of my first draft. I save it twice, send it to one friend and put the kettle on.&rdquo;</p>

      <h2 id="mistakes">Common scripting mistakes</h2>
      <ul>
        <li><strong>Writing a fantasy instead of a moment.</strong> A whole perfect life in one paragraph is hard to believe. One scene is easier.</li>
        <li><strong>Scripting other people&rsquo;s choices.</strong> Write about your own actions and feelings. &ldquo;I feel loved and chosen&rdquo; works; deciding what a specific person will do does not.</li>
        <li><strong>Changing the desire every day.</strong> Stay with one scene for at least a week so it can become familiar.</li>
        <li><strong>Waiting for it to feel true.</strong> Some days it will feel fake. Write anyway, keep it short, and add one detail that is already true today.</li>
        <li><strong>Skipping the real step.</strong> A script without any action stays a daydream.</li>
      </ul>

      <h2 id="369">Scripting and the 369 method</h2>
      <p>The two practices fit together well. The <a href="/369-method/">369 method</a> repeats one short affirmation 3, 6 and 9 times a day; scripting gives that affirmation a scene. A simple way to combine them:</p>
""" + table(["Practice", "What you write", "When"], [
        ["369 method", "One affirmation line, 18 times a day", "Morning, afternoon and night"],
        ["Scripting", "One short scene of the same desire", "Once a day or a few times a week, often at night"],
    ]) + """
      <p>Use the same desire for both. For example, the affirmation &ldquo;I am thriving in my new role&rdquo; pairs with the second-week scene above.</p>
      <p>Scripting also pairs well with gratitude. Writing thanks for what is already good, and for what you are working toward, puts you in the same &ldquo;it&rsquo;s already happening&rdquo; frame. Try the &ldquo;Gratitude for what&rsquo;s coming&rdquo; theme in our <a href="/gratitude-journal-prompts/">gratitude journal prompts</a>.</p>

      <h2 id="work">Does scripting work?</h2>
      <p>No study shows that writing a scene makes outside events happen by itself, and we won&rsquo;t promise that it does. What has modest research behind it is writing about your best possible future: it can lift mood and make goals feel clearer and more reachable. Scripting is most useful as a daily reminder of what you want, paired with small real steps.</p>
""",
    "faq": [
        ("What is scripting in manifestation?", "Scripting is writing one moment of your desire as if it has already happened, with real details and a feeling, usually in the past or present tense. It is a journaling practice from the law of attraction world."),
        ("How long should a manifestation script be?", "Most scripts are 100 to 300 words, about one notebook page. One clear moment is better than a long description of a whole perfect life."),
        ("Should I script in the past or present tense?", "Either works. Present tense (“I am walking in”) feels immediate; past tense written as a memory (“I remember when…”) often feels easier to believe."),
        ("Can I script about a specific person?", "Write about your own feelings and actions rather than deciding what another person will do. “I feel loved and secure in my relationship” respects both of you."),
        ("How often should I script?", "Once a day for a week or more is a good start, with the same desire and the same scene, so it becomes familiar. Many people script at night."),
        ("Can I combine scripting with the 369 method?", "Yes. Write your 369 affirmation morning, afternoon and night, and add one short script of the same desire once a day."),
    ],
    "end": book_card("scripting", "web_scripting_post", heading="h3") + "\n" + app_plug(
        "Script on your iPhone",
        "369 Journal includes free guided scripting next to your daily 369 writing, with reminders and a private, on-device journal.",
        "site-scripting"),
    "related": [
        ("/books/", "Books: The 369 Method and Scripting Manifestation"),
        ("/369-method/", "How to do the 369 method"),
        ("/369-method/examples/", "50 369 method examples"),
        ("/369-manifestation-journal/", "How to keep a 369 manifestation journal"),
        ("/new-year-manifestation-challenge/", "A 21-day New Year manifestation challenge"),
    ],
})

# ------------------------------------------------------------------ 369 journal
PAGES.append({
    "path": "/369-manifestation-journal/",
    "crumb": "369 manifestation journal",
    "title": "369 Manifestation Journal: How to Set One Up | 369 Journal",
    "h1": "How to Keep a 369 Manifestation Journal, on Paper or in an App",
    "description": "How to set up a 369 manifestation journal: what to write each session, a simple page layout, tracking 21, 33 or 45 days, and paper vs app.",
    "lede": "A 369 manifestation journal is where you write one affirmation 3 times in the morning, 6 in the afternoon and 9 at night. Here is a page layout that works, what to write each session, and an honest look at paper versus an app.",
    "body": """      <nav class="toc" aria-label="On this page">
        <strong>On this page</strong>
        <ol>
          <li><a href="#what">What goes in a 369 journal</a></li>
          <li><a href="#setup">How to set up the pages</a></li>
          <li><a href="#sessions">What to write each session</a></li>
          <li><a href="#length">21, 33 or 45 days</a></li>
          <li><a href="#paper-or-app">Paper, app or both?</a></li>
        </ol>
      </nav>

      <h2 id="what">What goes in a 369 manifestation journal</h2>
      <p>Only four things matter:</p>
      <ul>
        <li><strong>One desire</strong>, chosen at the start and kept for the whole cycle.</li>
        <li><strong>One affirmation</strong> for it, short and in the present tense. See <a href="/369-method/examples/">50 examples</a> if you need wording.</li>
        <li><strong>18 lines a day:</strong> 3 in the morning, 6 in the afternoon, 9 at night, always with the same words.</li>
        <li><strong>A short note</strong> at night: one thing you noticed or did that points toward your desire. Some people add one line of thanks too; <a href="/gratitude-journal-prompts/">gratitude journal prompts</a> help on blank days.</li>
      </ul>
      <p>That last note is the part most people skip, and it is the part that makes the journal feel useful after a few weeks, because you can look back and see progress.</p>

      <h2 id="setup">How to set up the pages</h2>
      <ol>
        <li><strong>First page:</strong> write your desire, your affirmation, the start date and the number of days (21, 33 or 45).</li>
        <li><strong>One page or spread per day:</strong> the date and day number at the top, then three labelled blocks: Morning (3 lines), Afternoon (6 lines), Night (9 lines).</li>
        <li><strong>A small box at the bottom</strong> for the night note.</li>
        <li><strong>A tracker</strong> at the front or back with one square per day to tick. Our <a href="/369-method/tracker/">free printable 33-day tracker</a> does this for you.</li>
      </ol>
      <p>A plain A5 notebook works well. Expect to fill around one page a day, so a 45-day cycle needs about 50 pages plus a few for notes.</p>

      <h2 id="sessions">What to write each session</h2>
""" + table(["Session", "Lines", "Tip"], [
        ["Morning", "3", "Write before checking your phone. Read the line once out loud."],
        ["Afternoon", "6", "Set a reminder; this is the session people miss most."],
        ["Night", "9", "Write slowly, then add one line about something you noticed today."],
    ]) + """
      <p>Write the affirmation exactly the same way every time. If you want to change the wording, finish the current cycle and start a new one.</p>

      <h2 id="length">21, 33 or 45 days</h2>
      <p><strong>21 days</strong> is a gentle first cycle. <strong>33 days</strong> is the most common choice. <strong>45 days</strong> suits a bigger, slower goal. If you miss a day, carry on the next morning rather than starting again; the habit matters more than a perfect streak. The full step-by-step is in <a href="/369-method/">how to do the 369 method</a>.</p>

      <h2 id="paper-or-app">Paper, app or both?</h2>
""" + table(["", "Paper journal", "App", "Both"], [
        ["Best for", "People who think better with a pen", "Busy days and remembering all three sessions", "Writing on paper, with reminders and a record on your phone"],
        ["Reminders", "None, unless you set alarms", "Built in", "From the app"],
        ["Counting lines", "By hand", "Automatic", "Either"],
        ["Privacy", "As private as your notebook", "Depends on the app", "Both private if the app stores data on your phone"],
        ["Cost", "A notebook, or a guided workbook", "Often free to start", "Both"],
    ]) + """
      <p>Many people end up doing both: they write on paper because handwriting feels more personal, and use an app so they never miss the afternoon session.</p>

      <h3>If you prefer paper: a guided workbook</h3>
      <p>We wrote <a href="/books/">The 369 Method</a> for people who want the practice on paper without designing their own pages. It is a short guide followed by 45 guided days, each with a lesson, a question and room for all 18 lines.</p>
""" + book_card("369", "web_journal_post") + """

      <h3>If you prefer your phone</h3>
      <p>The 369 Journal app reminds you morning, afternoon and night (at most three times a day, and it skips sessions you have already written), counts every line and keeps your journal private on your iPhone. Your first 21-day cycle is free.</p>
""",
    "faq": [
        ("What is a 369 manifestation journal?", "A notebook or app where you write one affirmation 3 times in the morning, 6 times in the afternoon and 9 times at night, every day for 21, 33 or 45 days."),
        ("Do I need a special journal for the 369 method?", "No. Any notebook works. A guided workbook or an app simply saves you setting up pages, counting lines and remembering the afternoon session."),
        ("How many pages does a 369 journal need?", "About one page a day, so roughly 25 pages for 21 days, 35 for 33 days and 50 for 45 days, plus a few for notes."),
        ("Can I keep my 369 journal on my phone?", "Yes. A 369 app can remind you three times a day and count your lines. Some people write on paper and use the app only for reminders."),
        ("What should I write at night besides the 9 lines?", "One short note about something you noticed or did today that points toward your desire. Over a cycle these notes show your progress."),
    ],
    "end": app_plug("Never miss the afternoon session",
                    "369 Journal reminds you morning, afternoon and night and counts every line. Free 21-day cycle; 33 and 45 days with 369 Pro.",
                    "site-journal"),
    "related": [
        ("/369-method/", "How to do the 369 method"),
        ("/369-method/tracker/", "Free printable 33-day tracker"),
        ("/369-method/examples/", "50 369 method examples"),
        ("/scripting-manifestation/", "Scripting manifestation, with examples"),
        ("/books/", "Books: The 369 Method and Scripting Manifestation"),
    ],
})

# ------------------------------------------------------------------ new year
DAYS = [
    ("Choose", [
        "Choose one desire for 2027. Write it on the first page.",
        "Word your affirmation: short, present tense, positive. Start 369 writing today.",
        "Read the affirmation out loud. If your body tenses, soften the wording.",
        "Write three lines on why this desire matters to you.",
        "Take the smallest possible first step, even five minutes.",
        "Notice one thing today that points toward your desire. Note it at night.",
        "Week review: what felt easy, and which session did you miss?",
    ]),
    ("Act", [
        "List three real actions that would move you forward.",
        "Do the smallest of the three.",
        "Write one short script of an ordinary moment after your desire comes true.",
        "Remove one thing that gets in the way: an app, a habit, a clutter pile.",
        "Ask one person for help, advice or an introduction.",
        "A gentle day: do only your 18 lines and rest.",
        "Week review: what moved, even a little?",
    ]),
    ("Close", [
        "Read back your night notes. Write down every small sign of progress.",
        "Keep the affirmation or adjust it now, ready for January.",
        'Write five things from 2026 you are grateful for. Stuck? Use these <a href="/gratitude-journal-prompts/">gratitude prompts</a>.',
        "Plan January's first week: when you will write and one action per week.",
        "Script the morning of 1 January 2027.",
        "Write a short letter from your future self, one year from now.",
        "Final day: review the 21 days and decide whether to carry on to 33 or 45.",
    ]),
]


def day_rows():
    rows, n = [], 1
    for week, tasks in DAYS:
        for t in tasks:
            rows.append([f"Day {n}", week, t])
            n += 1
    return rows


PAGES.append({
    "path": "/new-year-manifestation-challenge/",
    "crumb": "21-day New Year manifestation challenge",
    "title": "21-Day New Year Manifestation Challenge 2027 | 369 Journal",
    "h1": "A 21-Day New Year Manifestation Challenge for 2027",
    "description": "A free 21-day New Year manifestation challenge with the 369 method: one desire, 18 lines and one small task a day, in December or January.",
    "lede": "Most New Year goals are forgotten by mid-January. This challenge starts earlier and stays small: one desire, the 369 method every day, and one task a day for 21 days. Start on 11 December to finish on New Year&rsquo;s Eve, or on 1 January to begin the year with it.",
    "body": """      <h2 id="how">How the challenge works</h2>
      <ul>
        <li><strong>One desire for 2027.</strong> Pick the one that would change your year most. Not sure where to start? <a href="/word-of-the-year/">Find your Word of the Year</a> in five questions, then build your desire around it.</li>
        <li><strong>The 369 method every day:</strong> your affirmation 3 times in the morning, 6 in the afternoon and 9 at night. New to it? Read <a href="/369-method/">how to do the 369 method</a>.</li>
        <li><strong>One small task a day</strong> from the plan below. Most take five to ten minutes.</li>
        <li><strong>Two start dates:</strong> 11 to 31 December (finish on New Year&rsquo;s Eve) or 1 to 21 January.</li>
      </ul>

      <h2 id="plan">The 21-day plan</h2>
      <p>Week one is about choosing, week two about acting, and week three about looking back and preparing for the new year.</p>
""" + table(["Day", "Week", "Task (plus your 18 lines)"], day_rows()) + """

      <h2 id="affirmations">New Year affirmations to start from</h2>
      <ul>
        <li>&ldquo;2027 is the year I feel calm and confident in my work.&rdquo;</li>
        <li>&ldquo;I am so grateful that I save money every month with ease.&rdquo;</li>
        <li>&ldquo;I keep the promises I make to myself.&rdquo;</li>
        <li>&ldquo;My home is peaceful, and I love coming back to it.&rdquo;</li>
        <li>&ldquo;I move my body in ways I enjoy, and I feel strong.&rdquo;</li>
      </ul>
      <p>Need more? See <a href="/369-method/examples/">50 369 method examples</a>, or the guides for <a href="/369-method/money/">money</a> and <a href="/369-method/love/">love</a>.</p>

      <h2 id="tips">Tips for finishing</h2>
      <ul>
        <li><strong>Set three reminders now</strong>, before day one. The afternoon session is the one most people miss.</li>
        <li><strong>Miss a day? Carry on.</strong> Don&rsquo;t restart; the challenge is about coming back.</li>
        <li><strong>Keep the tasks small</strong> over the holidays. Five honest minutes beat an hour you skip.</li>
        <li><strong>Do it with a friend</strong> and send each other one line at night.</li>
      </ul>

      <h2 id="tools">Doing the challenge on paper or in the app</h2>
      <p><strong>On paper:</strong> any notebook works, and our <a href="/369-method/tracker/">free printable tracker</a> helps you tick off each day. If you want guided pages, <a href="/books/">our two workbooks</a> also make a thoughtful gift for someone starting the new year with an intention.</p>
      <p><strong>In the app:</strong> the 369 Journal app runs its own 21-day challenge on the same dates from 11 December, with a challenge card on the Today screen, reminders for all three sessions and a badge when you finish. You can follow this plan alongside it.</p>
""",
    "faq": [
        ("When should I start a New Year manifestation challenge?", "Either 11 December, so the 21 days end on New Year’s Eve, or 1 January, so they end on 21 January. Starting in December means you begin the year with the habit already in place."),
        ("Is the New Year manifestation challenge free?", "Yes. The plan on this page is free, and you can do it in any notebook. The 369 Journal app’s first 21-day cycle is also free."),
        ("What if I miss a day of the challenge?", "Carry on the next day. Write your 18 lines and do that day’s task. There is no need to restart."),
        ("Can I manifest more than one thing in the challenge?", "Choose one desire for these 21 days. One clear focus is easier to keep and to notice progress on. You can start a new cycle for the next desire afterwards."),
        ("What happens after the 21 days?", "Review your night notes, then decide whether to continue to 33 or 45 days with the same desire or start a new cycle."),
    ],
    "end": "      <h2 id=\"books\">Our books, for a paper challenge or a gift</h2>\n" + book_card("369", "web_newyear_post") + "\n" + book_card("scripting", "web_newyear_post", note=False) + "\n" + app_plug(
        "Join the challenge in the app",
        "From 11 December the Today screen shows a 21-day challenge on the same dates, with reminders for all three sessions. Free to start.",
        "site-newyear"),
    "related": [
        ("/369-method/", "How to do the 369 method"),
        ("/369-method/examples/", "50 369 method examples"),
        ("/369-method/tracker/", "Free printable 33-day tracker"),
        ("/scripting-manifestation/", "Scripting manifestation, with examples"),
        ("/369-manifestation-journal/", "How to keep a 369 manifestation journal"),
    ],
})

# ------------------------------------------------------------------ tesla
PAGES.append({
    "path": "/369-method/tesla/",
    "parents": [("The 369 method", "/369-method/")],
    "crumb": "Did Tesla create the 369 method?",
    "title": "Did Nikola Tesla Really Create the 369 Method? | 369 Journal",
    "h1": "Did Nikola Tesla Really Create the 369 Method?",
    "description": "The 369 method is often credited to Nikola Tesla. What the record actually shows, where the method really came from, and why it can still help.",
    "lede": "Almost every 369 method video opens with Nikola Tesla. The truth is less magical but more useful: Tesla did not invent a journaling method, and the practice works for ordinary reasons that have nothing to do with him.",
    "body": """      <h2 id="quote">The quote everyone shares</h2>
      <p>The line usually credited to Tesla says that if you only knew the magnificence of 3, 6 and 9, you would have a key to the universe. It appears on countless posters, videos and app pages.</p>
      <p>There is no reliable source for it. It has not been found in Tesla&rsquo;s verified writings, and the posts that share it never give a date, letter, lecture or interview. The fact-checking site <a href="https://www.truthorfiction.com/?p=138454" rel="nofollow noopener" target="_blank">Truth or Fiction</a> found no trace of it before about 2018, decades after his death in 1943, and rates it as misattributed.</p>

      <h2 id="habits">What Tesla really did with the number 3</h2>
      <p>Tesla did have a well-known fondness for the number three. His biographer Margaret Cheney described how he asked for 18 napkins at meals because the number was divisible by three (<a href="https://www.pbs.org/tesla/dis/cheney.html" rel="nofollow noopener" target="_blank">PBS interview</a>). Other, less well sourced stories say he walked around a block three times before going into a building and preferred hotel room numbers divisible by three. These read as personal habits, not a spiritual system.</p>
      <p>None of these accounts mention writing an affirmation 3, 6 and 9 times a day. That connection was made by others, decades later.</p>

      <h2 id="origin">Where the 369 method actually came from</h2>
      <p>The 369 method as people practise it today became popular through law of attraction communities and TikTok around 2020 and 2021. Creators combined an older idea, writing a desire repeatedly as a daily ritual, with Tesla&rsquo;s name and his supposed quote, which gave it a memorable story. It spread quickly because it is simple, free and easy to share. The numbers themselves come from numerology, where 3, 6 and 9 each carry their own associations; see <a href="/369-meaning/">what 369 means</a>, or work out your own numbers with the free <a href="/numerology-calculator/">numerology calculator</a>.</p>
""" + table(["Claim", "What we can say"], [
        ["Tesla said 3, 6 and 9 are the key to the universe", "No reliable source; fact-checkers found no trace before about 2018"],
        ["Tesla was fascinated by the number 3", "Yes; his biographer describes habits built around threes"],
        ["Tesla created the 369 writing method", "No evidence; the method spread online around 2020 to 2021"],
        ["The method needs Tesla to work", "No. Its structure is useful on its own"],
    ]) + """

      <h2 id="does-it-matter">Does the Tesla story matter?</h2>
      <p>Not much. What helps people is the structure, not the name behind it:</p>
      <ul>
        <li><strong>Three sessions a day</strong> keep your goal in mind morning, afternoon and night instead of once a year.</li>
        <li><strong>Writing by hand or typing slowly</strong> makes you read your goal properly.</li>
        <li><strong>A fixed length</strong> (21, 33 or 45 days) gives the habit a clear finish line.</li>
        <li><strong>A short note each night</strong> helps you notice small progress you would otherwise forget.</li>
      </ul>
      <p>We don&rsquo;t use Tesla to sell our app or books, and we don&rsquo;t promise that writing an affirmation makes things happen by itself. We think the 369 method is worth doing as a calm daily focus habit, which it is, whoever came up with it.</p>
      <p>Ready to try it? Start with <a href="/369-method/">how to do the 369 method</a>.</p>
""",
    "faq": [
        ("Did Nikola Tesla invent the 369 method?", "No. There is no record of Tesla creating or describing a journaling method. The 369 method became popular online around 2020 and 2021, and his name was attached to it later."),
        ("Did Tesla say 3, 6 and 9 are the key to the universe?", "There is no reliable source for this quote. It has not been found in his verified writings or interviews, and fact-checkers found no trace of it before about 2018."),
        ("Why is Tesla linked to the number 3?", "His biographer Margaret Cheney described habits built around threes, such as asking for 18 napkins because the number is divisible by three. Other stories, like walking around a block three times, are repeated widely but less well sourced."),
        ("Does the 369 method work if Tesla didn’t create it?", "The method was never powered by Tesla. As a habit it can help you keep a goal in mind three times a day and notice progress, but there is no scientific evidence that it makes outside events happen by itself."),
    ],
    "end": book_card("369", "web_tesla_post") + "\n" + app_plug(
        "Try the 369 method, honestly",
        "369 Journal reminds you morning, afternoon and night and counts every line. No hype, no promises. Free 21-day cycle.",
        "site-tesla"),
    "related": [
        ("/369-method/", "How to do the 369 method"),
        ("/369-method/vs-55x5/", "369 vs 55x5 method"),
        ("/369-method/examples/", "50 369 method examples"),
        ("/369-manifestation-journal/", "How to keep a 369 manifestation journal"),
        ("/books/", "Books: The 369 Method and Scripting Manifestation"),
    ],
})


# ------------------------------------------------------------------ books page
def books_page():
    p = {
        "path": "/books/",
        "crumb": "Books",
        "title": "The 369 Method and Scripting Manifestation Books | 369 Journal",
        "h1": "Books for a Calm Manifestation Practice",
        "description": "Two guided workbooks by Tejas Rane: The 369 Method (a 45-day workbook) and Scripting Manifestation (a 30-day workbook). Paperback and Kindle.",
        "og_type": "website",
        "og_image": "/assets/img/books/the-369-method.jpg",
    }
    ld = {"@context": "https://schema.org", "@graph": [crumbs(p)] + [
        {
            "@type": "Book",
            "name": b["title"],
            "alternativeHeadline": b["subtitle"],
            "author": {"@type": "Person", "name": "Tejas Rane", "url": f"{SITE}/about/"},
            "image": f"{SITE}{b['cover']}",
            "description": b["pitch"],
            "inLanguage": "en",
            "url": f"{SITE}/books/#{bid}",
            "workExample": [
                {"@type": "Book", "bookFormat": "https://schema.org/Paperback", "url": f"https://www.amazon.com/dp/{b['asins']['paperback']}",
                 **({"isbn": b["isbn"]} if b.get("isbn") else {})},
                {"@type": "Book", "bookFormat": "https://schema.org/EBook", "url": f"https://www.amazon.com/dp/{b['asins']['kindle']}"},
            ],
        } for bid, b in BOOKS.items()
    ]}
    return head(p, ld) + f"""
  <main>
    <div class="narrow article-head">
      <h1>{p['h1']}</h1>
      <p>Two guided workbooks from the maker of 369 Journal, for people who like to write on paper. Each has a short guide, then one page a day, with honest advice and no promised outcomes.</p>
    </div>

    <div class="narrow prose">
      <section id="369" aria-labelledby="book-369">
{book_card("369", "web_books", heading='h2').replace('<h2>', '<h2 id="book-369">', 1)}
        <ul>
          <li><strong>Part one, the guide:</strong> the method on one page, where 369 really comes from, what it can&rsquo;t do, choosing one desire, writing your sentence, planning your cycle and ten common mistakes.</li>
          <li><strong>Part two, the practice:</strong> 45 guided days. Each day has a short lesson, a question and room for all 18 lines.</li>
          <li><strong>Part three, the toolkit:</strong> what to do when you feel stuck, honest answers to common questions, a proof log and a plan for your next cycle.</li>
        </ul>
      </section>

      <section id="scripting" aria-labelledby="book-scripting" style="margin-top:3rem">
{book_card("scripting", "web_books", heading='h2').replace('<h2>', '<h2 id="book-scripting">', 1)}
        <ul>
          <li><strong>Part one, the guide:</strong> what scripting is, what it can and can&rsquo;t do, and how to write a scene you can actually believe.</li>
          <li><strong>Part two, the practice:</strong> 30 days, each with a short lesson, an example script, a prompt and a full page to write.</li>
          <li><strong>Part three, the toolkit:</strong> help for doubt days, how to revise a script, and how to pair scripting with the 369 method.</li>
        </ul>
        <p>New to scripting? Read our free guide, <a href="/scripting-manifestation/">scripting manifestation, with examples</a>.</p>
      </section>

      <h2 id="which">Which book should I start with?</h2>
      <ul>
        <li><strong>The 369 Method</strong> if you want a short daily ritual: one affirmation, 18 lines a day.</li>
        <li><strong>Scripting Manifestation</strong> if you prefer writing a short scene and picturing it clearly.</li>
        <li><strong>Both</strong> if you want to combine them: the 369 lines through the day and one script at night.</li>
      </ul>

      <h2 id="formats">Paperback or Kindle?</h2>
      <p>The <strong>paperback</strong> is the full workbook, with a ready-made page for every day. The <strong>Kindle eBook</strong> has the guide and every daily lesson to read, and you write in your own notebook. Both are on Amazon; the links above take you to your own country&rsquo;s store. In India, Brazil and Mexico, Amazon sells the Kindle edition only.</p>

      <h2 id="app">The app that goes with them</h2>
      <p>The books work on their own: you don&rsquo;t need the app to use them. If you also want reminders morning, afternoon and night, the 369 Journal app is free to start on iPhone and iPad.</p>
{app_plug("369 Journal for iPhone", "Reminders for all three sessions, every line counted, and a private journal on your phone. Free 21-day cycle.", "site-books")}
    </div>
  </main>

  {footer()}
</body>
</html>
"""


def write(path, text):
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print("built ->", out.relative_to(ROOT))


def main():
    for p in PAGES:
        write(p["path"], post(p))
    write("/books/", books_page())


if __name__ == "__main__":
    main()

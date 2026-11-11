#!/usr/bin/env python3
"""Builds the topic guide pages (money, love, examples, 369 vs 55x5).

Edit the content dicts below, then run:  python3 scripts/build_guides.py
Each page gets the shared header/footer, Article + FAQPage + Breadcrumb
structured data, and an App Store button with its own campaign tag.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://369journal.app"
APP_LINK = "https://apps.apple.com/app/apple-store/id6770804298?pt=128923117&amp;ct={ct}&amp;mt=8"
UPDATED = "2026-11-11"

HEADER = """  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="/"><img src="/assets/img/favicon-48.png" alt="" width="32" height="32">369 Journal</a>
      <nav class="nav" aria-label="Main">
        <a href="/369-method/">The 369 method</a>
        <a href="/369-method/tracker/">Free tracker</a>
        <a href="/best-369-method-apps/">Best 369 apps</a>
        <a href="/faq/">FAQ</a>
      </nav>
      <a class="btn" href="https://apps.apple.com/app/apple-store/id6770804298?pt=128923117&amp;ct=site-header&amp;mt=8" data-cta="header">Get the app</a>
    </div>
  </header>"""

FOOTER = """  <footer class="site-footer">
    <div class="wrap">
      <p>369 Journal for iPhone and iPad. &copy; 2026</p>
      <nav aria-label="Footer">
        <a href="/369-method/">The 369 method</a>
        <a href="/369-method/tracker/">Free 33-day tracker</a>
        <a href="/369-method/examples/">369 examples</a>
        <a href="/best-369-method-apps/">Best 369 apps</a>
        <a href="/faq/">FAQ</a>
        <a href="/about/">About</a>
        <a href="https://tejas3732.github.io/369-journal-legal/privacy.html">Privacy</a>
        <a href="https://tejas3732.github.io/369-journal-legal/support.html">Support</a>
      </nav>
    </div>
  </footer>"""

RELATED = [
    ("/369-method/", "How to do the 369 method"),
    ("/369-method/money/", "369 method for money"),
    ("/369-method/love/", "369 method for love"),
    ("/369-method/examples/", "50 369 method examples"),
    ("/369-method/vs-55x5/", "369 vs 55x5 method"),
    ("/369-method/tracker/", "Free 33-day tracker"),
]


def table(headers, rows):
    head = "".join(f'<th scope="col">{h}</th>' for h in headers)
    body = "\n".join(
        "<tr>" + "".join((f'<th scope="row">{c}</th>' if i == 0 else f"<td>{c}</td>") for i, c in enumerate(r)) + "</tr>"
        for r in rows
    )
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>\n{body}\n</tbody></table></div>'


def page(p):
    url = f"{SITE}{p['path']}"
    faq_ld = {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]
        ],
    }
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": p["h1"],
                "description": p["description"],
                "url": url,
                "datePublished": UPDATED,
                "dateModified": UPDATED,
                "author": {"@type": "Person", "name": "Tejas Rane", "url": f"{SITE}/about/"},
                "publisher": {"@type": "Organization", "name": "369 Journal", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/app-icon-512.png"}},
                "mainEntityOfPage": url,
            },
            faq_ld,
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "The 369 method", "item": f"{SITE}/369-method/"},
                    {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": url},
                ],
            },
        ],
    }
    faq_html = "\n".join(
        f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in p["faq"]
    )
    related = "\n".join(f'<li><a href="{h}">{t}</a></li>' for h, t in RELATED if h != p["path"])
    cta = APP_LINK.format(ct=p["ct"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p['title']}</title>
  <meta name="description" content="{html.escape(p['description'])}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#faf6f0">
  <meta name="apple-itunes-app" content="app-id=6770804298">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="369 Journal">
  <meta property="og:title" content="{html.escape(p['h1'])}">
  <meta property="og:description" content="{html.escape(p['description'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/og.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/assets/img/favicon-48.png" sizes="48x48">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="/assets/site.css">
  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
  <script src="/assets/analytics.js" defer></script>
</head>
<body>
{HEADER}

  <main>
    <div class="narrow article-head">
      <h1>{p['h1']}</h1>
      <p>{p['lede']}</p>
      <p class="meta">Updated November 2026 &middot; By <a href="/about/">Tejas Rane</a>, maker of 369 Journal</p>
    </div>

    <article class="narrow prose">
{p['body']}

      <h2 id="faq">Questions</h2>
{faq_html}

      <div class="app-plug" style="margin-top:2.5rem">
        <img src="/assets/img/app-icon-512.png" alt="369 Journal app icon" width="64" height="64">
        <div>
          <h3>{p['plug_title']}</h3>
          <p>369 Journal reminds you morning, afternoon and night and counts every line. Free 21-day cycle; 33 and 45 days with 369 Pro.</p>
        </div>
        <a class="btn clay" href="{cta}" data-cta="{p['ct']}">Download free</a>
      </div>

      <h2>Keep reading</h2>
      <ul>
{related}
      </ul>
    </article>
  </main>

{FOOTER}
</body>
</html>
"""


PAGES = []

# ---------------------------------------------------------------- money
PAGES.append({
    "path": "/369-method/money/",
    "ct": "site-money",
    "crumb": "369 method for money",
    "title": "369 method for money: affirmations and how to do it | 369 Journal",
    "h1": "The 369 method for money: affirmations and how to do it",
    "description": "How to use the 369 manifestation method for money: write one money affirmation 3, 6 and 9 times a day. How to word it, 15 example money affirmations, and how to pair it with real action.",
    "lede": "Money is the most common reason people try the 369 method. Here is how to word a money affirmation that feels believable, examples you can adapt, and how to turn the ritual into steady progress.",
    "plug_title": "Track your money affirmation",
    "body": """      <h2 id="how">How to do the 369 method for money</h2>
      <ol>
        <li><strong>Choose one money goal.</strong> A raise, paying off a card, a savings target, your first client. One goal for the whole cycle.</li>
        <li><strong>Write it as a present-tense affirmation</strong>, as if it is already true.</li>
        <li><strong>Write it 3 times in the morning, 6 in the afternoon and 9 at night,</strong> using exactly the same words each time.</li>
        <li><strong>Repeat for 21, 33 or 45 days.</strong> 33 days is the most common choice for money goals.</li>
        <li><strong>Take one small money action each day.</strong> Send the email, check the budget, ask the question.</li>
      </ol>

      <h2 id="wording">How to word a money affirmation</h2>
      <ul>
        <li><strong>Present tense:</strong> &ldquo;I earn&rdquo;, not &ldquo;I will earn&rdquo;.</li>
        <li><strong>Specific but believable:</strong> a clear amount works for some people; for others a feeling (&ldquo;secure&rdquo;, &ldquo;at ease&rdquo;) feels more honest. If a number makes you tense, use the feeling.</li>
        <li><strong>Positive:</strong> write what you want (&ldquo;I am debt-free&rdquo;), not what you want to avoid (&ldquo;I am not in debt&rdquo;).</li>
        <li><strong>Short:</strong> you will write it 18 times a day, so keep it to one line.</li>
      </ul>
      <blockquote>A useful test: read it out loud. If your body relaxes a little, it is the right sentence.</blockquote>

      <h2 id="examples">15 money affirmations for the 369 method</h2>
""" + table(["Goal", "Example affirmation"], [
        ["Income", "I am so grateful that I earn $8,000 every month doing work I enjoy."],
        ["Income", "Money comes to me easily and often."],
        ["Raise", "I am happily accepting the raise I have earned."],
        ["New job", "I am thriving in a well-paid role that fits me perfectly."],
        ["Clients", "I am grateful for the steady stream of clients who value my work."],
        ["Business", "My business is profitable and growing every month."],
        ["Debt", "I am completely debt-free and proud of how I did it."],
        ["Debt", "Every payment I make brings me closer to freedom."],
        ["Savings", "I have $10,000 saved and I feel safe and calm."],
        ["Savings", "Saving money feels natural and easy for me."],
        ["Security", "I always have more than enough for what I need."],
        ["Mindset", "I am worthy of wealth and I welcome it."],
        ["Mindset", "I make wise, confident decisions with money."],
        ["Windfall", "Unexpected money finds its way to me."],
        ["Generosity", "I have plenty to enjoy and plenty to share."],
    ]) + """
      <p>Change the amounts to fit your life. Copy one, make it yours, and keep it the same for the whole cycle.</p>

      <h2 id="action">Pair it with one money action a day</h2>
      <p>Writing keeps the goal in front of you; action moves it. Pick one small step each day, such as checking a balance, cancelling an unused subscription, updating your CV, or sending one pitch. Many people log these in the evening, after the night session.</p>

      <h2 id="evidence">Does the 369 method work for money?</h2>
      <p>There is no scientific evidence that writing an affirmation brings money by itself. What it can do is keep your goal visible three times a day, which makes it easier to notice opportunities, stick to a plan and act on it. Use it as a focus ritual alongside practical steps, never instead of financial advice.</p>
""",
    "faq": [
        ("Can I use a specific amount of money in a 369 affirmation?", "Yes. Many people write a specific amount, such as I earn $8,000 a month. If a number feels unbelievable or stressful, use a feeling instead, such as I feel secure and at ease with money."),
        ("How long should I do the 369 method for money?", "Most people choose 33 days for money goals, but 21 or 45 days also work. Choose a length you can finish."),
        ("What if no money shows up after the 369 method?", "There is no guarantee of results. Look back at what you noticed and did during the cycle, adjust your affirmation or goal, and pair the next cycle with one practical money action a day."),
        ("Can I manifest money and love at the same time?", "Most people focus on one desire per cycle, so the 18 daily repetitions all point the same way. Finish your money cycle, then start a new one for love."),
    ],
})

# ---------------------------------------------------------------- love
PAGES.append({
    "path": "/369-method/love/",
    "ct": "site-love",
    "crumb": "369 method for love",
    "title": "369 method for love and a specific person: how to do it | 369 Journal",
    "h1": "The 369 method for love, a relationship or a specific person",
    "description": "How to use the 369 manifestation method for love: self-love, a new relationship, a current partner or a specific person. How to word it kindly, example love affirmations and common questions.",
    "lede": "Love is one of the most popular uses of the 369 method. The kindest and most effective way to do it is to write about the love you want to feel and give, not to try to control someone else.",
    "plug_title": "Keep your love affirmation close",
    "body": """      <h2 id="how">How to do the 369 method for love</h2>
      <ol>
        <li><strong>Decide what kind of love you are writing about:</strong> self-love, a new relationship, your current partner, or a specific person.</li>
        <li><strong>Write one present-tense affirmation</strong> about how the love feels and what it is like.</li>
        <li><strong>Write it 3 times in the morning, 6 in the afternoon and 9 at night,</strong> for 21, 33 or 45 days.</li>
        <li><strong>Notice the shifts:</strong> how you feel, who you meet, and how you show up in your relationships.</li>
      </ol>

      <h2 id="specific-person">The 369 method for a specific person</h2>
      <p>Many people use the 369 method for a specific person, often an ex or a crush. Here is an approach that is kinder to you and to them:</p>
      <ul>
        <li><strong>Write about the relationship, not about controlling them.</strong> &ldquo;I am in a loving, happy relationship with someone who chooses me&rdquo; respects that the other person makes their own choices.</li>
        <li><strong>Focus on your feelings.</strong> &ldquo;I feel calm, secure and loved&rdquo; keeps the ritual about your wellbeing.</li>
        <li><strong>Leave room for better.</strong> Some people add &ldquo;this or something better&rdquo;, which makes it easier to let go if it is not meant to be.</li>
        <li><strong>Look after yourself.</strong> If the practice leaves you anxious or checking their messages, switch to a self-love affirmation for a cycle.</li>
      </ul>

      <h2 id="examples">Love affirmations for the 369 method</h2>
""" + table(["For", "Example affirmation"], [
        ["Self-love", "I love and accept myself exactly as I am today."],
        ["Self-love", "I am worthy of deep, gentle, lasting love."],
        ["New relationship", "I am in a loving relationship that feels safe, easy and fun."],
        ["New relationship", "I am grateful for the kind partner who chooses me every day."],
        ["Current partner", "Our relationship grows closer and more loving every day."],
        ["Current partner", "We understand each other and communicate with ease."],
        ["Specific person", "I am in a happy, loving relationship with someone who truly wants to be with me."],
        ["Specific person", "I feel loved, respected and chosen, with this person or someone even better."],
        ["After a breakup", "I am healing, and my heart is open to the love that is right for me."],
        ["Friendship and family", "I am surrounded by people who love and support me."],
    ]) + """

      <h2 id="evidence">Does the 369 method work for love?</h2>
      <p>No ritual can make another person feel something. There is no scientific evidence that writing an affirmation changes someone else&rsquo;s choices. What the 369 method can do is keep your attention on the love you want, which often changes how open, confident and present you are, and that changes relationships.</p>
""",
    "faq": [
        ("Can I use the 369 method on a specific person?", "Many people do. A kinder approach is to write about the loving relationship you want and how you feel, rather than trying to control the other person, for example: I am in a happy relationship with someone who truly wants to be with me."),
        ("How long should I do the 369 method for love?", "21, 33 or 45 days are the usual choices. Many people start with 21 days for self-love and then a 33-day cycle for a relationship."),
        ("Should I write my crush's or ex's name?", "Some people do, but it can keep you focused on one outcome. Writing about the relationship and feelings you want keeps the practice healthier and leaves room for something better."),
        ("What if the person does not come back after the 369 method?", "That is their choice, and no ritual can change it. Use what you noticed during the cycle, consider a self-love cycle next, and stay open to a relationship that chooses you freely."),
    ],
})

# ---------------------------------------------------------------- examples
examples = {
    "Money": ["I am so grateful that money comes to me easily and often.", "I earn more than enough doing work I love.", "I am debt-free and financially secure.", "I make wise, confident decisions with money.", "My income grows every month."],
    "Career and job": ["I am thriving in a job that fits me perfectly.", "I am grateful for my new well-paid role.", "I am confident in every interview and meeting.", "My work is valued and rewarded.", "I am building a career I am proud of."],
    "Love": ["I am in a loving relationship that feels safe and easy.", "I am worthy of deep, lasting love.", "My partner and I grow closer every day.", "I attract kind, loving people into my life.", "My heart is open and I feel loved."],
    "Self-love and confidence": ["I love and accept myself exactly as I am.", "I trust myself and my decisions.", "I speak with calm confidence.", "I am enough, just as I am.", "I treat myself with kindness every day."],
    "Health and energy": ["I feel strong, rested and full of energy.", "My body is healing a little more every day.", "I sleep deeply and wake up refreshed.", "I enjoy moving my body.", "I am calm, healthy and at peace."],
    "Home": ["I am so happy living in my bright, peaceful home.", "I have found the perfect home for me.", "My home is calm, warm and full of light.", "I am grateful for my beautiful new apartment.", "Everything about my home feels right."],
    "Study and exams": ["I passed my exam with ease and confidence.", "I learn quickly and remember clearly.", "I am accepted into the program I want.", "I stay focused and calm while studying.", "I am proud of my results."],
    "Peace and happiness": ["I am calm, grounded and at peace.", "I let go of what I cannot control.", "Joy comes to me easily every day.", "I feel grateful for my life as it is now.", "I trust that good things are coming."],
    "Travel and adventure": ["I am enjoying my dream trip.", "I travel easily and often.", "New adventures find me at the perfect time.", "I am grateful for the places I get to see.", "I live a life full of exciting experiences."],
    "Friendship and family": ["I am surrounded by people who love and support me.", "My family relationships are warm and peaceful.", "I attract true, lasting friendships.", "I feel connected and understood.", "My home is full of love and laughter."],
}
ex_html = "\n".join(
    f'      <h3>{cat}</h3>\n      <ul>\n' + "\n".join(f"        <li>{e}</li>" for e in items) + "\n      </ul>"
    for cat, items in examples.items()
)
PAGES.append({
    "path": "/369-method/examples/",
    "ct": "site-examples",
    "crumb": "369 method examples",
    "title": "50 369 method examples and affirmations to copy | 369 Journal",
    "h1": "50 369 method examples you can copy and make your own",
    "description": "50 ready-to-use 369 method affirmation examples for money, career, love, self-love, health, home, exams, peace, travel and family, plus a simple formula to write your own.",
    "lede": "Not sure what to write? Here are 50 present-tense 369 affirmations across ten areas of life, plus a simple formula to write your own in a minute.",
    "plug_title": "Write your 369 affirmation tonight",
    "body": """      <h2 id="formula">A simple formula for your own 369 affirmation</h2>
      <p>Most strong 369 affirmations follow one of these shapes:</p>
      <ul>
        <li><strong>I am</strong> [the person who has it]: &ldquo;I am thriving in my new career.&rdquo;</li>
        <li><strong>I am so grateful that</strong> [it is already true]: &ldquo;I am so grateful that I passed my exam.&rdquo;</li>
        <li><strong>I feel</strong> [the feeling of having it]: &ldquo;I feel calm and secure with money.&rdquo;</li>
      </ul>
      <p>If the full version feels too far away, soften it with &ldquo;I am becoming&rdquo; or &ldquo;I am learning to&rdquo;. A sentence you believe is better than a bigger one you resist.</p>

      <h2 id="examples">50 examples by area of life</h2>
""" + ex_html + """

      <h2 id="tips">Tips for using these examples</h2>
      <ul>
        <li><strong>Pick one.</strong> Use a single affirmation for your whole 21, 33 or 45-day cycle.</li>
        <li><strong>Make it yours.</strong> Change names, amounts and details until it sounds like you.</li>
        <li><strong>Keep the exact words.</strong> Write the same sentence 3, 6 and 9 times each day.</li>
        <li><strong>Read it before you write it.</strong> A slow read first helps you mean it, not just copy it.</li>
      </ul>
""",
    "faq": [
        ("What is a good example of a 369 method affirmation?", "A good 369 affirmation is short, in the present tense and believable, for example: I am so grateful that money comes to me easily and often, or I am thriving in a job that fits me perfectly."),
        ("Can I use more than one 369 affirmation?", "Most people use one affirmation per cycle and write it 18 times a day. Start a new cycle with a new affirmation when the first one is finished."),
        ("Should a 369 affirmation start with I am?", "It does not have to, but I am, I am so grateful that and I feel are the most common openings because they put the desire in the present tense."),
        ("Can I change my 369 affirmation halfway?", "It is best to keep the same words for the whole cycle. If it truly does not fit, adjust it once and continue, rather than changing it every day."),
    ],
})

# ---------------------------------------------------------------- 369 vs 55x5
PAGES.append({
    "path": "/369-method/vs-55x5/",
    "ct": "site-55x5",
    "crumb": "369 vs 55x5 method",
    "title": "369 method vs 55x5 method: differences and which to choose | 369 Journal",
    "h1": "369 method vs 55x5 method: which should you choose?",
    "description": "The 369 method and the 55x5 method compared: how many times you write, for how long, how much time each takes, and which suits you. Plus how to do the 55x5 method.",
    "lede": "Both are popular manifestation writing rituals, and both repeat one affirmation. The difference is rhythm: the 369 method spreads it across your day for weeks, while 55x5 packs it into five intense days.",
    "plug_title": "Prefer the 369 rhythm?",
    "body": """      <h2 id="compare">The 369 method and 55x5 method side by side</h2>
""" + table(["", "369 method", "55x5 method"], [
        ["How it works", "Write one affirmation 3 times in the morning, 6 in the afternoon and 9 at night", "Write one affirmation 55 times in one sitting each day"],
        ["Writes per day", "18, in three short sessions", "55, in one longer session"],
        ["How long", "21, 33 or 45 days", "5 days in a row"],
        ["Total writes", "378 to 810", "275"],
        ["Time per day", "About 5 to 10 minutes, split up", "About 20 to 30 minutes at once"],
        ["Feels like", "A calm daily habit", "A short, intense sprint"],
        ["Best for", "Bigger, longer-term desires and building consistency", "A focused push or a deadline within a week"],
    ]) + """

      <h2 id="55x5">How to do the 55x5 method</h2>
      <ol>
        <li>Choose one desire and write it as a present-tense affirmation.</li>
        <li>Each day, write it 55 times in one sitting, staying focused on the feeling.</li>
        <li>Repeat for 5 days in a row, then let it go.</li>
      </ol>

      <h2 id="choose">Which one should you choose?</h2>
      <ul>
        <li><strong>Choose the 369 method</strong> if you want a gentle routine that fits around your day, or your desire is bigger and longer-term.</li>
        <li><strong>Choose 55x5</strong> if you prefer one block of focused time and want a short, five-day commitment.</li>
        <li><strong>Struggling to stay consistent?</strong> The 369 method&rsquo;s three short sessions are easier to keep with reminders.</li>
        <li><strong>Can you combine them?</strong> Some people do a 55x5 sprint first, then continue with a 369 cycle. Keep the same affirmation if you do.</li>
      </ul>

      <h2 id="evidence">Does either method work better?</h2>
      <p>There is no scientific evidence that either method makes outcomes happen, or that one works better than the other. Both are focus rituals. The best one is the one you will actually finish.</p>
""",
    "faq": [
        ("What is the difference between the 369 method and the 55x5 method?", "The 369 method has you write one affirmation 18 times a day across morning, afternoon and night for 21, 33 or 45 days. The 55x5 method has you write it 55 times in one sitting each day for 5 days."),
        ("Is the 369 method or 55x5 better?", "Neither is proven to work better. The 369 method suits people who want a gentle daily habit over several weeks; 55x5 suits people who prefer a short, intense five-day push."),
        ("Can I do the 369 method and 55x5 at the same time?", "It is usually easier to do one at a time. Some people do a 55x5 sprint first and then continue with a 369 cycle using the same affirmation."),
        ("How long does the 55x5 method take each day?", "Writing an affirmation 55 times usually takes about 20 to 30 minutes in one sitting."),
    ],
})


ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg>'


def guide_rows(items):
    return "\n".join(
        f'        <a class="guide" href="{h}"><strong>{t}</strong><span>{d}</span>{ARROW}</a>' for h, t, d in items
    )


def hub():
    import layout  # noqa: E402  (same folder)
    start = [g for g in layout.GUIDES if g[0] in ("/369-method/", "/369-method/examples/", "/369-method/tracker/")]
    goals = [g for g in layout.GUIDES if g[0] in ("/369-method/money/", "/369-method/love/")]
    compare = [g for g in layout.GUIDES if g[0] in ("/369-method/vs-55x5/", "/best-369-method-apps/")]
    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "369 method guides",
        "url": f"{SITE}/guides/",
        "hasPart": [{"@type": "WebPage", "name": t, "url": f"{SITE}{h}"} for h, t, _ in layout.GUIDES],
    }
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>369 method guides: how to, examples, money, love | 369 Journal</title>
  <meta name="description" content="Every 369 Journal guide in one place: how to do the 369 method, 50 affirmation examples, the 369 method for money and love, 369 vs 55x5, a free printable tracker and an honest app comparison.">
  <link rel="canonical" href="{SITE}/guides/">
  <meta name="theme-color" content="#faf6f0">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="369 Journal">
  <meta property="og:title" content="369 method guides">
  <meta property="og:description" content="How to do the 369 method, examples, money, love and more.">
  <meta property="og:url" content="{SITE}/guides/">
  <meta property="og:image" content="{SITE}/assets/img/og.jpg">
  <link rel="icon" href="/assets/img/favicon-48.png" sizes="48x48">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="/assets/site.css">
  <script type="application/ld+json">
{json.dumps(ld, indent=2, ensure_ascii=False)}
  </script>
  <script src="/assets/analytics.js" defer></script>
</head>
<body>
{HEADER}

  <main>
    <div class="narrow article-head">
      <h1>369 method guides</h1>
      <p>Everything you need to practice the 369 manifestation method: how to start, what to write, how to use it for money or love, and free tools.</p>
    </div>
    <div class="narrow prose">
      <h2 style="margin-top:0">Start here</h2>
      <div class="guides" style="grid-template-columns:1fr">
{guide_rows(start)}
      </div>
      <h2>For your goal</h2>
      <div class="guides" style="grid-template-columns:1fr">
{guide_rows(goals)}
      </div>
      <h2>Compare</h2>
      <div class="guides" style="grid-template-columns:1fr">
{guide_rows(compare)}
      </div>
      <div class="app-plug" style="margin-top:3rem">
        <img src="/assets/img/app-icon-512.png" alt="369 Journal app icon" width="64" height="64">
        <div>
          <h3>Practice with reminders</h3>
          <p>369 Journal reminds you morning, afternoon and night and counts every line.</p>
        </div>
        <a class="btn clay" href="{APP_LINK.format(ct='site-guides')}" data-cta="site-guides">Download free</a>
      </div>
    </div>
  </main>

{FOOTER}
</body>
</html>
"""


def main():
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    for p in PAGES:
        out = ROOT / p["path"].strip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(p))
        print("wrote", out.relative_to(ROOT))
    out = ROOT / "guides" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(hub())
    print("wrote", out.relative_to(ROOT))
    import layout
    layout.main()


if __name__ == "__main__":
    main()

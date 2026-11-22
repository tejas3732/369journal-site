#!/usr/bin/env python3
"""Builds /morning-affirmations/, /self-love-affirmations/ and /money-affirmations/.

Run:  cd scripts && python3 tool_affirmation_lists.py
(The lead runs layout.py afterwards for the shared header/footer.)
One shared script and stylesheet: assets/tools/affirmation-lists.{js,css}.
All affirmations are written for the site. Each one is a real <button> in the HTML
(for search engines and no-JS readers) and is also embedded as JSON for the script.
"""
import html
import json

from toolkit import next_steps, privacy, tool_page, write

PUBLISHED_NEW = "2026-11-22"

I_SHUFFLE = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16.5 10a6.5 6.5 0 1 1-1.9-4.6"/><path d="M16.5 3.5v3.4h-3.4"/></svg>'
I_COPY = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="7" width="9.5" height="9.5" rx="2"/><path d="M13 7V5a1.5 1.5 0 0 0-1.5-1.5h-6A1.5 1.5 0 0 0 4 5v6.5A1.5 1.5 0 0 0 5.5 13H7"/></svg>'
I_SAVE = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5.5 3.5h9v13l-4.5-3-4.5 3z"/></svg>'

# ------------------------------------------------------------------ MORNING

MORNING = [
    ("energy", "Energy and a fresh start", "For the first minutes, before the day picks up speed.", None, False, [
        "I wake up with a calm body and a clear mind.",
        "Today I have enough energy for what matters.",
        "I move through this morning at my own steady pace.",
        "My body carried me through the night, and I am ready for the day.",
        "I start slowly, and that is allowed.",
        "Each breath I take wakes me up a little more.",
        "I look after my energy today by resting, eating and drinking water.",
        "This is a fresh page, and I get to write on it.",
        "I do not have to be at my best, only present.",
        "I greet this day with an open mind.",
        "A good day can begin with one small thing done well.",
        "I am awake, I am here, and that is a good start.",
    ]),
    ("calm", "Calm", "For mornings that begin in a rush or with worry.", None, False, [
        "I take my time this morning. Nothing needs to be rushed.",
        "I breathe in slowly and let my shoulders drop.",
        "I let go of last night's worries and start again.",
        "I can feel calm even when the day is busy.",
        "One thing at a time is enough.",
        "I choose to begin this day gently.",
        "My mind is quiet enough to hear what I need.",
        "I do not have to solve everything before breakfast.",
        "I breathe out the tension I woke up with.",
        "There is room in my day for rest.",
        "I move calmly towards what is in front of me.",
        "I trust myself to handle what comes today.",
    ]),
    ("confidence", "Confidence", "For a day with a meeting, a conversation or a risk in it.", None, False, [
        "I am capable of handling today.",
        "I speak up for what I need, kindly and clearly.",
        "I have done hard things before, and I can do this too.",
        "I trust my judgement today.",
        "It is fine to take up space.",
        "I do not need everyone's approval to move forward.",
        "I bring something useful to every room I enter.",
        "I am learning, and learning is enough.",
        "My voice matters, even when it shakes.",
        "I act on my plan, one step at a time.",
        "I keep my promises to myself today.",
        "I walk into today as myself.",
    ]),
    ("work", "Work and focus", "For the workday, studying or a long to-do list.", None, False, [
        "I focus on one task at a time and finish it well.",
        "I begin with the most important thing, even if it is small.",
        "I do good work and I take breaks when I need them.",
        "I ask for help when I need it.",
        "I handle my to-do list with patience, not panic.",
        "Mistakes are information, not a verdict on me.",
        "I give my full attention to the work in front of me.",
        "I keep a steady pace and finish what I start today.",
        "I am allowed to say no to what does not fit my day.",
        "I treat my colleagues and myself with respect.",
        "I am making progress, even on slow days.",
        "My effort today counts.",
    ]),
    ("gratitude", "Gratitude", "For turning your attention to what is already good.", None, False, [
        "I am thankful for this new day.",
        "I notice one good thing before I look at my phone.",
        "I am grateful for a bed, a roof and a cup of something warm.",
        "Today I look for small things to be glad about.",
        "I appreciate the people who make my life easier.",
        "I am thankful for my body, as it is today.",
        "There is already something good in this day.",
        "I am grateful for another chance to try.",
        "I thank myself for showing up yesterday.",
        "I welcome the good things that are already here.",
    ]),
    ("short", "Short ones for your lock screen", "A few words each, easy to read at a glance.", None, True, [
        "I am calm.", "Begin gently.", "Today is mine.", "I have enough.", "One step at a time.", "I am ready.",
        "I choose peace.", "I can do this.", "Breathe in, begin.", "Good things are possible.", "I am here now.", "Steady and kind.",
    ]),
]

MORNING_FAQ = [
    ("What are morning affirmations?",
     "Morning affirmations are short, positive sentences you read or say at the start of the day, such as “I take my time this morning.” They give your mind a calm, kind first thought instead of a rush to your phone."),
    ("How do I use morning affirmations?",
     "Pick one to three that fit today. Read them out loud once or twice, ideally somewhere you pause anyway: at the mirror, with your tea or on the bus. Two to five minutes is plenty. Writing them down, or putting one on your lock screen, helps them stick."),
    ("Do morning affirmations really work?",
     "Not in a magic way. Research on self-affirmation suggests it can lower stress and make people a little more open to hard information, but an affirmation does not make events happen on its own. The honest use is a small daily habit that sets your mood and reminds you what you care about."),
    ("What is a good affirmation to say every morning?",
     "A good one is in the present tense, kind and believable to you. “I take today one step at a time” works for many people. If a line feels false when you say it, soften it, for example from “I am confident” to “I am learning to trust myself.”"),
    ("How many morning affirmations should I say?",
     "One to three is enough. A single line you really mean beats a long list you rush through. Keep the same line for a week or two so it becomes familiar."),
    ("Can I put a morning affirmation on my phone lock screen?",
     "Yes, and it is one of the easiest ways to see it every day. Pick one here, then use our free affirmation wallpaper maker to put it on a lock screen in a few taps."),
]

MORNING_ARTICLE = """      <h2 id="how">How to use morning affirmations</h2>
      <p>You do not need a long ritual. A two to five minute routine is enough, and the best one is the one that fits into a morning you already have. Here is a simple way to start:</p>
      <ol>
        <li><strong>Choose one to three affirmations</strong> from the lists above. Tap to select them, then copy or favourite them.</li>
        <li><strong>Take one slow breath</strong> before you read. It makes the words land more calmly.</li>
        <li><strong>Say them out loud or in your head, slowly.</strong> Pause on each one and notice how it feels. If part of it feels untrue, change the wording until it feels fair.</li>
        <li><strong>Add a tiny action.</strong> After &ldquo;I begin with the most important thing,&rdquo; actually do the first small step on your list.</li>
        <li><strong>Keep it up for a week or two</strong> before you swap the line.</li>
      </ol>
      <h3>Three easy ways to fit it in</h3>
      <ul>
        <li><strong>At the mirror.</strong> Look at yourself and say one line while you brush your teeth or wash your face.</li>
        <li><strong>On paper.</strong> Write one line a few times in a notebook with your tea. Writing slows you down and keeps your attention on the words.</li>
        <li><strong>On your lock screen.</strong> Put one short line where you look first. Our <a href="/affirmation-wallpaper/">free affirmation wallpaper maker</a> does it in a minute.</li>
      </ul>

      <h2 id="write-your-own">How to write your own morning affirmations</h2>
      <p>Ready-made lines are a good start, but your own words often work better. Three simple rules:</p>
      <ul>
        <li><strong>Use the present tense.</strong> &ldquo;I take my time&rdquo; rather than &ldquo;I will stop rushing&rdquo;.</li>
        <li><strong>Say what you want, not what you want to avoid.</strong> &ldquo;I feel steady&rdquo; rather than &ldquo;I am not anxious&rdquo;.</li>
        <li><strong>Make it believable.</strong> If you do not believe the sentence, your mind argues with it. Try &ldquo;I am learning to feel calm&rdquo; instead of &ldquo;I am always calm&rdquo;.</li>
      </ul>
      <p>The <a href="/affirmation-generator/">affirmation generator</a> has a checker that shows whether your line follows these rules, and you can <a href="/369-method/examples/">browse 50 more examples</a> for every area of life.</p>

      <h2 id="evidence">What the research says, honestly</h2>
      <p>Studies on <em>self-affirmation</em>, where people reflect on their values or strengths, suggest it can lower stress and make people a little more open to information that would otherwise feel threatening. Those results are real but modest, and they come from reflecting on what matters to you, not from repeating a sentence you do not believe.</p>
      <p>What affirmations cannot do is change your circumstances by themselves. They are a small mental habit. Used well, they help you start the day in a calmer frame of mind and remind you what you are working towards, which can make it easier to take the next small step. If you are struggling with anxiety or low mood that does not lift, please talk to a doctor or counsellor. An affirmation is a support, not a treatment.</p>

      <h2 id="gratitude">Pair them with gratitude</h2>
      <p>If you want a second two-minute habit, add a line of gratitude: one thing you are thankful for before you say your affirmation. Our <a href="/gratitude-journal-prompts/">gratitude journal prompts</a> have plenty to choose from. On a heavy morning, try the <a href="/self-love-affirmations/">self love affirmations</a>, which are written for gentler days.</p>

      <h2 id="369">Make it a three-times-a-day habit</h2>
      <p>The <a href="/369-method/">369 method</a> is a simple structure for this: write one affirmation 3 times in the morning, 6 times in the afternoon and 9 times at night. You can do it with any line from this page.</p>"""

# ------------------------------------------------------------------ SELF LOVE

SELFLOVE = [
    ("body", "Body", "For the days you are hard on how you look or feel.", None, False, [
        "I treat my body with care and respect.",
        "My body does a lot for me, and I thank it.",
        "I do not have to look a certain way to deserve kindness.",
        "I listen to what my body needs today.",
        "I rest when I am tired, and that is not laziness.",
        "My body is not an ornament, it is where I live.",
        "I feed my body in a way that helps me feel well.",
        "I am more than how I look.",
        "I let myself enjoy moving in ways that feel good.",
        "I speak about my body the way I would to someone I love.",
        "My body is allowed to change.",
        "I am learning to feel at home in my own skin.",
    ]),
    ("worth", "Worth", "For when you feel you have to earn your place.", None, False, [
        "I am worthy of love as I am today.",
        "My worth does not depend on what I get done.",
        "I deserve good things, including rest.",
        "I am enough, even when I am unfinished.",
        "I do not have to earn kindness.",
        "I matter, and so do my needs.",
        "I am allowed to be proud of myself.",
        "My value was never up for a vote.",
        "I accept compliments without arguing with them.",
        "I have a lot to offer, and I offer it in my own way.",
        "I am not too much and I am not too little.",
        "I belong here.",
    ]),
    ("boundaries", "Boundaries", "For saying no, asking for space and protecting your energy.", None, False, [
        "I am allowed to say no without a long explanation.",
        "My time and energy are worth protecting.",
        "I can be kind and still keep my boundaries.",
        "I do not owe anyone access to me at all hours.",
        "I choose who gets my energy.",
        "It is okay to leave a conversation that hurts.",
        "I ask for what I need, clearly and calmly.",
        "Other people's disappointment is not always my fault.",
        "I listen to my gut when something feels wrong.",
        "I do not have to fix everyone's problems.",
        "I am allowed to change my mind.",
        "Saying no to others can be saying yes to myself.",
    ]),
    ("healing", "Healing", "For hard seasons. Go gently, and talk to someone if it is heavy.", None, False, [
        "I am healing, at the pace that is right for me.",
        "It is okay to have bad days on the way to better ones.",
        "I forgive myself for what I did not know then.",
        "My past is part of my story, but it is not all of it.",
        "I give myself the patience I would give a friend.",
        "My feelings are allowed, even the hard ones.",
        "I can ask for help, and asking is brave.",
        "I do not have to be over it yet.",
        "I am proud of how far I have come.",
        "I let myself rest when I am hurting.",
        "Small steps still count as healing.",
        "I am safe to feel what I feel right now.",
    ]),
    ("confidence", "Confidence", "For trusting yourself a little more each day.", None, False, [
        "I trust myself more each day.",
        "I am allowed to be a beginner.",
        "I like who I am becoming.",
        "I back myself, even when I feel unsure.",
        "My opinions are worth sharing.",
        "I do not need to compare myself to anyone today.",
        "I am proud to be exactly who I am.",
        "I take up space calmly.",
        "I celebrate small wins without waiting for big ones.",
        "My mistakes do not define me.",
        "I choose to speak to myself with encouragement.",
        "I am good company for myself.",
    ]),
    ("short", "Short ones for your lock screen", "A few words each. Easy to see and easy to believe.", None, True, [
        "I am enough.", "I am worthy.", "I am doing my best.", "I choose kindness, starting with me.", "I am allowed to rest.", "I deserve care.",
        "I am learning to love myself.", "Be gentle with me.", "I am not behind.", "I am safe to be me.", "I like myself.", "I am proud of me.",
    ]),
]

SELFLOVE_FAQ = [
    ("What are self love affirmations?",
     "Self love affirmations are short, kind sentences you say or write to yourself, such as “I am allowed to rest.” They are a way to practise speaking to yourself the way you would speak to a friend."),
    ("How do I use self love affirmations?",
     "Choose one or two that feel true enough to say. Read them out loud at the mirror or write them in a notebook, ideally at the same time each day. Start with a few minutes. If a line feels too big, pick a softer one, or add “I am learning to” at the front."),
    ("What if I do not believe the affirmation?",
     "That is very common, and it is a sign to adjust the wording, not to give up. Try a gentler version: “I am learning to like myself” instead of “I love myself completely.” A line that feels slightly hopeful is better than one you argue with."),
    ("Do self love affirmations work?",
     "They are not a cure, and they do not change things alone. Research on self-affirmation suggests that reflecting on your values and strengths can lower stress for some people. Used as a kind daily habit, along with real actions such as rest and support, they can help you feel a little steadier."),
    ("What is a good self love affirmation for a bad day?",
     "Try “I am allowed to rest,” “I am doing my best,” or “My feelings are allowed.” They do not ask you to feel great. They give you permission to be where you are."),
    ("Are these affirmations a substitute for therapy?",
     "No. They are a small, gentle habit. If you are dealing with trauma, depression or anxiety that does not ease, please speak to a doctor or a qualified counsellor."),
]

SELFLOVE_ARTICLE = """      <h2 id="how">How to use self love affirmations</h2>
      <p>Self love is not a feeling you switch on. It is closer to a habit of how you treat yourself, and affirmations are one small way to practise it. Here is a gentle way to begin:</p>
      <ol>
        <li><strong>Pick one or two lines</strong> that feel slightly hopeful, not perfect. Tap them above to save them to your favourites.</li>
        <li><strong>Read them at the mirror, or write them down.</strong> Looking at yourself while you say a kind sentence can feel awkward at first. That is normal, so go slowly.</li>
        <li><strong>Notice the push-back.</strong> If a voice says &ldquo;that is not true&rdquo;, soften the line until it feels fair, then try again.</li>
        <li><strong>Back it up with one small act of care:</strong> a glass of water, a walk, an early night, a message to someone safe.</li>
        <li><strong>Return daily for two weeks</strong> before you change the line.</li>
      </ol>

      <h2 id="write-your-own">How to write your own</h2>
      <ul>
        <li><strong>Use the present tense:</strong> &ldquo;I am allowed to rest.&rdquo;</li>
        <li><strong>Be positive:</strong> say what you want to feel, not what you want to stop feeling.</li>
        <li><strong>Make it believable.</strong> Words like &ldquo;learning&rdquo;, &ldquo;allowed&rdquo; and &ldquo;choosing&rdquo; keep it honest. &ldquo;I am learning to trust myself&rdquo; is easier to accept than &ldquo;I trust myself completely&rdquo;.</li>
        <li><strong>Write it as if to a friend.</strong> If you would not say it to someone you love, rephrase it.</li>
      </ul>

      <h2 id="evidence">What the research says, honestly</h2>
      <p>Studies on self-affirmation, where people reflect on what they value and their strengths, suggest that it can lower stress and make people a little more open to difficult feedback. The effects are modest. The research is also about thinking about your values, which is not the same as repeating a line you do not believe.</p>
      <p>Affirmations do not heal on their own and they do not replace help. If you are struggling, tell someone you trust or speak to a doctor or counsellor. Think of these lines as a kind voice you are practising, alongside real support, rest and good habits.</p>

      <h2 id="love">Self love and the 369 method</h2>
      <p>If you want a structure, the <a href="/369-method/love/">369 method for love and self-love</a> shows how to choose a line and write it 3 times in the morning, 6 in the afternoon and 9 at night. For gentler mornings, see our <a href="/morning-affirmations/">morning affirmations</a>, and for the days money feels heavy, the <a href="/money-affirmations/">money affirmations</a>.</p>

      <h2 id="gratitude">Add a little gratitude</h2>
      <p>A simple pairing is one affirmation and one thing you are grateful for about yourself: &ldquo;I am proud that I kept going.&rdquo; Our <a href="/gratitude-journal-prompts/">gratitude journal prompts</a> have a whole theme for this.</p>"""

# ------------------------------------------------------------------ MONEY

MONEY = [
    ("saving", "Saving", "For building a cushion and feeling calmer about spending.",
     "Set up a small automatic transfer on payday, even a few dollars, into an account you name for something you care about.", False, [
        "I pay attention to where my money goes.",
        "I put a small amount aside, and small amounts add up.",
        "I make spending choices that match what I care about.",
        "I can wait a day before a big purchase.",
        "I am building a safety cushion, one deposit at a time.",
        "I know what I have, and knowing helps me feel steady.",
        "Saving is a way of looking after my future self.",
        "I enjoy spending on what matters and cut what does not.",
        "I follow a simple plan for my money.",
        "I am allowed to enjoy small pleasures within my budget.",
        "I check my accounts calmly, without fear.",
        "Every deposit is a vote for the life I want.",
    ]),
    ("earning", "Earning", "For asking, offering and growing your income step by step.",
     "Write down three skills people have thanked you for, then choose one way to offer one of them this month: update your CV, send one message, or set a price.", False, [
        "I am open to new ways of earning money.",
        "My skills have value, and I can learn more.",
        "I ask for fair pay for my work.",
        "I look for chances to use my strengths.",
        "I take small steps towards the income I want.",
        "I follow up on opportunities instead of waiting for them.",
        "I can offer something useful to others.",
        "I am willing to learn what I need to earn more.",
        "I keep track of my wins and share them when it counts.",
        "I put my effort into work I can be proud of.",
        "I am patient and persistent with my goals.",
        "I can build more than one source of income over time.",
    ]),
    ("debt", "Debt", "For facing what you owe without shame.",
     "List every debt on one page with its balance, interest rate and minimum payment, then pick the one to focus on first. If it feels too heavy, a free non-profit debt advice service can help.", False, [
        "I face my debt with honesty, not shame.",
        "I can make a plan for what I owe.",
        "Every payment is a step forward.",
        "I know the number, and knowing it gives me power.",
        "I am more than my debt.",
        "I make the payment I can make, and I keep going.",
        "I ask for help or advice when I need it.",
        "I choose steady progress over perfect progress.",
        "I am learning from my money mistakes.",
        "I can talk about money without hiding.",
        "I stay patient on the days it feels slow.",
        "I am working towards being free of this debt.",
    ]),
    ("mindset", "A steadier money mindset", "For the thoughts and old stories behind how you feel about money.",
     "Write down one belief about money you grew up with, then one new sentence you would like to try in its place.", False, [
        "I can think about money without panic.",
        "I notice what I already have.",
        "My worth is not my net worth.",
        "I am learning to make good money decisions.",
        "Money is a tool, and I am learning to use it well.",
        "I can want more and be grateful for what I have.",
        "I look for what is possible, not only what is missing.",
        "I am allowed to enjoy money and spend it on what matters.",
        "I let go of old stories about money that do not help me.",
        "I am calm about money, even when the numbers are not perfect.",
        "I make choices that my future self will thank me for.",
        "I can ask for what I need and look for ways to get there.",
    ]),
    ("generosity", "Generosity", "For giving in ways that fit your life and your budget.",
     "Choose one small, affordable way to give this week: a sincere compliment, an hour of your skills, or a few dollars to a cause you care about.", False, [
        "I give in ways that feel good and that I can afford.",
        "A small kindness is still a kindness.",
        "I share my time, skills and attention, not only money.",
        "I celebrate other people's good news.",
        "Generosity makes my life feel bigger.",
        "I give without guilt and receive without shame.",
        "I can say no to a request and still be generous.",
        "I support causes that matter to me.",
        "I enjoy treating someone I love within my means.",
        "What I give does not have to be big to matter.",
    ]),
    ("career", "Career", "For growing at work and speaking up for your value.",
     "Pick one skill and book 30 minutes this week to learn it, or write down your achievements from the last six months to use in your next review.", False, [
        "I am growing in my career at a pace that suits me.",
        "I bring value to my team.",
        "I speak up about my work and my ideas.",
        "I am ready to learn the next skill I need.",
        "I am allowed to ask for a raise, and I prepare to do it well.",
        "I build good relationships with the people around me.",
        "I say yes to chances that fit me and no to ones that do not.",
        "I take on a stretch task and learn from it.",
        "My work has meaning, and I can shape how it looks.",
        "I am patient with setbacks and learn from them.",
        "I look for mentors and thank them.",
        "I can change direction if my career asks for it.",
    ]),
]

MONEY_FAQ = [
    ("What are money affirmations?",
     "Money affirmations are short, present-tense sentences about your relationship with money, such as “I check my accounts calmly.” Their job is to calm money-related worry and keep your goals in view, not to bring in cash by themselves."),
    ("Do affirmations for money work?",
     "Affirmations alone do not create money, and anyone who promises that is selling something. What they can do is steady your thinking so you are more likely to make a budget, ask for fair pay or pay off a debt. The action is what moves your finances, and the affirmation supports it."),
    ("What is a good money affirmation to start with?",
     "A believable one. “I pay attention to where my money goes” is easier to accept than “I am rich,” and it points to something you can do today. Pick a line that feels true enough, then pair it with one small action."),
    ("How do I use money affirmations every day?",
     "Choose one or two, read or write them each morning for two to five minutes, then do the small action listed under each group. Many people write the same line 3 times in the morning, 6 in the afternoon and 9 at night using the 369 method."),
    ("Can affirmations help with debt?",
     "They can help with the shame and avoidance that often come with debt, so it is easier to look at the numbers and make a plan. They do not pay the debt, though. If you are struggling, free non-profit debt advice services can help you set up a plan."),
    ("Is this financial advice?",
     "No. This page gives gentle ideas and habits, not financial advice. For decisions about investing, tax or borrowing, speak to a qualified professional."),
]

MONEY_ARTICLE = """      <h2 id="how">How to use money affirmations</h2>
      <p>Affirmations about money work best when they are paired with something real. The lists above give you a sentence and one small action for each group. A simple routine:</p>
      <ol>
        <li><strong>Pick one or two lines</strong> that feel believable. Tap to select them, then copy or favourite them.</li>
        <li><strong>Read or write them each morning</strong> for two to five minutes. Say them slowly and notice how each feels.</li>
        <li><strong>Do the one small action</strong> from that group, such as setting up a transfer or listing your debts. Do it that same day if you can.</li>
        <li><strong>Check in weekly.</strong> Look at your accounts calmly, note one thing that went well and choose one next step.</li>
      </ol>
      <p>If you like structure, the <a href="/369-method/money/">369 method for money</a> explains how to word a money affirmation and write it 3 times in the morning, 6 in the afternoon and 9 at night.</p>

      <h2 id="write-your-own">How to write your own money affirmations</h2>
      <ul>
        <li><strong>Present tense:</strong> &ldquo;I check my accounts calmly,&rdquo; not &ldquo;I will stop being scared of money&rdquo;.</li>
        <li><strong>Positive:</strong> say what you are building rather than what you are avoiding.</li>
        <li><strong>Believable and specific:</strong> &ldquo;I put a little aside every payday&rdquo; is easier to accept than &ldquo;I have unlimited money&rdquo;, and it points to a habit you can keep.</li>
        <li><strong>In your control:</strong> write about your actions and attitude, not outcomes that depend on others, like winning a prize.</li>
      </ul>

      <h2 id="evidence">What affirmations can and cannot do</h2>
      <p>To be straight about it: affirmations do not attract money, and no sentence will pay a bill. Research on self-affirmation, where people reflect on their values and strengths, suggests it can lower stress and make people more open to useful information. That is the realistic benefit here. If money makes you anxious or you avoid opening your statements, a calmer mind makes it easier to face the numbers and take the next practical step.</p>
      <p>The practical steps are what change things: knowing what you spend, making a plan, saving a little, asking for fair pay, getting advice about debt. Use the words to support those actions. This page is not financial advice.</p>

      <h2 id="mindset">When money feels heavy</h2>
      <p>Money stress is common and it is not a personal failing. If you are in debt or your income is unsteady, start with the smallest step: write down the facts, or call a free debt advice service. Pair it with a kind line such as &ldquo;I face this with honesty, not shame.&rdquo; For the feelings underneath, our <a href="/self-love-affirmations/">self love affirmations</a> are written for harder days, and <a href="/morning-affirmations/">morning affirmations</a> can help you start the day steadier.</p>

      <h2 id="tools">More ways to use a line</h2>
      <p>Put a line where you will see it with the <a href="/affirmation-wallpaper/">affirmation wallpaper maker</a>, or make a printable sheet in the <a href="/affirmation-generator/">affirmation generator</a>.</p>"""

# ------------------------------------------------------------------ pages

PAGES = [
    {
        "key": "morning",
        "path": "/morning-affirmations/",
        "crumb": "Morning affirmations",
        "h1": "Morning Affirmations",
        "title_fmt": "{n} Morning Affirmations to Start Your Day | 369 Journal",
        "description": "{n} morning affirmations for energy, calm, confidence, work and gratitude. Tap to copy, shuffle a daily one, or put it on your lock screen. Free.",
        "lede": "{n} short, kind morning affirmations in simple words. Tap the ones you like to copy or save them, shuffle a daily one, and use a line as your lock screen.",
        "badges": ["Free, no sign-up", "{n} affirmations", "Copy, save or print"],
        "sections": MORNING, "faq": MORNING_FAQ, "article": MORNING_ARTICLE,
        "src": "web_morning_aff", "ct": "site-morning-aff",
        "next_title": "Make it a three-times-a-day habit",
        "next_text": "Pick one affirmation from this page and write it 3 times in the morning, 6 in the afternoon and 9 at night. That is the 369 method. The 45-day guided workbook is the paper way to do it, or let your phone keep count.",
        "app_title": "A gentle reminder, three times a day",
        "app_text": "369 Journal reminds you morning, afternoon and night, counts your lines and keeps your streak. Private, no account, and your first 21-day cycle is free.",
        "daily_title": "A morning affirmation for today",
    },
    {
        "key": "selflove",
        "path": "/self-love-affirmations/",
        "crumb": "Self love affirmations",
        "h1": "Self Love Affirmations",
        "title_fmt": "{n} Self Love Affirmations to Read Daily | 369 Journal",
        "description": "{n} self love affirmations for your body, worth, boundaries, healing and confidence. Tap to copy, save favourites or use one on your lock screen. Free.",
        "lede": "{n} gentle self love affirmations for body, worth, boundaries, healing and confidence. Tap the ones that feel true enough, copy them or save your favourites.",
        "badges": ["Free, no sign-up", "{n} affirmations", "Copy, save or print"],
        "sections": SELFLOVE, "faq": SELFLOVE_FAQ, "article": SELFLOVE_ARTICLE,
        "src": "web_selflove_aff", "ct": "site-selflove-aff",
        "next_title": "Practise it a little every day",
        "next_text": "Pick one self love affirmation and write it 3 times in the morning, 6 in the afternoon and 9 at night. It takes a few minutes and builds a kinder voice. The 45-day guided workbook is the paper way to do it, or let your phone keep count.",
        "app_title": "A kind reminder, three times a day",
        "app_text": "369 Journal reminds you morning, afternoon and night, counts your lines and keeps your streak. Private, no account, and your first 21-day cycle is free.",
        "daily_title": "A self love affirmation for today",
    },
    {
        "key": "money",
        "path": "/money-affirmations/",
        "crumb": "Money affirmations",
        "h1": "Affirmations for Money",
        "title_fmt": "Affirmations for Money: {n} Honest Ones | 369 Journal",
        "description": "{n} money affirmations for saving, earning, debt, mindset, generosity and career, each group with one small real action. Tap to copy. Free to use.",
        "lede": "{n} honest money affirmations for saving, earning, debt, mindset, generosity and career. No promises of wealth, just calm words and one small real action for each group.",
        "badges": ["Free, no sign-up", "{n} affirmations", "One small action per group"],
        "sections": MONEY, "faq": MONEY_FAQ, "article": MONEY_ARTICLE,
        "src": "web_money_aff", "ct": "site-money-aff",
        "next_title": "Pair the words with a daily habit",
        "next_text": "Pick one money affirmation and write it 3 times in the morning, 6 in the afternoon and 9 at night, then do the small action beside it. The 45-day guided workbook is the paper way to do it, or let your phone keep count.",
        "app_title": "Let your phone keep count",
        "app_text": "369 Journal reminds you morning, afternoon and night, counts your lines and keeps your streak. Private, no account, and your first 21-day cycle is free.",
        "daily_title": "A money affirmation for today",
    },
]


def build(cfg):
    sections = cfg["sections"]
    n = sum(len(s[5]) for s in sections)
    title = cfg["title_fmt"].format(n=n)
    desc = cfg["description"].format(n=n)
    assert len(title) <= 60, (title, len(title))
    assert 140 <= len(desc) <= 160, (desc, len(desc))
    p = {
        "path": cfg["path"], "crumb": cfg["crumb"], "title": title, "h1": cfg["h1"],
        "description": desc, "lede": cfg["lede"].format(n=n),
        "badges": [b.format(n=n) for b in cfg["badges"]], "published": PUBLISHED_NEW,
    }

    jump = "\n".join(f'        <a href="#{sid}">{html.escape(label)}</a>' for sid, label, *_ in sections)
    secs = []
    for sid, label, intro, action, short, items in sections:
        lis = "\n".join(
            f'          <li><button class="af-item" type="button" aria-pressed="false">{html.escape(t, quote=False)}</button></li>' for t in items)
        act = f'\n      <p class="af-action"><strong>One small action:</strong> {html.escape(action, quote=False)}</p>' if action else ""
        secs.append(f"""      <section class="af-section" id="{sid}" aria-labelledby="{sid}-h">
        <h2 id="{sid}-h">{html.escape(label)}</h2>
        <p class="af-intro">{html.escape(intro)}</p>
        <ul class="af-list{' short' if short else ''}">
{lis}
        </ul>{act}
      </section>""")

    data = json.dumps({"page": cfg["key"], "sections": [
        {"id": sid, "label": label, "items": items} for sid, label, _i, _a, _s, items in sections]},
        ensure_ascii=False).replace("</", "<\\/")

    body = f"""  <div class="af-wrap" data-affirmations>
    <section class="af-daily" aria-labelledby="af-daily-h">
      <h2 id="af-daily-h">{cfg['daily_title']}</h2>
      <p class="af-daily-text" data-daily-text aria-live="polite"></p>
      <p class="t-hint" style="margin:0.5rem 0 0" data-daily-label>Today&rsquo;s pick</p>
      <div class="af-actions">
        <button class="btn clay" type="button" data-shuffle>{I_SHUFFLE}Shuffle</button>
        <button class="btn ghost" type="button" data-daily-copy>{I_COPY}Copy</button>
        <button class="btn ghost" type="button" data-daily-fav aria-pressed="false">{I_SAVE}<span data-daily-fav-label>Favourite</span></button>
      </div>
      <div class="af-out">
        <a href="/affirmation-wallpaper/" data-out="wallpaper">Make it my lock screen</a>
        <a href="/affirmation-generator/" data-out="sheet">Print my 369 sheet</a>
        <p class="af-out-note">We copy the line first (your selected one, or the one above), so you can paste it into the next page.</p>
      </div>
    </section>

    <nav class="af-jump" aria-label="Jump to a group">
{jump}
    </nav>
    <p class="af-howto">Tap an affirmation to select it. You can select several, then copy them or save them to your favourites.</p>

{chr(10).join(secs)}

    <div class="af-bar print-hide" data-bar hidden role="region" aria-label="Selected affirmations">
      <span class="af-count" data-sel-count aria-live="polite">0 selected</span>
      <button type="button" data-sel-copy>Copy</button>
      <button type="button" data-sel-fav>Save to favourites</button>
      <button type="button" class="quiet" data-sel-clear>Clear</button>
    </div>

    <section class="tool-panel af-favs" aria-labelledby="af-favs-h">
      <div class="saved-head">
        <h2 class="t-step" id="af-favs-h">My favourites <span class="saved-count" data-fav-count>0</span></h2>
      </div>
      <ul class="af-favlist" data-fav-list></ul>
      <p class="t-hint" data-fav-empty>Affirmations you save appear here. They stay on this device only, and are shared across our three affirmation pages.</p>
      <button class="t-link-btn" type="button" data-fav-copyall hidden>Copy all my favourites</button>
      <div style="margin-top:1rem">{privacy("Runs in your browser. Favourites stay on this device and nothing you choose is sent anywhere.")}</div>
    </section>
  </div>

  <script type="application/json" id="affirmation-data">{data}</script>"""

    nxt = next_steps(cfg["next_title"], cfg["next_text"], "369", cfg["src"], cfg["app_title"], cfg["app_text"], cfg["ct"])
    return p, tool_page(p, cfg["faq"], body, js="affirmation-lists.js", css="affirmation-lists.css",
                        article=cfg["article"], next_html=nxt), n


if __name__ == "__main__":
    for cfg in PAGES:
        p, page, n = build(cfg)
        write(p["path"], page)
        print("  ", n, "affirmations |", p["title"], f"({len(p['title'])}) |", f"desc {len(p['description'])}")

#!/usr/bin/env python3
"""One page per popular angel number (/angel-numbers/<n>/) plus the hub (/angel-numbers/).

Run:  cd scripts && python3 tool_angel_pages.py   (then the lead runs layout.py)
Each page has a small free tool (pick where you saw the number, get a tailored reading),
embedded as JSON and driven by assets/tools/angel-pages.js, plus unique written content.
Wording stays honest: "commonly associated with", no predictions, no promises.
"""
import html
import json

from build_posts import crumbs, footer, head, write
from toolkit import ASSET_V, more_tools, next_steps, privacy, tool_page

ORDER = ["111", "222", "333", "444", "555", "777", "999", "1010", "1111", "1212", "369"]
CONTEXTS = [("general", "General"), ("love", "Love & relationships"), ("someone", "Someone specific"),
            ("money", "Money & work"), ("decision", "A decision"), ("low", "Feeling low")]
PUBLISHED_ON = "2026-11-22"

N = {}

N["111"] = dict(
    words=["Beginnings", "Focus", "Intention"],
    hub="A cue to notice where your attention is going.",
    lead="111 Angel Number Meaning: Love and Money",
    desc="111 angel number meaning: what people commonly link it with in love, money and spirituality, plus a free tool for what you were thinking when you saw it.",
    lede="Where were you, and what were you thinking about when 111 showed up? Pick one below for a short reading, a question and an affirmation. Then read the full meaning.",
    one="<p>111 is most often read as a number about <strong>beginnings and attention</strong>. The digit 1 is linked with starting, with independence and with the self, so three of them together are commonly taken as a cue: <em>notice what you are thinking right now.</em> Many people treat 111 as a prompt to check whether their thoughts, plans and actions are pointing the same way.</p><p>It is not a forecast. A more grounded reading is that 111 is a small pause the day hands you, and what you do with the pause is the useful part.</p>",
    love="<p>In love, 111 is commonly read as a nudge to get clear about what <em>you</em> want before worrying about what the other person wants. If you are single, people link it with being open to a fresh start without rushing one. If you are in a relationship, it is often read as a cue to say one honest thing you have been keeping back.</p><p>Notice the pattern: the advice is almost always about your own clarity, not about a person arriving. That is a healthier way to use any number sign.</p>",
    someone="<p>A lot of people search for 111 while thinking about a particular person. Honestly, the most likely explanation is plain: when someone is on your mind, you notice numbers more, and 111 is an easy one to notice. There is no evidence that it means they are thinking of you.</p><p>If you want a useful reading, try this one: 111 is about your own attention. Ask yourself whether thinking about this person is helping you or keeping you stuck, and whether there is one small, real step (a message, or a decision to let it rest) that would make you feel clearer.</p>",
    twin="<p>Twin flame is a popular idea online: the belief that each person has one mirror soul. There is no scientific evidence for it, and many counsellors warn that it can make people stay in unhappy situations waiting for a sign. In those communities, 111 is usually described as a sign of a new stage or of awakening.</p><p>If the idea comforts you, you can hold it lightly. If a relationship hurts, a number is not a reason to stay. Trust how the relationship treats you over any sign.</p>",
    money_h="What does 111 mean financially?",
    money="<p>People commonly link 111 with <strong>starting something and focusing your thinking</strong> on it: a new budget, a side project, a first savings goal. It is not a sign that money is on its way, and it is not advice to take a financial risk.</p><p>A practical way to use it: when you see 111, write down the single money intention you most want to grow (for example, &ldquo;save $50 a week&rdquo;), then do one small thing for it today. Clarity beats luck for most financial progress.</p>",
    spirit="<p>Spiritually, 111 is often called a &ldquo;gateway&rdquo; or &ldquo;alignment&rdquo; number: a moment to bring your thoughts, words and actions back into line. People who meditate or pray sometimes use it as a reminder to start their practice again.</p><p>Whether you see it as a message or as your own mind catching a pattern, the invitation is similar: slow down for one breath and ask what you actually want to focus on.</p>",
    digit_h="What 1 means in numerology",
    digit="<p>In numerology the digit 1 is associated with <strong>beginnings, independence and leadership</strong>: the first step, the self, the spark. Three 1s repeat that idea three times, so 111 is read as it turned up loud. Add the digits (1 + 1 + 1) and you reach 3, linked with expression and creativity, so some readers add a note about saying what you mean. Curious about the numbers in your own date of birth? Try the <a href=\"/numerology-calculator/\">numerology calculator</a>.</p>",
    steps=["<strong>Pause for one breath</strong> and notice the thought that was in your head when you saw it.", "<strong>Name one thing you want to grow.</strong> Write it as one short, present-tense line.", "<strong>Take one small step today</strong> that matches it, then repeat the line tomorrow."],
    related=[("1111", "Alignment, a quiet wish", "Same digit with more weight, often tied to making a wish"), ("222", "Balance, patience", "Where 111 is starting, 222 is steadying"), ("333", "Expression, creativity", "Moves from focus to saying it out loud"), ("1010", "Growth, self-belief", "Adds the idea of being further along than you feel")],
    faq=[("What does 111 mean?", "111 is commonly associated with new beginnings, focus and intention. Many people read it as a cue to notice what they are thinking and to set one clear intention."),
         ("Is 111 a good number to see?", "Most people read it positively, as encouragement to start or to refocus. There is no scientific evidence that numbers carry messages, so treat it as a prompt to reflect, not a guarantee."),
         ("What does 111 mean when thinking about someone?", "Usually it means someone is on your mind, so you notice the number more. It is not evidence of what they are thinking. A more useful reading is to check how this person affects your focus and what you want."),
         ("What does 111 mean spiritually?", "In many spiritual communities 111 is called an alignment or gateway number, a reminder to bring thoughts and actions together. It is a personal belief, not a proven fact."),
         ("What does 111 mean in love?", "It is often read as a cue to get clear about what you want and to be honest about it. It is not a prediction that a partner is arriving."),
         ("What should I do when I see 111?", "Pause, notice your thought, name one thing you want to grow and take one small step toward it today.")],
    reads=dict(
        general=("Seeing 111 is commonly read as a nudge to notice where your attention is going. It is a good moment to choose, on purpose, what you want to give your focus to.", "What have I been thinking about most this week, and do I want to keep growing it?", "My thoughts are clear, and I choose them with care."),
        love=("In love, 111 is often read as a cue to get clear about what you want before anything else. Clarity about yourself tends to be the best start for any relationship.", "What do I want from love, in plain words, and have I said it out loud?", "I know what I want in love, and I say it kindly."),
        someone=("When someone is on your mind you notice numbers more, so 111 may simply be your attention at work. It is not proof of what they feel. It is a prompt to check what you want here.", "Is thinking about this person helping me, or keeping me stuck?", "I give my attention to what helps me grow."),
        money=("For money and work, 111 is often read as focus on one thing: one goal, one first step. It is not a sign that money is coming, just a good time to decide what you are building.", "What is the single money goal I would most like to grow this month?", "I focus on one clear goal and take one small step."),
        decision=("When a decision is open, 111 is commonly read as a call for clarity rather than an answer. Write down what you want in one sentence, then see which option fits it.", "Which option fits what I actually want, not what I think I should want?", "I choose clearly, and I trust my next step."),
        low=("If you feel low, 111 can be a small pause: one breath, one gentle thought you actually want to keep. It does not need to fix anything. Smallest next step is enough.", "What is one kind thing I could do for myself in the next hour?", "I begin again gently, as many times as I need."),
    ),
)

N["222"] = dict(
    words=["Balance", "Patience", "Partnership"],
    hub="A reminder that steady, two-way progress still counts.",
    lead="222 Angel Number Meaning: Love and Twin Flame",
    desc="222 angel number meaning: what 222 is commonly linked with in love, money and twin flame stories, what it means spiritually, and a free tool to reflect.",
    lede="Seen 222 and wondering what it means for you? Pick what you were thinking about for a short reading, a question and an affirmation. Then read the full 222 meaning below.",
    one="<p>222 is commonly read as a number of <strong>balance, patience and partnership</strong>. The digit 2 is the number of pairs: two sides, give and take, two people. Repeated three times, it is often taken as a reminder that things are settling into place, even if slowly, and that relationships, work and rest all need both effort and ease.</p><p>People who feel stuck often notice 222. A grounded way to hear it is as permission to be patient with the pace of things you cannot rush, while still doing your part.</p>",
    love="<p>222 is one of the most &ldquo;relationship&rdquo; numbers. In love, it is commonly read as a reminder that a good relationship works in both directions: you listen and you are heard, you give and you receive. If things feel uneven, 222 is often read as a nudge to talk about it kindly.</p><p>For single people, the common reading is patience: do not settle just to feel paired, and do not close your heart either. The healthy use is turning it into a question about balance, not waiting for someone to appear.</p>",
    someone="<p>If you keep seeing 222 while thinking about a specific person, it often comes with waiting: for a reply, a decision, an apology. The number is most commonly read as <em>patience</em>, but be careful not to read it as a promise. There is no evidence that it means the person is thinking of you or will come back.</p><p>A kinder way to use it is to ask what balance looks like here. Are you giving much more than you are getting? Is this a conversation you could start gently, or a wait you could set a limit on?</p>",
    twin="<p>In twin flame writing, 222 is often described as the number of harmony and of two halves coming into balance. Twin flame is a popular online idea, not a proven one: there is no evidence that each person has a single mirror soul, and some therapists note that the idea can keep people in painful, one-sided relationships.</p><p>If you like the story, enjoy it, but measure a relationship by how it treats you each day, not by numbers.</p>",
    money_h="What does 222 mean financially?",
    money="<p>For money and work, 222 is commonly linked with <strong>balance and cooperation</strong>: shared finances, fair deals, a team that pulls together, and steady, patient growth. It is not a sign of a windfall.</p><p>If you see it, you might ask where your money life is lopsided. Are you spending far more than you save? Giving far more at work than you are paid for? Is there a money conversation with a partner or colleague you have been postponing? Small, steady, fair changes are the usual theme.</p>",
    spirit="<p>Spiritually, 222 is often called the number of trust: the sense that something is quietly coming together even when you cannot see it. People who pray or meditate sometimes treat it as a reminder to stop forcing outcomes and to keep faith with their effort.</p><p>Whether you read it as a message or as your own mind noticing a pattern, the invitation is similar: let your shoulders drop, and keep going at a steady pace.</p>",
    digit_h="What 2 means in numerology",
    digit="<p>In numerology, 2 is associated with <strong>balance, cooperation and sensitivity</strong>: the peacemaker, the listener, the partner. Three 2s emphasise those traits. Add the digits (2 + 2 + 2) and you reach 6, linked with care, home and responsibility, so many readers also hear a note about looking after the people and places close to you. You can see how your own numbers work with the <a href=\"/numerology-calculator/\">numerology calculator</a>.</p>",
    steps=["<strong>Take one slow breath</strong> and ask where in your life you are pushing hard but not receiving, or the other way round.", "<strong>Write one sentence</strong> about the balance you would like, such as &ldquo;I ask for help as easily as I give it.&rdquo;", "<strong>Do one fair, small thing today:</strong> a kind message, a boundary, or an hour of rest."],
    related=[("111", "Beginnings, focus", "Where 222 steadies, 111 starts"), ("333", "Expression, creativity", "Moves from balance to saying what you feel"), ("444", "Support, steady work", "Adds a sense of foundations and effort"), ("1212", "Trust, steady steps", "Mixes 1 and 2: a brave step, taken gently")],
    faq=[("What does 222 mean?", "222 is commonly associated with balance, patience and partnership. Many people read it as a reminder to be patient and to keep relationships and effort fair in both directions."),
         ("What does 222 mean in love?", "It is often read as a sign to value two-way effort: listening, being heard, and giving and receiving. It is not a prediction about a specific person."),
         ("What does 222 mean when thinking about someone?", "Mostly that someone is on your mind. Some read it as patience while you wait, but there is no evidence it means they are thinking of you. Use it to ask what balance would look like."),
         ("What is 222 in twin flame terms?", "In twin flame communities it is often described as harmony and balance between two people. Twin flame is a popular belief with no scientific evidence."),
         ("What does 222 mean financially?", "It is commonly linked with balance, fair deals and steady growth. It is not a sign that money is coming. A useful use is to check where your money life is lopsided."),
         ("Is 222 a good sign?", "Most people read it positively, as encouragement to be patient. There is no scientific evidence numbers carry messages, so treat it as a prompt to reflect.")],
    reads=dict(
        general=("222 is commonly read as a call for balance and patience. It is a good moment to notice what is quietly working and to stop rushing what cannot be rushed.", "Where in my life could a little more patience help?", "I trust the pace of my life, and I stay steady."),
        love=("In love, 222 is often read as a reminder that a good relationship works both ways. Listening and being heard, giving and receiving, all count.", "Is the effort in this relationship fair on both sides, and have I said so kindly?", "I give and receive love in balance."),
        someone=("If you are waiting on someone, 222 is often read as patience. It is not a promise about what they feel. A better use is to ask what balance and a fair limit would look like.", "What would I like to say or decide about this, so I am not just waiting?", "I stay kind to myself while I wait, and I act when it is time."),
        money=("For money and work, 222 is often read as balance and fairness: shared money, fair deals, steady growth. It is not a sign of a windfall, just a nudge to even things out.", "Where is my money or work life lopsided right now?", "I build my money life steadily and fairly."),
        decision=("When you are torn between two choices, 222 can be a reminder to weigh both sides calmly. Rushing rarely helps. Give each option an honest hour, then decide.", "If I weighed both options calmly, which one would I choose?", "I weigh my choices calmly and decide with trust."),
        low=("If you feel low, 222 can be a gentle cue that steady counts and that you do not have to fix everything today. Rest and ordinary routines are part of progress.", "What is one small, steady thing that would make today easier?", "I let myself rest, and I keep going gently."),
    ),
)

N["333"] = dict(
    words=["Creativity", "Expression", "Support"],
    hub="A prompt to say what you feel and make something.",
    lead="333 Angel Number Meaning: Love and Money",
    desc="333 angel number meaning: what people commonly link 333 with in love, money and spirituality, plus a free tool tailored to what you were thinking about.",
    lede="Keep noticing 333? Choose what was on your mind for a short, tailored reading with a question and an affirmation, then read the full 333 angel number meaning below.",
    one="<p>333 is commonly read as a number of <strong>creativity, expression and encouragement</strong>. In numerology the digit 3 is the number of speaking, making and enjoying: voice, humour, art, play. Three of them together are often taken as a nudge to say what you have been holding back, or to make the thing you have been putting off.</p><p>It also carries a warm &ldquo;you are not alone&rdquo; note in popular writing. Take that as you like: as spiritual comfort, or as a reminder to lean on the people around you.</p>",
    love="<p>In relationships, 333 is commonly read as a call to <strong>communicate</strong>. Say the kind thing, say the hard thing gently, tell someone what they mean to you. It is also linked with playfulness, which is easy to lose in long relationships. Many people read it as a reminder to laugh together again.</p><p>If you are single, the usual reading is to enjoy your own company and creative life, and let connection grow from being yourself rather than from searching.</p>",
    someone="<p>Seeing 333 while thinking about someone is commonly read as: <em>say it</em>. That does not mean you must confess feelings today, and it is not evidence that the person is thinking about you. It means the unsaid thing is taking up room in your head.</p><p>Ask what you would say if there were no risk. A short honest message, a letter you never send, or a conversation with a friend about it can all take the pressure off. Expression helps, even if the person never reads it.</p>",
    twin="<p>In twin flame communities 333 is sometimes described as a sign of support or of a connection growing through honest communication. Twin flame is a popular idea, not an established one: there is no scientific evidence for a single mirror soul, and treating a number as a sign can make it harder to see a relationship clearly.</p><p>The idea in 333 worth keeping, with or without the story, is simple: talk honestly, and let people show you who they are.</p>",
    money_h="What does 333 mean financially?",
    money="<p>For money and work, 333 is commonly linked with <strong>creative income and speaking up</strong>: pitching the idea, sharing your work, asking for what your skills are worth. It is not a forecast of earnings.</p><p>If you see it, ask what you have made or learned that other people would pay for, or what you have been too shy to share. Small public steps, such as posting the portfolio or sending the email, are the usual theme. Always weigh any financial decision on its own facts, not on a number.</p>",
    spirit="<p>Spiritually, 333 is often linked with support and with the idea of being guided or watched over. People of many beliefs use it as a prompt to say a short prayer, thank someone, or feel less alone in a hard season.</p><p>Without any belief at all, it still works as a cue to check in with your own voice: are you saying what you mean, and creating what you want to create?</p>",
    digit_h="What 3 means in numerology",
    digit="<p>In numerology, 3 is associated with <strong>creativity, joy and self-expression</strong>: the storyteller, the performer, the friend who makes things lighter. Three 3s turn that up. Add the digits (3 + 3 + 3) and you reach 9, linked with completion and compassion, so some readers hear a note about finishing what you start and being kind. Fun fact: 3 is also the first number in the 369 method, the morning count. The <a href=\"/369-meaning/\">369 meaning page</a> explains how.</p>",
    steps=["<strong>Take a breath and ask:</strong> what is something I want to say, or make, and keep postponing?", "<strong>Do the smallest version of it today:</strong> a three-line message, a sketch, ten minutes of writing.", "<strong>Share it or put it somewhere you will see it.</strong> Expression gets easier with practice."],
    related=[("222", "Balance, patience", "Pairs well with 333: say it kindly and wait patiently"), ("999", "Completion, letting go", "3 x 3: the finishing end of the creative cycle"), ("1111", "Alignment, awareness", "Moves from creating to checking you are aligned"), ("369", "The 369 method", "Uses the 3 as the morning count")],
    faq=[("What does 333 mean?", "333 is commonly associated with creativity, self-expression and encouragement. Many people read it as a nudge to say what they feel or to make something they have been postponing."),
         ("What does 333 mean in love?", "It is often read as a call to communicate honestly and keep playfulness alive. It is not a prediction about a specific person."),
         ("What does 333 mean when thinking about someone?", "It is commonly read as: say the unsaid thing, in a way that suits you. It is not evidence about what the other person feels."),
         ("What does 333 mean financially?", "People link it with creative work and speaking up: sharing your skills, asking for fair pay. It is not a promise of income."),
         ("Is 333 a spiritual sign?", "Many people read it as support or guidance. There is no scientific evidence that numbers carry messages, so you can hold that belief lightly."),
         ("What should I do when I see 333?", "Pause, name something you want to say or make, and do the smallest version of it today.")],
    reads=dict(
        general=("333 is commonly read as encouragement to express yourself: to say it, make it or share it. It is a good moment to ask what you have been holding back.", "What have I been wanting to say or make, and what is the smallest version I could do today?", "I express myself freely, and my voice matters."),
        love=("In love, 333 is often read as a call for honest, warm communication, and for a little play. Naming a feeling kindly usually helps more than guessing.", "What one thing would I like my partner, or my future partner, to know about me?", "I speak kindly and honestly in love."),
        someone=("With someone on your mind, 333 is commonly read as: say the unsaid thing, in your own time. That might be to them, to a friend, or on a page you never send.", "What would I say if there were no risk, and who could I say it to first?", "I say what I mean with care."),
        money=("For money and work, 333 is often read as creative income and speaking up: sharing your work or asking for what it is worth. It is not a promise of earnings.", "What have I made or learned that I have been too shy to share?", "I share my work with confidence."),
        decision=("When you are deciding, 333 is commonly read as a nudge to talk it through. Say it aloud or write it down; you often hear your answer in your own words.", "If I explained this decision to a friend, what would I hear myself say?", "I find clarity when I express what I think."),
        low=("If you feel low, 333 is often read as encouragement and a reminder you are not alone. A short message to someone, or a few honest lines on paper, can lighten the load.", "Who could I tell how I am really feeling, even in one sentence?", "I am supported, and I let myself be heard."),
    ),
)

N["444"] = dict(
    words=["Foundations", "Support", "Steady work"],
    hub="The most searched angel number: steady effort and feeling supported.",
    lead="444 Angel Number Meaning: Love and Money",
    desc="444 angel number meaning: what 444 is commonly linked with in love, money and spiritually, what it means when thinking about someone, and a free tool.",
    lede="Seeing 444 everywhere? Pick where you saw it or what you were thinking about for a short reading, a question and an affirmation. The full 444 meaning follows, without the hype.",
    one="<p>444 is commonly read as a number of <strong>foundations, support and steady work</strong>. The digit 4 is the number of structure: four walls, four seasons, four corners of a table. Three 4s together are often taken to mean that what you are building is on a solid footing and that you are more supported than you feel.</p><p>It is also the number people most often see when they are tired or anxious, and most readings are comforting: slow down, keep going, you are not doing this alone. You have probably read that 444 means something dramatic. Most careful sources are calmer than that, and so are we.</p>",
    love="<p>In love, 444 is commonly read as <strong>stability</strong>. For couples, it is a reminder that good relationships are built from boring, repeated, kind habits: turning up, listening, following through. For singles, it is usually read as &ldquo;build your own foundation first&rdquo;: friendships, routines, self-respect.</p><p>It is not a sign that a particular person is coming, or that a relationship is destined. If it makes you ask whether your current relationship feels safe, steady and kind, that is the useful part.</p>",
    someone="<p>&ldquo;Seeing 444 when thinking about someone&rdquo; is one of the most common searches. The plain explanation first: when a person is on your mind, you notice numbers more, and 444 is a number people look for. There is no evidence it means they are thinking of you.</p><p>If you want a kinder reading, 444 is about foundations, so ask: is this connection steady, honest and good for me? If yes, tend it with small, consistent actions. If it feels uncertain, give yourself steady ground first, such as sleep, friends and routine, rather than waiting for another sign.</p>",
    twin="<p>In twin flame writing, 444 is often described as a sign of protection or of a relationship being rebuilt on firmer ground. Twin flame is a popular idea, not a fact. There is no scientific evidence for a single mirror soul, and counsellors warn that it can encourage people to chase intense, unstable connections.</p><p>If you take one thing from the 444 version of the story, make it this: a relationship that is steady, respectful and kind is worth more than one that feels cosmically meant.</p>",
    money_h="What does 444 mean financially?",
    money="<p>This is where 444 gets practical. It is commonly linked with <strong>building steadily</strong>: saving regularly, paying down debt, learning a skill, doing solid work. It is not a sign that a windfall is near, and it is not financial advice.</p><p>If you see it, try a steady-foundations check: do you have a simple budget, a small emergency fund, and one habit (even $10 a week) that you repeat? The 4 is the number of unglamorous consistency. Many people find the day-to-day boredom of doing this is exactly the point.</p>",
    spirit="<p>&ldquo;What is 444 trying to tell me spiritually?&rdquo; Most traditions of angel numbers say 444 means you are supported: that angels, guides or your higher self are near. People of many faiths read it as comfort during a hard stretch.</p><p>Whether or not you hold that belief, it can work as a gentle prompt: you are doing more than you give yourself credit for. Slow down, thank whoever or whatever has helped you, and keep your next step small.</p>",
    digit_h="What 4 means in numerology",
    digit="<p>In numerology, 4 is associated with <strong>stability, hard work and structure</strong>: the builder, the planner, the person who finishes things properly. 444 stresses all of that. Add the digits (4 + 4 + 4) and you reach 12, then 3 (1 + 2), so some readers add a note of creativity and expression coming from solid ground. You can explore the numbers in your own birth date with the <a href=\"/numerology-calculator/\">numerology calculator</a>.</p>",
    steps=["<strong>Check your footing:</strong> sleep, food, one honest conversation, one small money habit. Pick the one that is wobbling.", "<strong>Write one line</strong> about the foundation you want, like &ldquo;I build steady habits that support me.&rdquo;", "<strong>Do one repeatable thing today</strong> and plan to do it again tomorrow. Consistency is the 4."],
    related=[("1111", "Alignment, awareness", "The digits of 1111 add to 4, so it shares the foundation theme"), ("222", "Balance, patience", "Gentler: patience in relationships"), ("555", "Change, freedom", "The opposite energy: movement after 444's stability"), ("777", "Reflection, learning", "Moves from building to thinking about what you learned")],
    faq=[("What does 444 mean?", "444 is commonly associated with stability, foundations and feeling supported. Many people read it as encouragement to keep building steadily."),
         ("What does 444 mean when thinking about someone?", "Mostly that someone is on your mind, so you notice the number. There is no evidence it means they are thinking of you. A more useful reading is to ask whether the connection is steady and good for you."),
         ("What does 444 mean financially?", "It is commonly linked with steady money habits: saving, learning, paying down debt. It is not a sign of a windfall or financial advice."),
         ("What is 444 trying to tell me spiritually?", "Many people read it as a sign of protection or support. That is a personal belief; there is no scientific evidence numbers carry messages. You can use it as a prompt to slow down and look after your foundations."),
         ("What does 444 mean in twin flame terms?", "In twin flame communities it is often described as protection or a relationship being rebuilt on firmer ground. Twin flame is a popular idea with no scientific evidence."),
         ("Is 444 a good or bad sign?", "Most people read it as good: reassurance and steadiness. It is not a warning. Treat it as a prompt to check your foundations."),
         ("Why do I keep seeing 444?", "Once you notice a number, you tend to notice it more. That is how attention works. You can ignore it or use it as a prompt to pause and check in.")],
    reads=dict(
        general=("444 is commonly read as steady support: your foundations matter, and slow, honest effort counts. It is a good moment to check what is holding you up, and what is wobbling.", "What is one steady habit that would support me most right now?", "I am supported, safe and steady."),
        love=("In love, 444 is often read as stability: trust, kindness and showing up, repeated. For singles it is read as building your own foundation first.", "Does my love life feel steady, honest and kind, and what is one small way to tend it?", "I build love on steady, honest ground."),
        someone=("If someone is on your mind, you notice 444 more. It is not proof of what they feel. Its theme is foundations: is this connection steady and good for you?", "If I stopped waiting for a sign, what would I want to do about this?", "I am steady whether or not I hear back."),
        money=("For money, 444 is commonly read as steady building: saving, learning, doing solid work. It is not a sign of a windfall, just a nudge toward boring consistency.", "What small money habit could I repeat every week?", "I build my finances steadily, one choice at a time."),
        decision=("When a decision is open, 444 is often read as: choose what is stable and honest, not what is exciting for a moment. Look at what you can keep up.", "Which option can I build on and keep up for a year?", "I choose steady ground, and I build on it."),
        low=("If you are struggling, 444 is often read as comfort: you are more supported than you feel. Start with the basics: water, sleep, one person you trust.", "Who could I reach out to today, even with one line?", "I am supported, and I do not have to do this alone."),
    ),
)

N["555"] = dict(
    words=["Change", "Freedom", "Curiosity"],
    hub="A cue to meet a change with curiosity, not panic.",
    lead="555 Angel Number Meaning: Love and Change",
    desc="555 angel number meaning: what people commonly link 555 with in change, love and money, what it means when thinking of someone, plus a free tailored tool.",
    lede="555 keeps turning up and you are wondering why. Pick what you were thinking about for a short reading, a question and an affirmation, then read the full 555 angel number meaning.",
    one="<p>555 is commonly read as the number of <strong>change, freedom and curiosity</strong>. The digit 5 sits in the middle of 1 to 9 and is linked with movement, with travel, with trying things, with a refusal to stay still. Three of them are often taken to mean a change is under way or due: a move, a job, a relationship shift, a new habit.</p><p>Many people see it during change that is already happening, which is probably part of why it feels meaningful. It is not a prediction that something dramatic is about to happen, and it is not a reason to burn anything down.</p>",
    love="<p>In relationships, 555 is commonly read as <strong>a time to be honest about change</strong>. Maybe you want something new, maybe the relationship needs a shift, or maybe you have outgrown a pattern. For singles, it often means being open to new people and places rather than waiting in the same spot.</p><p>It is not a sign to end a relationship, nor to start one. A good use is to ask what you want to be different and whether you have said so to the person it concerns.</p>",
    someone="<p>If 555 appears while you are thinking about a person, some people read it as a sign of change in how things stand between you, or of an old connection resurfacing. There is no evidence for either. Often it is simply that a person who is on your mind makes you notice numbers more.</p><p>The useful question is about <em>you</em>: what do you want to change about this situation? Waiting for a sign can keep you in the same place. A small active step, such as a message, a clear decision or new plans of your own, usually feels better than hoping a number will decide.</p>",
    twin="<p>In twin flame writing, 555 is often described as a sign of upheaval or of a reunion or separation phase. Twin flame is a popular online idea, not a scientific one, and these stories can make instability feel romantic. There is no evidence that any pattern in numbers predicts who will return.</p><p>A grounded takeaway: changes in a relationship are worth talking about openly with the person involved, not decoding from numbers.</p>",
    money_h="What does 555 mean financially?",
    money="<p>For money and work, 555 is commonly linked with <strong>changes in how you earn or spend</strong>: a new job, a move, a different approach. It is not advice to take a financial risk, and it is not a sign that money is coming.</p><p>If you see it, a careful reading is: change is possible, so plan it. Big money decisions are best made slowly, with facts and, where needed, a professional, rather than because of a number. Curiosity is the right tone: what is one small thing I could test, like a short course or a side hour a week?</p>",
    spirit="<p>Spiritually, 555 is often called a number of transformation: shedding the old, stepping into something new. People use it as a prompt to ask what they have outgrown, and what they are afraid to look at.</p><p>Whether or not you read it as a message, the invitation is the same: do not wait to feel completely ready. Let one small thing change, and see how it feels.</p>",
    digit_h="What 5 means in numerology",
    digit="<p>In numerology, 5 is associated with <strong>change, freedom and adventure</strong>: the traveller, the curious one, the person who likes variety. Three 5s turn that up. Add the digits (5 + 5 + 5) and you reach 15, then 6 (1 + 5), so many readers add a note about home and responsibility: change that still looks after the people you love. Want to see your own numbers? Try the <a href=\"/numerology-calculator/\">numerology calculator</a>.</p>",
    steps=["<strong>Name the change</strong> you are feeling pulled toward, or the one that is already happening.", "<strong>Write one line</strong> about how you would like to meet it: &ldquo;I meet change with curiosity and courage.&rdquo;", "<strong>Take one small, reversible step</strong> this week. Try before you leap."],
    related=[("444", "Foundations, support", "The grounded partner of 555: stability before change"), ("999", "Completion, letting go", "Where 555 changes, 999 closes a chapter"), ("1212", "Trust, steady steps", "A gentler form of change: one brave step"), ("111", "Beginnings, focus", "Where change begins with attention")],
    faq=[("What does 555 mean?", "555 is commonly associated with change, freedom and curiosity. Many people read it as a sign that a change is under way or that it is time to try something new."),
         ("What does 555 mean when thinking about someone?", "There is no evidence it says anything about the other person. Some read it as change in how things stand. A more useful reading is to ask what you want to change."),
         ("What does 555 mean in love?", "It is commonly read as a prompt to be honest about change: what you want to be different. It is not a sign to start or end a relationship."),
         ("What does 555 mean financially?", "It is commonly linked with changes in how you earn or spend. It is not financial advice or a sign of money coming. Make big money decisions slowly and with facts."),
         ("Is 555 a warning?", "Not usually. Most readings describe change as exciting or neutral rather than a warning. There is no evidence numbers predict events."),
         ("What should I do when I see 555?", "Name the change you feel, write how you would like to meet it, and take one small, reversible step.")],
    reads=dict(
        general=("555 is commonly read as change and curiosity: something is moving, or ready to. It is a good moment to meet it on purpose rather than by default.", "What change am I feeling pulled toward, and what is a small first step?", "I meet change with curiosity and courage."),
        love=("In love, 555 is often read as a prompt to be honest about change. Say what you want to be different, to the person it concerns or to yourself.", "What would I like to change in my love life, and have I said it out loud?", "I welcome honest change in my relationships."),
        someone=("If someone is on your mind, 555 is not evidence of what they feel. Its theme is change, so ask what you want to change about this situation, and act on that.", "What is one step I could take that does not depend on their reply?", "I move forward, whatever happens next."),
        money=("For money and work, 555 is often read as change in how you earn or spend. It is not a sign of a windfall. Plan the change, try a small test, and decide slowly.", "What is one small thing I could test in my work or money life?", "I explore new options with care and curiosity."),
        decision=("For a decision, 555 is commonly read as permission to choose change, but not recklessly. Try the smallest, most reversible version of the new option first.", "What is the smallest way I could test the change before I commit?", "I choose growth, one safe step at a time."),
        low=("If you feel low, 555 can be a reminder that this will move, because things do. A small change of scene, routine or company can help it shift.", "What is one small thing I could change today: a walk, a call, a tidy corner?", "This will change, and I can help it along gently."),
    ),
)

N["777"] = dict(
    words=["Reflection", "Learning", "Inner wisdom"],
    hub="The calm, thoughtful number: slow down and learn.",
    lead="777 Angel Number Meaning: Love and Money",
    desc="777 angel number meaning: what 777 is commonly linked with in love, money and spirituality, how it differs from lucky 7, and a free tailored tool.",
    lede="Did 777 show up and you wonder whether it is luck or a sign? Pick what you were thinking about for a short reading and a question, then read the full 777 meaning below.",
    one="<p>777 is commonly read as a number of <strong>reflection, learning and inner wisdom</strong>. The digit 7 is long linked with the thoughtful side of life: study, silence, the seeker. Three of them are often taken as a call to slow down, learn from what has happened, and trust your own judgment.</p><p>Many people also hear &ldquo;lucky 777&rdquo; because of slot machines and the popular idea of lucky seven. That is a cultural habit, not part of the numerology. A calmer reading is that 777 is less about luck arriving and more about <em>understanding what you already have</em>.</p>",
    love="<p>In love, 777 is commonly read as an invitation to <strong>go deeper</strong>: with a partner, through honest conversation; or with yourself, through time alone. For singles, it is often read as a season for reflection rather than searching: what have your relationships taught you, and what do you want next?</p><p>It does not say a partner is coming, and it does not mean you should be alone. It is a prompt to look at patterns with kindness, not blame.</p>",
    someone="<p>If you see 777 while thinking about someone, it is commonly read as a nudge to <em>reflect</em> on what this person has taught you. There is no evidence it means they are thinking of you. Often it just means the person is on your mind, so you notice numbers more.</p><p>A helpful exercise: write down what you learned from knowing them, what you need, and what you would do differently. That is worth more than waiting for another sign, and it works whether or not you ever speak again.</p>",
    twin="<p>In twin flame writing, 777 is sometimes described as spiritual awakening or inner work done before a reunion. Twin flame is a popular online idea, not an evidence-based one. There is no scientific support for a single mirror soul.</p><p>The part of this story worth keeping is the inner-work part: time spent on your own healing and understanding is useful, whatever your relationships turn out to be.</p>",
    money_h="What does 777 mean financially?",
    money="<p>For money and work, 777 is commonly linked with <strong>learning and research</strong>: studying a skill, understanding your finances properly, thinking before acting. It is not a sign of luck or a jackpot, and no number is a reason to gamble.</p><p>If you see it, you might ask what you do not yet understand about your money or career, and set aside time to learn it: read a book, take a course, ask someone experienced. Quiet knowledge usually beats lucky guesses over time.</p>",
    spirit="<p>Spiritually, 777 is often called a number of insight or divine perfection, because 7 appears in many traditions (seven days, seven colours, seven chakras in some systems). People use it as a prompt to meditate, journal or take a quiet walk.</p><p>Whatever your beliefs, the common thread is turning inward: spend a little time with your own thoughts and notice what has been trying to get your attention.</p>",
    digit_h="What 7 means in numerology",
    digit="<p>In numerology, 7 is associated with <strong>reflection, analysis and inner wisdom</strong>: the researcher, the thinker, the one who needs quiet. Three 7s emphasise it. Add the digits (7 + 7 + 7) and you reach 21, then 3 (2 + 1), so some readers add a note about expressing what you have learned. You can find the numbers in your own birthday with the <a href=\"/numerology-calculator/\">numerology calculator</a>.</p>",
    steps=["<strong>Find ten quiet minutes</strong> today, with no phone, for a walk or a cup of tea.", "<strong>Write down what this season has been teaching you.</strong> One honest sentence is enough.", "<strong>Choose one thing to learn or look into</strong> this week, and put it in your calendar."],
    related=[("444", "Foundations, support", "Builds the base that 777 reflects on"), ("999", "Completion, letting go", "After reflecting comes closing the chapter"), ("1111", "Alignment, awareness", "Adds the idea of tuning in to what you want"), ("369", "The 369 method", "A daily writing practice that is also quiet reflection")],
    faq=[("What does 777 mean?", "777 is commonly associated with reflection, learning and inner wisdom. Many people read it as a cue to slow down and listen to their own judgment."),
         ("Is 777 lucky?", "Popular culture treats seven as lucky, but in numerology 777 is more about reflection than luck. There is no scientific evidence numbers bring luck."),
         ("What does 777 mean in love?", "It is commonly read as a prompt to go deeper, with a partner or with yourself, and to reflect on patterns. It is not a prediction."),
         ("What does 777 mean when thinking about someone?", "Mostly that the person is on your mind. Some read it as a cue to reflect on what they taught you. There is no evidence it means they are thinking of you."),
         ("What does 777 mean financially?", "It is commonly linked with learning and thinking before acting. It is not a sign of luck and it is not a reason to gamble."),
         ("What does 777 mean spiritually?", "It is often called a number of insight and inner wisdom. That is a personal belief; try it as a prompt to meditate or journal.")],
    reads=dict(
        general=("777 is commonly read as an invitation to reflect: slow down, learn from what has happened and trust your own judgment. It is less about luck and more about understanding.", "What has this season of my life been trying to teach me?", "I trust my inner wisdom, and I keep learning."),
        love=("In love, 777 is often read as a call to go deeper, with a partner or with yourself. It is a good time to look at patterns with kindness, not blame.", "What have my relationships taught me about what I need?", "I learn from love, and I grow wiser in it."),
        someone=("With someone on your mind, 777 is commonly read as a prompt to reflect on what they taught you. It is not proof of what they feel. Reflection is useful either way.", "What did knowing this person teach me, and what do I want to carry forward?", "I learn from every connection, and I carry the best of it."),
        money=("For money and work, 777 is often read as learning before acting. It is not a sign of luck. Study a skill or understand your finances properly.", "What do I not yet understand about my money or career that I could learn?", "I learn, think and then act with confidence."),
        decision=("For a decision, 777 is commonly read as: take quiet time and listen to your own judgment. Give it a night, and write your thoughts down.", "What does my quiet, calm self say about this decision?", "I listen to my own wisdom and decide calmly."),
        low=("If you feel low, 777 can be a cue for quiet and gentleness: time alone, a walk, a few lines on paper. Reflection is a form of rest.", "What do I need most right now, and can I give myself ten minutes of it?", "I give myself quiet, and I listen with kindness."),
    ),
)

N["999"] = dict(
    words=["Completion", "Closure", "Letting go"],
    hub="Permission to finish a chapter well and let it go.",
    lead="999 Angel Number Meaning: Love and Endings",
    desc="999 angel number meaning: what people commonly link 999 with in endings, love and money, what it means when thinking of someone, and a free tailored tool.",
    lede="Is 999 following you around? Pick what you were thinking about for a short, tailored reading, then read the full 999 angel number meaning. It is gentler than its reputation.",
    one="<p>999 is commonly read as a number of <strong>completion, closure and letting go</strong>. The digit 9 is the last single digit, so it is linked with endings, with finishing cycles and with compassion. Three 9s are often taken as a sign that a chapter is closing, and that finishing it well makes room for what follows.</p><p>Endings can sound scary, so people sometimes read 999 as a warning. Most sources describe it more like permission: you are allowed to finish, to stop carrying what is done, and to be proud of how far you have come.</p>",
    love="<p>In love, 999 is commonly read as <strong>closure</strong>. That can mean letting go of an old relationship you keep replaying, forgiving someone (or yourself), or ending a pattern. Within a relationship, it can mean closing an old argument and starting fresh.</p><p>It does not mean a relationship must end, and it does not mean a new one is coming. If it nudges you toward the question &ldquo;what am I still carrying that I could put down?&rdquo;, that is where its value lies.</p>",
    someone="<p>999 appears in a lot of searches about someone from the past. The honest answer: the person is on your mind, so you notice the number. There is no evidence it means they are thinking of you or that you will reconnect.</p><p>The common reading is closure: the chapter with this person may be done, and the number invites you to finish it in your own way. That might be writing the letter you never send, forgiving, or deciding to stop checking their profile. Closure usually comes from your own choice, not from a sign.</p>",
    twin="<p>In twin flame writing, 999 is often described as the end of a cycle or the &ldquo;final stage&rdquo; before a reunion. Twin flame is a popular online idea, not a proven one, and these stories can make it harder to move on. There is no scientific evidence that numbers predict reunions.</p><p>If you are tempted to read 999 as &ldquo;wait for them to return&rdquo;, consider the other reading: it is about <em>your</em> completion, and your next chapter is yours to start.</p>",
    money_h="What does 999 mean financially?",
    money="<p>For money and work, 999 is commonly linked with <strong>finishing and clearing</strong>: wrapping up a project, closing an old account, paying off a debt, leaving a job that has run its course. It is not a prediction of money coming or going.</p><p>A practical use: list the money loose ends you have been avoiding, such as an unpaid bill, an unused subscription or an unfinished project, and close one. Finishing frees time and attention, which are worth a lot. For larger moves, like leaving a job, plan with facts.</p>",
    spirit="<p>Spiritually, 999 is often called the number of completion and of service: a cycle ends, and the lessons are taken forward. Some traditions link 9 with compassion and with helping others once your own chapter has closed.</p><p>Whether you read it as a message or as your own mind finding a pattern, the invitation is the same: appreciate what has been, thank it, and let it go with some grace.</p>",
    digit_h="What 9 means in numerology",
    digit="<p>In numerology, 9 is associated with <strong>completion, compassion and letting go</strong>: the humanitarian, the wise elder, the one who sees the big picture. Three 9s emphasise it. Add the digits (9 + 9 + 9) and you reach 27, then 9 again (2 + 7), a fitting loop for a number about cycles. 9 is also the closing count in the 369 method: nine lines at night to close the day. See the <a href=\"/369-meaning/\">369 meaning page</a>.</p>",
    steps=["<strong>Name what is ready to end:</strong> a project, a habit, a story you tell yourself.", "<strong>Thank it in one line</strong> and write what it gave you. Then write what you are ready to put down.", "<strong>Do one closing act today:</strong> send the message, cancel the subscription, finish the draft."],
    related=[("555", "Change, freedom", "Where 999 closes a chapter, 555 starts the change"), ("333", "Expression, creativity", "3 x 3: say it, then let it go"), ("777", "Reflection, learning", "Reflect first, then close the chapter"), ("369", "The 369 method", "9 is the closing count of the day")],
    faq=[("What does 999 mean?", "999 is commonly associated with completion, closure and letting go. Many people read it as a sign that a chapter is closing and that finishing it well makes room for what is next."),
         ("Is 999 a bad number?", "No. It is sometimes mistaken for a warning, but most readings treat it as permission to finish and move on. There is no evidence numbers predict endings."),
         ("What does 999 mean in love?", "It is commonly read as closure: letting go of an old relationship, forgiving, or ending a pattern. It does not mean a relationship must end."),
         ("What does 999 mean when thinking about someone?", "Mostly that someone is on your mind. Some read it as closure with that person. There is no evidence it means they are thinking of you or will return."),
         ("What does 999 mean financially?", "It is commonly linked with finishing and clearing: wrapping up projects or debts. It is not a prediction of money coming or going."),
         ("What does 999 mean spiritually?", "Often completion and compassion. Many people read it as a call to thank a chapter and let it go. That is a personal belief rather than a proven fact.")],
    reads=dict(
        general=("999 is commonly read as completion: a chapter is ready to close. It is a good moment to finish something well and put down what is already done.", "What is ready to be finished, so something new can begin?", "I let go with gratitude and make room for what's next."),
        love=("In love, 999 is often read as closure: forgiving, finishing an old story or closing a pattern. It does not mean a relationship must end.", "What am I still carrying from past love that I could put down?", "I release the past with kindness and keep what I learned."),
        someone=("If someone from the past is on your mind, 999 is commonly read as closure on your own terms. It is not a sign that they will return. Closure is something you can choose.", "What would help me close this chapter, even if I never speak to them again?", "I give myself the closure I am waiting for."),
        money=("For money and work, 999 is often read as finishing and clearing: closing a loose end, wrapping up a project. It is not a prediction, just a good prompt to finish something.", "Which money or work loose end could I close this week?", "I finish what I start and clear what no longer serves me."),
        decision=("For a decision, 999 is commonly read as: if something has run its course, you are allowed to finish. Ask what you would be relieved to complete.", "What would I be relieved to end, and what would I be sad to lose?", "I choose endings that make room for good things."),
        low=("If you feel low, 999 can be a reminder that hard chapters do end, and that you have already completed many. Be gentle with what you are carrying.", "What have I already got through that I rarely give myself credit for?", "I have completed hard things, and I can complete this too."),
    ),
)

N["1010"] = dict(
    words=["Growth", "Self-belief", "Next level"],
    hub="A nudge that you are further along than you feel.",
    lead="1010 Angel Number Meaning: Love and Money",
    desc="1010 angel number meaning: what people commonly link 1010 with in growth, love and money, what it means when thinking of someone, plus a free tailored tool.",
    lede="Keep seeing 1010 on the clock? Pick what was on your mind for a short reading and a question, then read the full 1010 angel number meaning and what to do next.",
    one="<p>1010 is commonly read as a number of <strong>growth and self-belief</strong>. It mixes 1 (beginnings, independence) and 0 (potential, wholeness), repeated twice. That pairing is often taken to mean that you are moving into a new stage, and that you are more ready than you think.</p><p>People who see 1010 are often at a moment of change, and the usual reading is encouraging: keep going, trust your direction, use your own judgment. Like any number sign it is an invitation to reflect, not a forecast.</p>",
    love="<p>In love, 1010 is commonly read as <strong>being yourself and growing</strong>. For singles, it is often read as building self-respect and a life you like, so that you meet people from fullness rather than need. In relationships, it is read as growth together: new habits, honest talks, being willing to change.</p><p>It does not say who or when. A grown-up use is to ask: am I being the person I want to be in my relationships?</p>",
    someone="<p>If 1010 comes up while someone is on your mind, the likely explanation is that you notice numbers more when a person is in your thoughts. It does not show what they are feeling.</p><p>The more useful reading is about growth: how are you changing, and is this connection supporting that? A small act of self-belief, like making plans of your own or having the conversation you have been avoiding, often does more for you than waiting for a sign.</p>",
    twin="<p>In twin flame writing, 1010 is sometimes described as spiritual growth or as a stage of learning to love yourself. Twin flame is a popular idea, not an established one, and there is no scientific evidence that it describes real relationships.</p><p>The part worth keeping: growth in self-belief and self-respect is useful with or without the story, and it makes every relationship healthier.</p>",
    money_h="What does 1010 mean financially?",
    money="<p>For money and work, 1010 is commonly linked with <strong>confidence and next steps</strong>: asking for the raise, starting the side project, raising your rates. It is not a sign that money is coming and not financial advice.</p><p>If you see it, ask: what is the &ldquo;next level&rdquo; step in my work I have been doubting myself on? Write the case for it: your evidence, your results. Confidence built on a list of real achievements is far steadier than confidence built on a number.</p>",
    spirit="<p>Spiritually, 1010 is often described as a number of awakening and of trusting your path. People use it as a prompt to meditate on what they truly want, to listen to their intuition, and to believe they are on the right track.</p><p>Without any belief, it still works as a cue to notice how far you have come, which is something most of us forget to do.</p>",
    digit_h="What 1 and 0 mean in numerology",
    digit="<p>In numerology, 1 is associated with <strong>beginnings and independence</strong>, and 0 with <strong>potential and wholeness</strong>: a blank page and a full circle. Together, 10 is often described as completing one cycle and starting another. Add the digits (1 + 0 + 1 + 0) and you reach 2, linked with balance and trust. See how the numbers in your own life work with the <a href=\"/numerology-calculator/\">numerology calculator</a>.</p>",
    steps=["<strong>Write down three things you have done</strong> in the last year that you are proud of.", "<strong>Name your next level:</strong> the one step you keep putting off because of self-doubt.", "<strong>Do the first ten minutes of it today.</strong> Belief grows from action."],
    related=[("111", "Beginnings, focus", "The 1 side: starting and attention"), ("1111", "Alignment, awareness", "Four 1s: a stronger focus on intention"), ("1212", "Trust, steady steps", "Another number about the next brave step"), ("555", "Change, freedom", "Growth that involves a bigger change")],
    faq=[("What does 1010 mean?", "1010 is commonly associated with growth, self-belief and moving to a new stage. Many people read it as encouragement to trust their direction."),
         ("What does 1010 mean in love?", "It is commonly read as growth and being yourself: building self-respect, and growing with a partner. It is not a prediction about a specific person."),
         ("What does 1010 mean when thinking about someone?", "Mostly that the person is on your mind. It does not show what they feel. A more useful reading is to ask how you are growing and whether the connection supports it."),
         ("What does 1010 mean financially?", "It is commonly linked with confidence and next steps in work or money. It is not a sign that money is coming or financial advice."),
         ("Why do I keep seeing 1010?", "Once a number catches your attention, you notice it more. Many people see 1010 on clocks because it is a time many people look at. You can use it as a prompt to reflect."),
         ("What does 1010 mean spiritually?", "Often growth, awakening and trusting your path. That is a personal belief, with no scientific evidence behind it.")],
    reads=dict(
        general=("1010 is commonly read as growth and self-belief: you are further along than you feel. It is a good moment to notice what has already changed in you.", "What evidence do I already have that I am growing?", "I believe in my path, and I keep growing."),
        love=("In love, 1010 is often read as being yourself and growing, alone or together. The more you like your own life, the clearer your choices tend to be.", "Am I being the person I want to be in my relationships?", "I grow in love, and I stay true to myself."),
        someone=("With someone on your mind, 1010 is not proof of what they feel. Its theme is your growth, so ask how you are changing and whether this connection supports it.", "What step could I take for my own growth, whatever they do?", "I believe in myself, whatever happens next."),
        money=("For money and work, 1010 is often read as confidence and a next step: the ask, the pitch, the new rate. It is not a sign of money coming.", "What next step in my work have I been doubting myself about?", "I step into my next level with confidence."),
        decision=("For a decision, 1010 is commonly read as a vote for growth: which option stretches you, in a way you could actually handle?", "Which option would I be proud of in a year?", "I trust my direction and choose growth."),
        low=("If you feel low, 1010 can be a reminder that you have grown more than you notice. Write down three things you have come through.", "What am I stronger at now than I was a year ago?", "I am growing, even on the days it does not feel like it."),
    ),
)

N["1111"] = dict(
    words=["Alignment", "Awareness", "Wishes"],
    hub="The famous wish-and-intention number.",
    lead="1111 Angel Number Meaning: Love and Wishes",
    desc="1111 angel number meaning: what 1111 is commonly linked with in love, money, twin flame stories and wishes, why 11:11 matters, and a free tool.",
    lede="See 1111 or 11:11 a lot? Choose what you were thinking about for a short reading, a question and an affirmation, then read the full 1111 meaning, wish tradition and all.",
    one="<p>1111 is probably the most famous angel number. It is commonly read as a number of <strong>alignment, awareness and intention</strong>. Four 1s make a strong emphasis on the digit of beginnings and focus, and 11 is a &ldquo;master number&rdquo; in numerology, linked with intuition.</p><p>Many people also treat 11:11 on a clock as a moment to <strong>make a wish</strong>, a custom that is more folk habit than anything ancient. A grounded way to use it: let the moment be a prompt to say what you actually want, quietly, and then look for one real thing you can do about it.</p>",
    love="<p>In love, 1111 is commonly read as a cue to get <strong>honest and aligned</strong>: with what you want, with who you are being in your relationship, and with your values. Singles often use the 11:11 moment to restate a wish about love.</p><p>It is not a sign that someone is about to arrive. The lasting part is the clarity: when your wish for love is specific and kind (&ldquo;a steady, honest partner&rdquo;), it is easier to notice who fits it.</p>",
    someone="<p>&ldquo;Seeing 1111 when thinking about someone&rdquo; is very common, and the plain explanation is that thinking of a person sharpens your attention to anything repeating. There is no evidence it means they are thinking of you, or that you are meant to be together.</p><p>If you want to use the moment, make the wish about <em>you</em>: &ldquo;I want to feel clear and calm about this.&rdquo; Then act on it: have the conversation, set the boundary, or stop checking. A wish for another person&rsquo;s feelings is not in your hands, but your next step is.</p>",
    twin="<p>1111 is the number most often named in twin flame communities, usually described as an &ldquo;awakening&rdquo; or &ldquo;portal&rdquo; sign. Twin flame is a popular online idea; there is no scientific evidence for it, and some therapists caution that it can keep people hooked on unhealthy, on-again-off-again relationships.</p><p>If you enjoy the idea, hold it lightly. A relationship is better judged by how it treats you over time than by how many repeating numbers you saw.</p>",
    money_h="What does 1111 mean financially?",
    money="<p>For money and work, 1111 is commonly linked with <strong>clear intention</strong>: knowing what you want from your work and finances, and aligning your habits with it. It is not a sign of money arriving and not financial advice.</p><p>A simple use of the moment: write down one specific money intention, such as &ldquo;Build a $1,000 cushion by March,&rdquo; and one action this week that moves toward it. Intentions with numbers and dates tend to be much easier to follow than vague hopes.</p>",
    spirit="<p>Spiritually, 1111 is often described as a sign of alignment with your higher self, a moment of heightened awareness. Many people stop, breathe and set an intention when they notice it. Others see it as a sign that they are on the right path.</p><p>Whether or not you believe that, the ritual is useful: a deliberate pause once or twice a day to ask what you want is a simple, evidence-friendly habit.</p>",
    digit_h="What 1 and 11 mean in numerology",
    digit="<p>In numerology, 1 stands for <strong>beginnings and independence</strong>, and 11 is a master number associated with <strong>intuition and inspiration</strong>. 1111 is two 11s side by side. Add the digits (1 + 1 + 1 + 1) and you reach 4, linked with foundations and steady work, so many readers add a note: make the wish, then build toward it. Explore your own numbers with the <a href=\"/numerology-calculator/\">numerology calculator</a>.</p>",
    steps=["<strong>Pause and take one slow breath</strong> as you notice the number.", "<strong>Make your wish specific:</strong> write it as one short, present-tense line, like &ldquo;I am steady and clear about what I want.&rdquo;", "<strong>Do one small real action</strong> that points toward it, then repeat the line again tomorrow."],
    related=[("111", "Beginnings, focus", "Fewer 1s, the same idea of focus and intention"), ("444", "Foundations, support", "1111 adds to 4: wish first, then build"), ("1212", "Trust, steady steps", "Another number about steady next steps"), ("369", "The 369 method", "A daily way to restate your intention")],
    faq=[("What does 1111 mean?", "1111 is commonly associated with alignment, awareness and intention. Many people read it as a moment to pause and make a wish or restate a goal."),
         ("Why do people make a wish at 11:11?", "It is a folk custom: because the clock shows four matching 1s, people treat it as a special moment for a wish. There is no scientific evidence it works, but it makes a handy prompt to say what you want."),
         ("What does 1111 mean in twin flame terms?", "It is the number most often cited in twin flame communities, usually as an awakening sign. Twin flame is a popular idea with no scientific evidence."),
         ("What does 1111 mean when thinking about someone?", "Mostly that someone is on your mind. There is no evidence it means they are thinking of you. Use it to get clear on what you want."),
         ("What does 1111 mean financially?", "It is commonly linked with clear intention about money. It is not a sign of money arriving. Pair an intention with a specific action."),
         ("Is 1111 a good sign?", "Most people read it as positive: awareness and alignment. It is a prompt to reflect, not a guarantee.")],
    reads=dict(
        general=("1111 is commonly read as alignment and awareness: a quiet moment to say what you want. Many people use it for a wish. Make it specific, and follow it with one small action.", "If I could set one intention right now, what would it be?", "I am aligned with what I truly want."),
        love=("In love, 1111 is often read as a cue to be honest and aligned with what you want and who you want to be. A specific, kind wish is easier to act on.", "What do I want from love, in one clear sentence?", "I am clear and open about the love I want."),
        someone=("With someone on your mind, 1111 is not evidence of what they feel. Make the wish about you: clarity, calm, a next step. That part is in your hands.", "What do I want to feel about this, and what is one step toward that?", "I am clear and calm about my next step."),
        money=("For money and work, 1111 is often read as clear intention. Put a number and a date on it, then choose one action this week.", "What specific money goal would I like to set, and what is the first action?", "I align my habits with the life I want to build."),
        decision=("For a decision, 1111 is commonly read as: check your alignment. Which option fits your values, and which fits only your fear?", "Which option is most in line with what I truly value?", "I choose what is aligned with who I am."),
        low=("If you feel low, 1111 can be a still moment to breathe and say one kind wish for yourself. It does not have to be big.", "What is one thing I wish for myself today, in simple words?", "I am allowed to hope, and I begin with one small step."),
    ),
)

N["1212"] = dict(
    words=["Trust", "Steady steps", "Comfort zone"],
    hub="A nudge to trust yourself and take one slightly brave step.",
    lead="1212 Angel Number Meaning: Love and Money",
    desc="1212 angel number meaning: what people commonly link 1212 with in love, money and spirituality, what it means when thinking of someone, and a free tool.",
    lede="Seeing 1212 on clocks and receipts? Pick what you were thinking about for a short reading and a question, then read what angel number 1212 commonly means and how to use it.",
    one="<p>1212 is commonly read as a number of <strong>trust and gentle courage</strong>. It mixes 1 (starting, independence) with 2 (balance, patience), twice over. The pairing is often taken to mean: take a step, then let things settle; be brave, but keep your feet on the ground.</p><p>It is popular with people who are thinking about moving out of a comfort zone and are not sure they are ready. The usual reading is encouraging, but it is not a green light for a risky leap. Think of it as a prompt to take the next small, sensible step.</p>",
    love="<p>In love, 1212 is commonly read as <strong>courage with patience</strong>. For singles, it can mean opening up a little, saying yes to an invitation, or updating a profile you have been avoiding, without forcing anything. In relationships, it is often read as a cue to take a small brave step together: a conversation, a trip, a boundary.</p><p>It does not say a specific person is meant for you. The helpful part is the pairing of courage and balance: be brave, and be kind to yourself about it.</p>",
    someone="<p>If you keep seeing 1212 while thinking about a particular person, the likely explanation is that your attention is sharper when someone is on your mind. There is no evidence it shows what they feel.</p><p>The useful reading is about your own step: what is one slightly brave thing you could do here, without forcing an outcome? That might be a short, honest message, or a boundary, or making plans that do not depend on them. Small steps, then patience, is the 1 and 2 of it.</p>",
    twin="<p>In twin flame communities, 1212 is sometimes described as a sign to trust the process or as a step toward reunion. Twin flame is a popular idea, not a scientific one, and there is no evidence that number patterns predict relationships.</p><p>If the phrase &ldquo;trust the process&rdquo; helps you, apply it to your own growth: take the next step you can see, and let other people show you their choices with their actions.</p>",
    money_h="What does 1212 mean financially?",
    money="<p>For money and work, 1212 is commonly linked with <strong>small brave steps</strong>: applying for the role, asking for a quote, setting up the savings transfer, sending the invoice you have been avoiding. It is not a sign of money coming and not financial advice.</p><p>The 2 half of the number is the part to remember: steady and patient. Choose a step that is a little uncomfortable but fully reversible, and then give it time. Big leaps are best planned with facts, and sometimes with a professional.</p>",
    spirit="<p>Spiritually, 1212 is often described as a message of encouragement: stay positive, trust that things are working out, keep growing. Some people read it as spiritual support while they step into something new.</p><p>You can also read it more simply, as your own mind reminding you that you have been wanting to take a step. Whichever view you take, the prompt is the same: choose a small step and take it.</p>",
    digit_h="What 1 and 2 mean in numerology",
    digit="<p>In numerology, 1 is associated with <strong>beginnings and independence</strong> and 2 with <strong>balance, patience and partnership</strong>. The alternating pattern 1-2-1-2 is often read as a step and a settle, a step and a settle. Add the digits (1 + 2 + 1 + 2) and you reach 6, linked with care, home and responsibility: bravery that still looks after the people and things you love. Try the <a href=\"/numerology-calculator/\">numerology calculator</a> for your own numbers.</p>",
    steps=["<strong>Name the step</strong> that is just outside your comfort zone, but safe to try.", "<strong>Make it smaller</strong> until it takes under 15 minutes, then do it today.", "<strong>Give it time.</strong> Notice how you feel, then choose the next small step."],
    related=[("111", "Beginnings, focus", "The 1 side: start and focus"), ("222", "Balance, patience", "The 2 side: settle and wait kindly"), ("1010", "Growth, self-belief", "Another number about believing in your direction"), ("555", "Change, freedom", "A bigger version: larger change")],
    faq=[("What does 1212 mean?", "1212 is commonly associated with trust, steady steps and moving a little outside your comfort zone. Many people read it as encouragement to take the next small step."),
         ("What does 1212 mean in love?", "It is commonly read as courage with patience: a small brave step, then letting things settle. It is not a prediction about a specific person."),
         ("What does 1212 mean when thinking about someone?", "Mostly that someone is on your mind. There is no evidence it shows what they feel. A better use is to ask what small brave step you could take."),
         ("What does 1212 mean financially?", "It is commonly linked with small brave steps: asking, applying, starting a saving habit. It is not a sign of money coming."),
         ("Is angel number 1212 good luck?", "Most people read it as encouraging. There is no scientific evidence numbers bring luck, so use it as a prompt to take a sensible next step."),
         ("What does 1212 mean spiritually?", "Often encouragement and trust. That is a personal belief; the practical reading is to take the next small step.")],
    reads=dict(
        general=("1212 is commonly read as encouragement to trust yourself and take a slightly brave step, then let things settle. Small, sensible steps count.", "What is one slightly brave step I could take this week?", "I trust myself to take the next step."),
        love=("In love, 1212 is often read as courage with patience: a small brave step, then letting it unfold. No forcing.", "What is one small, brave thing I could do in love this week?", "I open my heart bravely and patiently."),
        someone=("With someone on your mind, 1212 is not proof of what they feel. Its theme is your next small step: a short honest message, a boundary, or plans of your own.", "What small step would help me feel better about this, whatever they do?", "I take small, brave steps and let the rest unfold."),
        money=("For money and work, 1212 is often read as small brave steps: asking, applying, saving. Choose one that is a bit uncomfortable but reversible.", "What small money or work step have I been putting off?", "I take small, steady steps toward what I want."),
        decision=("For a decision, 1212 is commonly read as: pick the option that stretches you a little but is still safe to try. Take a step, then look again.", "Which option is a small stretch rather than a leap?", "I step forward with trust and keep my feet on the ground."),
        low=("If you feel low, 1212 can be a reminder that the next step can be tiny. One small action, then patience, is enough for today.", "What is one tiny thing I could do in the next ten minutes?", "I take it one small step at a time."),
    ),
)

N["369"] = dict(
    words=["The 369 method", "Intention", "Daily focus"],
    hub="Best known as a daily writing method, not just a number.",
    lead="369 Angel Number Meaning and the 369 Method",
    desc="369 angel number meaning: what 3, 6 and 9 stand for, what it means when you keep seeing 369, how it links to the 369 method, plus a free tailored tool.",
    lede="Keep seeing 369? Pick what you were thinking about for a short reading, a question and an affirmation. Below, what 369 commonly means and how the 369 method turns it into a daily practice.",
    one="<p>369 is the angel number with a built-in practice. As a number, it is commonly read as <strong>express it (3), care for it (6), let it go (9)</strong>: say what you want, tend it every day, then trust it. Today it is best known through the <a href=\"/369-method/\">369 method</a>, where you write one intention 3 times in the morning, 6 in the afternoon and 9 at night.</p><p>So if 369 keeps showing up, the grounded reading is: <em>you have been thinking about what you want, and a daily habit might help.</em> For the full story of the number, including where it comes from, see our <a href=\"/369-meaning/\">369 meaning</a> guide.</p>",
    love="<p>In love, 369 is commonly read as a call to <strong>be clear about what you want and to care for it daily</strong>. Write one sentence about the kind of relationship you want to be in, or the kind of partner you want to be, and return to it through the day.</p><p>A caution worth repeating: the 369 method is for your own intentions, not for controlling another person&rsquo;s feelings. Write about your own habits, your own openness and your own boundaries. It cannot make a particular person love you, and a number cannot either.</p>",
    someone="<p>If 369 comes up while you think about someone, the likely explanation is attention: your mind is on them, so you notice numbers. There is no evidence it means they are thinking of you.</p><p>In the 369 method, the better question is what you want <em>for yourself</em> in this situation. Many people write lines like &ldquo;I feel calm and clear whatever happens&rdquo; rather than lines about the other person. Writing about your own feelings and actions is healthier, and far more within your control.</p>",
    twin="<p>369 is not one of the main numbers in twin flame writing, but it turns up in forums that combine twin flame and manifestation ideas. Twin flame is a popular online idea with no scientific evidence, and manifesting a specific person is not something the 369 method (or any method) can do.</p><p>If you are drawn to it, use the method for what it can do: help you stay focused on your own goals, habits and feelings.</p>",
    money_h="What does 369 mean financially?",
    money="<p>For money, 369 is commonly linked with <strong>writing a money intention and returning to it daily</strong>. Many people choose a goal like &ldquo;I save $200 a month and feel calm about money.&rdquo; The method works best with real action alongside the writing: a budget, a transfer, a conversation.</p><p>It is not a way to make money appear, and writing a number does not change a bank balance. What it can do is keep a goal in front of you three times a day, which makes it more likely you follow through on the practical steps.</p>",
    spirit="<p>Spiritually, 369 is often described as a number of creation and divine order, largely through the popular (and unsourced) idea that it holds a secret of the universe. We looked into that claim: there is no reliable source for the famous quote, which is covered on our page about <a href=\"/369-method/tesla/\">Tesla and 369</a>.</p><p>What survives is the human version: a number that gives you a reason to stop, set an intention and come back to it. Many people find the rhythm itself, morning, afternoon, night, quietly calming.</p>",
    digit_h="What 3, 6 and 9 mean in numerology",
    digit="<p>In numerology, <strong>3</strong> is associated with creativity and expression, <strong>6</strong> with care, home and responsibility, and <strong>9</strong> with completion and compassion. Added together (3 + 6 + 9) you get 18, then 9 again (1 + 8), a nice loop for a number about daily cycles. In the 369 method the numbers become counts: write 3 lines in the morning to set the tone, 6 in the afternoon to return, 9 at night to close the day.</p><p>Curious how this works with your own birth numbers? Try the <a href=\"/numerology-calculator/\">numerology calculator</a>.</p>",
    steps=["<strong>Choose one intention</strong> and write it as a short present-tense line, like &ldquo;I am steady and I follow through.&rdquo;", "<strong>Write it 3 times this morning.</strong> Then 6 times in the afternoon and 9 times at night. It takes a few minutes in total.", "<strong>Do one small real thing</strong> that matches the line each day, and keep it up for 21 days before you judge it."],
    related=[("333", "Creativity, expression", "The morning count: say what you want"), ("999", "Completion, letting go", "The night count: close the day"), ("1111", "Alignment, awareness", "Another number people use to restate an intention"), ("777", "Reflection, learning", "A quieter route to the same reflection")],
    faq=[("What does the 369 angel number mean?", "369 is commonly read as: express what you want (3), care for it daily (6) and let it go (9). It is best known through the 369 manifestation method, a daily writing practice."),
         ("What does it mean when I keep seeing 369?", "Often that your mind is on something you want, so you notice the number. Many people use it as a cue to write down one intention and return to it through the day."),
         ("How do I do the 369 method?", "Choose one short intention and write it 3 times in the morning, 6 in the afternoon and 9 at night, usually for 21 to 45 days, alongside one small real action."),
         ("What does 369 mean when thinking about someone?", "Mostly that someone is on your mind. The 369 method works on your own habits and feelings, not on another person. Write about what you can control."),
         ("Did Tesla say 3, 6 and 9 are the key to the universe?", "There is no reliable source for that quote. It does not appear before about 2018, many years after his death. We go through the evidence on our Tesla and 369 page."),
         ("Does the 369 method work?", "There is no scientific evidence that writing an intention changes outside events. Many people do find that a daily habit keeps a goal in mind and helps them take action.")],
    reads=dict(
        general=("369 is commonly read as a reminder to restate an intention: say what you want in the morning, return to it midday, close the day with it. It is a prompt to focus, not a promise.", "If I wrote one sentence 18 times today, what would I want it to be?", "I keep my intention in front of me, morning, afternoon and night."),
        love=("In love, 369 is often read as: be clear about what you want and care for it daily. Write about your own openness and habits, not about controlling another person.", "What kind of partner do I want to be, and what is one habit that shows it?", "I show up for love with clarity and care."),
        someone=("With someone on your mind, 369 is not evidence of what they feel. If you use the method, write about what you want for yourself: calm, clarity, a next step.", "What do I want to feel about this, whatever happens?", "I feel calm and clear, whatever happens."),
        money=("For money, 369 is often read as writing one money intention and returning to it daily. The writing helps focus. The real work is the budget, the transfer, the conversation.", "What one money intention will I write, and what action will go with it?", "I take steady, practical steps toward my money goals."),
        decision=("For a decision, 369 can be a way to listen: write the question once in the morning, once at midday, once at night, and notice how your answer changes.", "What answer do I keep coming back to when I write it down?", "I trust the answer that stays when I write it down."),
        low=("If you feel low, 369 can be a very small routine: three lines, then six, then nine. It is a gentle structure when the day feels shapeless.", "What is one kind sentence I would like to read to myself today?", "I take today gently, one line and one breath at a time."),
    ),
)


# ---------------------------------------------------------------- page builders

HONEST = ("<p>To be straightforward: there is no scientific evidence that numbers carry messages. Our minds are good at "
          "spotting patterns, and once you notice {n} you tend to notice it more. That does not make the moment useless. "
          "Many people use it as a small cue to pause, breathe and ask what they want, and that is how we suggest you use it.</p>")

BRIDGE = {
    "default": "A number is a moment. Writing your intention every day is a practice. The <a href=\"/369-method/\">369 method</a> is a simple way to do it: write one short line 3 times in the morning, 6 in the afternoon and 9 at night. <a href=\"/369-meaning/\">What 369 means</a> explains where it comes from.",
    "369": "The 369 method is the point of this number. Choose one line, write it 3 times in the morning, 6 in the afternoon and 9 at night, and pair it with one real action. The <a href=\"/369-method/\">full step-by-step is here</a>, and the <a href=\"/369-meaning/\">369 meaning</a> page covers the history honestly.",
}


def esc(s):
    return html.escape(s, quote=True)


def reading_html(n, ctx, label, e):
    text, ask, aff = e
    return (f'<div class="ap-result"><p class="ap-ctx">{n} &middot; {esc(label)}</p>'
            f'<p class="ap-text">{esc(text)}</p>'
            f'<div class="ap-box"><p class="ap-k">A question to sit with</p><p class="ap-q">{esc(ask)}</p></div>'
            f'<div class="ap-box ap-aff"><p class="ap-k">An affirmation to try</p><p class="ap-aff-t">&ldquo;{esc(aff)}&rdquo;</p></div>'
            f'<div class="ap-actions"><button type="button" class="btn small" data-copy="{esc(aff)}">Copy affirmation</button>'
            f'<a class="btn ghost small" href="/affirmation-wallpaper/" data-wallpaper data-copy-text="{esc(aff)}">Make it my lock screen</a></div>'
            f'<p class="ap-note">A reflection prompt, not a prediction. There is no scientific evidence that numbers carry messages.</p></div>')


def tool_body(n):
    d = N[n]
    chips = "".join(
        f'<button type="button" class="ap-chip" data-ctx="{k}" aria-pressed="{"true" if k == "general" else "false"}">{esc(lbl)}</button>'
        for k, lbl in CONTEXTS)
    data = {"n": n, "labels": dict(CONTEXTS),
            "reads": {k: {"text": v[0], "ask": v[1], "aff": v[2]} for k, v in d["reads"].items()}}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    first = reading_html(n, "general", "General", d["reads"]["general"])
    return f"""    <div class="tool-shell single ap" data-angel-page data-number="{n}">
      <div class="tool-panel print-hide">
        <p class="t-label" id="ap-q">Where did you see {n}, or what were you thinking about?</p>
        <div class="ap-chips" role="group" aria-labelledby="ap-q">{chips}</div>
        {privacy("Runs in your browser. Nothing you choose is saved or sent with your name.")}
      </div>
      <div class="ap-card" aria-live="polite" data-result>{first}</div>
    </div>
    <script type="application/json" id="ap-data">{blob}</script>"""


def related_table(n):
    rows = "\n".join(
        f'<tr><th scope="row"><a href="/angel-numbers/{m}/">{m}</a></th><td>{esc(assoc)}</td><td>{esc(diff)}</td></tr>'
        for m, assoc, diff in N[n]["related"])
    return ('      <div class="table-wrap"><table><thead><tr><th scope="col">Number</th><th scope="col">Commonly associated with</th>'
            f'<th scope="col">How it differs from {n}</th></tr></thead><tbody>\n{rows}\n</tbody></table></div>')


def number_page(n):
    d = N[n]
    h1 = f"{n} Angel Number Meaning"
    title = f"{d['lead']} | 369 Journal"
    assert len(title) <= 60, (n, len(title), title)
    assert 140 <= len(d["desc"]) <= 160, (n, len(d["desc"]))
    toc = [("one", f"{n} meaning in one minute"), ("love", f"{n} in love and relationships"),
           ("someone", f"Seeing {n} when thinking about someone"), ("twin", f"{n} twin flame meaning"),
           ("money", d["money_h"]), ("spirit", f"{n} spiritual meaning"), ("digit", d["digit_h"]),
           ("practice", f"What to do when you see {n}"), ("related", "Related angel numbers")]
    toc_html = "".join(f'<li><a href="#{k}">{esc(t)}</a></li>' for k, t in toc)
    steps = "".join(f"<li>{s}</li>" for s in d["steps"])
    bridge = BRIDGE["369"] if n == "369" else BRIDGE["default"]
    article = f"""      <nav class="toc" aria-label="On this page">
        <strong>On this page</strong>
        <ol>{toc_html}</ol>
      </nav>

      <h2 id="one">{n} meaning in one minute</h2>
      {d['one']}
      {HONEST.format(n=n)}

      <h2 id="love">{n} in love and relationships</h2>
      {d['love']}

      <h2 id="someone">Seeing {n} when you are thinking about someone</h2>
      {d['someone']}

      <h2 id="twin">{n} twin flame meaning</h2>
      {d['twin']}

      <h2 id="money">{d['money_h']}</h2>
      {d['money']}

      <h2 id="spirit">{n} spiritual meaning: what is it trying to tell you?</h2>
      {d['spirit']}

      <h2 id="digit">{d['digit_h']}</h2>
      {d['digit']}

      <h2 id="practice">What to do when you see {n}</h2>
      <ol>{steps}</ol>
      <p>{bridge}</p>

      <h2 id="related">Related angel numbers</h2>
{related_table(n)}
      <p>Seeing a different number? Try the <a href="/angel-number-calculator/">angel number calculator</a> for any number, browse <a href="/angel-numbers/">all angel numbers</a>, or find the numbers in your birth date with the <a href="/numerology-calculator/">numerology calculator</a>.</p>"""
    p = {
        "path": f"/angel-numbers/{n}/",
        "crumb": f"{n} meaning",
        "title": title,
        "h1": h1,
        "description": d["desc"],
        "lede": d["lede"],
        "published": PUBLISHED_ON,
        "parents": [("Angel numbers", "/angel-numbers/")],
        "badges": ["Free", "No sign-up", "Nothing saved or sent"],
    }
    art_ld = {"@type": "Article", "headline": h1, "description": d["desc"], "url": f"https://369journal.app{p['path']}",
              "datePublished": PUBLISHED_ON, "dateModified": PUBLISHED_ON,
              "author": {"@type": "Person", "name": "Tejas Rane", "url": "https://369journal.app/about/"},
              "publisher": {"@type": "Organization", "name": "369 Journal"},
              "mainEntityOfPage": f"https://369journal.app{p['path']}"}
    nxt = next_steps(
        "From a sign to a daily practice",
        f"Noticing {n} is a moment. Writing your intention every day is what builds something. Here are two calm ways to keep going.",
        "369", f"web_angel_{n}",
        "Write your intention 3, 6 and 9 times a day",
        "369 Journal reminds you morning, afternoon and night (at most three times a day) and counts every line. Your first 21-day cycle is free.",
        f"site-angel-{n}")
    return tool_page(p, d["faq"], tool_body(n), js="angel-pages.js", css="angel-pages.css",
                     extra_ld=[art_ld], article=article, next_html=nxt)


HUB_FAQ = [
    ("What are angel numbers?", "Angel numbers are repeating or patterned numbers, such as 111, 444 or 1212, that some people notice again and again and read as meaningful. The idea comes from numerology and modern spiritual communities."),
    ("Are angel numbers real?", "There is no scientific evidence that numbers carry messages. Our brains are very good at noticing patterns, especially ones connected to what we are already thinking about. Many people still find angel numbers useful as a prompt to pause and reflect."),
    ("Why do I keep seeing the same number?", "Once a number catches your attention you notice it more often, which is called frequency illusion. Some numbers, like 11:11 or 12:34, are also times many people look at on a clock."),
    ("Which angel number is the most common?", "In searches, 444 is the most popular, followed by 555, 222 and 333. 1111 is the best known for making a wish."),
    ("What if my number is not listed?", "Use the angel number calculator. It gives a written meaning for popular numbers and builds a reading from the digits for any other number."),
    ("How is 369 different from other angel numbers?", "369 is also a daily writing method: you write one intention 3 times in the morning, 6 in the afternoon and 9 at night. See the 369 method for the steps."),
]


def hub_page():
    cards = "".join(
        f'<a class="hub-tool" href="/angel-numbers/{n}/"><strong>{n}</strong><span>{esc(N[n]["hub"])}</span>'
        f'<span class="hub-meta">{esc(" · ".join(N[n]["words"]))}</span></a>' for n in ORDER)
    p = {
        "path": "/angel-numbers/",
        "crumb": "Angel numbers",
        "title": "Angel Numbers: Meanings of 111 to 1212 | 369 Journal",
        "h1": "Angel Numbers: What 111 to 1212 Mean",
        "description": "Angel number meanings for 111, 222, 333, 444, 555, 777, 999, 1010, 1111, 1212 and 369: love, money and spirituality, with a free tool on every page.",
        "lede": "Pick the number you keep seeing. Each page has a free tool for what you were thinking about, plus an honest, calm meaning for love, money and spirituality.",
        "published": PUBLISHED_ON,
    }
    assert len(p["title"]) <= 60 and 140 <= len(p["description"]) <= 160, len(p["description"])
    url = "https://369journal.app/angel-numbers/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": p["h1"], "url": url, "description": p["description"],
         "datePublished": PUBLISHED_ON,
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": f"{n} angel number meaning",
              "url": f"https://369journal.app/angel-numbers/{n}/"} for i, n in enumerate(ORDER)]}},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in HUB_FAQ]},
        crumbs(p)]}
    faq_html = "\n".join(f"      <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in HUB_FAQ)
    nxt = next_steps(
        "From a sign to a daily practice",
        "Noticing a number is a moment. Writing your intention every day is a practice. Here are two calm ways to keep going.",
        "369", "web_angel_hub",
        "Write your intention 3, 6 and 9 times a day",
        "369 Journal reminds you morning, afternoon and night (at most three times a day) and counts every line. Your first 21-day cycle is free.",
        "site-angel-hub")
    assets = ('  <link rel="stylesheet" href="/assets/tools.css?v=%s">\n  <link rel="stylesheet" href="/assets/tools/angel-pages.css?v=%s">\n' % (ASSET_V, ASSET_V))
    return head(p, ld).replace("</head>", assets + "</head>") + f"""
  <main data-tool="angel-numbers">
    <div class="tool-head">
      <div class="wrap">
        <h1>{p['h1']}</h1>
        <p>{p['lede']}</p>
        <ul class="tool-badges"><li>Eleven numbers</li><li>Free tool on every page</li><li>No predictions, no hype</li></ul>
      </div>
    </div>

    <section class="hub" aria-label="Angel numbers">
      <div class="hub-grid">{cards}</div>
    </section>

    <div class="hub ap-cta">
      <div>
        <h2>Seeing a different number?</h2>
        <p>The angel number calculator gives a meaning for any number, and a birthday number too.</p>
      </div>
      <a class="btn" href="/angel-number-calculator/">Open the angel number calculator</a>
    </div>

{nxt}

    <article class="narrow prose">
      <h2 id="real">Are angel numbers real?</h2>
      <p>Honestly: there is no scientific evidence that numbers carry messages from anyone. People notice patterns, especially in things they already have on their mind, and numbers are everywhere. That is why 11:11 or 444 seem to follow you once you start looking.</p>
      <p>That does not make angel numbers worthless. Many people use them the way you might use a bell that rings on the hour: a small cue to stop, breathe and ask yourself what you want. If that helps, it is a perfectly good use. We treat meanings as <em>commonly associated with</em>, never as predictions, and we would suggest you do too.</p>
      <p>Want to turn a moment into a habit? The <a href="/369-method/">369 method</a> is a simple daily practice: write one line 3, 6 and 9 times a day. You can also find the numbers in your birth date with the <a href="/numerology-calculator/">numerology calculator</a>.</p>

      <h2 id="faq">Questions</h2>
{faq_html}

      <h2>More free tools</h2>
      {more_tools('/angel-numbers/')}
    </article>
  </main>

  {footer()}
</body>
</html>
"""


if __name__ == "__main__":
    for n in ORDER:
        write(f"/angel-numbers/{n}/", number_page(n))
    write("/angel-numbers/", hub_page())

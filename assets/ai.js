/* "Personalise it for me": one shared AI panel for the free tools (Claude Haiku 5.5 via our API).
   The panel is opt-in. The free tool on each page works without it.
   Markup: <section class="ai" data-ai="MODE" [data-number] [data-area] [data-kind] [data-book]>, injected by layout.py.
   Everything the API returns is plain text and is placed with textContent (never innerHTML). */
(function () {
  "use strict";
  var root = document.querySelector("[data-ai]");
  if (!root) return;

  var LOCAL = /^(localhost|127\.0\.0\.1)$/.test(location.hostname);
  var API = LOCAL ? "http://localhost:8370/api/web-ai" : "https://369-journal-api.vercel.app/api/web-ai";
  var TURNSTILE_SITE_KEY = ""; // Cloudflare Turnstile site key. Leave empty until the keys are created.
  var APP = "https://apps.apple.com/app/apple-store/id6770804298?pt=128923117&ct=site-ai-{m}&mt=8";
  var BOOK = "https://369-journal-api.vercel.app/api/book?b={b}&f=paperback&src=web_ai_{m}";
  var HISTORY_KEY = "369ai.history";
  var mode = root.getAttribute("data-ai");

  function track(name, props) { try { if (window.posthog) window.posthog.capture(name, props || {}); } catch (e) {} }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function store(get, val) {
    try {
      if (get) return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
      localStorage.setItem(HISTORY_KEY, JSON.stringify(val));
    } catch (e) { return []; }
  }

  // ------------------------------------------------------------ numerology (same convention as the site's calculators)
  function digits(n) { return String(n).split("").reduce(function (a, d) { return a + Number(d); }, 0); }
  function reduce(n, keepMaster) { while (n > 9 && !(keepMaster && (n === 11 || n === 22 || n === 33))) n = digits(n); return n; }
  function lifePath(y, m, d) { return reduce(reduce(m, true) + reduce(d, true) + reduce(digits(y), true), true); }
  function personalYear(m, d, year) { return reduce(reduce(m) + reduce(d) + reduce(digits(year))); }
  var CHART = {}; "AJS BKT CLU DMV ENW FOX GPY HQZ IR".split(" ").forEach(function (g, i) { g.split("").forEach(function (c) { CHART[c] = i + 1; }); });
  function nameNums(name) {
    var letters = String(name || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toUpperCase().replace(/[^A-Z]/g, "");
    if (!letters) return {};
    var all = 0, vow = 0;
    letters.split("").forEach(function (c) { all += CHART[c]; if ("AEIOU".indexOf(c) > -1) vow += CHART[c]; });
    return { expression: String(reduce(all, true)), soulUrge: vow ? String(reduce(vow, true)) : "" };
  }

  // ------------------------------------------------------------ per-mode form + result layout
  var M = {
    affirm: {
      title: "Write affirmations just for me",
      lede: "Tell us what's going on in a sentence or two. You'll get five affirmations written for your situation, plus one small step for today.",
      fields: [{ name: "situation", label: "What's going on, or what do you want?", type: "textarea", max: 300, ph: "e.g. I moved to a new city and want to feel at home and make real friends" }],
      button: "Write my affirmations",
      card: function (r) { return r.affirmations[r.pick] || r.affirmations[0]; },
    },
    angel: {
      title: "What does it mean for me?",
      lede: "Say what was on your mind when you saw it. You'll get a short, honest reflection for your situation, a question and an affirmation.",
      fields: [
        { name: "number", label: "The number you keep seeing", type: "number", max: 6, ph: "e.g. 444", fixed: "number" },
        { name: "context", label: "What were you thinking about or going through?", type: "textarea", max: 300, ph: "e.g. I saw it right after I applied for a new job" },
      ],
      button: "Read it for me",
      card: function (r) { return r.affirmation; },
    },
    numerology: {
      title: "My personal 2027 reading",
      lede: "We work out your numbers in your browser and send only the numbers (and your first name, if you add it). You'll get a reading that weaves them together for 2027.",
      fields: [
        { name: "dob", label: "Date of birth", type: "date" },
        { name: "name", label: "Full birth name", hint: "optional, for name numbers", type: "text", max: 80, ph: "e.g. Maria Lopez" },
        { name: "focus", label: "What do you want 2027 to be about?", hint: "optional", type: "textarea", max: 200, ph: "e.g. a calmer job and more time for my health" },
      ],
      button: "Write my 2027 reading",
      card: function (r) { return r.affirmation; },
    },
    resolution: {
      title: "Make my resolution stick",
      lede: "Write your goal the way you'd say it out loud. You'll get a clear version, a two-minute daily habit, a weekly action and a plan for the days it gets hard.",
      fields: [{ name: "goal", label: "Your resolution or goal", type: "textarea", max: 300, ph: "e.g. get fit, stop scrolling at night, save more" }],
      button: "Make it stick",
      card: function (r) { return r.clearGoal; },
    },
    scripting: {
      title: "Write my first script",
      lede: "Tell us what you'd like to manifest. You'll get a short first-draft script of one ordinary moment after it came true, ready for you to edit and make your own.",
      fields: [
        { name: "desire", label: "What would you like to script?", type: "textarea", max: 300, ph: "e.g. working from my own little studio by the sea" },
        { name: "detail", label: "Any details to include?", hint: "optional", type: "text", max: 200, ph: "e.g. my dog, morning light, a calm inbox" },
      ],
      button: "Write my script",
      card: function (r) { return r.affirmation; },
    },
    letter: {
      title: "Help me start my letter",
      lede: "Blank pages are hard. Tell us a little and we'll write an opening in your voice, plus three questions to keep you going.",
      fields: [
        { name: "now", label: "Your life right now, in a line", type: "textarea", max: 300, ph: "e.g. final year of uni, nervous about what comes next" },
        { name: "hopes", label: "What you hope for", type: "textarea", max: 300, ph: "e.g. a job I like, my own place, being kinder to myself" },
        { name: "timeframe", label: "Opens in", type: "select", options: ["6 months", "1 year", "3 years"], value: "1 year" },
      ],
      button: "Write my opening",
      card: function (r) { return r.opening.split(". ").slice(0, 2).join(". ") + "."; },
    },
  };
  var cfg = M[mode];
  if (!cfg) return;

  // ------------------------------------------------------------ build the panel
  var fixedNumber = root.getAttribute("data-number");
  var form = el("form", "ai-form");
  form.noValidate = true;
  cfg.fields.forEach(function (f) {
    if (f.fixed === "number" && fixedNumber) return;
    var id = "ai-" + f.name;
    var label = el("label", "t-label", f.label);
    label.htmlFor = id;
    if (f.hint) { var h = el("span", null, " (" + f.hint + ")"); label.appendChild(h); }
    var input;
    if (f.type === "textarea") { input = el("textarea", "t-textarea ai-textarea"); input.rows = 3; }
    else if (f.type === "select") {
      input = el("select", "t-select");
      f.options.forEach(function (o) { var op = el("option", null, o); op.value = o; if (o === f.value) op.selected = true; input.appendChild(op); });
    } else {
      input = el("input", "t-input");
      input.type = f.type === "number" ? "text" : f.type;
      if (f.type === "number") { input.inputMode = "numeric"; input.pattern = "[0-9]*"; }
      if (f.type === "date") { input.min = "1900-01-01"; input.max = new Date().toISOString().slice(0, 10); }
    }
    input.id = id; input.name = f.name;
    if (f.max) input.maxLength = f.max;
    if (f.ph) input.placeholder = f.ph;
    var wrap = el("div", "ai-field");
    wrap.appendChild(label); wrap.appendChild(input);
    form.appendChild(wrap);
  });
  var tsBox = el("div", "ai-turnstile");
  form.appendChild(tsBox);
  var submit = el("button", "btn ai-go", cfg.button);
  submit.type = "submit";
  var actions = el("div", "ai-actions");
  actions.appendChild(submit);
  var left = el("span", "ai-left");
  actions.appendChild(left);
  form.appendChild(actions);

  var head = el("div", "ai-head");
  var spark = el("span", "ai-spark", "✦");
  spark.setAttribute("aria-hidden", "true");
  head.appendChild(spark);
  var h2 = el("h2", null, cfg.title);
  h2.id = "ai-title";
  head.appendChild(h2);
  root.setAttribute("aria-labelledby", "ai-title");
  var lede = el("p", "ai-lede", cfg.lede);
  var note = el("p", "ai-note", "Free, up to 5 a day. What you type is sent to our server and to Anthropic’s Claude to write your result, and isn’t stored. AI can get things wrong; take what helps.");
  var status = el("p", "ai-status");
  status.setAttribute("role", "status");
  status.setAttribute("aria-live", "polite");
  var out = el("div", "ai-out");
  out.hidden = true;
  out.setAttribute("aria-live", "polite");
  var recent = el("div", "ai-recent");

  var inner = el("div", "ai-inner");
  [head, lede, form, note, status, out, recent].forEach(function (n) { inner.appendChild(n); });
  root.appendChild(inner);

  // ------------------------------------------------------------ Turnstile (optional bot check)
  var tsToken = "", tsWidget = null;
  function loadTurnstile() {
    if (!TURNSTILE_SITE_KEY || window.turnstile) return renderTurnstile();
    var s = document.createElement("script");
    s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
    s.async = true; s.onload = renderTurnstile;
    document.head.appendChild(s);
  }
  function renderTurnstile() {
    if (!TURNSTILE_SITE_KEY || !window.turnstile || tsWidget !== null) return;
    tsWidget = window.turnstile.render(tsBox, { sitekey: TURNSTILE_SITE_KEY, size: "flexible", appearance: "interaction-only",
      callback: function (t) { tsToken = t; }, "expired-callback": function () { tsToken = ""; } });
  }
  if (TURNSTILE_SITE_KEY) {
    var io = "IntersectionObserver" in window ? new IntersectionObserver(function (e) { if (e[0].isIntersecting) { loadTurnstile(); io.disconnect(); } }) : null;
    if (io) io.observe(root); else loadTurnstile();
  }

  // ------------------------------------------------------------ collect input
  function val(name) { var n = form.elements[name]; return n ? n.value.trim() : ""; }
  function collect() {
    if (mode === "numerology") {
      var dob = val("dob");
      var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(dob);
      if (!m) return { error: "Add your date of birth first." };
      var y = +m[1], mo = +m[2], d = +m[3];
      var nn = nameNums(val("name"));
      return { input: { lifePath: String(lifePath(y, mo, d)), personalYear: String(personalYear(mo, d, 2027)), expression: nn.expression || "", soulUrge: nn.soulUrge || "", firstName: val("name").split(/\s+/)[0] || "", focus: val("focus") } };
    }
    var input = {};
    cfg.fields.forEach(function (f) { if (!(f.fixed === "number" && fixedNumber)) input[f.name] = val(f.name); });
    if (mode === "angel") { input.number = (fixedNumber || input.number || "").replace(/\D/g, ""); if (!input.number) return { error: "Type the number you keep seeing." }; }
    if (mode === "affirm") { input.area = root.getAttribute("data-area") || "any"; if (input.situation.length < 3) return { error: "Tell us a little about what's going on." }; }
    if (mode === "resolution") { input.kind = root.getAttribute("data-kind") || "resolution"; if (input.goal.length < 3) return { error: "Write your goal in a few words." }; }
    if (mode === "scripting" && input.desire.length < 3) return { error: "Write what you'd like to script in a few words." };
    if (mode === "letter" && (input.now + input.hopes).length < 5) return { error: "Write a line about your life now or what you hope for." };
    return { input: input };
  }

  // ------------------------------------------------------------ submit
  var busy = false;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    var c = collect();
    if (c.error) { status.textContent = c.error; status.className = "ai-status warn"; return; }
    if (TURNSTILE_SITE_KEY && !tsToken) { loadTurnstile(); status.textContent = "One quick check, then tap again."; status.className = "ai-status warn"; return; }
    busy = true; submit.disabled = true; submit.classList.add("is-busy");
    status.textContent = "Writing yours…"; status.className = "ai-status";
    track("website ai requested", { mode: mode });
    fetch(API, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ mode: mode, input: c.input, turnstileToken: tsToken || undefined }) })
      .then(function (res) { return res.json().catch(function () { return {}; }).then(function (b) { return { ok: res.ok, status: res.status, body: b }; }); })
      .then(function (r) {
        if (!r.ok || !r.body.result) {
          status.textContent = (r.body && r.body.error) || "Something went wrong. Please try again.";
          status.className = "ai-status warn";
          track("website ai blocked", { mode: mode, code: (r.body && r.body.code) || r.status });
          return;
        }
        status.textContent = ""; status.className = "ai-status";
        if (typeof r.body.remainingToday === "number") left.textContent = r.body.remainingToday + " left today";
        show(r.body.result, true);
        track("website ai generated", { mode: mode, care: !!r.body.result.care });
      })
      .catch(function () { status.textContent = "Couldn't reach us. Check your connection and try again."; status.className = "ai-status warn"; })
      .then(function () {
        busy = false; submit.disabled = false; submit.classList.remove("is-busy");
        if (tsWidget !== null && window.turnstile) { window.turnstile.reset(tsWidget); tsToken = ""; }
      });
  });

  // ------------------------------------------------------------ render a result
  function section(label, text) { var s = el("div", "ai-sec"); s.appendChild(el("p", "ai-k", label)); s.appendChild(el("p", "ai-v", text)); return s; }
  function list(label, items, ordered) {
    var s = el("div", "ai-sec"); s.appendChild(el("p", "ai-k", label));
    var l = el(ordered ? "ol" : "ul", "ai-list"); items.forEach(function (t) { l.appendChild(el("li", null, t)); }); s.appendChild(l); return s;
  }
  function careBox() {
    var b = el("div", "ai-care");
    b.appendChild(el("p", null, "It sounds like things are heavy right now. You don’t have to work through this alone. If you might be in danger, please call your local emergency number. In the US you can call or text 988, in the UK call Samaritans on 116 123, or find a helpline near you at findahelpline.com."));
    return b;
  }

  function show(r, fresh) {
    out.innerHTML = "";
    out.hidden = false;
    var card = el("article", "ai-card");
    if (r.care) card.appendChild(careBox());
    if (mode === "affirm") {
      if (r.intro) card.appendChild(el("p", "ai-intro", r.intro));
      var ul = el("ul", "ai-affs");
      r.affirmations.forEach(function (a, i) {
        var li = el("li", i === r.pick ? "is-pick" : "");
        var b = el("button", "ai-aff", a); b.type = "button";
        b.addEventListener("click", function () { copy(a, "Copied"); });
        li.appendChild(b);
        if (i === r.pick) li.appendChild(el("span", "ai-tag", "Best for 369"));
        ul.appendChild(li);
      });
      card.appendChild(ul);
      if (r.tinyAction) card.appendChild(section("One small step today", r.tinyAction));
    } else if (mode === "angel") {
      card.appendChild(el("h3", "ai-h", r.headline));
      card.appendChild(el("p", "ai-v", r.reading));
      card.appendChild(section("A question for you", r.question));
      card.appendChild(section("An affirmation to try", r.affirmation));
      card.appendChild(section("One small step", r.tinyAction));
    } else if (mode === "numerology") {
      card.appendChild(el("h3", "ai-h", r.headline));
      card.appendChild(el("p", "ai-v", r.overview));
      if (r.strengths.length) card.appendChild(list("Your strengths", r.strengths));
      card.appendChild(section("Worth watching", r.watchFor));
      card.appendChild(section("Your 2027", r.year2027));
      card.appendChild(section("Your 2027 affirmation", r.affirmation));
      card.appendChild(section("A question for you", r.question));
    } else if (mode === "resolution") {
      card.appendChild(el("h3", "ai-h", r.clearGoal));
      card.appendChild(section("Why it matters", r.why));
      card.appendChild(section("Your affirmation", r.affirmation));
      card.appendChild(section("Every day (two minutes)", r.dailyTiny));
      card.appendChild(section("Every week", r.weeklyAction));
      if (r.ifThen.length) card.appendChild(list("When it gets hard", r.ifThen));
      card.appendChild(section("How you'll know it's working", r.measure));
    } else if (mode === "scripting") {
      card.appendChild(el("h3", "ai-h", r.title));
      var ta = el("textarea", "t-textarea ai-edit"); ta.value = r.script; ta.rows = 9; ta.setAttribute("aria-label", "Your script, edit it freely");
      card.appendChild(ta);
      card.appendChild(section("Affirmation from your script", r.affirmation));
      card.appendChild(section("One step this week", r.nextStep));
    } else if (mode === "letter") {
      var t2 = el("textarea", "t-textarea ai-edit"); t2.value = r.opening.replace(/^Dear future me,\s*/i, "Dear future me,\n\n") + " "; t2.rows = 10; t2.setAttribute("aria-label", "Your letter, keep writing");
      card.appendChild(t2);
      if (r.prompts.length) card.appendChild(list("Questions to keep writing", r.prompts));
    }
    out.appendChild(card);
    out.appendChild(tools(r));
    out.appendChild(nextStep());
    if (fresh) {
      save(r);
      out.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    }
  }

  function plainText(r) {
    var edit = out.querySelector(".ai-edit");
    var lines = [];
    Object.keys(r).forEach(function (k) {
      if (k === "care" || k === "pick") return;
      var v = r[k];
      if ((k === "script" || k === "opening") && edit) v = edit.value;
      lines.push(Array.isArray(v) ? v.map(function (x) { return "- " + x; }).join("\n") : v);
    });
    return lines.join("\n\n") + "\n\nMade at 369journal.app";
  }

  function tools(r) {
    var row = el("div", "ai-tools");
    var b1 = el("button", "btn ai-share", "Save as image"); b1.type = "button";
    b1.addEventListener("click", function () { shareImage(r); });
    var b2 = el("button", "btn ghost", "Copy text"); b2.type = "button";
    b2.addEventListener("click", function () { copy(plainText(r), "Copied"); track("website ai copied", { mode: mode }); });
    var b3 = el("button", "btn ghost", "Try again"); b3.type = "button";
    b3.addEventListener("click", function () { form.querySelector("textarea, input").focus(); });
    row.appendChild(b1); row.appendChild(b2); row.appendChild(b3);
    return row;
  }

  function nextStep() {
    var box = el("div", "ai-next");
    var book = root.getAttribute("data-book") || "369";
    var text = {
      affirm: "Pick one and write it 3 times in the morning, 6 in the afternoon and 9 at night. 369 Journal reminds you and counts every line.",
      angel: "A number is a moment. Writing your intention daily is a practice. 369 Journal helps you write it 3, 6 and 9 times a day.",
      numerology: "Turn your 2027 theme into a daily habit: write your affirmation 3, 6 and 9 times a day with 369 Journal.",
      resolution: "Write your affirmation daily for 21 days. 369 Journal's first 21-day cycle is free, with gentle reminders.",
      scripting: "Read your script each morning and write its affirmation through the day. 369 Journal keeps the habit going.",
      letter: "While you wait for your letter to open, write one intention daily. 369 Journal reminds you morning, afternoon and night.",
    }[mode];
    box.appendChild(el("p", null, text));
    var links = el("div", "ai-next-links");
    var a = el("a", "btn", "Get 369 Journal free"); a.href = APP.replace("{m}", mode); a.setAttribute("data-cta", "ai-" + mode);
    var bk = el("a", "btn ghost", book === "scripting" ? "Scripting Manifestation book" : "The 369 Method book");
    bk.href = BOOK.replace("{b}", book).replace("{m}", mode); bk.setAttribute("data-book", book + "-paperback");
    links.appendChild(a); links.appendChild(bk);
    box.appendChild(links);
    return box;
  }

  // ------------------------------------------------------------ share card (canvas, 1080 x 1350)
  function wrapLines(ctx, text, maxW) {
    var words = String(text).split(/\s+/), lines = [], line = "";
    words.forEach(function (w) { var t = line ? line + " " + w : w; if (ctx.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t; });
    if (line) lines.push(line);
    return lines;
  }
  function shareImage(r) {
    var W = 1080, H = 1350, c = document.createElement("canvas"); c.width = W; c.height = H;
    var x = c.getContext("2d");
    var g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#faf6f0"); g.addColorStop(1, "#f0e2d0");
    x.fillStyle = g; x.fillRect(0, 0, W, H);
    x.strokeStyle = "rgba(176,89,51,0.35)"; x.lineWidth = 3; x.strokeRect(54, 54, W - 108, H - 108);
    var serif = '"New York", "Iowan Old Style", Georgia, serif', sans = "-apple-system, system-ui, sans-serif";
    x.fillStyle = "#b05933"; x.font = "600 30px " + sans; x.textAlign = "center";
    x.fillText({ affirm: "MY AFFIRMATION", angel: (fixedNumber || val("number")) + " · FOR ME", numerology: "MY 2027", resolution: "MY 2027 RESOLUTION", scripting: "MY SCRIPT", letter: "DEAR FUTURE ME" }[mode], W / 2, 190);
    var main = cfg.card(r) || "";
    var size = main.length > 120 ? 54 : main.length > 70 ? 64 : 76;
    x.fillStyle = "#1c1814"; x.font = "500 " + size + "px " + serif;
    var lines = wrapLines(x, main, W - 240).slice(0, 9), lh = size * 1.3, y = H / 2 - (lines.length * lh) / 2 + size * 0.4;
    lines.forEach(function (l, i) { x.fillText(l, W / 2, y + i * lh); });
    x.fillStyle = "#6e6052"; x.font = "400 30px " + sans;
    x.fillText("Write it 3, 6 and 9 times a day", W / 2, H - 210);
    x.fillStyle = "#1c1814"; x.font = "600 36px " + sans;
    x.fillText("369journal.app", W / 2, H - 150);
    c.toBlob(function (blob) {
      if (!blob) return;
      var file = new File([blob], "369-journal-" + mode + ".png", { type: "image/png" });
      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        navigator.share({ files: [file], title: "369 Journal", text: "Made at 369journal.app" }).catch(function () {});
        track("website ai shared", { mode: mode, via: "share" });
      } else {
        var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = file.name;
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
        track("website ai shared", { mode: mode, via: "download" });
      }
    }, "image/png");
  }

  function copy(text, msg) {
    var done = function () { status.textContent = msg; status.className = "ai-status ok"; setTimeout(function () { if (status.textContent === msg) status.textContent = ""; }, 1800); };
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, done); else done();
  }

  // ------------------------------------------------------------ recent results (this browser only)
  function save(r) {
    var h = store(true).filter(function (x) { return x && x.r; });
    h.unshift({ m: mode, p: location.pathname, t: Date.now(), r: r });
    store(false, h.slice(0, 12));
    renderRecent();
  }
  function renderRecent() {
    recent.innerHTML = "";
    var mine = store(true).filter(function (x) { return x && x.m === mode && x.r; }).slice(0, 4);
    if (!mine.length) return;
    recent.appendChild(el("p", "ai-k", "Your recent results (saved only in this browser)"));
    var row = el("div", "ai-recent-row");
    mine.forEach(function (x) {
      var b = el("button", "ai-chip", new Date(x.t).toLocaleDateString(undefined, { day: "numeric", month: "short" }) + " · " + (cfg.card(x.r) || "").slice(0, 38) + "…");
      b.type = "button";
      b.addEventListener("click", function () { show(x.r, false); });
      row.appendChild(b);
    });
    var clear = el("button", "ai-chip ghost", "Clear"); clear.type = "button";
    clear.addEventListener("click", function () { store(false, store(true).filter(function (x) { return x.m !== mode; })); renderRecent(); });
    row.appendChild(clear);
    recent.appendChild(row);
  }
  renderRecent();
})();

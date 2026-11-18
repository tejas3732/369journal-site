/* Word of the Year finder. Runs entirely in the browser.
   Analytics never include anything the visitor types (custom words stay local). */
(function () {
  "use strict";
  var root = document.querySelector("[data-woty]");
  if (!root) return;
  function $(s) { return root.querySelector(s); }
  function $$(s) { return Array.prototype.slice.call(root.querySelectorAll(s)); }
  function track(name, props) { try { if (window.posthog) window.posthog.capture(name, props || {}); } catch (e) {} }

  var YEAR = 2027;

  // word: [meaning, affirmation, one small daily action, journal prompt]
  var WORDS = {
    slow: ["A year of doing fewer things, more fully.", "I move at the pace that lets me feel my life.", "Leave five minutes between plans.", "What would I stop rushing if nothing bad happened?"],
    rest: ["A year where rest is part of the plan, not a reward.", "I rest before I'm empty.", "Put one empty evening in your calendar each week.", "What does real rest look like for me?"],
    present: ["A year of being where your feet are.", "I am here, and here is enough.", "Eat one meal a day without your phone.", "When did I last feel fully present?"],
    begin: ["A year for starting the thing you keep postponing.", "I begin before I feel ready.", "Spend ten minutes on it today, badly.", "What have I been waiting for permission to start?"],
    brave: ["A year of small acts of courage.", "I do the thing while I'm still a little scared.", "Do one slightly uncomfortable thing each day.", "Where is fear making my choices for me?"],
    momentum: ["A year of small steps that add up.", "Every small step counts, and I keep stepping.", "Never skip twice in a row.", "What tiny action would keep me moving today?"],
    heal: ["A year to recover, mend and come back to yourself.", "I give myself time to heal.", "Do one kind thing for your body or mind each day.", "What part of me needs care right now?"],
    gentle: ["A year of speaking to yourself kindly.", "I am gentle with myself, and I still grow.", "Notice one harsh thought a day and soften it.", "How would I talk to a friend in my place?"],
    light: ["A year of carrying less: fewer worries, less stuff, more joy.", "I let my life feel lighter.", "Let go of one thing you don't need each week.", "What am I carrying that isn't mine to carry?"],
    expand: ["A year of growing past your old limits.", "There is room for more good in my life.", "Say yes to one new idea or invitation a week.", "Where have I been thinking too small?"],
    abundance: ["A year of noticing and welcoming enough, and more.", "Good things flow to me and through me.", "Write down three things you already have plenty of.", "What would feel abundant to me this year?"],
    rise: ["A year of stepping up into your next level.", "I rise to meet the life I want.", "Do one thing your future self would be proud of.", "What does the next level of me do differently?"],
    peace: ["A year of protecting your calm.", "My peace comes first.", "Take three slow breaths before you reply to anything stressful.", "What steals my peace, and what restores it?"],
    ease: ["A year where things don't have to be hard to be worth it.", "I allow things to be easy.", "Ask each morning: what would make today easier?", "Where am I making things harder than they need to be?"],
    steady: ["A year of showing up, again and again.", "I am steady, and steady wins.", "Pick one daily habit and keep it small enough to never miss.", "What would I build if I just kept going?"],
    build: ["A year of laying bricks for the life you want.", "I am building something that lasts.", "Spend 20 focused minutes on your one big project each day.", "What am I building, and why does it matter to me?"],
    open: ["A year of letting people and chances in.", "I am open to love, help and new chances.", "Say yes to one invitation you'd usually decline.", "What would I let in if I wasn't afraid?"],
    together: ["A year of connection: friends, family, love.", "I make time for the people I love.", "Message one person you miss each week.", "Who do I want closer to me this year?"],
    bold: ["A year of asking for more and taking up space.", "I ask boldly and I take up space.", "Make one bold ask each month.", "What would I do if I weren't worried what people think?"],
    focus: ["A year of fewer goals and full attention.", "My attention goes where my heart is.", "Write tomorrow's one most important task tonight.", "What's the one thing that would change everything?"],
    trust: ["A year of trusting yourself and the timing of your life.", "I trust myself to handle what comes.", "When you can't decide, choose and move on.", "Where do I need to trust myself more?"],
    release: ["A year of letting go of what no longer fits.", "I release what I've outgrown.", "Write one thing down that you're done carrying, then cross it out.", "What am I ready to let go of?"],
    simple: ["A year of cutting the clutter: plans, things, noise.", "I keep my life simple and clear.", "Remove one thing from your to-do list every day.", "What would a simpler version of my life look like?"],
    worthy: ["A year of believing you deserve good things.", "I am worthy of the life I want.", "Accept every compliment with a simple thank you.", "Where do I act as if I don't deserve more?"],
    voice: ["A year of saying what you really think and want.", "My voice matters and I use it.", "Share one honest opinion a day.", "What have I not been saying out loud?"],
    enough: ["A year of knowing you are enough and you have enough.", "I am enough, and I have enough.", "End each day by naming one thing that was enough.", "What would change if I believed I was already enough?"],
    devoted: ["A year of committing fully to what matters.", "I am devoted to the life I'm creating.", "Keep one promise to yourself every day.", "What am I ready to fully commit to?"],
    savor: ["A year of enjoying the good moments while they happen.", "I slow down and savor the good.", "Pause for ten seconds whenever something feels good.", "What small joy did I almost miss today?"],
    strong: ["A year of building strength in body and mind.", "I am getting stronger every day.", "Move your body for ten minutes, every day.", "Where do I want to feel stronger?"],
    create: ["A year of making things: art, work, ideas, a life.", "I am a creator, and I make things real.", "Make something small every day, even if no one sees it.", "What do I want to bring into the world?"],
    explore: ["A year of new places, ideas and experiences.", "I explore with an open heart.", "Try one new thing each week, however small.", "Where do I want to go, inside or out?"],
    free: ["A year of more freedom: with your time, money or choices.", "I choose freedom in small ways every day.", "Protect one hour a day that belongs only to you.", "What would freedom look like for me this year?"],
    curious: ["A year of asking questions instead of judging.", "I meet life with curiosity.", "When something annoys you, ask: what's interesting about this?", "What do I want to learn this year?"],
    home: ["A year of feeling at home, in your space and in yourself.", "I create a home I love coming back to.", "Make one small improvement to your space each week.", "What makes a place feel like home to me?"],
    bloom: ["A year of growing into who you're becoming.", "I am blooming in my own time.", "Notice one way you've grown each week.", "What is quietly growing in me right now?"],
    grateful: ["A year of noticing what's already good.", "I notice the good, and more good finds me.", "Write three good things before bed.", "What am I grateful for that I usually overlook?"]
  };

  // Each answer gives points to three words (3, 2, 1).
  var QUESTIONS = [
    { q: "How did " + (YEAR - 1) + " feel, mostly?", a: [
      ["Rushed and busy", ["slow", "present", "rest"]],
      ["Stuck, or on hold", ["begin", "momentum", "brave"]],
      ["Heavy or hard", ["heal", "gentle", "light"]],
      ["Good, and I want more", ["expand", "rise", "abundance"]]] },
    { q: "What do you want more of in " + YEAR + "?", a: [
      ["Calm", ["peace", "ease", "simple"]],
      ["Money and security", ["abundance", "build", "steady"]],
      ["Love and connection", ["open", "together", "grateful"]],
      ["Growth and success", ["rise", "focus", "bold"]]] },
    { q: "What usually gets in your way?", a: [
      ["Overthinking", ["trust", "release", "simple"]],
      ["Doubting myself", ["worthy", "brave", "voice"]],
      ["Saying yes to everything", ["enough", "focus", "free"]],
      ["Starting but not finishing", ["devoted", "steady", "momentum"]]] },
    { q: "Which morning sounds best?", a: [
      ["Slow coffee and quiet", ["savor", "present", "peace"]],
      ["A walk, a run or a workout", ["strong", "steady", "light"]],
      ["Straight into work I love", ["create", "build", "focus"]],
      ["Waking up somewhere new", ["explore", "free", "curious"]]] },
    { q: "On 31 December " + YEAR + ", you want to feel…", a: [
      ["Proud", ["devoted", "rise", "bold"]],
      ["Peaceful", ["peace", "home", "ease"]],
      ["Free", ["free", "light", "release"]],
      ["Grateful", ["grateful", "bloom", "abundance"]]] }
  ];

  var THEMES = {
    paper: { bg: ["#fbf6ee", "#efe2d0"], ink: "#1c1814", soft: "#6f5f50", accent: "#b05933" },
    midnight: { bg: ["#1b1a24", "#0f0e14"], ink: "#f6efe4", soft: "#b9ad9c", accent: "#d9b46a" },
    clay: { bg: ["#c46a43", "#8f4426"], ink: "#fff8f0", soft: "#f6dccb", accent: "#fff3e6" },
    sage: { bg: ["#e9eee3", "#cfdac6"], ink: "#22301f", soft: "#5d6b57", accent: "#4f6b47" }
  };
  var SIZES = { phone: [1179, 2556, "Phone wallpaper, 1179 × 2556"], square: [2160, 2160, "Square, for posts and printing"] };

  var state = { step: 0, answers: [], word: null, alts: [], custom: false, theme: "paper", size: "phone" };

  // ---------- Quiz ----------
  var quiz = $("[data-quiz]"), result = $("[data-result]");
  var qText = $("[data-q-text]"), qOpts = $("[data-q-opts]"), qCount = $("[data-q-count]"), qBar = $("[data-q-bar]"), back = $("[data-back]");

  function showQuestion(i, focus) {
    state.step = i;
    var Q = QUESTIONS[i];
    qText.textContent = Q.q;
    qCount.textContent = "Question " + (i + 1) + " of " + QUESTIONS.length;
    qBar.style.width = ((i) / QUESTIONS.length * 100) + "%";
    back.hidden = i === 0;
    qOpts.innerHTML = "";
    Q.a.forEach(function (opt, k) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "woty-opt"; b.textContent = opt[0];
      if (state.answers[i] === k) b.setAttribute("aria-pressed", "true");
      b.addEventListener("click", function () { choose(k); });
      qOpts.appendChild(b);
    });
    quiz.classList.remove("swap"); void quiz.offsetWidth; quiz.classList.add("swap");
    if (focus) qText.focus();
  }

  function choose(k) {
    state.answers[state.step] = k;
    if (state.step < QUESTIONS.length - 1) showQuestion(state.step + 1, true);
    else finish();
  }

  back.addEventListener("click", function () { if (state.step > 0) showQuestion(state.step - 1, true); });

  function score() {
    var pts = {};
    state.answers.forEach(function (k, i) {
      QUESTIONS[i].a[k][1].forEach(function (w, r) { pts[w] = (pts[w] || 0) + (3 - r); });
    });
    // Ties broken randomly so retakes can surface a different close match.
    return Object.keys(pts).map(function (w) { return [w, pts[w] + Math.random() * 0.5]; })
      .sort(function (a, b) { return b[1] - a[1]; }).map(function (x) { return x[0]; });
  }

  function finish() {
    var ranked = score();
    setWord(ranked[0], ranked.slice(1, 4), false);
    quiz.hidden = true; result.hidden = false;
    $("[data-r-word]").focus();
    track("website word of the year found", { word: ranked[0] });
  }

  // ---------- Result ----------
  function cap(w) { return w.charAt(0).toUpperCase() + w.slice(1); }

  function setWord(word, alts, custom) {
    state.word = word; state.custom = custom;
    if (alts) state.alts = alts;
    var d = WORDS[word.toLowerCase()];
    $("[data-r-word]").textContent = cap(word);
    $("[data-r-meaning]").textContent = d ? d[0] : "A word you chose for yourself. Let it guide one small choice a day.";
    $("[data-r-aff]").textContent = d ? d[1] : "In " + YEAR + ", I let " + word.toLowerCase() + " guide my choices.";
    $("[data-r-action]").textContent = d ? d[2] : "Each morning, ask: what would " + word.toLowerCase() + " look like today?";
    $("[data-r-prompt]").textContent = d ? d[3] : "What does " + word.toLowerCase() + " mean to me, in one sentence?";
    var altWrap = $("[data-r-alts]");
    altWrap.innerHTML = "";
    state.alts.filter(function (w) { return w !== word; }).slice(0, 3).forEach(function (w) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "woty-alt"; b.textContent = cap(w);
      b.addEventListener("click", function () {
        var prev = state.word;
        state.alts = state.alts.map(function (x) { return x === w ? prev : x; });
        setWord(w, null, false);
        track("website word of the year switched", { word: w });
      });
      altWrap.appendChild(b);
    });
    $("[data-alts-wrap]").hidden = !altWrap.children.length;
    try { history.replaceState(null, "", custom ? location.pathname : "#w=" + word); } catch (e) {}
    render();
  }

  $("[data-retake]").addEventListener("click", function () {
    state.answers = []; result.hidden = true; quiz.hidden = false; showQuestion(0, true);
    try { history.replaceState(null, "", location.pathname); } catch (e) {}
  });

  var own = $("#woty-own");
  $("[data-own-form]").addEventListener("submit", function (e) {
    e.preventDefault();
    var w = (own.value || "").trim().replace(/\s+/g, " ").slice(0, 18);
    if (!w) { own.focus(); return; }
    var known = WORDS[w.toLowerCase()] ? w.toLowerCase() : null;
    setWord(known || w, null, !known);
    if (result.hidden) { quiz.hidden = true; result.hidden = false; }
    toast("Your card now says " + cap(w));
    track("website word of the year custom", { known: !!known });
  });

  // ---------- Card (canvas) ----------
  var canvas = $("#woty-canvas"), ctx = canvas.getContext("2d");
  var css = getComputedStyle(document.documentElement);
  var SERIF = css.getPropertyValue("--serif").trim() || "Georgia, serif";
  var SANS = css.getPropertyValue("--sans").trim() || "system-ui, sans-serif";

  function fit(text, weight, family, maxW, start) {
    var px = start;
    do { ctx.font = weight + " " + px + "px " + family; px -= 4; } while (ctx.measureText(text).width > maxW && px > 40);
    return px + 4;
  }

  function wrap(text, maxW) {
    var words = text.split(" "), lines = [], line = "";
    words.forEach(function (w) {
      var t = line ? line + " " + w : w;
      if (ctx.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t;
    });
    if (line) lines.push(line);
    return lines;
  }

  function render() {
    var S = SIZES[state.size], W = S[0], H = S[1], T = THEMES[state.theme];
    canvas.width = W; canvas.height = H;
    var g = ctx.createLinearGradient(0, 0, W * 0.4, H);
    g.addColorStop(0, T.bg[0]); g.addColorStop(1, T.bg[1]);
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    if ("letterSpacing" in ctx) ctx.letterSpacing = "0px";
    ctx.textAlign = "center"; ctx.textBaseline = "alphabetic";

    var phone = state.size === "phone";
    var cx = W / 2, cy = phone ? H * 0.56 : H * 0.5, maxW = W * 0.8;
    var word = cap(state.word || "Your word");

    // Year label
    var yl = Math.round(W * (phone ? 0.034 : 0.026));
    ctx.fillStyle = T.accent; ctx.font = "600 " + yl + "px " + SANS;
    if ("letterSpacing" in ctx) ctx.letterSpacing = Math.round(yl * 0.32) + "px";
    ctx.fillText("MY WORD FOR " + YEAR, cx + Math.round(yl * 0.16), cy - W * (phone ? 0.21 : 0.17));
    if ("letterSpacing" in ctx) ctx.letterSpacing = "0px";

    // The word
    var px = fit(word, "600", SERIF, maxW, Math.round(W * (phone ? 0.2 : 0.17)));
    ctx.font = "600 " + px + "px " + SERIF; ctx.fillStyle = T.ink;
    ctx.fillText(word, cx, cy);

    // Rule + affirmation
    ctx.fillStyle = T.accent;
    ctx.fillRect(cx - W * 0.04, cy + px * 0.32, W * 0.08, Math.max(3, W * 0.003));
    var aff = $("[data-r-aff]").textContent;
    var ap = Math.round(W * (phone ? 0.042 : 0.032));
    ctx.font = "400 " + ap + "px " + SERIF; ctx.fillStyle = T.soft;
    wrap(aff, W * 0.72).forEach(function (l, i) { ctx.fillText(l, cx, cy + px * 0.32 + ap * 2.1 + i * ap * 1.4); });

    if ($("#woty-mark").checked) {
      var mp = Math.round(W * 0.022);
      ctx.font = "500 " + mp + "px " + SANS; ctx.fillStyle = T.soft; ctx.globalAlpha = 0.75;
      ctx.fillText("369journal.app", cx, H - (phone ? H * 0.12 : mp * 2.6));
      ctx.globalAlpha = 1;
    }
    $("[data-size-label]").textContent = S[2];
    root.classList.toggle("is-phone", phone);
  }

  root.addEventListener("change", function (e) {
    var t = e.target;
    if (t.name === "woty-theme") state.theme = t.value;
    else if (t.name === "woty-size") state.size = t.value;
    render();
  });

  // ---------- Save, share, copy ----------
  var toastEl = document.querySelector("[data-toast]"), toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toastTimer); toastTimer = setTimeout(function () { toastEl.classList.remove("show"); }, 2200);
  }
  function fileName() { return "word-of-the-year-" + YEAR + ".png"; }
  function getBlob(cb) { render(); canvas.toBlob(function (b) { cb(b); }, "image/png"); }

  $("#woty-download").addEventListener("click", function () {
    getBlob(function (blob) {
      if (!blob) return;
      var url = URL.createObjectURL(blob), a = document.createElement("a");
      a.href = url; a.download = fileName();
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
      toast("Image downloaded");
      track("website word of the year saved", { size: state.size, theme: state.theme, method: "download", custom: state.custom });
    });
  });

  var shareBtn = $("#woty-share");
  try {
    var probe = new File([new Blob(["x"], { type: "image/png" })], "p.png", { type: "image/png" });
    if (navigator.canShare && navigator.canShare({ files: [probe] })) {
      shareBtn.hidden = false;
      if (!/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)) shareBtn.textContent = "Share";
    }
  } catch (e) {}
  shareBtn.addEventListener("click", function () {
    getBlob(function (blob) {
      if (!blob) return;
      navigator.share({ files: [new File([blob], fileName(), { type: "image/png" })] }).then(function () {
        track("website word of the year saved", { size: state.size, theme: state.theme, method: "share", custom: state.custom });
      }).catch(function () {});
    });
  });

  $("[data-copy]").addEventListener("click", function () {
    var text = "My word for " + YEAR + ": " + cap(state.word) + "\n" + $("[data-r-aff]").textContent;
    var done = function () { toast("Copied"); };
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () { toast("Couldn't copy. Select the text instead."); });
    else toast("Couldn't copy on this browser.");
  });

  // ---------- Browse all words ----------
  var grid = $("[data-all]");
  Object.keys(WORDS).sort().forEach(function (w) {
    var b = document.createElement("button");
    b.type = "button"; b.className = "woty-chip"; b.textContent = cap(w);
    b.addEventListener("click", function () {
      setWord(w, null, false);
      if (result.hidden) { quiz.hidden = true; result.hidden = false; }
      result.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
      track("website word of the year browsed", { word: w });
    });
    grid.appendChild(b);
  });

  // ---------- Start ----------
  var m = /#w=([a-z]+)/.exec(location.hash);
  if (m && WORDS[m[1]]) {
    setWord(m[1], [], false); quiz.hidden = true; result.hidden = false;
  } else { showQuestion(0, false); render(); }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(render);
})();

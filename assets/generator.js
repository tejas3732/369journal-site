/* Free affirmation generator + personalised 369 sheet.
   Runs entirely in the browser: nothing the visitor types is sent anywhere.
   Analytics records only the area, whether a detail was added, and sheet length. */
(function () {
  "use strict";
  var root = document.querySelector("[data-generator]");
  if (!root) return;

  var track = function (name, props) {
    try { if (window.posthog) window.posthog.capture(name, props || {}); } catch (e) {}
  };

  // {d} = the visitor's optional detail. Templates with {d} are used only when a detail is given.
  var AREAS = {
    money: {
      label: "Money", hint: "e.g. $5,000 in savings", guide: ["/369-method/money/", "The 369 method for money"],
      generic: [
        "Money comes to me easily and often.",
        "I am so grateful for the steady money that flows into my life.",
        "I handle money calmly and wisely, and it grows.",
        "I am worthy of financial security, and I have it.",
        "I earn well doing work that matters to me.",
        "Every day I make choices that grow my savings.",
        "I feel safe and relaxed when I check my bank account."
      ],
      detail: [
        "I am so grateful that I now have {d}.",
        "{D} is mine, and it arrived with ease.",
        "I am calm and proud now that I have {d}."
      ]
    },
    career: {
      label: "Career", hint: "e.g. my new role as a designer", guide: ["/369-method/examples/", "50 369 method examples"],
      generic: [
        "I am thriving in work that I enjoy.",
        "My work is valued, and I am paid well for it.",
        "Opportunities find me, and I am ready for them.",
        "I speak up with confidence, and people listen.",
        "I am growing into the best version of myself at work.",
        "I finish what I start, and it shows.",
        "I am proud of the work I do every day."
      ],
      detail: [
        "I am so happy and grateful now that I have {d}.",
        "I am thriving in {d}.",
        "{D} feels natural to me, because it is mine."
      ]
    },
    love: {
      label: "Love", hint: "e.g. a kind, loving partner", guide: ["/369-method/love/", "The 369 method for love"],
      generic: [
        "I give and receive love easily.",
        "I am loved, valued and safe in my relationships.",
        "My heart is open, and love comes to me naturally.",
        "I attract people who treat me with kindness.",
        "I am worthy of a deep and lasting love.",
        "My relationship is calm, honest and full of joy.",
        "I feel chosen, cherished and at home with the one I love."
      ],
      detail: [
        "I am so grateful for {d} in my life.",
        "I share my days with {d}, and it feels easy.",
        "{D} is part of my life, and I feel at peace."
      ]
    },
    selflove: {
      label: "Self-love", hint: "e.g. my body", guide: ["/369-method/love/", "The 369 method for love"],
      generic: [
        "I am enough exactly as I am.",
        "I treat myself with the kindness I give others.",
        "I trust myself and the choices I make.",
        "I am proud of how far I have come.",
        "I speak to myself gently, every day.",
        "I deserve rest, joy and good things.",
        "I keep the promises I make to myself."
      ],
      detail: [
        "I love and appreciate {d}.",
        "I am kind and patient with {d}.",
        "I am grateful for {d}, just as it is."
      ]
    },
    health: {
      label: "Health", hint: "e.g. running 5 km", guide: ["/369-method/examples/", "50 369 method examples"],
      generic: [
        "My body is strong, healthy and full of energy.",
        "I sleep deeply and wake up refreshed.",
        "I move my body in ways I enjoy, and I feel strong.",
        "I choose foods that make me feel good.",
        "Every day my body heals and grows stronger.",
        "I feel calm, light and healthy in my body.",
        "I take care of my health with ease and joy."
      ],
      detail: [
        "I am so proud that I can now do {d}.",
        "{D} feels easy and natural to me.",
        "I am grateful for my strong body and for {d}."
      ]
    },
    home: {
      label: "Home", hint: "e.g. my own flat by the sea", guide: ["/369-method/examples/", "50 369 method examples"],
      generic: [
        "My home is peaceful, and I love coming back to it.",
        "I live in a home that feels safe, bright and mine.",
        "I am so grateful for the perfect home I live in.",
        "My home is full of light, calm and good people.",
        "I wake up every morning happy in my own home."
      ],
      detail: [
        "I am so grateful that I now live in {d}.",
        "{D} is my home, and it feels just right.",
        "I unlock the door to {d} and smile every time."
      ]
    },
    calm: {
      label: "Calm", hint: "e.g. stressful mornings", guide: ["/369-method/examples/", "50 369 method examples"],
      generic: [
        "I am calm, clear and in control of my day.",
        "I breathe slowly, and my mind settles.",
        "I let go of what I cannot control.",
        "Peace is my natural state.",
        "I handle whatever today brings with a steady mind.",
        "My thoughts are kind, quiet and clear."
      ],
      detail: [
        "I stay calm and steady through {d}.",
        "I meet {d} with a clear and peaceful mind.",
        "{D} no longer shakes me. I feel at ease."
      ]
    },
    newyear: {
      label: "New Year 2027", hint: "e.g. my first book published", guide: ["/new-year-manifestation-challenge/", "The 21-day New Year challenge"],
      generic: [
        "2027 is the year I keep the promises I make to myself.",
        "2027 is calm, abundant and full of good surprises.",
        "This year I grow in ways that make me proud.",
        "2027 brings me the peace and progress I am ready for.",
        "I step into 2027 confident, clear and ready."
      ],
      detail: [
        "2027 is the year of {d}, and I am so grateful.",
        "I am celebrating {d} in 2027.",
        "{D} happens for me in 2027, step by step."
      ]
    }
  };

  var $ = function (sel) { return root.querySelector(sel); };
  var areaInputs = root.querySelectorAll("input[name=area]");
  var detailInput = $("#gen-detail");
  var list = $("#gen-results");
  var resultsBox = $("#gen-output");
  var guideLink = $("#gen-guide");
  var ownInput = $("#gen-own");
  var checks = $("#gen-checks");
  var copyNudge = $("#gen-copy-nudge");
  var sheetBox = $("#gen-sheet");
  var lastShown = [];

  function currentArea() {
    for (var i = 0; i < areaInputs.length; i++) if (areaInputs[i].checked) return areaInputs[i].value;
    return "money";
  }

  function clean(detail) {
    return detail.trim().replace(/\s+/g, " ").replace(/[.!?]+$/, "").slice(0, 60);
  }

  function fill(t, d) {
    var cap = d.charAt(0).toUpperCase() + d.slice(1);
    return t.replace("{D}", cap).replace("{d}", d);
  }

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var x = a[i]; a[i] = a[j]; a[j] = x; }
    return a;
  }

  function generate() {
    var key = currentArea();
    var area = AREAS[key];
    var d = clean(detailInput.value);
    var pool = d ? area.detail.map(function (t) { return fill(t, d); }) : [];
    var generic = shuffle(area.generic.filter(function (g) { return lastShown.indexOf(g) === -1; }).slice());
    if (generic.length < 3) generic = shuffle(area.generic.slice());
    var picks = d ? shuffle(pool).slice(0, 2).concat(generic.slice(0, 2)) : generic.slice(0, 4);
    lastShown = picks;
    render(picks);
    guideLink.href = area.guide[0];
    guideLink.textContent = area.guide[1];
    resultsBox.hidden = false;
    track("website generator used", { area: key, has_detail: !!d });
  }

  function render(picks) {
    list.innerHTML = "";
    picks.forEach(function (text) {
      var li = document.createElement("li");
      var p = document.createElement("p");
      p.className = "aff";
      p.textContent = text;
      var actions = document.createElement("div");
      actions.className = "aff-actions";
      var copy = button("Copy", "ghost small", function () { copyText(text, copy); });
      var use = button("Make my 369 sheet", "small", function () { useForSheet(text); });
      actions.appendChild(copy);
      actions.appendChild(use);
      li.appendChild(p);
      li.appendChild(actions);
      list.appendChild(li);
    });
  }

  function button(label, cls, onClick) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "btn " + cls;
    b.textContent = label;
    b.addEventListener("click", onClick);
    return b;
  }

  function copyText(text, btn) {
    var done = function () {
      var old = btn.textContent;
      btn.textContent = "Copied";
      setTimeout(function () { btn.textContent = old; }, 1600);
      copyNudge.hidden = false;
      track("website generator copied", { area: currentArea() });
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, done);
    } else {
      var ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch (e) {}
      ta.remove(); done();
    }
  }

  // ---------- Wording checker for the visitor's own affirmation ----------
  var RULES = [
    { id: "tense", test: function (s) { return !/\b(will|going to|someday|one day|hope to|i want|i wish|soon)\b/i.test(s); },
      ok: "Written as if it is already true", fix: "Try the present tense: “I am” or “I have”, not “I will” or “I want”" },
    { id: "positive", test: function (s) { return !/\b(not|no|don'?t|never|won'?t|can'?t|stop|without|less)\b/i.test(s); },
      ok: "Says what you want", fix: "Say what you want, not what you want to avoid" },
    { id: "short", test: function (s) { var n = s.trim().split(/\s+/).filter(Boolean).length; return n >= 3 && n <= 20; },
      ok: "Short enough to write 18 times a day", fix: "Aim for 3 to 20 words, one line" },
    { id: "you", test: function (s) { return /^(i|i'm|i’m|my|2027|this year|every)\b/i.test(s.trim()); },
      ok: "Starts with you", fix: "Starting with “I” or “My” keeps it about you" }
  ];

  function checkOwn() {
    var s = ownInput.value;
    checks.innerHTML = "";
    if (!s.trim()) { checks.hidden = true; return; }
    checks.hidden = false;
    RULES.forEach(function (r) {
      var pass = r.test(s);
      var li = document.createElement("li");
      li.className = pass ? "pass" : "fix";
      li.textContent = pass ? r.ok : r.fix;
      checks.appendChild(li);
    });
  }

  // ---------- Personalised printable sheet ----------
  var sheetAff = $("#sheet-aff");
  var sheetDays = $("#sheet-days");
  var sheetStart = $("#sheet-start");
  var sheetBody = $("#sheet-body");
  var sheetTitle = $("#sheet-title");

  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }

  function circles(n) { var s = ""; for (var i = 0; i < n; i++) s += '<span class="b"></span>'; return s; }

  function buildSheet() {
    var days = parseInt(sheetDays.value, 10) || 33;
    var start = sheetStart.value ? new Date(sheetStart.value + "T12:00:00") : null;
    var fmt = new Intl.DateTimeFormat(undefined, { day: "numeric", month: "short" });
    var rows = "";
    for (var i = 0; i < days; i++) {
      var date = "";
      if (start) { var d = new Date(start); d.setDate(start.getDate() + i); date = fmt.format(d); }
      rows += '<tr><th scope="row">' + (i + 1) + '</th><td class="date">' + date + "</td><td>" + circles(3) + "</td><td>" + circles(6) + "</td><td>" + circles(9) + "</td></tr>";
    }
    sheetBody.innerHTML = rows;
    sheetTitle.textContent = "My 369 sheet: " + days + " days";
    $("#sheet-print-aff").textContent = sheetAff.value.trim() || " ";
  }

  function useForSheet(text) {
    sheetAff.value = text;
    sheetBox.hidden = false;
    buildSheet();
    track("website generator sheet made", { area: currentArea(), days: parseInt(sheetDays.value, 10) });
    sheetBox.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
  }

  // ---------- Wire up ----------
  $("#gen-go").addEventListener("click", generate);
  $("#gen-more").addEventListener("click", generate);
  detailInput.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); generate(); } });
  Array.prototype.forEach.call(areaInputs, function (r) {
    r.addEventListener("change", function () { detailInput.placeholder = AREAS[r.value].hint; lastShown = []; if (!resultsBox.hidden) generate(); });
  });
  ownInput.addEventListener("input", checkOwn);
  $("#gen-own-use").addEventListener("click", function () { if (ownInput.value.trim()) useForSheet(ownInput.value.trim()); else ownInput.focus(); });
  $("#gen-own-copy").addEventListener("click", function (e) { if (ownInput.value.trim()) copyText(ownInput.value.trim(), e.currentTarget); });
  sheetAff.addEventListener("input", buildSheet);
  sheetDays.addEventListener("change", buildSheet);
  sheetStart.addEventListener("change", buildSheet);
  $("#sheet-print").addEventListener("click", function () {
    buildSheet();
    track("website generator printed", { days: parseInt(sheetDays.value, 10), has_dates: !!sheetStart.value });
    window.print();
  });

  sheetStart.value = iso(new Date());
  detailInput.placeholder = AREAS[currentArea()].hint;
})();

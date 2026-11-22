/* Numerology pages: personal year, name numerology and life path (with compatibility).
   One file, three modes, chosen by data-nup on the tool shell. Runs in the browser only; meanings
   come from the page (#nup-data). Analytics: result numbers only. Never a name, never a date.
   Nothing the visitor types is written to the URL, stored or sent. */
(function () {
  "use strict";
  var root = document.querySelector("[data-nup]");
  var dataEl = document.getElementById("nup-data");
  if (!root || !dataEl) return;
  var MODE = root.getAttribute("data-nup");
  var DATA = JSON.parse(dataEl.textContent);
  var form = root.querySelector("[data-form]");
  var card = root.querySelector("[data-result]");
  var toastEl = document.querySelector("[data-toast]");
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var MASTER = { "11": 1, "22": 1, "33": 1 };
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  var DIM = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  var lastCopy = "";

  function track(name, props) { try { if (window.posthog) window.posthog.capture(name, props || {}); } catch (e) {} }
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toast.t);
    toast.t = setTimeout(function () { toastEl.classList.remove("show"); }, 1800);
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function digitSum(str) { return String(str).split("").reduce(function (a, d) { return a + Number(d); }, 0); }

  // Reduce to 1-9. keepMaster keeps 11, 22 and 33. steps read like "1 + 9 + 9 + 0 = 19".
  function reduce(n, keepMaster) {
    var cur = String(n), steps = [], passed = "";
    while (cur.length > 1 && !(keepMaster && MASTER[cur])) {
      var s = digitSum(cur);
      steps.push(cur.split("").join(" + ") + " = " + s);
      cur = String(s);
      if (MASTER[cur] && cur.length > 1) passed = cur;
    }
    return { value: cur, steps: steps, passed: passed };
  }
  function chain(r, start) { return r.steps.length ? r.steps.join(", then ") : String(start) + " stays " + r.value; }
  function words(list) { return '<ul class="nu-words">' + list.map(function (w) { return "<li>" + esc(w) + "</li>"; }).join("") + "</ul>"; }
  function mathBox(title, lines) { return '<div class="nu-math"><p class="nu-k">' + esc(title) + "</p><p>" + lines.map(esc).join("<br>") + "</p></div>"; }
  function honest() {
    return '<p class="nu-honest">There is no scientific evidence that numbers predict personality or the future. These are the meanings numerologists traditionally associate with each number. Take what feels true, leave the rest, and use it as a prompt for reflection.</p>';
  }
  function actions(extra) {
    return '<div class="nu-actions print-hide"><button type="button" class="btn small" data-copy="result">Copy result</button>' + (extra || "") + "</div>";
  }
  function show(html, opts) {
    card.innerHTML = '<div class="nu-result">' + html + "</div>";
    if (!reduceMotion) { card.classList.remove("nu-in"); void card.offsetWidth; card.classList.add("nu-in"); }
    if (!(opts && opts.noScroll) && window.innerWidth < 900) card.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
  }
  function copyText(text, msg) {
    var done = function () { toast(msg); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, done);
    else { var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); } catch (x) {} ta.remove(); done(); }
  }

  function parseDate(v) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v || "");
    if (!m) return null;
    var y = +m[1], mo = +m[2], d = +m[3];
    var t = new Date(Date.UTC(y, mo - 1, d));
    if (y < 1900 || y > 2100 || t.getUTCFullYear() !== y || t.getUTCMonth() !== mo - 1 || t.getUTCDate() !== d) return null;
    return { y: y, m: mo, d: d };
  }
  function partLine(label, n, r) {
    return label + " " + n + ": " + (r.steps.length ? chain(r, n) : n + (MASTER[r.value] && r.value === String(n) ? " (master number, kept)" : ""));
  }
  function lifePath(dt) {
    var rm = reduce(dt.m, true), rd = reduce(dt.d, true), ry = reduce(dt.y, true);
    var sum = +rm.value + +rd.value + +ry.value;
    var rt = reduce(sum, true);
    return {
      value: rt.value,
      lines: [
        partLine("Month", dt.m, rm), partLine("Day", dt.d, rd), partLine("Year", dt.y, ry),
        "Add them: " + rm.value + " + " + rd.value + " + " + ry.value + " = " + sum + (rt.steps.length ? ", then " + rt.steps.join(", then ") : (MASTER[rt.value] ? " (master number, kept)" : ""))
      ]
    };
  }

  var esel = function (id) { return document.getElementById(id); };

  /* ---------------- personal year ---------------- */
  function personalYear(m, d, year) {
    var rm = reduce(m, false), rd = reduce(d, false), ry = reduce(year, false);
    var sum = +rm.value + +rd.value + +ry.value;
    var rt = reduce(sum, false);
    return {
      value: rt.value, sum: sum,
      masterTotal: MASTER[String(sum)] ? String(sum) : "",
      masterYear: ry.passed,
      lines: [
        "Birth month: " + MONTHS[m - 1] + " = " + m + (rm.steps.length ? ", so " + rm.steps.join(", then ") : ""),
        "Birth day: " + d + (rd.steps.length ? ", so " + rd.steps.join(", then ") : " stays " + rd.value),
        "The year " + year + ": " + chain(ry, year),
        "Add them: " + rm.value + " + " + rd.value + " + " + ry.value + " = " + sum + (rt.steps.length ? ", then " + rt.steps.join(", then ") : "")
      ]
    };
  }
  function pyState() {
    var mSel = esel("nup-month"), dSel = esel("nup-day");
    var m = +mSel.value, d = +dSel.value;
    if (!m) { mSel.focus(); toast("Choose your birth month"); return null; }
    if (!d) { dSel.focus(); toast("Choose your birth day"); return null; }
    if (d > DIM[m - 1]) { dSel.focus(); toast(MONTHS[m - 1] + " has no day " + d); return null; }
    var y = form.querySelector('input[name="nup-year"]:checked');
    return { m: m, d: d, year: y ? +y.value : 2027 };
  }
  function renderPY(opts) {
    var s = pyState();
    if (!s) return;
    var py = personalYear(s.m, s.d, s.year), t = DATA.py[py.value];
    var notes = "";
    if (py.masterYear) notes += '<p class="nu-soft">The digits of ' + s.year + " add up to " + py.masterYear + ", a master number. We reduce it to " + reduce(s.year, false).value + " for personal years, which is the usual method.</p>";
    if (py.masterTotal) notes += '<p class="nu-soft">Your total passes through ' + py.masterTotal + ", a master number. Some numerologists read this year as a more intense " + py.value + ". We show the single-digit year.</p>";
    var strip = '<ol class="nup-strip">';
    var ex = "";
    for (var i = 1; i <= 12; i++) {
      var pm = reduce(+py.value + i, false);
      if (i === 1) ex = "January: " + py.value + " + 1 = " + (+py.value + 1) + (pm.steps.length ? ", then " + pm.steps.join(", then ") : "") + ".";
      strip += '<li><span class="nup-mo">' + MONTHS[i - 1].slice(0, 3) + '</span><span class="nup-n" aria-label="' + MONTHS[i - 1] + ", personal month " + pm.value + '">' + pm.value + '</span><span class="nup-w">' + esc(DATA.pm[pm.value]) + "</span></li>";
    }
    strip += "</ol>";
    var html = '<section class="nu-sec nu-year nu-feature" aria-labelledby="nup-h"><p class="nu-k" id="nup-h">Your personal year for ' + s.year + "</p>" +
      '<div class="nu-yrow"><p class="nu-big nu-mid">' + py.value + '</p><p class="nu-theme">' + esc(t.theme) + "</p></div>" +
      '<p class="nu-text">' + esc(t.text) + "</p>" +
      '<p class="nu-do"><strong>One suggestion:</strong> ' + esc(t["do"]) + "</p>" +
      '<p class="nu-aff nu-aff-line"><span class="nu-k">Affirmation</span><span class="nu-serif">“' + esc(t.aff) + "”</span></p>" +
      mathBox("The maths, step by step", py.lines) + notes + "</section>" +
      '<section class="nu-sec" aria-labelledby="nup-hm"><p class="nu-k" id="nup-hm">Your personal month, January to December ' + s.year + "</p>" + strip +
      '<p class="nu-soft nu-tiny">Personal month = your personal year + the calendar month number, reduced to one digit. ' + esc(ex) + "</p></section>" +
      honest() + actions('<a class="btn ghost small" href="/new-year-manifestation-challenge/">Start the 21-day challenge</a>');
    lastCopy = "My personal year for " + s.year + " is " + py.value + " (" + t.theme.toLowerCase() + "). A prompt for reflection, not a prediction. Find yours: " + location.origin + location.pathname;
    show(html, opts);
    track("website personal year calculated", { personal_year: Number(py.value), year: s.year });
  }

  /* ---------------- name numerology ---------------- */
  var CHART = {};
  "AJS BKT CLU DMV ENW FOX GPY HQZ IR".split(" ").forEach(function (g, i) { g.split("").forEach(function (c) { CHART[c] = i + 1; }); });
  function isV(c) { return "AEIOU".indexOf(c) > -1; }
  function clean(raw) {
    var s = String(raw || "");
    try { s = s.normalize("NFD"); } catch (e) {}
    return s.replace(/[̀-ͯ]/g, "").toUpperCase();
  }
  function splitWords(raw) {
    return clean(raw).split(/[^A-Z]+/).filter(function (w) { return w.length; });
  }
  function tally(letters, filter) {
    var total = 0, used = 0, parts = [];
    for (var i = 0; i < letters.length; i++) { var c = letters[i]; if (filter(c)) { total += CHART[c]; used++; parts.push(CHART[c]); } }
    if (!used) return null;
    var r = reduce(total, true);
    return { value: r.value, total: total, parts: parts, steps: r.steps };
  }
  function nameNums(ws) {
    var all = ws.join("");
    return { expression: tally(all, function () { return true; }), soul: tally(all, isV), personality: tally(all, function (c) { return !isV(c); }) };
  }
  function howLine(r) { return r.parts.join(" + ") + " = " + r.total + (r.steps.length ? ", then " + r.steps.join(", then ") : (MASTER[r.value] ? " (master number, kept)" : "")); }
  function letterRows(ws) {
    var out = '<div class="nup-words">';
    ws.forEach(function (w) {
      out += '<ul class="nup-letters" aria-label="' + esc(w) + '">';
      w.split("").forEach(function (c) {
        out += '<li class="' + (isV(c) ? "nup-vowel" : "") + '" aria-label="' + c + ", value " + CHART[c] + (isV(c) ? ", vowel" : "") + '"><span class="nup-l">' + c + '</span><span class="nup-v">' + CHART[c] + "</span></li>";
      });
      out += "</ul>";
    });
    return out + '</div><p class="nu-soft nu-tiny">Shaded letters are vowels (A, E, I, O, U). Y counts as a consonant.</p>';
  }
  function nameBlock(title, ws, nn, idp) {
    var out = '<section class="nu-sec" aria-labelledby="' + idp + '"><p class="nu-k" id="' + idp + '">' + esc(title) + "</p>" + letterRows(ws) + '<div class="nu-names">';
    [["expression", "expression"], ["soul", "soul"], ["personality", "personality"]].forEach(function (pair) {
      var t = DATA.types[pair[0]], r = nn[pair[1]];
      if (!r) { out += '<article class="nu-name"><h3>' + esc(t.name) + '</h3><p class="nu-soft">This name has no letters to use for this one.</p></article>'; return; }
      var d = DATA.num[r.value];
      out += '<article class="nu-name"><div class="nu-name-top"><p class="nu-big nu-mid">' + r.value + "</p><h3>" + esc(t.name) + "</h3></div>" +
        '<p class="nu-soft">' + esc(t.how) + "</p>" + words(d.words) +
        '<p class="nu-text">' + esc(d.text) + "</p>" +
        '<p class="nu-soft nu-tiny">The maths: ' + esc(howLine(r)) + ".</p>" +
        '<p class="nu-soft"><strong>To reflect on:</strong> ' + esc(d.ask) + "</p></article>";
    });
    return out + "</div></section>";
  }
  function compareTable(a, b) {
    var rows = [["Expression", "expression"], ["Soul urge", "soul"], ["Personality", "personality"]].map(function (p) {
      var x = a[p[1]] ? a[p[1]].value : "-", y = b[p[1]] ? b[p[1]].value : "-";
      return "<tr><th scope=\"row\">" + p[0] + "</th><td>" + x + "</td><td>" + y + "</td><td>" + (x === y ? "Same" : "Different") + "</td></tr>";
    }).join("");
    return '<section class="nu-sec" aria-labelledby="nup-cmp"><p class="nu-k" id="nup-cmp">Birth name and current name side by side</p>' +
      '<div class="table-wrap"><table class="nup-table"><thead><tr><th scope="col">Number</th><th scope="col">Birth name</th><th scope="col">Current name</th><th scope="col">Result</th></tr></thead><tbody>' + rows + "</tbody></table></div>" +
      '<p class="nu-soft">Traditionally, the birth name is the main one. Many people read the current name as the way you present yourself now, and notice where the two agree.</p></section>';
  }
  function renderName(opts) {
    var b = esel("nup-name"), c = esel("nup-name2");
    var wb = splitWords(b.value);
    if (!wb.length) { b.focus(); toast("Type your full birth name"); return; }
    var wc = splitWords(c.value);
    var nb = nameNums(wb), nc = wc.length ? nameNums(wc) : null;
    var html = nameBlock(nc ? "Your birth name" : "Your name numbers", wb, nb, "nup-h-b");
    if (nc) html += compareTable(nb, nc) + nameBlock("Your current name", wc, nc, "nup-h-c");
    html += honest() + actions('<a class="btn ghost small" href="/life-path-number-calculator/">Find your life path number</a>');
    var bits = [];
    if (nb.expression) bits.push("expression " + nb.expression.value);
    if (nb.soul) bits.push("soul urge " + nb.soul.value);
    if (nb.personality) bits.push("personality " + nb.personality.value);
    lastCopy = "My name numbers: " + bits.join(", ") + ". A prompt for reflection, not a prediction. Find yours: " + location.origin + location.pathname;
    show(html, opts);
    track("website name numerology calculated", { expression: nb.expression ? Number(nb.expression.value) : null, soul: nb.soul ? Number(nb.soul.value) : null, personality: nb.personality ? Number(nb.personality.value) : null, has_current_name: !!nc });
  }

  /* ---------------- life path + compatibility ---------------- */
  function base(v) { return DATA.base[v] || v; }
  function compatKey(a, b) { var x = +base(a), y = +base(b); return Math.min(x, y) + "-" + Math.max(x, y); }
  function compatBlock(a, b) {
    var e = DATA.compat[compatKey(a, b)], lv = DATA.levels[e[0]];
    var masters = (base(a) !== a || base(b) !== b) ? '<p class="nu-soft nu-tiny">For pairings, master numbers are read as their single-digit form: 11 as 2, 22 as 4 and 33 as 6.</p>' : "";
    return '<section class="nu-sec" aria-labelledby="nup-h-c"><p class="nu-k" id="nup-h-c">Life path compatibility</p>' +
      '<div class="nup-pair"><div><p class="nu-k">You</p><p class="nu-big nu-mid">' + a + '</p></div><p class="nup-amp" aria-hidden="true">+</p><div><p class="nu-k">Them</p><p class="nu-big nu-mid">' + b + "</p></div></div>" +
      '<p class="nup-level nup-l-' + e[0] + '">' + esc(lv) + "</p>" +
      '<p class="nu-text">Numerologists traditionally say ' + esc(e[1]) + "</p>" + masters +
      '<p class="nu-soft">This is a conversation starter, not a verdict. Every pairing can work, and no number decides how a relationship goes.</p></section>';
  }
  function renderLP(opts) {
    var in1 = esel("nup-birth"), in2 = esel("nup-birth2");
    var dt = parseDate(in1.value);
    if (!dt) { in1.focus(); toast("Choose your date of birth"); return; }
    var dt2 = null;
    if (in2.value) {
      dt2 = parseDate(in2.value);
      if (!dt2) { in2.focus(); toast("That second date is not valid"); return; }
    }
    var lp = lifePath(dt), n = DATA.num[lp.value];
    var html = '<section class="nu-sec nu-hero" aria-labelledby="nup-h-lp"><p class="nu-k" id="nup-h-lp">Your life path number</p>' +
      '<p class="nu-big">' + lp.value + "</p>" + words(n.words) +
      '<p class="nu-text">' + esc(n.text) + "</p>" +
      '<div class="nup-two"><div class="nu-name"><p class="nu-k">Traditional strengths</p><p class="nu-soft">' + esc(n.words.join(", ").toLowerCase()) + ", and " + esc(n.short) + ".</p></div>" +
      '<div class="nu-name"><p class="nu-k">Worth watching</p><p class="nu-soft">' + esc(DATA.caution[lp.value]) + "</p></div></div>" +
      mathBox("How we got there", lp.lines) +
      '<div class="nu-ask"><p class="nu-k">A question to sit with</p><p class="nu-serif">' + esc(n.ask) + "</p></div>" +
      '<div class="nu-aff"><p class="nu-k">An affirmation to try</p><p class="nu-serif">“' + esc(n.aff) + "”</p></div></section>";
    var copy = "My life path number is " + lp.value + " (" + n.words.join(", ").toLowerCase() + ").";
    var props = { life_path: Number(lp.value), has_compat: !!dt2 };
    if (dt2) {
      var lp2 = lifePath(dt2);
      html += compatBlock(lp.value, lp2.value);
      copy += " Compatibility with a " + lp2.value + ": " + DATA.levels[DATA.compat[compatKey(lp.value, lp2.value)][0]].toLowerCase() + ".";
      props.partner_life_path = Number(lp2.value);
    }
    html += honest() + actions('<a class="btn ghost small" href="/personal-year-number-calculator/">See your 2027 personal year</a>');
    lastCopy = copy + " A prompt for reflection, not a prediction. Find yours: " + location.origin + location.pathname;
    show(html, opts);
    track("website life path calculated", props);
  }

  /* ---------------- wiring ---------------- */
  var render = { "personal-year": renderPY, "name": renderName, "life-path": renderLP }[MODE];
  if (!render) return;
  form.addEventListener("submit", function (e) { e.preventDefault(); render(); });
  if (MODE === "personal-year") {
    form.addEventListener("change", function (e) {
      if (e.target && e.target.name === "nup-year" && card.querySelector(".nu-result")) render({ noScroll: true });
    });
  }
  card.addEventListener("click", function (e) {
    if (e.target.closest("[data-copy]")) copyText(lastCopy, "Result copied");
  });
})();

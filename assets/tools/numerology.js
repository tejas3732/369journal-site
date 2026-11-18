/* Numerology calculator. Runs in the browser only; meanings come from the page (#numerology-data).
   Analytics: life path result and whether a name was used. Never the name, never the date.
   Neither the date nor the name is ever written to the URL, stored or sent. */
(function () {
  "use strict";
  var root = document.querySelector("[data-numerology]");
  var dataEl = document.getElementById("numerology-data");
  if (!root || !dataEl) return;
  var DATA = JSON.parse(dataEl.textContent);
  var form = root.querySelector("[data-form]");
  var card = root.querySelector("[data-result]");
  var birth = document.getElementById("nu-birth");
  var nameIn = document.getElementById("nu-name");
  var toastEl = document.querySelector("[data-toast]");
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var lastCopy = "";
  var MASTER = { "11": 1, "22": 1, "33": 1 };

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

  // Reduce a number to 1-9. keepMaster keeps 11, 22 and 33. Returns { value, steps[] } where each
  // step reads like "1 + 9 + 9 + 0 = 19".
  function reduce(n, keepMaster) {
    var cur = String(n), steps = [];
    while (cur.length > 1 && !(keepMaster && MASTER[cur])) {
      var s = digitSum(cur);
      steps.push(cur.split("").join(" + ") + " = " + s);
      cur = String(s);
    }
    return { value: cur, steps: steps };
  }
  function chain(r, start) { // "1990: 1 + 9 + 9 + 0 = 19, 1 + 9 = 10, 1 + 0 = 1"
    return r.steps.length ? r.steps.join(", then ") : String(start) + " stays " + r.value;
  }

  function parseDate(v) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v || "");
    if (!m) return null;
    var y = +m[1], mo = +m[2], d = +m[3];
    var t = new Date(Date.UTC(y, mo - 1, d));
    if (y < 1900 || y > 2100 || t.getUTCFullYear() !== y || t.getUTCMonth() !== mo - 1 || t.getUTCDate() !== d) return null;
    return { y: y, m: mo, d: d, iso: v };
  }

  function lifePath(dt) {
    var rm = reduce(dt.m, true), rd = reduce(dt.d, true), ry = reduce(dt.y, true);
    var sum = +rm.value + +rd.value + +ry.value;
    var rt = reduce(sum, true);
    var lines = [
      "Month " + dt.m + ": " + (dt.m < 10 || MASTER[dt.m] ? dt.m + (MASTER[dt.m] ? " (master number, kept)" : "") : chain(rm, dt.m)),
      "Day " + dt.d + ": " + (dt.d < 10 ? dt.d : chain(rd, dt.d) + (MASTER[rd.value] && rd.steps.length === 0 ? " (master number, kept)" : "")),
      "Year " + dt.y + ": " + chain(ry, dt.y),
      "Add them: " + rm.value + " + " + rd.value + " + " + ry.value + " = " + sum + (rt.steps.length ? ", then " + rt.steps.join(", then ") : "")
    ];
    return { value: rt.value, lines: lines };
  }

  function personalYear(dt, year) {
    var rm = reduce(dt.m, false), rd = reduce(dt.d, false), ry = reduce(year, false);
    var sum = +rm.value + +rd.value + +ry.value;
    var rt = reduce(sum, false);
    var master = (MASTER[String(sum)]) ? String(sum) : "";
    return {
      value: rt.value, master: master,
      line: rm.value + " (month) + " + rd.value + " (day) + " + ry.value + " (" + year + ") = " + sum + (rt.steps.length ? ", then " + rt.steps.join(", then ") : "")
    };
  }

  // Pythagorean chart.
  var CHART = {};
  "AJS BKT CLU DMV ENW FOX GPY HQZ IR".split(" ").forEach(function (g, i) {
    g.split("").forEach(function (c) { CHART[c] = i + 1; });
  });
  function cleanName(raw) {
    var s = String(raw || "");
    try { s = s.normalize("NFD"); } catch (e) {}
    return s.replace(/[̀-ͯ]/g, "").toUpperCase().replace(/[^A-Z]/g, "");
  }
  function nameNumbers(letters) {
    function tally(filter) {
      var total = 0, used = 0;
      for (var i = 0; i < letters.length; i++) { var c = letters[i]; if (filter(c)) { total += CHART[c]; used++; } }
      if (!used) return null;
      var r = reduce(total, true);
      return { value: r.value, total: total, used: used, steps: r.steps };
    }
    var isV = function (c) { return "AEIOU".indexOf(c) > -1; };
    return {
      expression: tally(function () { return true; }),
      soul: tally(isV),
      personality: tally(function (c) { return !isV(c); })
    };
  }

  function words(list) { return '<ul class="nu-words">' + list.map(function (w) { return "<li>" + esc(w) + "</li>"; }).join("") + "</ul>"; }
  function mathBox(title, lines) {
    return '<div class="nu-math"><p class="nu-k">' + esc(title) + "</p><p>" + lines.map(esc).join("<br>") + "</p></div>";
  }

  function lifeCard(lp) {
    var n = DATA.num[lp.value];
    return '<section class="nu-sec nu-hero" aria-labelledby="nu-h-lp">' +
      '<p class="nu-k" id="nu-h-lp">Your life path number</p>' +
      '<p class="nu-big">' + lp.value + "</p>" +
      words(n.words) +
      '<p class="nu-text">' + esc(n.text) + "</p>" +
      mathBox("How we got there", lp.lines) +
      '<div class="nu-ask"><p class="nu-k">A question to sit with</p><p class="nu-serif">' + esc(n.ask) + "</p></div>" +
      '<div class="nu-aff"><p class="nu-k">An affirmation to try</p><p class="nu-serif">“' + esc(n.aff) + '”</p></div>' +
      "</section>";
  }

  function yearCard(py, year, feature) {
    var t = DATA.py[py.value];
    var note = py.master ? '<p class="nu-soft">Your total passes through ' + py.master + ", a master number. Some numerologists read this year as a more intense " + py.value + ". We show the single-digit year here.</p>" : "";
    return '<section class="nu-sec' + (feature ? " nu-year nu-feature" : " nu-year nu-past") + '" aria-labelledby="nu-h-' + year + '">' +
      '<p class="nu-k" id="nu-h-' + year + '">' + (feature ? "Your personal year for " + year + (feature === "next" ? " (the year ahead)" : "") : "Your personal year for " + year + " (this year)") + "</p>" +
      '<div class="nu-yrow"><p class="nu-big nu-mid">' + py.value + '</p><p class="nu-theme">' + esc(t.theme) + "</p></div>" +
      '<p class="nu-text">' + esc(t.text) + "</p>" +
      '<p class="nu-do"><strong>One suggestion:</strong> ' + esc(t["do"]) + "</p>" +
      '<p class="nu-aff nu-aff-line"><span class="nu-k">Affirmation</span><span class="nu-serif">“' + esc(t.aff) + "”</span></p>" +
      mathBox("The maths", [py.line]) + note +
      "</section>";
  }

  function nameCards(nn, hasName) {
    if (!hasName) {
      return '<section class="nu-sec nu-namepromo"><p class="nu-k">Name numbers</p><p class="nu-text">Add your full birth name to see your expression (destiny), soul urge and personality numbers.</p>' +
        '<button type="button" class="btn ghost small" data-focus-name>Add my name</button></section>';
    }
    var out = '<section class="nu-sec" aria-labelledby="nu-h-names"><p class="nu-k" id="nu-h-names">Your name numbers</p><div class="nu-names">';
    [["expression", "expression"], ["soul", "soul"], ["personality", "personality"]].forEach(function (pair) {
      var t = DATA.types[pair[0]], r = nn[pair[1]];
      if (!r) {
        out += '<article class="nu-name"><h3>' + esc(t.name) + '</h3><p class="nu-soft">Your name has no letters to use for this one.</p></article>';
        return;
      }
      var d = DATA.num[r.value];
      var how = r.total + (r.steps.length ? ", then " + r.steps.join(", then ") : "");
      out += '<article class="nu-name"><div class="nu-name-top"><p class="nu-big nu-mid">' + r.value + "</p><h3>" + esc(t.name) + "</h3></div>" +
        '<p class="nu-soft">' + esc(t.how) + "</p>" + words(d.words) +
        '<p class="nu-text">Traditionally linked with ' + esc(d.short) + ".</p>" +
        '<p class="nu-soft nu-tiny">Letter values add up to ' + esc(how) + ".</p></article>";
    });
    return out + "</div></section>";
  }

  function summary(dt, lp, pyN, pyC, nn) {
    var t = DATA.num[lp.value], parts = [];
    parts.push("My life path number is " + lp.value + " (" + t.words.join(", ").toLowerCase() + ").");
    parts.push("My personal year for 2027 is " + pyN.value + " (" + DATA.py[pyN.value].theme.toLowerCase() + ").");
    if (nn) {
      var bits = [];
      if (nn.expression) bits.push("expression " + nn.expression.value);
      if (nn.soul) bits.push("soul urge " + nn.soul.value);
      if (nn.personality) bits.push("personality " + nn.personality.value);
      if (bits.length) parts.push("Name numbers: " + bits.join(", ") + ".");
    }
    parts.push("A prompt for reflection, not a prediction. Find yours: " + location.origin + location.pathname);
    return parts.join("\n");
  }

  function calc(opts) {
    opts = opts || {};
    var dt = parseDate(birth.value);
    if (!dt) { if (!opts.silent) { birth.focus(); toast("Choose your date of birth"); } return; }
    var letters = cleanName(nameIn.value);
    var hasName = letters.length > 0;
    var nn = hasName ? nameNumbers(letters) : null;
    var lp = lifePath(dt);
    var py27 = personalYear(dt, 2027), py26 = personalYear(dt, 2026);
    lastCopy = summary(dt, lp, py27, py26, nn);
    card.innerHTML = '<div class="nu-result">' +
      lifeCard(lp) + yearCard(py27, 2027, "next") + yearCard(py26, 2026, false) + nameCards(nn, hasName) +
      '<p class="nu-honest">There is no scientific evidence that numbers predict personality or the future. These are the meanings numerologists traditionally associate with each number. Take what feels true, leave the rest, and use it as a prompt for reflection.</p>' +
      '<div class="nu-actions print-hide"><button type="button" class="btn small" data-copy="result">Copy result</button>' +
      '<a class="btn ghost small" href="/journal-prompt-generator/">Get a journal prompt</a></div></div>';
    if (!reduceMotion) { card.classList.remove("nu-in"); void card.offsetWidth; card.classList.add("nu-in"); }
    if (!opts.noScroll && window.innerWidth < 900) card.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    // Never put the birthday in the URL: analytics and tag scripts record page URLs.
    track("website numerology calculated", { life_path: Number(lp.value), has_name: hasName });
  }

  function copyText(text, msg) {
    var done = function () { toast(msg); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, done);
    else { var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); } catch (x) {} ta.remove(); done(); }
  }

  form.addEventListener("submit", function (e) { e.preventDefault(); calc(); });
  card.addEventListener("click", function (e) {
    var b = e.target.closest("[data-copy]");
    if (b) {
      copyText(lastCopy, "Result copied");
      return;
    }
    if (e.target.closest("[data-focus-name]")) { nameIn.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" }); nameIn.focus({ preventScroll: true }); }
  });

})();

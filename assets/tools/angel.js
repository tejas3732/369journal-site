/* Angel number meanings. Runs in the browser only; data comes from the page (#angel-data).
   Analytics: the looked-up number (not personal) and the birthday RESULT only, never the date. */
(function () {
  "use strict";
  var root = document.querySelector("[data-angel]");
  var dataEl = document.getElementById("angel-data");
  if (!root || !dataEl) return;
  var DATA = JSON.parse(dataEl.textContent);
  var card = root.querySelector("[data-result]");
  var numInput = document.getElementById("an-number");
  var birthInput = document.getElementById("an-birth");
  var toastEl = document.querySelector("[data-toast]");
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function track(name, props) { try { if (window.posthog) window.posthog.capture(name, props || {}); } catch (e) {} }

  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toast.t);
    toast.t = setTimeout(function () { toastEl.classList.remove("show"); }, 1800);
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function sumDigits(str) { return str.split("").reduce(function (a, d) { return a + Number(d); }, 0); }

  // Reduce to 1-9, keeping master numbers 11, 22, 33. Returns the steps shown to the reader.
  function reduce(str) {
    var steps = [];
    var cur = str;
    while (cur.length > 1 && !(cur === "11" || cur === "22" || cur === "33")) {
      var s = sumDigits(cur);
      steps.push(cur.split("").join(" + ") + " = " + s);
      cur = String(s);
    }
    return { value: cur, steps: steps };
  }

  function dots() {
    return '<span class="an-dots" aria-hidden="true"><span><i></i><i></i><i></i></span><span><b></b><b></b><b></b><b></b><b></b><b></b></span><span><em></em><em></em><em></em><em></em><em></em><em></em><em></em><em></em><em></em></span></span>';
  }

  function patternNotes(n) {
    var notes = [];
    var uniq = n.split("").filter(function (d, i, a) { return a.indexOf(d) === i; });
    if (n.length > 1 && uniq.length === 1) notes.push("Every digit is the same, which people read as that number's meaning turned up loud.");
    if (n.length > 2 && n === n.split("").reverse().join("") && uniq.length > 1) notes.push("It reads the same forwards and backwards (a mirror number), often linked with reflection and balance.");
    var up = true, down = true;
    for (var i = 1; i < n.length; i++) {
      if (Number(n[i]) !== Number(n[i - 1]) + 1) up = false;
      if (Number(n[i]) !== Number(n[i - 1]) - 1) down = false;
    }
    if (n.length > 2 && up) notes.push("Its digits climb in order, often read as steady, step-by-step progress.");
    if (n.length > 2 && down) notes.push("Its digits count down, often read as something coming to a close.");
    if (n.length >= 4 && n.length % 2 === 0 && n.slice(0, n.length / 2) === n.slice(n.length / 2) && uniq.length > 1) notes.push("It repeats a pair, which people read as that pair's meaning doubled.");
    return notes;
  }

  function actions(aff, n) {
    var related = /^(369|963|639)$/.test(n) ? '<a class="t-link-btn an-related" href="/369-meaning/">Read the full meaning of 369</a>' : "";
    return '<div class="an-actions">' +
      '<button type="button" class="btn small" data-copy="' + esc(aff) + '">Copy affirmation</button>' +
      '<a class="btn ghost small" href="/affirmation-wallpaper/">Make it a wallpaper</a>' +
      '<a class="btn ghost small" href="/affirmation-generator/">Write it with the 369 method</a>' +
      "</div>" + related;
  }

  function renderCurated(n, e, label) {
    return '<div class="an-result">' +
      '<div class="an-top">' + dots() + '<p class="an-num">' + esc(n) + "</p>" + (label ? '<p class="an-label">' + label + "</p>" : "") + "</div>" +
      '<ul class="an-words">' + e.words.map(function (w) { return "<li>" + esc(w) + "</li>"; }).join("") + "</ul>" +
      '<p class="an-text">' + esc(e.text) + "</p>" +
      '<div class="an-ask"><p class="an-ask-k">A question to sit with</p><p>' + esc(e.ask) + "</p></div>" +
      '<div class="an-aff"><p class="an-ask-k">An affirmation to try</p><p class="an-aff-t">“' + esc(e.aff) + '”</p></div>' +
      actions(e.aff, n) + "</div>";
  }

  function renderComputed(n) {
    var uniq = n.split("").filter(function (d, i, a) { return a.indexOf(d) === i; });
    var r = reduce(n);
    var rd = DATA.digits[r.value];
    var words = uniq.slice(0, 3).map(function (d) { return DATA.digits[d].word; });
    var lines = uniq.map(function (d) { return "<li><strong>" + d + "</strong> is commonly associated with " + esc(DATA.digits[d].text) + ".</li>"; }).join("");
    var notes = patternNotes(n).map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("");
    var aff = "I move toward what matters to me with " + rd.word.toLowerCase() + " and care.";
    var ask = "What does " + rd.word.toLowerCase() + " look like in your life this week?";
    return '<div class="an-result">' +
      '<div class="an-top">' + dots() + '<p class="an-num">' + esc(n) + '</p><p class="an-label">Built from its digits</p></div>' +
      '<ul class="an-words">' + words.map(function (w) { return "<li>" + esc(w) + "</li>"; }).join("") + "</ul>" +
      '<p class="an-text">We don’t have a written meaning for ' + esc(n) + ", so here is a reading built from its digits, the way numerology usually does it.</p>" +
      '<ul class="an-list">' + lines + notes + "</ul>" +
      (r.steps.length ? '<div class="an-math"><p class="an-ask-k">Its root number</p><p>' + r.steps.map(esc).join("<br>") + '</p><p class="an-root"><strong>' + r.value + "</strong>: " + esc(rd.text) + "</p></div>" : "") +
      '<div class="an-ask"><p class="an-ask-k">A question to sit with</p><p>' + esc(ask) + "</p></div>" +
      '<div class="an-aff"><p class="an-ask-k">An affirmation to try</p><p class="an-aff-t">“' + esc(aff) + '”</p></div>' +
      actions(aff, n) + "</div>";
  }

  function show(htmlStr, noScroll) {
    card.innerHTML = htmlStr;
    if (!reduceMotion) { card.classList.remove("an-in"); void card.offsetWidth; card.classList.add("an-in"); }
    if (!noScroll && window.innerWidth < 900) card.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
  }

  function lookup(raw, fromHash) {
    var n = String(raw || "").replace(/\D/g, "").slice(0, 6);
    if (!n) { numInput.focus(); toast("Type a number first"); return; }
    numInput.value = n;
    var e = DATA.numbers[n];
    show(e ? renderCurated(n, e) : renderComputed(n), fromHash);
    if (location.hash !== "#n=" + n) history.replaceState(null, "", "#n=" + n);
    if (!fromHash) track("website angel number looked up", { number: n, curated: !!e });
  }

  function birthday() {
    var v = birthInput.value; // yyyy-mm-dd
    if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) { birthInput.focus(); toast("Choose your date of birth"); return; }
    var digits = v.replace(/-/g, "");
    var first = sumDigits(digits);
    var steps = [digits.split("").join(" + ") + " = " + first];
    var r = reduce(String(first));
    steps = steps.concat(r.steps);
    var num = r.value;
    var d = DATA.digits[num];
    var aff = "I trust my own way of " + d.word.toLowerCase() + ", and I let it guide me.";
    show('<div class="an-result">' +
      '<div class="an-top">' + dots() + '<p class="an-num">' + num + '</p><p class="an-label">Your birthday number</p></div>' +
      '<ul class="an-words"><li>' + esc(d.word) + "</li></ul>" +
      '<div class="an-math"><p class="an-ask-k">How we got there</p><p>' + steps.map(esc).join("<br>") + "</p></div>" +
      '<p class="an-text">In numerology this is often called a life path number. ' + esc(DATA.birth[num]) + " It is commonly associated with " + esc(d.text) + ".</p>" +
      '<p class="an-text an-soft">Take what feels true and leave the rest. A number can’t define you; it can only give you something to think about.</p>' +
      '<div class="an-aff"><p class="an-ask-k">An affirmation to try</p><p class="an-aff-t">“' + esc(aff) + '”</p></div>' +
      actions(aff, num) + "</div>");
    track("website birthday number", { result: num });
  }

  function setMode(mode) {
    root.querySelectorAll("[data-pane]").forEach(function (p) { p.hidden = p.getAttribute("data-pane") !== mode; });
    var r = root.querySelector('input[name="an-mode"][value="' + mode + '"]');
    if (r) r.checked = true;
  }

  root.querySelectorAll('input[name="an-mode"]').forEach(function (r) {
    r.addEventListener("change", function () { setMode(r.value); });
  });
  root.querySelector('[data-pane="number"]').addEventListener("submit", function (e) { e.preventDefault(); lookup(numInput.value); });
  root.querySelector('[data-pane="birthday"]').addEventListener("submit", function (e) { e.preventDefault(); birthday(); });
  numInput.addEventListener("input", function () { var c = numInput.value.replace(/\D/g, "").slice(0, 6); if (c !== numInput.value) numInput.value = c; });
  root.querySelectorAll(".an-chip").forEach(function (b) {
    b.addEventListener("click", function () { setMode("number"); lookup(b.getAttribute("data-n")); });
  });

  card.addEventListener("click", function (e) {
    var b = e.target.closest("[data-copy]");
    if (!b) return;
    var text = b.getAttribute("data-copy");
    var done = function () { toast("Affirmation copied"); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, done);
    else { var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); } catch (x) {} ta.remove(); done(); }
  });

  // Links in the static table (#n=444) open the number in the tool above.
  document.querySelectorAll("a[data-n]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      setMode("number");
      lookup(a.getAttribute("data-n"));
      root.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    });
  });

  function fromHash() {
    var m = location.hash.match(/^#n=(\d{1,6})$/);
    if (m) { setMode("number"); lookup(m[1], true); }
  }
  window.addEventListener("hashchange", fromHash);
  fromHash();
})();

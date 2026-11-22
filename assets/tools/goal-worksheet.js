/* Goal setting worksheet. Runs entirely in the browser.
   Answers are kept in localStorage on this device only. Analytics never include what you type. */
(function () {
  "use strict";
  var root = document.querySelector("[data-goal]");
  if (!root) return;

  var KEY = "369j-goal-worksheet";
  var EXAMPLE = {
    goal: "Run 5 km without stopping",
    why: "I want more energy for my family and to feel strong in my body.",
    success: "I jog 5 km on a Saturday morning in about 35 minutes and feel good afterwards.",
    deadline: "31 March 2027",
    if1: "it rains", then1: "I do a 20-minute indoor workout",
    if2: "I feel too tired", then2: "I put my shoes on and do just 10 minutes",
    if3: "I skip a day", then3: "I go the next day (never miss twice)",
    step1: "Buy running shoes by Sunday",
    step2: "Walk or jog 20 minutes on Tuesday",
    step3: "Pick a local 5 km event for March",
    weekly: "Three 20-minute sessions: Tue, Thu, Sat at 7am",
    aff: "I am someone who keeps showing up for my body."
  };

  var fields = [].slice.call(root.querySelectorAll("[data-f]"));
  var sheet = root.querySelector("[data-sheet]");
  var toastEl = document.querySelector("[data-toast]");
  var track = function (name, props) {
    try { if (window.posthog) window.posthog.capture(name, props || {}); } catch (e) {}
  };
  var toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove("show"); }, 1800);
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function radio(name) { var el = root.querySelector('input[name="' + name + '"]:checked'); return el ? el.value : ""; }
  function setRadio(name, v) { var el = root.querySelector('input[name="' + name + '"][value="' + v + '"]'); if (el) el.checked = true; }

  function values() {
    var v = {};
    fields.forEach(function (f) { v[f.getAttribute("data-f")] = f.value.trim(); });
    return v;
  }
  function filledCount(v) { return Object.keys(v).filter(function (k) { return v[k]; }).length; }

  function save() {
    try {
      var o = {};
      fields.forEach(function (f) { o[f.getAttribute("data-f")] = f.value; });
      o._paper = radio("gwpaper");
      localStorage.setItem(KEY, JSON.stringify(o));
    } catch (e) {}
  }
  function load() {
    try {
      var o = JSON.parse(localStorage.getItem(KEY) || "null");
      if (!o || typeof o !== "object") return;
      fields.forEach(function (f) {
        var k = f.getAttribute("data-f");
        if (typeof o[k] === "string") f.value = o[k].slice(0, +f.getAttribute("maxlength") || 300);
      });
      if (o._paper) setRadio("gwpaper", o._paper);
    } catch (e) {}
  }

  var pageStyle = document.createElement("style");
  document.head.appendChild(pageStyle);

  function lines(n) {
    var s = "";
    for (var i = 0; i < n; i++) s += '<span class="gw-line"></span>';
    return '<div class="gw-lines">' + s + "</div>";
  }
  // A labelled block: the typed text sits on ruled lines, or empty lines for handwriting.
  function block(label, hint, text, n) {
    var body = text ? '<p class="gw-val" style="--n:' + n + '">' + esc(text) + "</p>" : lines(n);
    return '<section class="gw-block"><h3>' + label + (hint ? " <span>" + hint + "</span>" : "") + "</h3>" + body + "</section>";
  }

  function render() {
    var blank = radio("gwmode") === "blank";
    var paper = radio("gwpaper") || "a4";
    var v = values();
    if (blank) Object.keys(v).forEach(function (k) { v[k] = ""; });

    var ifthen = [1, 2, 3].map(function (i) {
      var a = v["if" + i], b = v["then" + i];
      return '<li><span class="gw-k">If</span>' + (a ? '<span class="gw-v">' + esc(a) + "</span>" : '<span class="gw-v empty"></span>') +
        '<span class="gw-k">then I will</span>' + (b ? '<span class="gw-v">' + esc(b) + "</span>" : '<span class="gw-v empty"></span>') + "</li>";
    }).join("");
    var steps = [1, 2, 3].map(function (i) {
      var s = v["step" + i];
      return '<li><span class="gw-box" aria-hidden="true"></span>' + (s ? '<span class="gw-v">' + esc(s) + "</span>" : '<span class="gw-v empty"></span>') + "</li>";
    }).join("");

    sheet.className = "gw-sheet paper-" + paper;
    sheet.innerHTML =
      '<div class="gw-title"><h2>My goal worksheet</h2><p>Date <span class="gw-blank"></span></p></div>' +
      block("My goal", "What do I want, in one clear sentence?", v.goal, 2) +
      '<div class="gw-two">' +
        block("Why it matters to me", "", v.why, 3) +
        block("What success looks like", "What will I see, have or feel?", v.success, 3) +
      "</div>" +
      '<section class="gw-block gw-by"><h3>By when</h3>' + (v.deadline ? '<p class="gw-val gw-short">' + esc(v.deadline) + "</p>" : '<span class="gw-line gw-short"></span>') + "</section>" +
      '<section class="gw-block"><h3>What could get in the way, and my plan <span>If this happens, then I will&hellip;</span></h3><ul class="gw-if">' + ifthen + "</ul></section>" +
      '<section class="gw-block"><h3>My first 3 steps <span>Small and close</span></h3><ul class="gw-steps-l">' + steps + "</ul></section>" +
      block("My weekly tiny action", "Small enough for a bad week", v.weekly, 1) +
      block("My affirmation line", "Present tense and believable. Read or write it each day.", v.aff, 1) +
      '<p class="gw-foot">Review this once a week: what did I do, what got in the way, what is my next small step? &middot; 369journal.app</p>';

    var size = paper === "letter" ? "letter" : "A4";
    pageStyle.textContent = "@media print { @page { size: " + size + " portrait; margin: 11mm; } }";
  }

  function update() { render(); save(); }

  fields.forEach(function (f) { f.addEventListener("input", update); });
  root.addEventListener("change", function (e) { if (e.target && e.target.type === "radio") update(); });

  var started = false;
  root.addEventListener("input", function () {
    if (!started) { started = true; track("website goal worksheet started"); }
  });

  root.querySelector("[data-example]").addEventListener("click", function () {
    fields.forEach(function (f) { f.value = EXAMPLE[f.getAttribute("data-f")] || ""; });
    setRadio("gwmode", "filled");
    update();
    toast("Example loaded. Change any line.");
    track("website goal worksheet example");
  });
  root.querySelector("[data-clear]").addEventListener("click", function () {
    fields.forEach(function (f) { f.value = ""; });
    update();
    fields[0].focus();
  });
  root.querySelector("[data-print]").addEventListener("click", function () {
    render();
    var v = values();
    track("website goal worksheet printed", { mode: radio("gwmode"), paper: radio("gwpaper"), fields_filled: filledCount(v) });
    window.print();
  });

  load();
  render();
})();

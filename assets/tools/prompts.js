/* Journal prompt generator. Runs entirely in the browser.
   Prompts come from the JSON block #prompt-data (built by scripts/tool_prompts.py).
   Saved prompts live in localStorage on this device only. Analytics never include prompt text. */
(function () {
  "use strict";
  var root = document.querySelector("[data-prompts]");
  var dataEl = document.getElementById("prompt-data");
  if (!root || !dataEl) return;

  var DATA;
  try { DATA = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var KEY = "369j-saved-prompts";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  var $ = function (s) { return document.querySelector(s); };
  var promptEl = $("[data-prompt]");
  var card = $(".prompt-card");
  var catLabel = $("[data-cat-label]");
  var saveBtn = $("[data-save]");
  var saveLabel = $("[data-save-label]");
  var savedList = $("[data-saved-list]");
  var savedEmpty = $("[data-saved-empty]");
  var savedCount = $("[data-saved-count]");
  var printCat = $("[data-print-cat]");
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

  // ---------- Saved prompts (localStorage, defensive) ----------
  function loadSaved() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v.filter(function (x) { return typeof x === "string"; }) : []; }
    catch (e) { return []; }
  }
  function storeSaved(list) {
    try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {}
  }
  var saved = loadSaved();

  function renderSaved() {
    savedList.innerHTML = "";
    saved.forEach(function (text, i) {
      var li = document.createElement("li");
      var p = document.createElement("p");
      p.textContent = text;
      var rm = document.createElement("button");
      rm.type = "button";
      rm.className = "saved-remove";
      rm.setAttribute("aria-label", "Remove saved prompt " + (i + 1));
      rm.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8"/></svg>';
      rm.addEventListener("click", function () {
        saved.splice(saved.indexOf(text), 1);
        storeSaved(saved);
        renderSaved();
        updateSaveBtn();
        toast("Removed");
      });
      li.appendChild(p);
      li.appendChild(rm);
      savedList.appendChild(li);
    });
    savedCount.textContent = saved.length;
    savedEmpty.hidden = saved.length > 0;
  }

  // ---------- Prompt selection ----------
  var current = "";
  var bags = {};

  function category() {
    var el = root.querySelector("input[name=pcat]:checked");
    return el && DATA[el.value] ? el.value : Object.keys(DATA)[0];
  }
  function mode() {
    var el = root.querySelector("input[name=pmode]:checked");
    return el ? el.value : "random";
  }

  function shuffled(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  // Shuffle bag: every prompt once before any repeats, never the same twice in a row.
  function nextRandom(cat) {
    var pool = DATA[cat].prompts;
    if (!bags[cat] || bags[cat].length === 0) {
      bags[cat] = shuffled(pool);
      if (bags[cat][bags[cat].length - 1] === current && bags[cat].length > 1) {
        var last = bags[cat].pop(); bags[cat].unshift(last);
      }
    }
    return bags[cat].pop();
  }

  // Same prompt for everyone on a given day and category.
  function todays(cat) {
    var d = new Date();
    var key = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
    var s = cat + ":" + key, h = 2166136261;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    var pool = DATA[cat].prompts;
    return pool[(h >>> 0) % pool.length];
  }

  function show(text) {
    current = text;
    var apply = function () { promptEl.textContent = text; updateSaveBtn(); };
    if (reduceMotion) { apply(); return; }
    card.classList.remove("swap-in");
    card.classList.add("swap-out");
    setTimeout(function () {
      apply();
      card.classList.remove("swap-out");
      void card.offsetWidth;
      card.classList.add("swap-in");
    }, 140);
  }

  function next() {
    var cat = category();
    show(mode() === "today" ? todays(cat) : nextRandom(cat));
    track("website prompt shown", { category: cat, mode: mode() });
  }

  function updateSaveBtn() {
    var on = !!current && saved.indexOf(current) !== -1;
    saveBtn.classList.toggle("is-saved", on);
    saveBtn.setAttribute("aria-pressed", on ? "true" : "false");
    saveLabel.textContent = on ? "Saved" : "Save";
  }

  function onCategory() {
    var cat = category();
    catLabel.textContent = DATA[cat].label;
    printCat.textContent = DATA[cat].label;
    next();
  }

  // ---------- Copy ----------
  function copy() {
    if (!current) return;
    var done = function () { toast("Copied"); track("website prompt copied", { category: category() }); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(current).then(done, fallback);
    } else { fallback(); }
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = current; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch (e) {}
      ta.remove(); done();
    }
  }

  function toggleSave() {
    if (!current) return;
    var i = saved.indexOf(current);
    if (i === -1) { saved.unshift(current); toast("Saved on this device"); }
    else { saved.splice(i, 1); toast("Removed"); }
    storeSaved(saved);
    renderSaved();
    updateSaveBtn();
  }

  // ---------- Print ----------
  function buildPrint() {
    var srcEl = root.querySelector("input[name=psource]:checked");
    var src = srcEl ? srcEl.value : "category";
    var cat = category();
    var items, title;
    if (src === "saved") {
      if (!saved.length) { toast("Save a few prompts first"); return null; }
      items = saved.slice(0, 30);
      title = "My saved journal prompts";
    } else {
      items = shuffled(DATA[cat].prompts);
      while (items.length < 30) items = items.concat(shuffled(DATA[cat].prompts));
      items = items.slice(0, 30);
      title = DATA[cat].label + " journal prompts";
    }
    document.querySelector("[data-print-title]").textContent = title;
    var list = document.querySelector("[data-print-list]");
    list.innerHTML = "";
    items.forEach(function (t) {
      var li = document.createElement("li");
      var p = document.createElement("p");
      p.textContent = t;
      var lines = document.createElement("div");
      lines.className = "pp-lines";
      li.appendChild(p);
      li.appendChild(lines);
      list.appendChild(li);
    });
    return { source: src, category: cat, count: items.length };
  }

  // ---------- Wire up ----------
  Array.prototype.forEach.call(root.querySelectorAll("input[name=pcat]"), function (r) { r.addEventListener("change", onCategory); });
  Array.prototype.forEach.call(root.querySelectorAll("input[name=pmode]"), function (r) { r.addEventListener("change", next); });
  $("[data-new]").addEventListener("click", function () {
    if (mode() === "today") { var r = root.querySelector("input[name=pmode][value=random]"); if (r) r.checked = true; }
    next();
  });
  $("[data-copy]").addEventListener("click", copy);
  saveBtn.addEventListener("click", toggleSave);
  $("[data-print]").addEventListener("click", function () {
    var info = buildPrint();
    if (!info) return;
    track("website prompts printed", info);
    window.print();
  });

  document.addEventListener("keydown", function (e) {
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key !== " " && e.key !== "Enter") return;
    var t = e.target;
    var tag = t && t.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || tag === "BUTTON" || tag === "A" || tag === "SUMMARY" || (t && t.isContentEditable)) return;
    e.preventDefault();
    if (mode() === "today") { var r = root.querySelector("input[name=pmode][value=random]"); if (r) r.checked = true; }
    next();
  });

  renderSaved();
  catLabel.textContent = DATA[category()].label;
  printCat.textContent = DATA[category()].label;
  // First prompt without animation so the page never shows a placeholder for long.
  current = nextRandom(category());
  promptEl.textContent = current;
  updateSaveBtn();
})();

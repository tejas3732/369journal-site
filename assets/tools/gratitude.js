/* Gratitude journal prompts. Runs entirely in the browser.
   Prompts come from the JSON block #gratitude-data (built by scripts/tool_gratitude.py).
   Saved prompts live in localStorage on this device only. Analytics never include prompt text. */
(function () {
  "use strict";
  var root = document.querySelector("[data-gratitude]");
  var dataEl = document.getElementById("gratitude-data");
  if (!root || !dataEl) return;

  var DATA;
  try { DATA = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var KEY = "369j-saved-gratitude";
  var THEMES = Object.keys(DATA);
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  var $ = function (s) { return document.querySelector(s); };
  var promptEl = $("[data-prompt]");
  var card = $(".gj-card");
  var oneBox = $("[data-one]");
  var threeBox = $("[data-three]");
  var threeList = $("[data-three-list]");
  var catLabel = $("[data-cat-label]");
  var newLabel = $("[data-new-label]");
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
  function storeSaved(list) { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {} }
  var saved = loadSaved();

  var X_ICON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8"/></svg>';
  var SAVE_ICON = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5.5 3.5h9v13l-4.5-3-4.5 3z"/></svg>';

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
      rm.innerHTML = X_ICON;
      rm.addEventListener("click", function () {
        saved.splice(saved.indexOf(text), 1);
        storeSaved(saved);
        renderSaved();
        refreshSaveStates();
        toast("Removed");
      });
      li.appendChild(p);
      li.appendChild(rm);
      savedList.appendChild(li);
    });
    savedCount.textContent = saved.length;
    savedEmpty.hidden = saved.length > 0;
  }

  // ---------- State ----------
  var current = "";        // single prompt
  var currentSet = [];     // three prompts
  var bags = {};

  function theme() {
    var el = root.querySelector("input[name=gtheme]:checked");
    return el && (el.value === "all" || DATA[el.value]) ? el.value : "all";
  }
  function view() { var el = root.querySelector("input[name=gview]:checked"); return el ? el.value : "one"; }
  function mode() { var el = root.querySelector("input[name=gmode]:checked"); return el ? el.value : "random"; }
  function themeLabel(t) { return t === "all" ? "All themes" : DATA[t].label; }

  // Flat pool of prompts for a theme key ("all" = every theme).
  function pool(t) {
    if (t !== "all") return DATA[t].prompts;
    var out = [];
    THEMES.forEach(function (k) { out = out.concat(DATA[k].prompts); });
    return out;
  }

  function shuffled(arr, rnd) {
    var r = rnd || Math.random;
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(r() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  // Shuffle bag: every prompt once before any repeat. "avoid" stops back-to-back repeats.
  function draw(t, n, avoid) {
    var out = [];
    var guard = 0;
    while (out.length < n && guard++ < 500) {
      if (!bags[t] || !bags[t].length) {
        bags[t] = shuffled(pool(t));
        // keep the last-shown prompts away from the end (the next to be popped)
        var tail = bags[t].length - 1;
        for (var k = 0; k < avoid.length && tail > 0; k++) {
          var idx = bags[t].indexOf(avoid[k]);
          if (idx > bags[t].length - 1 - n - avoid.length) { var tmp = bags[t][idx]; bags[t][idx] = bags[t][0]; bags[t][0] = tmp; }
        }
      }
      var p = bags[t].pop();
      if (out.indexOf(p) === -1 && (avoid.indexOf(p) === -1 || bags[t].length === 0)) out.push(p);
    }
    return out;
  }

  // Same prompts for everyone on a given day and theme.
  function seedFor(t) {
    var d = new Date();
    var key = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
    var s = "gratitude:" + t + ":" + key, h = 2166136261;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  function mulberry(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function todays(t, n) { return shuffled(pool(t), mulberry(seedFor(t))).slice(0, n); }

  // Three good things: when "All", one from each of three different themes.
  function pickThree(t) {
    if (mode() === "today") {
      if (t !== "all") return todays(t, 3);
      var r = mulberry(seedFor("all3"));
      return shuffled(THEMES, r).slice(0, 3).map(function (k) { var p = DATA[k].prompts; return p[Math.floor(r() * p.length)]; });
    }
    if (t !== "all") return draw(t, 3, currentSet);
    var picks = [];
    shuffled(THEMES).slice(0, 3).forEach(function (k) {
      var p = shuffled(DATA[k].prompts).filter(function (x) { return currentSet.indexOf(x) === -1; })[0];
      picks.push(p);
    });
    return picks;
  }

  // ---------- Rendering ----------
  function isSaved(text) { return saved.indexOf(text) !== -1; }

  function refreshSaveStates() {
    var on = !!current && isSaved(current);
    saveBtn.classList.toggle("is-saved", on);
    saveBtn.setAttribute("aria-pressed", on ? "true" : "false");
    saveLabel.textContent = on ? "Saved" : "Save";
    Array.prototype.forEach.call(threeList.querySelectorAll("[data-item-save]"), function (b) {
      var s = isSaved(b.getAttribute("data-text"));
      b.classList.toggle("is-saved", s);
      b.setAttribute("aria-pressed", s ? "true" : "false");
      b.setAttribute("aria-label", (s ? "Remove from saved: " : "Save: ") + b.getAttribute("data-text"));
    });
  }

  function renderThree(items) {
    currentSet = items;
    threeList.innerHTML = "";
    items.forEach(function (text) {
      var li = document.createElement("li");
      var p = document.createElement("p");
      p.textContent = text;
      var b = document.createElement("button");
      b.type = "button";
      b.className = "gj-item-save";
      b.setAttribute("data-item-save", "");
      b.setAttribute("data-text", text);
      b.innerHTML = SAVE_ICON;
      b.addEventListener("click", function () { toggleSave(text); });
      li.appendChild(p);
      li.appendChild(b);
      threeList.appendChild(li);
    });
    refreshSaveStates();
  }

  function swap(apply, el) {
    if (reduceMotion || !el) { apply(); return; }
    el.classList.remove("swap-in");
    el.classList.add("swap-out");
    setTimeout(function () {
      apply();
      el.classList.remove("swap-out");
      void el.offsetWidth;
      el.classList.add("swap-in");
    }, 140);
  }

  function next() {
    var t = theme();
    if (view() === "three") {
      var items = pickThree(t);
      swap(function () { renderThree(items); }, threeList);
    } else {
      var text = mode() === "today" ? todays(t, 1)[0] : draw(t, 1, [current])[0];
      current = text;
      swap(function () { promptEl.textContent = text; refreshSaveStates(); }, card);
    }
    track("website gratitude prompt", { theme: t, view: view(), mode: mode() });
  }

  function applyView() {
    var three = view() === "three";
    oneBox.hidden = three;
    threeBox.hidden = !three;
    saveBtn.hidden = three;
    newLabel.textContent = three ? "New three" : "New prompt";
    if (three && !currentSet.length) renderThree(pickThree(theme()));
  }

  function onView() { applyView(); next(); }

  function onTheme() {
    var t = theme();
    catLabel.textContent = themeLabel(t);
    printCat.textContent = t === "all" ? "mixed themes" : DATA[t].label;
    next();
  }

  function forceRandom() {
    if (mode() === "today") { var r = root.querySelector("input[name=gmode][value=random]"); if (r) r.checked = true; }
  }

  // ---------- Copy, save ----------
  function copy() {
    var text = view() === "three"
      ? currentSet.map(function (t, i) { return (i + 1) + ". " + t; }).join("\n")
      : current;
    if (!text) return;
    var done = function () { toast("Copied"); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else { fallback(); }
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch (e) {}
      ta.remove(); done();
    }
  }

  function toggleSave(text) {
    if (!text) return;
    var i = saved.indexOf(text);
    if (i === -1) { saved.unshift(text); toast("Saved on this device"); }
    else { saved.splice(i, 1); toast("Removed"); }
    storeSaved(saved);
    renderSaved();
    refreshSaveStates();
  }

  // ---------- Print: 30-day journal ----------
  function thirtyFor(t) {
    var first = t === "all" ? [] : shuffled(DATA[t].prompts);
    var rest = shuffled(pool("all").filter(function (p) { return first.indexOf(p) === -1; }));
    if (t === "all") {
      // round-robin across themes so a mixed journal has variety
      var lists = shuffled(THEMES).map(function (k) { return shuffled(DATA[k].prompts); });
      var out = [];
      for (var n = 0; out.length < 30 && n < 40; n++) {
        lists.forEach(function (l) { if (l[n] && out.length < 30) out.push(l[n]); });
      }
      return out;
    }
    return first.concat(rest).slice(0, 30);
  }

  function buildPrint() {
    var srcEl = root.querySelector("input[name=gsource]:checked");
    var src = srcEl ? srcEl.value : "theme";
    var t = theme();
    var items, title;
    if (src === "saved") {
      if (!saved.length) { toast("Save a few prompts first"); return null; }
      items = saved.slice(0, 30);
      title = "My gratitude journal";
    } else {
      items = thirtyFor(t);
      title = "30-day gratitude journal" + (t === "all" ? "" : ": " + DATA[t].label);
    }
    document.querySelector("[data-print-title]").textContent = title;
    var list = document.querySelector("[data-print-list]");
    list.innerHTML = "";
    items.forEach(function (text, i) {
      var li = document.createElement("li");
      var head = document.createElement("div");
      head.className = "gp-head";
      head.innerHTML = '<b>Day ' + (i + 1) + '</b><span>Date: ______________</span>';
      var p = document.createElement("p");
      p.textContent = text;
      var lines = document.createElement("div");
      lines.className = "gp-lines";
      li.appendChild(head);
      li.appendChild(p);
      li.appendChild(lines);
      list.appendChild(li);
    });
    return { source: src, theme: t, count: items.length };
  }

  // ---------- Wire up ----------
  var each = function (sel, fn) { Array.prototype.forEach.call(root.querySelectorAll(sel), fn); };
  each("input[name=gtheme]", function (r) { r.addEventListener("change", onTheme); });
  each("input[name=gview]", function (r) { r.addEventListener("change", onView); });
  each("input[name=gmode]", function (r) { r.addEventListener("change", next); });
  $("[data-new]").addEventListener("click", function () { forceRandom(); next(); });
  $("[data-copy]").addEventListener("click", copy);
  saveBtn.addEventListener("click", function () { toggleSave(current); });
  $("[data-print]").addEventListener("click", function () {
    var info = buildPrint();
    if (!info) return;
    track("website gratitude printed", info);
    window.print();
  });

  document.addEventListener("keydown", function (e) {
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key !== " " && e.key !== "Enter") return;
    var t = e.target, tag = t && t.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || tag === "BUTTON" || tag === "A" || tag === "SUMMARY" || (t && t.isContentEditable)) return;
    e.preventDefault();
    forceRandom();
    next();
  });

  renderSaved();
  catLabel.textContent = themeLabel(theme());
  printCat.textContent = "mixed themes";
  // First prompt without animation so the page never shows a placeholder for long.
  current = draw(theme(), 1, [])[0];
  promptEl.textContent = current;
  refreshSaveStates();
  applyView();
})();

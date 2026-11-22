/* Affirmation list pages (morning, self-love, money). Runs entirely in the browser.
   The affirmations are also in the page HTML (one button each) and in the JSON block #affirmation-data.
   Favourites live in localStorage on this device only. Analytics never include the affirmation text. */
(function () {
  "use strict";
  var root = document.querySelector("[data-affirmations]");
  var dataEl = document.getElementById("affirmation-data");
  if (!root || !dataEl) return;

  var D;
  try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var KEY = "369j-affirmation-favourites";
  var PAGE = D.page;

  var $ = function (s) { return root.querySelector(s); };
  var toastEl = document.querySelector("[data-toast]");
  var track = function (name, props) {
    try { if (window.posthog) { var p = props || {}; p.page = PAGE; window.posthog.capture(name, p); } } catch (e) {}
  };
  var toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove("show"); }, 2000);
  }

  // ---------- All affirmations (flat) ----------
  var ALL = [];
  D.sections.forEach(function (s) { s.items.forEach(function (t) { ALL.push(t); }); });

  // ---------- Copy ----------
  function copyText(text, done) {
    var ok = function () { if (done) done(true); };
    var fail = function () { if (done) done(false); };
    function legacy() {
      try {
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.setAttribute("readonly", "");
        ta.style.position = "fixed";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        var good = document.execCommand("copy");
        document.body.removeChild(ta);
        good ? ok() : fail();
      } catch (e) { fail(); }
    }
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(ok, legacy);
      else legacy();
    } catch (e) { legacy(); }
  }

  // ---------- Favourites (localStorage, defensive) ----------
  function loadFavs() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || "[]");
      return Array.isArray(v) ? v.filter(function (x) { return typeof x === "string" && x; }).slice(0, 200) : [];
    } catch (e) { return []; }
  }
  function storeFavs(l) { try { localStorage.setItem(KEY, JSON.stringify(l)); } catch (e) {} }
  var favs = loadFavs();

  var favList = $("[data-fav-list]");
  var favEmpty = $("[data-fav-empty]");
  var favCount = $("[data-fav-count]");
  var favCopyAll = $("[data-fav-copyall]");
  var X_ICON = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8"/></svg>';

  function renderFavs() {
    favList.innerHTML = "";
    favs.forEach(function (text, i) {
      var li = document.createElement("li");
      var p = document.createElement("p");
      p.textContent = text;
      var rm = document.createElement("button");
      rm.type = "button";
      rm.className = "af-remove";
      rm.setAttribute("aria-label", "Remove favourite " + (i + 1));
      rm.innerHTML = X_ICON;
      rm.addEventListener("click", function () {
        favs.splice(favs.indexOf(text), 1);
        storeFavs(favs);
        renderFavs();
        markFavs();
        syncDailyFav();
        toast("Removed");
      });
      li.appendChild(p);
      li.appendChild(rm);
      favList.appendChild(li);
    });
    favCount.textContent = favs.length;
    favEmpty.hidden = favs.length > 0;
    favCopyAll.hidden = favs.length === 0;
  }
  function addFavs(list) {
    var added = 0;
    list.forEach(function (t) { if (favs.indexOf(t) === -1) { favs.push(t); added++; } });
    storeFavs(favs);
    renderFavs();
    markFavs();
    syncDailyFav();
    return added;
  }
  favCopyAll.addEventListener("click", function () {
    copyText(favs.join("\n"), function (ok) { toast(ok ? "Copied all favourites" : "Could not copy"); });
    track("website affirmations copied", { count: favs.length, from: "favourites" });
  });

  // ---------- List buttons: tap to select ----------
  var items = [].slice.call(root.querySelectorAll(".af-item"));
  var selected = [];   // texts, in the order picked
  var bar = $("[data-bar]");
  var barCount = $("[data-sel-count]");

  function markFavs() {
    items.forEach(function (b) { b.classList.toggle("is-fav", favs.indexOf(b.textContent) !== -1); });
  }
  function refreshBar() {
    bar.hidden = selected.length === 0;
    barCount.textContent = selected.length + " selected";
  }
  items.forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.textContent;
      var i = selected.indexOf(t);
      if (i === -1) selected.push(t); else selected.splice(i, 1);
      b.setAttribute("aria-pressed", i === -1 ? "true" : "false");
      b.classList.toggle("is-selected", i === -1);
      refreshBar();
    });
  });
  function clearSelection() {
    selected = [];
    items.forEach(function (b) { b.setAttribute("aria-pressed", "false"); b.classList.remove("is-selected"); });
    refreshBar();
  }
  $("[data-sel-clear]").addEventListener("click", clearSelection);
  $("[data-sel-copy]").addEventListener("click", function () {
    var list = selected.slice();
    copyText(list.join("\n"), function (ok) { toast(ok ? (list.length === 1 ? "Copied" : "Copied " + list.length + " affirmations") : "Could not copy"); });
    track("website affirmations copied", { count: list.length, from: "list" });
  });
  $("[data-sel-fav]").addEventListener("click", function () {
    var n = addFavs(selected);
    toast(n ? "Saved to favourites" : "Already in your favourites");
    track("website affirmations favourited", { count: n });
    clearSelection();
  });

  // ---------- Daily / shuffled affirmation ----------
  var dailyText = $("[data-daily-text]");
  var dailyLabel = $("[data-daily-label]");
  var dailyFav = $("[data-daily-fav]");
  var dailyFavLabel = $("[data-daily-fav-label]");
  var current = "";

  function mulberry(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function todaysIndex() {
    var d = new Date();
    var s = PAGE + ":" + (d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate()), h = 2166136261;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return Math.floor(mulberry(h >>> 0)() * ALL.length);
  }
  var bag = [];
  function nextRandom() {
    if (!bag.length) {
      bag = ALL.slice();
      for (var i = bag.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = bag[i]; bag[i] = bag[j]; bag[j] = t; }
    }
    var p = bag.pop();
    if (p === current && bag.length) p = bag.pop();
    return p;
  }
  function syncDailyFav() {
    var isFav = favs.indexOf(current) !== -1;
    dailyFav.classList.toggle("is-saved", isFav);
    dailyFav.setAttribute("aria-pressed", isFav ? "true" : "false");
    dailyFavLabel.textContent = isFav ? "Saved" : "Favourite";
  }
  function show(text, label) {
    current = text;
    dailyText.textContent = text;
    dailyLabel.textContent = label;
    syncDailyFav();
  }
  show(ALL[todaysIndex()], "Today’s pick");

  $("[data-shuffle]").addEventListener("click", function () {
    show(nextRandom(), "Shuffled");
    track("website affirmation shuffled");
  });
  $("[data-daily-copy]").addEventListener("click", function () {
    copyText(current, function (ok) { toast(ok ? "Copied" : "Could not copy"); });
    track("website affirmations copied", { count: 1, from: "daily" });
  });
  dailyFav.addEventListener("click", function () {
    var i = favs.indexOf(current);
    if (i === -1) { addFavs([current]); toast("Saved to favourites"); track("website affirmations favourited", { count: 1 }); }
    else { favs.splice(i, 1); storeFavs(favs); renderFavs(); markFavs(); syncDailyFav(); toast("Removed"); }
  });

  // ---------- Links to the wallpaper maker and the 369 sheet ----------
  // Those tools have no prefill, so we copy the chosen line first and the reader pastes it in.
  [].forEach.call(root.querySelectorAll("[data-out]"), function (a) {
    a.addEventListener("click", function (e) {
      var text = selected.length ? selected[0] : current;
      var target = a.getAttribute("data-out");
      track("website affirmation sent to tool", { target: target, from: selected.length ? "selected" : "daily" });
      var plain = e.button === 0 && !e.metaKey && !e.ctrlKey && !e.shiftKey && !e.altKey;
      var go = function (ok) { toast(ok ? "Copied. Paste it into the box." : "Opening…"); };
      if (!plain) { copyText(text, go); return; }
      e.preventDefault();
      var href = a.href;
      var done = false;
      var leave = function (ok) { if (done) return; done = true; go(ok); setTimeout(function () { window.location.href = href; }, 450); };
      copyText(text, leave);
      setTimeout(function () { leave(false); }, 900);
    });
  });

  renderFavs();
  markFavs();
  refreshBar();
})();

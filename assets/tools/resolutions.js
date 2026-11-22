/* New year resolution picker. Runs entirely in the browser. Ideas come from the JSON block
   #rz-data (built by scripts/tool_newyear_pages.py). Nothing is sent or saved. Analytics only
   record which areas and size were chosen, never the text you edit. */
(function () {
  "use strict";
  var root = document.querySelector("[data-rz]");
  var dataEl = document.getElementById("rz-data");
  if (!root || !dataEl) return;

  var DATA;
  try { DATA = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var MAX_AREAS = 3;
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var SIZE_LABEL = { t: "Tiny habit", s: "Steady change", b: "Big goal" };

  var $ = function (s) { return root.querySelector(s); };
  var track = function (n, p) { try { if (window.posthog) window.posthog.capture(n, p || {}); } catch (e) {} };
  var toastEl = document.querySelector("[data-toast]");
  var toast = function (msg) {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toast.t); toast.t = setTimeout(function () { toastEl.classList.remove("show"); }, 2000);
  };

  // Flat list of ideas, each knows its area.
  var ITEMS = [];
  DATA.areas.forEach(function (a) {
    a.items.forEach(function (it) {
      ITEMS.push({ area: a.id, areaLabel: a.label, size: it[0], res: it[1], aff: it[2], act: it[3] });
    });
  });

  var areaInputs = Array.prototype.slice.call(root.querySelectorAll("input[name=rz-area]"));
  var sizeInputs = Array.prototype.slice.call(root.querySelectorAll("input[name=rz-size]"));
  var countEl = $("[data-rz-count]");
  var listEl = $("[data-rz-ideas]");
  var emptyEl = $("[data-rz-empty]");
  var noteEl = $("[data-rz-note]");
  var shuffleBtn = $("[data-rz-shuffle]");
  var editPanel = $("[data-rz-edit]");
  var resIn = $("#rz-res");
  var affIn = $("#rz-aff");
  var actIn = $("#rz-act");
  var cardRes = $("[data-c-res]");
  var cardAff = $("[data-c-aff]");
  var cardAct = $("[data-c-act]");
  var cardEl = $("[data-rz-card]");
  var copyBtn = $("[data-rz-copy]");
  var printBtn = $("[data-rz-print]");

  var drawn = [];
  var lastPool = null;
  var picked = -1;     // index into ITEMS, or -1
  var bag = { key: "", order: [], pos: 0 };

  function chosenAreas() { return areaInputs.filter(function (i) { return i.checked; }).map(function (i) { return i.value; }); }
  function chosenSize() { var el = sizeInputs.filter(function (i) { return i.checked; })[0]; return el ? el.value : "any"; }

  function shuffled(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  function pool() {
    var areas = chosenAreas(), size = chosenSize();
    var all = [], i;
    for (i = 0; i < ITEMS.length; i++) if (areas.indexOf(ITEMS[i].area) !== -1) all.push(i);
    if (size === "any") return { ids: all, fallback: false };
    var bySize = all.filter(function (id) { return ITEMS[id].size === size; });
    if (bySize.length >= 3) return { ids: bySize, fallback: false };
    return { ids: all, fallback: true };
  }

  function draw(reset) {
    var p = pool();
    var key = p.ids.join(",");
    if (reset || bag.key !== key) bag = { key: key, order: shuffled(p.ids), pos: 0 };
    var want = Math.min(3, p.ids.length), out = [], guard = 0;
    while (out.length < want && guard++ < 200) {
      if (bag.pos >= bag.order.length) { bag.order = shuffled(p.ids); bag.pos = 0; }
      var id = bag.order[bag.pos++];
      if (out.indexOf(id) === -1) out.push(id);
    }
    drawn = out;
    return p;
  }

  function renderIdeas(p) {
    listEl.innerHTML = "";
    var has = drawn.length > 0;
    emptyEl.hidden = has;
    shuffleBtn.hidden = !has;
    noteEl.hidden = !(has && p && p.fallback);
    if (has && p && p.fallback) {
      var s = chosenSize();
      noteEl.textContent = "There are not many " + SIZE_LABEL[s].toLowerCase() + " ideas in these areas, so we added a few other sizes.";
    }
    drawn.forEach(function (id) {
      var it = ITEMS[id];
      var li = document.createElement("li");
      li.className = "rz-idea" + (id === picked ? " is-picked" : "");
      var txt = document.createElement("div");
      var t = document.createElement("p");
      t.className = "rz-idea-t";
      t.textContent = it.res;
      var tag = document.createElement("span");
      tag.className = "rz-tag rz-tag-" + it.size;
      tag.textContent = SIZE_LABEL[it.size] + " · " + it.areaLabel;
      txt.appendChild(t); txt.appendChild(tag);
      var b = document.createElement("button");
      b.type = "button";
      b.className = "btn small " + (id === picked ? "" : "ghost");
      b.textContent = id === picked ? "Picked" : "Pick this one";
      b.setAttribute("aria-pressed", id === picked ? "true" : "false");
      b.addEventListener("click", function () { pick(id); });
      li.appendChild(txt); li.appendChild(b);
      listEl.appendChild(li);
    });
  }

  function refreshCard() {
    var has = picked !== -1;
    cardEl.classList.toggle("is-empty", !has);
    cardRes.textContent = resIn.value.trim() || "Your resolution goes here";
    cardAff.textContent = affIn.value.trim() || "Your affirmation goes here";
    cardAct.textContent = actIn.value.trim() || "Your weekly action goes here";
    copyBtn.disabled = !has;
    printBtn.disabled = !has;
  }

  function pick(id) {
    picked = id;
    var it = ITEMS[id];
    resIn.value = it.res; affIn.value = it.aff; actIn.value = it.act;
    editPanel.hidden = false;
    renderIdeas(lastPool);
    refreshCard();
    track("website resolution picked", { area: it.area, size: it.size, area_count: chosenAreas().length, size_filter: chosenSize() });
    var narrow = window.matchMedia && matchMedia("(max-width: 900px)").matches;
    if (narrow) cardEl.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    toast("Added to your card");
  }

  function updateAreaState() {
    var chosen = chosenAreas();
    areaInputs.forEach(function (i) { i.disabled = !i.checked && chosen.length >= MAX_AREAS; });
    countEl.textContent = chosen.length + " of " + MAX_AREAS + " chosen";
  }

  function refreshIdeas(reset) {
    updateAreaState();
    if (!chosenAreas().length) { drawn = []; lastPool = null; renderIdeas(null); return; }
    var p = draw(reset);
    lastPool = p;
    renderIdeas(p);
  }

  areaInputs.forEach(function (i) { i.addEventListener("change", function () { refreshIdeas(false); }); });
  sizeInputs.forEach(function (i) { i.addEventListener("change", function () { refreshIdeas(true); }); });
  shuffleBtn.addEventListener("click", function () {
    var p = draw(false);
    lastPool = p;
    renderIdeas(p);
    track("website resolution shuffled", { area_count: chosenAreas().length, size_filter: chosenSize() });
  });
  [resIn, affIn, actIn].forEach(function (el) { el.addEventListener("input", refreshCard); });

  function cardText() {
    return "My 2027 resolution\n" + (resIn.value.trim()) + "\n\nI tell myself: " + affIn.value.trim() +
      "\nEach week: " + actIn.value.trim() + "\n\nWrite it every day for 21 days.\n369journal.app";
  }
  copyBtn.addEventListener("click", function () {
    var text = cardText();
    var done = function () { toast("Copied"); track("website resolution copied", {}); };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text, done); });
    } else { fallbackCopy(text, done); }
  });
  function fallbackCopy(text, done) {
    var ta = document.createElement("textarea");
    ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); done(); } catch (e) { toast("Press and hold to copy the text"); }
    document.body.removeChild(ta);
  }
  printBtn.addEventListener("click", function () {
    track("website resolution printed", {});
    window.print();
  });

  refreshIdeas(true);
  refreshCard();
})();

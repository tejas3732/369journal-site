/* Printable vision board templates. Everything happens in the browser: the sheet is plain
   HTML/CSS and printing uses window.print(), so nothing is uploaded or saved.
   Analytics never include the title or label text, only which template and paper were used. */
(function () {
  "use strict";
  var root = document.querySelector("[data-vt]");
  if (!root) return;

  var $ = function (s) { return root.querySelector(s); };
  var track = function (n, p) { try { if (window.posthog) window.posthog.capture(n, p || {}); } catch (e) {} };
  var toastEl = document.querySelector("[data-toast]");
  var toast = function (msg) {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toast.t); toast.t = setTimeout(function () { toastEl.classList.remove("show"); }, 2200);
  };

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  var QUARTER_SPANS = ["Jan to Mar", "Apr to Jun", "Jul to Sep", "Oct to Dec"];

  function box(label) {
    return '<div class="vt-box">' + (label ? '<span class="vt-lab">' + esc(label) + "</span>" : "") + "</div>";
  }

  function wheel(L) {
    var cx = 100, cy = 100, R = 96, r0 = 20, i, a, rad;
    var s = '<svg viewBox="0 0 200 200" class="vt-wheel" aria-hidden="true">';
    s += '<circle class="vt-w-fill" cx="100" cy="100" r="96"/>';
    s += '<circle class="vt-w-ring" cx="100" cy="100" r="58"/><circle class="vt-w-ring" cx="100" cy="100" r="40"/>';
    for (i = 0; i < 8; i++) {
      rad = (i * 45) * Math.PI / 180;
      s += '<line class="vt-w-spoke" x1="' + (cx + r0 * Math.sin(rad)).toFixed(2) + '" y1="' + (cy - r0 * Math.cos(rad)).toFixed(2) +
        '" x2="' + (cx + R * Math.sin(rad)).toFixed(2) + '" y2="' + (cy - R * Math.cos(rad)).toFixed(2) + '"/>';
    }
    s += '<circle class="vt-w-edge" cx="100" cy="100" r="96"/>';
    s += '<circle class="vt-w-core" cx="100" cy="100" r="' + r0 + '"/><text class="vt-w-core-t" x="100" y="100.5">Me</text>';
    for (i = 0; i < 8; i++) {
      a = (i * 45 + 22.5) * Math.PI / 180;
      s += '<text class="vt-w-t" x="' + (cx + 76 * Math.sin(a)).toFixed(2) + '" y="' + (cy - 76 * Math.cos(a)).toFixed(2) + '">' + esc(L[i]) + "</text>";
    }
    return s + "</svg>";
  }

  var TEMPLATES = [
    {
      id: "grid9", name: "9-box grid",
      desc: "Nine boxes, one for each part of life. Paste, draw or write inside each one.",
      noun: "Box names", labels: ["Career", "Money", "Health", "Love", "Self-love", "Home", "Travel", "Learning", "Joy"], max: 16,
      render: function (L) { return '<div class="vt-grid9">' + L.map(box).join("") + "</div>"; }
    },
    {
      id: "wheel", name: "Life areas wheel",
      desc: "A circle with eight slices. Write a picture or a word in each, and shade how full each area feels.",
      noun: "Slice names", labels: ["Career", "Money", "Health", "Love", "Home", "Friends", "Growth", "Joy"], max: 12,
      render: function (L) { return wheel(L); }
    },
    {
      id: "year", name: "2027 year at a glance",
      desc: "Twelve months, each with lines for one goal and a few steps. Good for a year you want to plan.",
      noun: "", labels: [], max: 0,
      render: function () {
        return '<div class="vt-year">' + MONTHS.map(function (m) {
          return '<div class="vt-month"><b>' + m + '</b><div class="vt-lines"></div></div>';
        }).join("") + "</div>";
      }
    },
    {
      id: "word", name: "One-word focus board",
      desc: "One big word in the middle, four spaces for pictures, and three short lines that explain it.",
      noun: "Your word and 3 lines", labels: ["Brave", "I begin before I feel ready", "I choose it on ordinary days", "I come back when I forget"], max: 40, wordMax: 12,
      render: function (L) {
        return '<div class="vt-one"><div class="vt-one-row">' + box("") + box("") + '</div>' +
          '<div class="vt-one-mid"><p class="vt-word">' + esc(L[0]) + '</p><p class="vt-one-line">' + esc(L[1]) + '</p><p class="vt-one-line">' + esc(L[2]) +
          '</p><p class="vt-one-line">' + esc(L[3]) + '</p></div><div class="vt-one-row">' + box("") + box("") + "</div></div>";
      }
    },
    {
      id: "quarters", name: "Four quarters goals",
      desc: "Four boxes for the four parts of the year, each with a goal line and three steps.",
      noun: "Quarter themes", labels: ["Begin", "Build", "Deepen", "Celebrate"], max: 16,
      render: function (L) {
        return '<div class="vt-quarters">' + L.map(function (l, i) {
          return '<div class="vt-q"><div class="vt-qh"><b>Q' + (i + 1) + '</b><span>' + esc(l) + '</span><small>' + QUARTER_SPANS[i] + '</small></div>' +
            '<p class="vt-qk">My goal</p><div class="vt-lines vt-goal"></div><p class="vt-qk">Three steps</p><div class="vt-lines vt-steps"></div></div>';
        }).join("") + "</div>";
      }
    },
    {
      id: "list", name: "Minimalist list board",
      desc: "Seven clean lines, one for each area. The calm option when a busy board feels like too much.",
      noun: "Line names", labels: ["Career", "Money", "Health", "Love", "Home", "Joy", "Me"], max: 16,
      render: function (L) {
        return '<div class="vt-list">' + L.map(function (l, i) {
          return '<div class="vt-li"><span class="vt-n">' + (i + 1) + '</span><span class="vt-lab">' + esc(l) + "</span></div>";
        }).join("") + "</div>";
      }
    }
  ];

  var PAGE = {
    a4: { portrait: "A4 portrait", landscape: "A4 landscape", css: "A4" },
    letter: { portrait: "US Letter portrait", landscape: "US Letter landscape", css: "letter" }
  };

  var state = {
    tpl: "grid9", paper: "a4", orient: "portrait", style: "warm", title: "My 2027 vision board", mark: true,
    labels: {}
  };
  TEMPLATES.forEach(function (t) { state.labels[t.id] = t.labels.slice(); });

  var wrap = $("[data-vt-wrap]");
  var sheet = $("[data-vt-sheet]");
  var descEl = $("[data-vt-desc]");
  var labelsBox = $("[data-vt-labels]");
  var labelsWrap = $("[data-vt-labels-wrap]");
  var labelsLegend = $("[data-vt-labels-legend]");
  var captionEl = $("[data-vt-caption]");
  var titleInput = $("#vt-title");
  var pageStyle = document.getElementById("vt-page-style");

  function tpl() {
    for (var i = 0; i < TEMPLATES.length; i++) if (TEMPLATES[i].id === state.tpl) return TEMPLATES[i];
    return TEMPLATES[0];
  }
  function checked(name) { var el = root.querySelector("input[name=" + name + "]:checked"); return el ? el.value : null; }

  function setPageRule() {
    if (!pageStyle) return;
    pageStyle.textContent = "@page { size: " + PAGE[state.paper].css + " " + state.orient + "; margin: 8mm; }";
  }

  function renderSheet() {
    var t = tpl();
    var L = state.labels[t.id];
    var html = "";
    if (state.title.trim()) {
      html += '<div class="vt-head"><h2 class="vt-title">' + esc(state.title.trim()) + '</h2><div class="vt-rule"></div></div>';
    }
    html += '<div class="vt-body">' + t.render(L) + "</div>";
    if (state.mark) html += '<p class="vt-foot">369journal.app</p>';
    sheet.innerHTML = html;
    wrap.setAttribute("data-paper", state.paper);
    wrap.setAttribute("data-orient", state.orient);
    wrap.setAttribute("data-style", state.style);
    wrap.setAttribute("data-tpl", t.id);
    wrap.setAttribute("aria-label", "Preview of the " + t.name + " template, " + PAGE[state.paper][state.orient]);
    captionEl.textContent = "Preview: " + t.name + ", " + PAGE[state.paper][state.orient];
    setPageRule();
  }

  function renderLabelInputs() {
    var t = tpl();
    labelsBox.innerHTML = "";
    if (!t.labels.length) { labelsWrap.hidden = true; return; }
    labelsWrap.hidden = false;
    labelsLegend.textContent = t.noun;
    state.labels[t.id].forEach(function (val, i) {
      var id = "vt-label-" + i;
      var row = document.createElement("div");
      row.className = "vt-label-row";
      var lab = document.createElement("label");
      lab.setAttribute("for", id);
      lab.className = "sr-only";
      lab.textContent = t.noun + " " + (i + 1);
      var inp = document.createElement("input");
      inp.type = "text"; inp.id = id; inp.className = "t-input";
      inp.maxLength = (t.wordMax && i === 0) ? t.wordMax : t.max;
      inp.autocomplete = "off";
      inp.value = val;
      inp.addEventListener("input", function () { state.labels[t.id][i] = inp.value; renderSheet(); });
      row.appendChild(lab); row.appendChild(inp);
      labelsBox.appendChild(row);
    });
  }

  function chooseTemplate(id, fromUser) {
    state.tpl = id;
    descEl.textContent = tpl().desc;
    renderLabelInputs();
    renderSheet();
    if (fromUser) track("website vision template chosen", { template: id });
  }

  // ---------- Events ----------
  Array.prototype.forEach.call(root.querySelectorAll("input[name=vt-tpl]"), function (el) {
    el.addEventListener("change", function () { if (el.checked) chooseTemplate(el.value, true); });
  });
  ["vt-paper", "vt-orient", "vt-style"].forEach(function (name) {
    Array.prototype.forEach.call(root.querySelectorAll("input[name=" + name + "]"), function (el) {
      el.addEventListener("change", function () {
        if (!el.checked) return;
        if (name === "vt-paper") state.paper = el.value;
        if (name === "vt-orient") state.orient = el.value;
        if (name === "vt-style") state.style = el.value;
        renderSheet();
      });
    });
  });
  titleInput.addEventListener("input", function () { state.title = titleInput.value; renderSheet(); });
  var markEl = $("#vt-mark");
  markEl.addEventListener("change", function () { state.mark = markEl.checked; renderSheet(); });

  var resetBtn = $("[data-vt-reset]");
  resetBtn.addEventListener("click", function () {
    var t = tpl();
    state.labels[t.id] = t.labels.slice();
    renderLabelInputs();
    renderSheet();
    toast("Names reset");
  });

  var printBtn = $("[data-vt-print]");
  printBtn.addEventListener("click", function () {
    setPageRule();
    track("website vision template printed", { template: state.tpl, paper: state.paper, orientation: state.orient, style: state.style });
    window.print();
  });

  // Start from any saved radio state the browser restored, then draw.
  state.paper = checked("vt-paper") || "a4";
  state.orient = checked("vt-orient") || "portrait";
  state.style = checked("vt-style") || "warm";
  state.tpl = checked("vt-tpl") || "grid9";
  state.title = titleInput.value;
  state.mark = markEl.checked;
  chooseTemplate(state.tpl, false);
})();

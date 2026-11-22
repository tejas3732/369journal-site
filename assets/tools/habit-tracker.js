/* Printable habit tracker builder. Runs entirely in the browser.
   Habits and options are kept in localStorage on this device only.
   Analytics never include habit text. */
(function () {
  "use strict";
  var root = document.querySelector("[data-habit]");
  if (!root) return;

  var KEY = "369j-habit-tracker";
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  var LETTERS = ["S", "M", "T", "W", "T", "F", "S"];
  var SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  var EXAMPLES = {
    morning: ["Drink a glass of water", "Make the bed", "Stretch for 5 minutes", "Write today's top 3", "Phone-free for 30 minutes"],
    health: ["Walk 20 minutes", "Drink 2 litres of water", "Eat a vegetable at every meal", "Lights out by 11pm", "Stretch or move for 10 minutes"],
    money: ["Note every spend", "No impulse buys", "Move a little into savings", "Check my balance", "Cook at home"],
    selfcare: ["10 quiet minutes", "Write 3 lines in my journal", "Screens off 30 minutes before bed", "Do one kind thing for me", "Message a friend"],
    "369": ["Morning 3", "Afternoon 6", "Night 9"]
  };

  var $ = function (s) { return root.querySelector(s); };
  var inputs = [].slice.call(root.querySelectorAll("[data-habit-input]"));
  var sheet = $("[data-sheet]");
  var monthSel = $("[data-month]");
  var titleIn = $("[data-title]");
  var monthHint = $("[data-month-hint]");
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
  function setRadio(name, value) {
    var el = root.querySelector('input[name="' + name + '"][value="' + value + '"]');
    if (el) el.checked = true;
  }

  // ---------- Month list: January 2026 to December 2027 ----------
  var opts = "";
  for (var y = 2026; y <= 2027; y++) for (var m = 0; m < 12; m++) {
    opts += '<option value="' + y + "-" + m + '">' + MONTHS[m] + " " + y + "</option>";
  }
  monthSel.innerHTML = opts;
  monthSel.value = "2027-0";

  // ---------- Saved settings ----------
  function save() {
    try {
      localStorage.setItem(KEY, JSON.stringify({
        habits: inputs.map(function (i) { return i.value; }),
        month: monthSel.value, layout: radio("htlayout"), style: radio("htstyle"), paper: radio("htpaper"), title: titleIn.value
      }));
    } catch (e) {}
  }
  function load() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || "null");
      if (!v || typeof v !== "object") return;
      if (Array.isArray(v.habits)) inputs.forEach(function (i, n) { i.value = typeof v.habits[n] === "string" ? v.habits[n].slice(0, 40) : ""; });
      if (typeof v.month === "string" && monthSel.querySelector('option[value="' + v.month + '"]')) monthSel.value = v.month;
      if (v.layout) setRadio("htlayout", v.layout);
      if (v.style) setRadio("htstyle", v.style);
      if (v.paper) setRadio("htpaper", v.paper);
      if (typeof v.title === "string") titleIn.value = v.title.slice(0, 40);
    } catch (e) {}
  }

  // ---------- Page size for printing ----------
  var pageStyle = document.createElement("style");
  document.head.appendChild(pageStyle);
  function setPage(layout, paper) {
    var size = paper === "letter" ? "letter" : "A4";
    var dir = layout === "week" ? "portrait" : "landscape";
    pageStyle.textContent = "@media print { @page { size: " + size + " " + dir + "; margin: 10mm; } }";
  }

  // ---------- Sheet ----------
  function habits() {
    return inputs.map(function (i) { return i.value.trim(); }).filter(Boolean);
  }

  function dayList(layout) {
    var out = [], i;
    if (layout === "week") {
      for (i = 0; i < 7; i++) out.push({ top: SHORT[i], num: "", we: i >= 5 });
    } else if (layout === "thirty") {
      for (i = 1; i <= 30; i++) out.push({ top: "", num: i, we: false });
    } else {
      var parts = monthSel.value.split("-");
      var yr = +parts[0], mo = +parts[1];
      var count = new Date(yr, mo + 1, 0).getDate();
      for (i = 1; i <= count; i++) {
        var wd = new Date(yr, mo, i).getDay();
        out.push({ top: LETTERS[wd], num: i, we: wd === 0 || wd === 6 });
      }
    }
    return out;
  }

  function lines(n) {
    var s = "";
    for (var i = 0; i < n; i++) s += '<span class="ht-line"></span>';
    return s;
  }

  function render() {
    var layout = radio("htlayout") || "month";
    var style = radio("htstyle") || "minimal";
    var paper = radio("htpaper") || "a4";
    var list = habits();
    var minRows = layout === "week" ? 8 : 8;
    var rows = list.slice();
    while (rows.length < minRows) rows.push("");
    var days = dayList(layout);

    var parts = monthSel.value.split("-");
    var monthLabel = MONTHS[+parts[1]] + " " + parts[0];
    var title = titleIn.value.trim() || "Habit tracker";
    var right = layout === "month" ? esc(monthLabel) : layout === "week" ? 'Week of <span class="ht-blank"></span>' : 'Start date <span class="ht-blank"></span>';

    var colgroup = '<col class="ht-namecol">' + days.map(function () { return "<col>"; }).join("");
    var head1 = '<th class="ht-corner" rowspan="' + (layout === "month" ? 2 : 1) + '" scope="col">Habit</th>';
    var head2 = "";
    if (layout === "month") {
      days.forEach(function (d) { head1 += '<th scope="col" class="ht-wd' + (d.we ? " we" : "") + '">' + d.top + "</th>"; });
      days.forEach(function (d) { head2 += '<th scope="col" class="ht-dn' + (d.we ? " we" : "") + '">' + d.num + "</th>"; });
    } else if (layout === "week") {
      days.forEach(function (d) { head1 += '<th scope="col" class="ht-wd' + (d.we ? " we" : "") + '">' + d.top + "</th>"; });
    } else {
      days.forEach(function (d) { head1 += '<th scope="col" class="ht-dn">' + d.num + "</th>"; });
    }

    var body = rows.map(function (h) {
      var cells = days.map(function (d) { return '<td class="ht-c' + (d.we ? " we" : "") + '"></td>'; }).join("");
      return '<tr><th scope="row" class="ht-name">' + (h ? esc(h) : "") + "</th>" + cells + "</tr>";
    }).join("");

    var below;
    if (layout === "week") {
      below = '<div class="ht-below"><div class="ht-box"><b>One small win this week</b>' + lines(2) + '</div><div class="ht-box"><b>Next week I will</b>' + lines(2) + "</div></div>";
    } else if (layout === "thirty") {
      below = '<div class="ht-below"><div class="ht-box"><b>Notes</b>' + lines(3) + '</div><div class="ht-box"><b>Day 30: how did it go?</b>' + lines(3) + "</div></div>";
    } else {
      below = '<div class="ht-below"><div class="ht-box"><b>Notes</b>' + lines(3) + '</div><div class="ht-box"><b>My win this month</b>' + lines(3) + "</div></div>";
    }

    sheet.className = "ht-sheet is-" + layout + " style-" + style + " paper-" + paper;
    sheet.innerHTML =
      '<div class="ht-title"><h2>' + esc(title) + "</h2><p>" + right + "</p></div>" +
      '<div class="ht-tablewrap"><table class="ht-table"><colgroup>' + colgroup + "</colgroup><thead><tr>" + head1 + "</tr>" +
      (head2 ? "<tr>" + head2 + "</tr>" : "") + "</thead><tbody>" + body + "</tbody></table></div>" +
      below +
      '<p class="ht-foot">Fill one box for each day you do it. Miss a day? Fine. Never miss twice. &middot; 369journal.app</p>';

    if (monthHint) monthHint.hidden = layout === "month";
    monthSel.disabled = layout !== "month";
    setPage(layout, paper);
  }

  function update() { render(); save(); }

  // ---------- Events ----------
  inputs.forEach(function (i) { i.addEventListener("input", update); });
  titleIn.addEventListener("input", update);
  monthSel.addEventListener("change", update);
  root.addEventListener("change", function (e) {
    if (e.target && e.target.type === "radio") update();
  });

  [].forEach.call(root.querySelectorAll("[data-example]"), function (b) {
    b.addEventListener("click", function () {
      var set = EXAMPLES[b.getAttribute("data-example")] || [];
      inputs.forEach(function (i, n) { i.value = set[n] || ""; });
      update();
      toast("Example added. Change any line you like.");
      track("website habit tracker example", { set: b.getAttribute("data-example") });
    });
  });

  var clearBtn = $("[data-clear]");
  if (clearBtn) clearBtn.addEventListener("click", function () {
    inputs.forEach(function (i) { i.value = ""; });
    update();
    inputs[0].focus();
  });

  var printBtn = $("[data-print]");
  if (printBtn) printBtn.addEventListener("click", function () {
    render();
    track("website habit tracker printed", { layout: radio("htlayout"), style: radio("htstyle"), paper: radio("htpaper"), habits: habits().length });
    window.print();
  });

  load();
  render();
})();

/* Letter to your future self.
   Everything stays in the browser: the draft is kept in localStorage on this device only,
   and the letter leaves the page only as a file the visitor downloads or prints.
   Analytics never include the letter text. */
(function () {
  "use strict";
  var root = document.querySelector("[data-letter]");
  if (!root) return;

  var KEY = "letter369-draft";
  var PROMPTS = [
    ["where", "Where are you as you read this?"],
    ["proud", "What I\u2019m proud of right now"],
    ["working", "What I\u2019m working towards"],
    ["letgo", "What I hope you\u2019ve let go of"],
    ["question", "A question for you"],
    ["remember", "Something I want you to remember"],
    ["else", "Anything else"]
  ];

  var $ = function (s) { return root.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(root.querySelectorAll(s)); };
  var toastEl = document.querySelector("[data-toast]");
  var toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove("show"); }, 2200);
  }
  function track(name, props) {
    try { if (window.posthog) window.posthog.capture(name, props || {}); } catch (e) {}
  }

  var modeInputs = $$("input[name=open-on]");
  var customDate = $("#letter-date");
  var customWrap = $("#letter-date-wrap");
  var nameInput = $("#letter-name");
  var fields = {};
  PROMPTS.forEach(function (p) { fields[p[0]] = $("#lp-" + p[0]); });
  var wordsEl = $("#letter-words");
  var started = false;

  var longDate = new Intl.DateTimeFormat(undefined, { day: "numeric", month: "long", year: "numeric" });
  var today = new Date();

  function iso(d) { return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0"); }
  function addMonths(d, m) { var x = new Date(d.getFullYear(), d.getMonth() + m, d.getDate(), 12); return x; }
  function mode() { for (var i = 0; i < modeInputs.length; i++) if (modeInputs[i].checked) return modeInputs[i].value; return "12"; }

  function openDate() {
    var m = mode();
    if (m === "pick") {
      if (customDate.value) return new Date(customDate.value + "T12:00:00");
      return addMonths(today, 12);
    }
    return addMonths(today, parseInt(m, 10));
  }
  function monthsAhead() {
    var d = openDate();
    return Math.max(0, Math.round((d - today) / (1000 * 60 * 60 * 24 * 30.44)));
  }

  // ---------- Letter text ----------
  function sections() {
    return PROMPTS.map(function (p) { return { id: p[0], label: p[1], text: fields[p[0]].value.trim() }; })
      .filter(function (s) { return s.text; });
  }
  function greeting() {
    var n = nameInput.value.trim();
    return "Dear " + (n || "future me") + ",";
  }
  function plainText() {
    var out = [];
    out.push("Written on " + longDate.format(today) + ". To be opened on " + longDate.format(openDate()) + ".");
    out.push("");
    out.push(greeting());
    out.push("");
    sections().forEach(function (s) {
      if (s.id !== "else") out.push(s.label);
      out.push(s.text);
      out.push("");
    });
    out.push("With love,");
    out.push("Me, on " + longDate.format(today));
    return out.join("\n");
  }

  // ---------- Preview ----------
  var pv = {
    written: $("#lv-written"), opens: $("#lv-opens"), greet: $("#lv-greet"),
    body: $("#lv-body"), sign: $("#lv-sign"), empty: $("#lv-empty")
  };
  function render() {
    customWrap.hidden = mode() !== "pick";
    pv.written.textContent = longDate.format(today);
    pv.opens.textContent = longDate.format(openDate());
    pv.greet.textContent = greeting();
    pv.sign.textContent = "Me, on " + longDate.format(today);
    var list = sections();
    pv.body.innerHTML = "";
    list.forEach(function (s) {
      var wrap = document.createElement("section");
      if (s.id !== "else") {
        var h = document.createElement("h3");
        h.textContent = s.label;
        wrap.appendChild(h);
      }
      s.text.split(/\n{2,}/).forEach(function (para) {
        var p = document.createElement("p");
        p.textContent = para;
        wrap.appendChild(p);
      });
      pv.body.appendChild(wrap);
    });
    pv.empty.hidden = list.length > 0;
    var words = list.reduce(function (n, s) { return n + s.text.split(/\s+/).filter(Boolean).length; }, 0);
    wordsEl.textContent = words === 1 ? "1 word" : words + " words";
    $$("[data-filled]").forEach(function (el) {
      var f = fields[el.getAttribute("data-filled")];
      el.classList.toggle("is-filled", !!(f && f.value.trim()));
    });
  }

  // ---------- Draft (this device only) ----------
  function save() {
    try {
      var data = { mode: mode(), date: customDate.value, name: nameInput.value, fields: {} };
      PROMPTS.forEach(function (p) { data.fields[p[0]] = fields[p[0]].value; });
      localStorage.setItem(KEY, JSON.stringify(data));
    } catch (e) {}
  }
  function load() {
    var raw = null;
    try { raw = localStorage.getItem(KEY); } catch (e) {}
    if (!raw) return false;
    try {
      var data = JSON.parse(raw);
      modeInputs.forEach(function (r) { r.checked = r.value === data.mode; });
      if (!modeInputs.some(function (r) { return r.checked; })) modeInputs[1].checked = true;
      customDate.value = data.date || "";
      nameInput.value = data.name || "";
      PROMPTS.forEach(function (p) { fields[p[0]].value = (data.fields && data.fields[p[0]]) || ""; });
      return PROMPTS.some(function (p) { return fields[p[0]].value.trim(); });
    } catch (e) { return false; }
  }
  function clearDraft() {
    try { localStorage.removeItem(KEY); } catch (e) {}
  }

  var saveTimer;
  function onEdit() {
    if (!started) { started = true; track("website letter started"); }
    render();
    clearTimeout(saveTimer);
    saveTimer = setTimeout(save, 300);
  }

  // ---------- Files ----------
  function download(name, text, type) {
    var blob = new Blob([text], { type: type });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1500);
  }

  function icsEscape(s) {
    return s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r?\n/g, "\\n");
  }
  // Fold to 75 octets per line (RFC 5545), never splitting a UTF-8 character.
  function fold(line) {
    var enc = new TextEncoder();
    var out = [], cur = "", bytes = 0, limit = 75;
    Array.from(line).forEach(function (ch) {
      var b = enc.encode(ch).length;
      if (bytes + b > limit) { out.push(cur); cur = " "; bytes = 1; limit = 75; }
      cur += ch; bytes += b;
    });
    out.push(cur);
    return out.join("\r\n");
  }
  function ymd(d) { return iso(d).replace(/-/g, ""); }
  function stamp(d) { return d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, ""); }
  function buildIcs() {
    var start = openDate();
    var end = new Date(start); end.setDate(end.getDate() + 1);
    var uid = "letter-" + Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 8) + "@369journal.app";
    var desc = "A letter from your past self, written on " + longDate.format(today) + ".\n\n" + plainText() +
      "\n\nWritten with the free tool at https://369journal.app/letter-to-future-self/";
    var lines = [
      "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//369 Journal//Letter to your future self//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
      "BEGIN:VEVENT",
      "UID:" + uid,
      "DTSTAMP:" + stamp(new Date()),
      "DTSTART;VALUE=DATE:" + ymd(start),
      "DTEND;VALUE=DATE:" + ymd(end),
      "SUMMARY:" + icsEscape("Open the letter from your past self"),
      "DESCRIPTION:" + icsEscape(desc),
      "TRANSP:TRANSPARENT",
      "BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER:PT9H", "DESCRIPTION:" + icsEscape("Open the letter from your past self"), "END:VALARM",
      "END:VEVENT", "END:VCALENDAR"
    ];
    return lines.map(fold).join("\r\n") + "\r\n";
  }
  root.__buildIcs = buildIcs; // for testing in the console only

  function hasText() { return sections().length > 0; }

  $("#letter-print").addEventListener("click", function () {
    if (!hasText()) { toast("Write a few lines first"); return; }
    track("website letter printed");
    window.print();
  });
  $("#letter-ics").addEventListener("click", function () {
    if (!hasText()) { toast("Write a few lines first"); return; }
    download("letter-to-future-self-" + iso(openDate()) + ".ics", buildIcs(), "text/calendar;charset=utf-8");
    track("website letter calendar added", { months: monthsAhead() });
    toast("Calendar file saved. Open it to add the reminder.");
  });
  $("#letter-txt").addEventListener("click", function () {
    if (!hasText()) { toast("Write a few lines first"); return; }
    download("letter-to-future-self.txt", plainText() + "\n", "text/plain;charset=utf-8");
    track("website letter downloaded");
    toast("Letter saved as a text file");
  });
  $("#letter-reset").addEventListener("click", function () {
    if (!window.confirm("Clear your letter and start over? This can\u2019t be undone.")) return;
    clearDraft();
    nameInput.value = "";
    PROMPTS.forEach(function (p) { fields[p[0]].value = ""; });
    modeInputs.forEach(function (r) { r.checked = r.value === "12"; });
    customDate.value = "";
    render();
    toast("Started a fresh letter");
  });

  // Wire up
  modeInputs.forEach(function (r) {
    r.addEventListener("change", function () {
      if (r.value === "pick" && !customDate.value) customDate.value = iso(addMonths(today, 12));
      onEdit();
      if (r.value === "pick") customDate.focus();
    });
  });
  [customDate, nameInput].concat(PROMPTS.map(function (p) { return fields[p[0]]; })).forEach(function (el) {
    el.addEventListener("input", onEdit);
    el.addEventListener("change", onEdit);
  });

  customDate.min = iso(new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1));
  if (load()) {
    started = true;
    // Open every prompt that already has words in it.
    $$("details.lp").forEach(function (d) {
      var f = d.querySelector("textarea");
      if (f && f.value.trim()) d.open = true;
    });
    var note = $("#letter-restored");
    if (note) note.hidden = false;
  }
  render();
})();

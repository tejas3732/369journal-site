/* Affirmation wallpaper maker. Renders on <canvas> in the browser; nothing is uploaded.
   Analytics never include the affirmation text. */
(function () {
  "use strict";
  var root = document.querySelector("[data-wallpaper]");
  if (!root) return;

  var $ = function (s) { return root.querySelector(s); };
  var canvas = $("#wp-canvas");
  var ctx = canvas.getContext("2d");
  var device = $("#wp-device");
  var textEl = $("#wp-text");
  var countEl = $("#wp-count");
  var toastEl = document.querySelector("[data-toast]");

  var SIZES = {
    iphone: { w: 1179, h: 2556, label: "iPhone" },
    android: { w: 1080, h: 2400, label: "Android" },
    desktop: { w: 2560, h: 1440, label: "Desktop" }
  };

  var SERIF = "'New York', 'Iowan Old Style', 'Palatino', Georgia, serif";
  var SANS = "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif";

  var STYLES = {
    paper: { tone: "dark", font: "serif", text: "#1c1814", mark: "rgba(28,24,20,0.42)",
      bg: function (w, h) { fill(w, h, "#f6efe4"); radial(w, h, "rgba(255,252,246,0.9)", "rgba(246,239,228,0)"); },
      deco: function (box, w) { rule(box, w, "#b05933", 0.11); } },
    midnight: { tone: "light", font: "serif", text: "#e8cd97", mark: "rgba(232,205,151,0.4)",
      bg: function (w, h) { linear(w, h, 0, 0, 0, h, [[0, "#1c1814"], [0.55, "#1a1d26"], [1, "#151c2c"]]); radial(w, h, "rgba(232,205,151,0.08)", "rgba(232,205,151,0)"); },
      deco: function (box, w) { rule(box, w, "rgba(232,205,151,0.75)", 0.08); } },
    dusk: { tone: "dark", font: "serif", text: "#2a2230", mark: "rgba(42,34,48,0.4)",
      bg: function (w, h) { linear(w, h, 0, 0, w, h, [[0, "#f8dcc6"], [0.5, "#efd3d6"], [1, "#d8c8e8"]]); },
      deco: function () {} },
    sage: { tone: "light", font: "serif", text: "#f6efe4", mark: "rgba(246,239,228,0.5)",
      bg: function (w, h) { linear(w, h, 0, 0, 0, h, [[0, "#8a9b84"], [1, "#66796a"]]); radial(w, h, "rgba(255,255,255,0.12)", "rgba(255,255,255,0)"); },
      deco: function (box, w) { rule(box, w, "rgba(246,239,228,0.7)", 0.08); } },
    minimal: { tone: "light", font: "sans", text: "#ffffff", mark: "rgba(255,255,255,0.38)",
      bg: function (w, h) { fill(w, h, "#000000"); },
      deco: function () {} },
    dots: { tone: "dark", font: "serif", text: "#1c1814", mark: "rgba(28,24,20,0.42)",
      bg: function (w, h) { fill(w, h, "#f6efe4"); radial(w, h, "rgba(255,252,246,0.9)", "rgba(246,239,228,0)"); },
      deco: function (box, w, h) { dotsMotif(box, w, h); }, decoAbove: true }
  };

  var IDEAS = [
    "Money comes to me easily and often.",
    "I am calm and secure with money.",
    "My savings grow every month.",
    "I am paid well for work I love.",
    "I give and receive love easily.",
    "I am loved, chosen and safe.",
    "My heart is open and at peace.",
    "I am enough exactly as I am.",
    "I trust myself.",
    "I speak to myself with kindness.",
    "I keep the promises I make to myself.",
    "I am proud of how far I have come.",
    "I am calm, clear and steady.",
    "Peace is my natural state.",
    "I breathe slowly and let it go.",
    "My body is strong and full of energy.",
    "I sleep deeply and wake up rested.",
    "I move my body with joy.",
    "Opportunities find me, and I am ready.",
    "I finish what I start.",
    "My work matters, and it shows.",
    "I am becoming who I want to be.",
    "2027 is my calmest, boldest year.",
    "In 2027 I keep my promises to myself.",
    "Good things are on their way to me.",
    "I am exactly where I need to be.",
    "Everything I need is already within me.",
    "I choose ease today.",
    "Small steps every day. Big change this year.",
    "I am open to what is meant for me."
  ];

  var state = { style: "paper", font: "serif", pos: "middle", size: "iphone", mark: true };
  var madeSent = false;
  var lastIdea = -1;

  /* ---------- drawing helpers ---------- */
  function fill(w, h, c) { ctx.fillStyle = c; ctx.fillRect(0, 0, w, h); }
  function linear(w, h, x0, y0, x1, y1, stops) {
    var g = ctx.createLinearGradient(x0, y0, x1, y1);
    stops.forEach(function (s) { g.addColorStop(s[0], s[1]); });
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  }
  function radial(w, h, inner, outer) {
    var g = ctx.createRadialGradient(w / 2, h * 0.45, 0, w / 2, h * 0.45, Math.max(w, h) * 0.6);
    g.addColorStop(0, inner); g.addColorStop(1, outer);
    ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
  }
  function rule(box, w, color, frac) {
    var len = w * frac, y = box.bottom + box.lineH * 0.55;
    ctx.fillStyle = color;
    ctx.fillRect((w - len) / 2, y, len, Math.max(2, w * 0.0022));
  }
  function dotsMotif(box, w) {
    var r = w * 0.0125, gap = r * 3.1;
    var rows = [[3, "#b05933"], [6, "#c7943f"], [9, "#1c1814"]];
    var rowGap = r * 3.2;
    var top = box.top - box.lineH * 0.85 - rowGap * 2 - r;
    rows.forEach(function (row, i) {
      var n = row[0], total = (n - 1) * gap;
      var x0 = (w - total) / 2, y = top + i * rowGap;
      ctx.fillStyle = row[1];
      for (var k = 0; k < n; k++) { ctx.beginPath(); ctx.arc(x0 + k * gap, y, r, 0, Math.PI * 2); ctx.fill(); }
    });
  }

  function fontString(px) {
    return state.font === "serif" ? "500 " + px + "px " + SERIF : "600 " + px + "px " + SANS;
  }

  // Greedy wrap at width, then shrink the width to balance line lengths.
  function wrap(words, maxW) {
    var lines = [], line = "";
    for (var i = 0; i < words.length; i++) {
      var test = line ? line + " " + words[i] : words[i];
      if (ctx.measureText(test).width <= maxW || !line) line = test;
      else { lines.push(line); line = words[i]; }
    }
    if (line) lines.push(line);
    return lines;
  }
  function balanced(words, maxW) {
    var base = wrap(words, maxW);
    if (base.length < 2) return base;
    var lo = maxW * 0.45, hi = maxW, best = base;
    for (var i = 0; i < 14; i++) {
      var mid = (lo + hi) / 2, t = wrap(words, mid);
      if (t.length <= base.length && widest(t) <= mid + 0.5) { best = t; hi = mid; } else lo = mid;
    }
    return best;
  }
  function widest(lines) { var m = 0; lines.forEach(function (l) { m = Math.max(m, ctx.measureText(l).width); }); return m; }

  function layoutText(text, w, h) {
    var portrait = h > w;
    var maxW = w * (portrait ? 0.76 : 0.56);
    var maxH = h * (portrait ? 0.34 : 0.5);
    var words = text.split(/\s+/).filter(Boolean);
    var size = Math.round((portrait ? w : h) * (portrait ? 0.088 : 0.085));
    var min = Math.round((portrait ? w : h) * 0.034);
    var lines, lineH;
    var lh = state.font === "serif" ? 1.24 : 1.18;
    while (true) {
      ctx.font = fontString(size);
      lines = balanced(words, maxW);
      lineH = size * lh;
      var tooWide = widest(lines) > maxW + 1;
      if ((lines.length * lineH <= maxH && lines.length <= 7 && !tooWide) || size <= min) break;
      size = Math.max(min, Math.round(size * 0.94));
    }
    var center = portrait ? (state.pos === "lower" ? h * 0.69 : h * 0.555) : (state.pos === "lower" ? h * 0.62 : h * 0.5);
    var blockH = lines.length * lineH;
    var top = center - blockH / 2;
    return { lines: lines, size: size, lineH: lineH, top: top, bottom: top + blockH };
  }

  function render() {
    var sz = SIZES[state.size], st = STYLES[state.style];
    var w = sz.w, h = sz.h;
    if (canvas.width !== w) canvas.width = w;
    if (canvas.height !== h) canvas.height = h;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, w, h);
    st.bg(w, h);

    var text = (textEl.value || "").trim() || textEl.placeholder;
    var box = layoutText(text, w, h);
    ctx.font = fontString(box.size);
    ctx.fillStyle = st.text;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    if ("letterSpacing" in ctx) ctx.letterSpacing = state.font === "serif" ? "0px" : "-" + Math.round(box.size * 0.01) + "px";
    box.lines.forEach(function (l, i) { ctx.fillText(l, w / 2, box.top + box.lineH * (i + 0.5)); });
    if ("letterSpacing" in ctx) ctx.letterSpacing = "0px";
    st.deco(box, w, h);

    if (state.mark) {
      var mp = Math.round(Math.min(w, h) * (h > w ? 0.022 : 0.016));
      ctx.font = "500 " + mp + "px " + SANS;
      ctx.fillStyle = st.mark;
      ctx.textBaseline = "alphabetic";
      ctx.fillText("369journal.app", w / 2, h - (h > w ? h * 0.045 : h * 0.06));
    }
    device.dataset.size = state.size;
    device.dataset.tone = st.tone;
  }

  /* ---------- UI ---------- */
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toast.t);
    toast.t = setTimeout(function () { toastEl.classList.remove("show"); }, 1800);
  }
  function track(name, props) { try { if (window.posthog) window.posthog.capture(name, props); } catch (e) {} }
  function made() {
    if (madeSent) return;
    madeSent = true;
    track("website wallpaper made", { style: state.style, size: state.size });
  }

  function updateCount() { countEl.textContent = textEl.value.length + " / " + textEl.maxLength; }

  function setRadio(name, value) {
    var el = root.querySelector('input[name="' + name + '"][value="' + value + '"]');
    if (el) el.checked = true;
  }

  root.addEventListener("change", function (e) {
    var t = e.target;
    if (t.name === "wp-style") {
      state.style = t.value;
      state.font = STYLES[t.value].font;
      setRadio("wp-font", state.font);
    } else if (t.name === "wp-font") state.font = t.value;
    else if (t.name === "wp-pos") state.pos = t.value;
    else if (t.name === "wp-size") state.size = t.value;
    else if (t.id === "wp-mark") state.mark = t.checked;
    else return;
    render(); made();
  });

  var raf = 0;
  textEl.addEventListener("input", function () {
    updateCount();
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function () { render(); made(); });
  });

  $("#wp-inspire").addEventListener("click", function () {
    var i;
    do { i = Math.floor(Math.random() * IDEAS.length); } while (i === lastIdea);
    lastIdea = i;
    textEl.value = IDEAS[i];
    updateCount(); render(); made();
  });

  function getBlob(cb) {
    render();
    canvas.toBlob(function (blob) { cb(blob); }, "image/png");
  }

  $("#wp-download").addEventListener("click", function () {
    getBlob(function (blob) {
      if (!blob) return;
      var url = URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url; a.download = "affirmation-wallpaper.png";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
      toast("Wallpaper downloaded");
      track("website wallpaper downloaded", { style: state.style, size: state.size, method: "download" });
    });
  });

  var shareBtn = $("#wp-share");
  try {
    var probe = new File([new Blob(["x"], { type: "image/png" })], "probe.png", { type: "image/png" });
    if (navigator.canShare && navigator.canShare({ files: [probe] })) shareBtn.hidden = false;
  } catch (e) {}
  shareBtn.addEventListener("click", function () {
    getBlob(function (blob) {
      if (!blob) return;
      var file = new File([blob], "affirmation-wallpaper.png", { type: "image/png" });
      navigator.share({ files: [file] }).then(function () {
        track("website wallpaper downloaded", { style: state.style, size: state.size, method: "share" });
      }).catch(function () {});
    });
  });

  // Faux lock screen clock + date for the preview only.
  var timeEl = $("#wp-time"), dateEl = $("#wp-date");
  function tick() {
    var now = new Date();
    timeEl.textContent = now.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }).replace(/\s?[AP]M$/i, "");
    dateEl.textContent = now.toLocaleDateString([], { weekday: "long", day: "numeric", month: "long" });
  }
  tick(); setInterval(tick, 30000);

  updateCount();
  render();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(render);
})();

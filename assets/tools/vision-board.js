/* Free vision board maker. Everything happens in the browser: photos are read
   locally with FileReader-free object URLs and never uploaded. The same render()
   draws the live preview (scaled down) and the full-size export. */
(function () {
  "use strict";
  var root = document.querySelector("[data-vision]");
  if (!root) return;

  var $ = function (s) { return root.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(root.querySelectorAll(s)); };
  var track = function (n, p) { try { if (window.posthog) window.posthog.capture(n, p || {}); } catch (e) {} };
  var toastEl = document.querySelector("[data-toast]");
  var toast = function (msg) {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(toast.t); toast.t = setTimeout(function () { toastEl.classList.remove("show"); }, 1800);
  };

  var SERIF = '"Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif';
  var SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';

  var FORMATS = {
    phone: { w: 1179, h: 2556, label: "Phone wallpaper", clock: true },
    print: { w: 1800, h: 2700, label: "Print or Pinterest" },
    desktop: { w: 2560, h: 1440, label: "Desktop" },
    square: { w: 2160, h: 2160, label: "Square" }
  };

  // Portrait layouts on a cols x rows grid: [col, row, colSpan, rowSpan].
  var LAYOUTS = {
    mosaic: { cols: 3, rows: 4, cells: [[0, 0, 2, 2], [2, 0, 1, 1], [2, 1, 1, 1], [0, 2, 1, 1], [1, 2, 2, 1], [0, 3, 1, 1], [1, 3, 1, 1], [2, 3, 1, 1]] },
    grid: { cols: 2, rows: 3, cells: [[0, 0, 1, 1], [1, 0, 1, 1], [0, 1, 1, 1], [1, 1, 1, 1], [0, 2, 1, 1], [1, 2, 1, 1]] },
    focus: { cols: 3, rows: 4, cells: [[0, 0, 3, 2], [0, 2, 1, 1], [1, 2, 1, 1], [2, 2, 1, 1], [0, 3, 3, 1]] }
  };

  var THEMES = {
    paper: { bg: "#f6efe6", tiles: ["#ead9c6", "#e3cdb4", "#f0e4d6"], text: "#1c1814", sub: "#7a6a5a", accent: "#b05933", dots: ["#b05933", "#c7943f", "#1c1814"] },
    midnight: { bg: "#14131a", tiles: ["#23212b", "#2b2833", "#1d1c24"], text: "#f3e7cf", sub: "#b9a98c", accent: "#d9b46a", dots: ["#d98a5f", "#d9b46a", "#f3e7cf"] },
    sage: { bg: "#e8ece2", tiles: ["#d3dccb", "#c7d3bd", "#dde4d6"], text: "#25301f", sub: "#5f6b56", accent: "#6c7f5a", dots: ["#b05933", "#c7943f", "#25301f"] },
    blush: { bg: "#f7ebe7", tiles: ["#efd6cf", "#e8c7be", "#f3e0db"], text: "#3f2522", sub: "#8a6560", accent: "#b9655a", dots: ["#b9655a", "#c7943f", "#3f2522"] },
    mono: { bg: "#fbfbfa", tiles: ["#efefed", "#e6e6e3", "#f5f5f3"], text: "#111111", sub: "#6b6b6b", accent: "#111111", dots: ["#111111", "#777777", "#111111"] }
  };

  var WORDS = {
    "2027": ["My best year yet", "Promises kept", "Calm mornings", "Growing every day", "Brave choices", "Joy in small things", "Healthy and strong", "Proud of me"],
    money: ["Savings growing", "Paid well for good work", "Debt-free", "Financially calm", "Generous", "A cushion for a rainy day", "Smart with money", "Abundance"],
    love: ["Kind, steady love", "Loved as I am", "Deep friendships", "Slow Sunday mornings", "Laughing together", "Open heart", "Family dinners", "Chosen and cherished"],
    health: ["Strong body", "Morning runs", "Deep sleep", "Energy all day", "Fresh food", "Stretch and breathe", "Feeling light", "Rest without guilt"],
    career: ["Work I love", "Confident voice", "Promoted", "Creative work shipped", "Respected and paid well", "Learning every week", "My own studio", "Doing it my way"],
    home: ["A home full of light", "My own space", "Plants on the windowsill", "A quiet desk", "Friends over for dinner", "Calm and tidy", "Home by the sea", "Cosy evenings"],
    calm: ["Calm mind", "Slow mornings", "Peace", "Breathe", "Phone down, eyes up", "Gentle with myself", "Quiet walks", "Enough"],
    travel: ["Japan in spring", "Sea air", "New cities", "Passport stamps", "Mountain mornings", "Road trip", "Sunsets abroad", "Say yes to adventure"]
  };

  var MAX_TILES = 8;
  var state = {
    format: "phone", layout: "mosaic", theme: "paper",
    title: "2027", subtitle: "The year it comes together", mark: true,
    tiles: WORDS["2027"].map(function (t) { return { text: t, img: null, url: null }; })
  };

  var canvas = $("#vb-canvas");
  var ctx = canvas.getContext("2d");
  var lastRects = [];
  var previewScale = 1;

  // ---------- geometry ----------
  function layoutFor(fmt) {
    var base = LAYOUTS[state.layout];
    if (fmt.w > fmt.h) {
      return { cols: base.rows, rows: base.cols, cells: base.cells.map(function (c) { return [c[1], c[0], c[3], c[2]]; }) };
    }
    return base;
  }

  function frame(W, H, fmt) {
    var u = Math.min(W, H);
    var m = u * 0.06, g = u * 0.018;
    var hasTitle = !!(state.title.trim() || state.subtitle.trim());
    var top = m, bottom = H - m, titleBox = null;
    if (fmt.clock) {
      top = H * 0.3; // keep the lock-screen clock clear
      if (hasTitle) { titleBox = { x: m, y: H - m - H * 0.12, w: W - 2 * m, h: H * 0.12, place: "bottom" }; bottom = titleBox.y - g * 1.5; }
    } else if (hasTitle) {
      var th = fmt.w > fmt.h ? H * 0.17 : H * 0.13;
      titleBox = { x: m, y: m, w: W - 2 * m, h: th, place: "top" };
      top = m + th + g;
    }
    if (state.mark) bottom -= u * 0.03;
    return { m: m, g: g, u: u, content: { x: m, y: top, w: W - 2 * m, h: bottom - top }, titleBox: titleBox };
  }

  function rectsFor(W, H, fmt) {
    var f = frame(W, H, fmt);
    var L = layoutFor(fmt), c = f.content, g = f.g;
    var cw = (c.w - g * (L.cols - 1)) / L.cols, ch = (c.h - g * (L.rows - 1)) / L.rows;
    return {
      f: f,
      rects: L.cells.map(function (cell) {
        return { x: c.x + cell[0] * (cw + g), y: c.y + cell[1] * (ch + g), w: cell[2] * cw + (cell[2] - 1) * g, h: cell[3] * ch + (cell[3] - 1) * g };
      })
    };
  }

  // ---------- drawing helpers ----------
  function rr(c, x, y, w, h, r) {
    c.beginPath();
    if (c.roundRect) { c.roundRect(x, y, w, h, r); return; }
    c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r);
    c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath();
  }

  function wrap(c, text, maxW) {
    var words = text.split(/\s+/).filter(Boolean), lines = [], line = "";
    words.forEach(function (w) {
      var test = line ? line + " " + w : w;
      if (c.measureText(test).width <= maxW || !line) line = test; else { lines.push(line); line = w; }
    });
    if (line) lines.push(line);
    return lines;
  }

  function fit(c, text, maxW, maxH, maxSize, minSize, family, weight, lh) {
    for (var s = maxSize; s >= minSize; s -= Math.max(1, s * 0.06)) {
      c.font = weight + " " + Math.round(s) + "px " + family;
      var lines = wrap(c, text, maxW);
      var widest = Math.max.apply(null, lines.map(function (l) { return c.measureText(l).width; }));
      if (lines.length * s * lh <= maxH && widest <= maxW) return { size: Math.round(s), lines: lines };
    }
    c.font = weight + " " + Math.round(minSize) + "px " + family;
    return { size: Math.round(minSize), lines: wrap(c, text, maxW) };
  }

  function drawText(c, text, box, opts) {
    var r = fit(c, text, box.w, box.h, opts.max, opts.min, opts.family, opts.weight, opts.lh);
    c.fillStyle = opts.color; c.textAlign = "center"; c.textBaseline = "middle";
    var total = r.lines.length * r.size * opts.lh;
    var y0 = box.y + box.h / 2 - total / 2 + (r.size * opts.lh) / 2;
    r.lines.forEach(function (l, i) { c.fillText(l, box.x + box.w / 2, y0 + i * r.size * opts.lh); });
  }

  function cover(c, img, x, y, w, h) {
    var ir = img.width / img.height, br = w / h, sw, sh, sx, sy;
    if (ir > br) { sh = img.height; sw = sh * br; sx = (img.width - sw) / 2; sy = 0; }
    else { sw = img.width; sh = sw / br; sx = 0; sy = (img.height - sh) / 2; }
    c.drawImage(img, sx, sy, sw, sh, x, y, w, h);
  }

  function dots(c, x, y, size, gap, colors) {
    [3, 6, 9].forEach(function (n, row) {
      for (var i = 0; i < n; i++) {
        c.fillStyle = colors[row];
        c.beginPath(); c.arc(x + i * (size + gap) + size / 2, y + row * (size + gap) + size / 2, size / 2, 0, Math.PI * 2); c.fill();
      }
    });
  }

  // ---------- render ----------
  function render(c, W, H, preview) {
    var fmt = FORMATS[state.format], T = THEMES[state.theme];
    var geo = rectsFor(W, H, fmt), f = geo.f, u = f.u;
    c.clearRect(0, 0, W, H);
    c.fillStyle = T.bg; c.fillRect(0, 0, W, H);

    geo.rects.forEach(function (r, i) {
      var tile = state.tiles[i] || { text: "", img: null };
      var rad = u * 0.024;
      c.save();
      rr(c, r.x, r.y, r.w, r.h, rad); c.clip();
      if (tile.img) {
        cover(c, tile.img, r.x, r.y, r.w, r.h);
        if (tile.text.trim()) {
          var gh = Math.min(r.h * 0.55, u * 0.28);
          var grad = c.createLinearGradient(0, r.y + r.h - gh, 0, r.y + r.h);
          grad.addColorStop(0, "rgba(0,0,0,0)"); grad.addColorStop(1, "rgba(0,0,0,0.55)");
          c.fillStyle = grad; c.fillRect(r.x, r.y + r.h - gh, r.w, gh);
          var pad = Math.min(r.w, r.h) * 0.08;
          drawText(c, tile.text.trim(), { x: r.x + pad, y: r.y + r.h - gh * 0.62, w: r.w - pad * 2, h: gh * 0.5 },
            { max: u * 0.05, min: u * 0.018, family: SERIF, weight: "600", lh: 1.15, color: "#fffaf3" });
        }
      } else {
        c.fillStyle = T.tiles[i % T.tiles.length]; c.fillRect(r.x, r.y, r.w, r.h);
        if (tile.text.trim()) {
          var p2 = Math.min(r.w, r.h) * 0.12;
          drawText(c, tile.text.trim(), { x: r.x + p2, y: r.y + p2, w: r.w - p2 * 2, h: r.h - p2 * 2 },
            { max: Math.min(r.h * 0.26, u * 0.085), min: u * 0.016, family: SERIF, weight: "600", lh: 1.12, color: T.text });
        } else if (preview) {
          c.fillStyle = T.sub; c.globalAlpha = 0.65;
          drawText(c, "+ photo or words", { x: r.x + 8, y: r.y + 8, w: r.w - 16, h: r.h - 16 },
            { max: u * 0.03, min: u * 0.014, family: SANS, weight: "500", lh: 1.2, color: T.sub });
          c.globalAlpha = 1;
        }
      }
      c.restore();
    });

    if (f.titleBox) {
      var tb = f.titleBox, title = state.title.trim(), sub = state.subtitle.trim();
      var dotSize = u * 0.012, dotGap = dotSize * 0.7;
      var titleH = sub ? tb.h * 0.62 : tb.h * 0.85;
      if (title) drawText(c, title, { x: tb.x, y: tb.y + (sub ? 0 : tb.h * 0.07), w: tb.w, h: titleH },
        { max: u * 0.12, min: u * 0.03, family: SERIF, weight: "700", lh: 1.05, color: T.text });
      if (sub) drawText(c, sub, { x: tb.x, y: tb.y + titleH, w: tb.w, h: tb.h - titleH },
        { max: u * 0.034, min: u * 0.016, family: SANS, weight: "500", lh: 1.2, color: T.sub });
      if (!fmt.clock) dots(c, tb.x, tb.y + tb.h * 0.08, dotSize, dotGap, T.dots);
    }
    if (state.mark) {
      c.font = "500 " + Math.round(u * 0.016) + "px " + SANS;
      c.fillStyle = T.sub; c.globalAlpha = 0.7; c.textAlign = "center"; c.textBaseline = "alphabetic";
      c.fillText("369journal.app", W / 2, H - f.m * 0.45);
      c.globalAlpha = 1;
    }
    return geo.rects;
  }

  function drawPreview() {
    var fmt = FORMATS[state.format];
    var stage = $(".preview-stage");
    var maxW = Math.min(stage.clientWidth - 32, 720);
    var maxH = Math.min(window.innerHeight * 0.68, 760);
    var s = Math.min(maxW / fmt.w, maxH / fmt.h);
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    previewScale = s;
    canvas.width = Math.round(fmt.w * s * dpr); canvas.height = Math.round(fmt.h * s * dpr);
    canvas.style.width = Math.round(fmt.w * s) + "px"; canvas.style.height = Math.round(fmt.h * s) + "px";
    ctx.setTransform(s * dpr, 0, 0, s * dpr, 0, 0);
    lastRects = render(ctx, fmt.w, fmt.h, true);
    $("#vb-size").textContent = fmt.label + " · " + fmt.w + " × " + fmt.h;
    root.classList.toggle("is-phone", !!fmt.clock);
  }

  var raf = 0;
  function update() { cancelAnimationFrame(raf); raf = requestAnimationFrame(drawPreview); }

  // ---------- tile editor ----------
  var list = $("#vb-tiles");
  function tileCount() { return LAYOUTS[state.layout].cells.length; }

  function buildTiles() {
    var n = tileCount();
    while (state.tiles.length < MAX_TILES) state.tiles.push({ text: "", img: null, url: null });
    list.innerHTML = "";
    for (var i = 0; i < n; i++) list.appendChild(tileRow(i));
  }

  function tileRow(i) {
    var t = state.tiles[i];
    var li = document.createElement("li");
    li.className = "vb-tile" + (t.img ? " has-photo" : "");
    li.dataset.index = i;
    li.innerHTML =
      '<span class="vb-thumb" aria-hidden="true">' + (t.url ? '<img alt="" src="' + t.url + '">' : '<b>' + (i + 1) + "</b>") + "</span>" +
      '<input class="t-input" type="text" maxlength="48" aria-label="Words for tile ' + (i + 1) + '" placeholder="' + (t.img ? "Caption (optional)" : "Words, or add a photo") + '">' +
      '<label class="vb-photo btn ghost small"><input type="file" accept="image/*" hidden>' + (t.img ? "Change" : "Photo") + "</label>" +
      (t.img || t.text ? '<button type="button" class="vb-clear" aria-label="Clear tile ' + (i + 1) + '">×</button>' : "");
    var input = li.querySelector(".t-input");
    input.value = t.text;
    input.addEventListener("input", function () { t.text = input.value; update(); });
    li.querySelector("input[type=file]").addEventListener("change", function (e) {
      if (e.target.files[0]) loadPhoto(e.target.files[0], i);
    });
    var clear = li.querySelector(".vb-clear");
    if (clear) clear.addEventListener("click", function () {
      if (t.url) URL.revokeObjectURL(t.url);
      state.tiles[i] = { text: "", img: null, url: null };
      buildTiles(); update();
    });
    return li;
  }

  function loadPhoto(file, i, quiet) {
    if (!/^image\//.test(file.type)) return;
    var url = URL.createObjectURL(file);
    var img = new Image();
    img.onload = function () {
      var t = state.tiles[i];
      if (t.url) URL.revokeObjectURL(t.url);
      state.tiles[i] = { text: t.img ? t.text : "", img: img, url: url };
      buildTiles(); update();
      if (!quiet) toast("Photo added");
    };
    img.onerror = function () { URL.revokeObjectURL(url); toast("That image could not be opened"); };
    img.src = url;
  }

  function addMany(files, startAt) {
    var n = tileCount(), slots = [];
    for (var i = 0; i < n; i++) if (!state.tiles[i].img) slots.push(i);
    if (startAt != null) slots.sort(function (a, b) { return (a === startAt ? -1 : 0) - (b === startAt ? -1 : 0); });
    var arr = Array.prototype.slice.call(files).filter(function (f) { return /^image\//.test(f.type); });
    arr.slice(0, slots.length).forEach(function (f, k) { loadPhoto(f, slots[k], true); });
    if (arr.length) toast(Math.min(arr.length, slots.length) + " photo" + (arr.length > 1 ? "s" : "") + " added");
    if (arr.length > slots.length) setTimeout(function () { toast("Board is full. Clear a tile to add more"); }, 1900);
  }

  $("#vb-multi").addEventListener("change", function (e) { addMany(e.target.files); e.target.value = ""; });

  // Words presets fill tiles without photos.
  $$("[data-words]").forEach(function (b) {
    b.addEventListener("click", function () {
      var r = { value: b.getAttribute("data-words") };
      $$("[data-words]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var words = WORDS[r.value].slice(), n = tileCount(), k = 0;
      for (var i = 0; i < n; i++) {
        if (!state.tiles[i].img) state.tiles[i].text = words[k++ % words.length];
      }
      if (r.value === "2027" && !state.title.trim()) state.title = "2027";
      buildTiles(); update();
      track("website vision board words", { set: r.value });
    });
  });

  // ---------- preview interactions: click a tile to edit it, drop photos on it ----------
  function tileAt(evt) {
    var b = canvas.getBoundingClientRect();
    var x = (evt.clientX - b.left) / previewScale, y = (evt.clientY - b.top) / previewScale;
    for (var i = 0; i < lastRects.length; i++) {
      var r = lastRects[i];
      if (x >= r.x && x <= r.x + r.w && y >= r.y && y <= r.y + r.h) return i;
    }
    return -1;
  }
  canvas.addEventListener("click", function (e) {
    var i = tileAt(e);
    if (i < 0) return;
    var row = list.querySelector('[data-index="' + i + '"]');
    if (!row) return;
    row.classList.remove("flash"); void row.offsetWidth; row.classList.add("flash");
    row.querySelector(".t-input").focus({ preventScroll: true });
    if (window.innerWidth < 900) row.scrollIntoView({ block: "center", behavior: "smooth" });
  });
  var stage = $(".preview-stage");
  ["dragenter", "dragover"].forEach(function (ev) {
    stage.addEventListener(ev, function (e) { e.preventDefault(); stage.classList.add("drop"); });
  });
  ["dragleave", "drop"].forEach(function (ev) {
    stage.addEventListener(ev, function (e) { e.preventDefault(); stage.classList.remove("drop"); });
  });
  stage.addEventListener("drop", function (e) {
    var files = e.dataTransfer && e.dataTransfer.files;
    if (!files || !files.length) return;
    var i = tileAt(e);
    if (files.length === 1 && i >= 0) loadPhoto(files[0], i); else addMany(files, i >= 0 ? i : null);
  });

  // ---------- settings ----------
  function bindRadio(name, key, after) {
    $$("input[name=" + name + "]").forEach(function (r) {
      r.addEventListener("change", function () { state[key] = r.value; if (after) after(); update(); });
    });
  }
  bindRadio("vb-format", "format");
  bindRadio("vb-layout", "layout", buildTiles);
  bindRadio("vb-theme", "theme");
  $("#vb-title").addEventListener("input", function (e) { state.title = e.target.value; update(); });
  $("#vb-subtitle").addEventListener("input", function (e) { state.subtitle = e.target.value; update(); });
  $("#vb-mark").addEventListener("change", function (e) { state.mark = e.target.checked; update(); });

  // ---------- export ----------
  function exportBlob() {
    var fmt = FORMATS[state.format];
    var out = document.createElement("canvas");
    out.width = fmt.w; out.height = fmt.h;
    render(out.getContext("2d"), fmt.w, fmt.h, false);
    return new Promise(function (res) { out.toBlob(function (b) { res({ blob: b, canvas: out }); }, "image/png"); });
  }

  function meta() {
    var photos = state.tiles.slice(0, tileCount()).filter(function (t) { return t.img; }).length;
    return { format: state.format, layout: state.layout, theme: state.theme, photos: photos };
  }

  function downloadBlob(blob, name) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
  }

  $("#vb-download").addEventListener("click", function () {
    exportBlob().then(function (r) {
      downloadBlob(r.blob, "vision-board-" + state.format + ".png");
      toast("Vision board saved");
      track("website vision board downloaded", Object.assign(meta(), { method: "download" }));
    });
  });

  var shareBtn = $("#vb-share");
  try {
    var probe = new File([new Blob(["x"], { type: "image/png" })], "x.png", { type: "image/png" });
    if (navigator.canShare && navigator.canShare({ files: [probe] })) {
      shareBtn.hidden = false;
      if (!/iPhone|iPad|iPod|Android/i.test(navigator.userAgent)) shareBtn.textContent = "Share";
    }
  } catch (e) {}
  shareBtn.addEventListener("click", function () {
    exportBlob().then(function (r) {
      var file = new File([r.blob], "vision-board.png", { type: "image/png" });
      navigator.share({ files: [file], title: "My vision board" }).then(function () {
        track("website vision board downloaded", Object.assign(meta(), { method: "share" }));
      }).catch(function () {});
    });
  });

  $("#vb-print").addEventListener("click", function () {
    exportBlob().then(function (r) {
      var img = $("#vb-print-img");
      img.onload = function () { setTimeout(function () { window.print(); }, 60); };
      img.src = r.canvas.toDataURL("image/png");
      track("website vision board downloaded", Object.assign(meta(), { method: "print" }));
    });
  });

  // ---------- go ----------
  buildTiles();
  window.addEventListener("resize", update);
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(update);
  update();
})();

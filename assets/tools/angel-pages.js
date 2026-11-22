/* Angel number pages: pick where you saw the number, get a tailored reading.
   Runs in the browser only; data comes from the page (#ap-data).
   Analytics: the number and the chosen context only, never anything personal. */
(function () {
  "use strict";
  var root = document.querySelector("[data-angel-page]");
  var dataEl = document.getElementById("ap-data");
  if (!root || !dataEl) return;
  var DATA = JSON.parse(dataEl.textContent);
  var card = root.querySelector("[data-result]");
  var toastEl = document.querySelector("[data-toast]");
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function track(name, props) { try { if (window.posthog) window.posthog.capture(name, props || {}); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toast.t);
    toast.t = setTimeout(function () { toastEl.classList.remove("show"); }, 2200);
  }

  function copyText(text, done) {
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, done);
    else {
      var ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch (x) {}
      ta.remove(); done();
    }
  }

  function render(ctx) {
    var e = DATA.reads[ctx];
    if (!e) return;
    card.innerHTML = '<div class="ap-result"><p class="ap-ctx">' + esc(DATA.n) + " &middot; " + esc(DATA.labels[ctx]) + "</p>" +
      '<p class="ap-text">' + esc(e.text) + "</p>" +
      '<div class="ap-box"><p class="ap-k">A question to sit with</p><p class="ap-q">' + esc(e.ask) + "</p></div>" +
      '<div class="ap-box ap-aff"><p class="ap-k">An affirmation to try</p><p class="ap-aff-t">&ldquo;' + esc(e.aff) + "&rdquo;</p></div>" +
      '<div class="ap-actions"><button type="button" class="btn small" data-copy="' + esc(e.aff) + '">Copy affirmation</button>' +
      '<a class="btn ghost small" href="/affirmation-wallpaper/" data-wallpaper data-copy-text="' + esc(e.aff) + '">Make it my lock screen</a></div>' +
      '<p class="ap-note">A reflection prompt, not a prediction. There is no scientific evidence that numbers carry messages.</p></div>';
    if (!reduceMotion) { card.classList.remove("ap-in"); void card.offsetWidth; card.classList.add("ap-in"); }
  }

  root.querySelectorAll(".ap-chip").forEach(function (b) {
    b.addEventListener("click", function () {
      var ctx = b.getAttribute("data-ctx");
      root.querySelectorAll(".ap-chip").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      render(ctx);
      track("website angel page reading", { number: DATA.n, context: ctx });
      if (window.innerWidth < 900) card.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "nearest" });
    });
  });

  card.addEventListener("click", function (ev) {
    var copy = ev.target.closest("button[data-copy]");
    if (copy) {
      copyText(copy.getAttribute("data-copy"), function () { toast("Affirmation copied"); });
      track("website angel page copied", { number: DATA.n });
      return;
    }
    var wp = ev.target.closest("a[data-wallpaper]");
    if (wp) {
      // The wallpaper maker has no prefill, so copy the line to paste there.
      copyText(wp.getAttribute("data-copy-text"), function () { toast("Copied. Paste it into the wallpaper maker."); });
      track("website angel page wallpaper click", { number: DATA.n });
    }
  });
})();

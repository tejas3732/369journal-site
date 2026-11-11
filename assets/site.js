/* Phone download bar: shows once the main App Store badge has scrolled away,
   hides again while any other badge is on screen. Also closes the Guides menu
   when you click elsewhere or press Escape. */
(function () {
  var bar = document.querySelector("[data-sticky]");
  if (bar && "IntersectionObserver" in window) {
    var visible = new Set();
    var scrolled = false;
    var update = function () {
      bar.classList.toggle("show", scrolled && visible.size === 0);
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) visible.add(e.target); else visible.delete(e.target);
      });
      update();
    });
    document.querySelectorAll(".store-badge").forEach(function (b) {
      if (!bar.contains(b) && !b.closest(".site-header")) io.observe(b);
    });
    window.addEventListener("scroll", function () {
      var s = window.scrollY > window.innerHeight * 0.6;
      if (s !== scrolled) { scrolled = s; update(); }
    }, { passive: true });
  }

  var menu = document.querySelector(".nav details");
  if (menu) {
    document.addEventListener("click", function (e) {
      if (menu.open && !menu.contains(e.target)) menu.open = false;
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.open) { menu.open = false; menu.querySelector("summary").focus(); }
    });
  }
})();

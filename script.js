/* Highlight Solutions — bilingual toggle (ar/rtl default), mobile nav, year. */
(function () {
  "use strict";

  var html = document.documentElement;
  var toggle = document.getElementById("lang-toggle");
  var navToggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("primary-nav");
  var STORAGE_KEY = "hs-lang";

  function applyLang(lang) {
    var useAr = lang === "ar";
    html.setAttribute("lang", useAr ? "ar" : "en");
    html.setAttribute("dir", useAr ? "rtl" : "ltr");
    document.querySelectorAll("[data-ar]").forEach(function (el) {
      el.textContent = useAr ? el.getAttribute("data-ar") : el.getAttribute("data-en");
    });
    // Toggle button shows the OTHER language
    toggle.querySelector("span:not(.visually-hidden)").textContent = useAr ? "EN" : "ع";
    toggle.setAttribute("aria-label", useAr
      ? "Switch language to English"
      : "تغيير اللغة إلى العربية");
    if (navToggle) {
      navToggle.setAttribute("aria-label", useAr
        ? navToggle.getAttribute("data-ar-label") || "القائمة"
        : navToggle.getAttribute("data-en-label") || "Menu");
    }
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { /* private mode */ }
  }

  var saved = null;
  try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) { /* ignore */ }
  applyLang(saved === "en" ? "en" : "ar");

  toggle.addEventListener("click", function () {
    applyLang(html.getAttribute("lang") === "ar" ? "en" : "ar");
  });

  // Mobile nav
  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Year
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());
})();

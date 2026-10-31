/**
 * 23:59 Barbershop — Bespoke Bilingual Engine & Interactive Controllers
 * Standards: Vanilla ES6+, Zero External Dependencies, High Accessibility
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'lead_factory_lang';
  const DEFAULT_LANG = 'ru';

  /**
   * Safe getter for user's selected language
   */
  function getSavedLang() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return (saved === 'ru' || saved === 'uz') ? saved : DEFAULT_LANG;
    } catch (e) {
      return DEFAULT_LANG;
    }
  }

  /**
   * Updates all DOM elements with .lang-text class to chosen language
   * @param {string} lang - 'ru' or 'uz'
   */
  function setLanguage(lang) {
    const validLang = (lang === 'uz') ? 'uz' : 'ru';
    document.documentElement.lang = validLang;

    try {
      localStorage.setItem(STORAGE_KEY, validLang);
    } catch (e) {
      // Storage unavailable or disabled
    }

    // Update switcher buttons UI state
    const btnRu = document.getElementById('btn-ru');
    const btnUz = document.getElementById('btn-uz');

    if (btnRu && btnUz) {
      if (validLang === 'ru') {
        btnRu.classList.add('active');
        btnRu.setAttribute('aria-pressed', 'true');
        btnUz.classList.remove('active');
        btnUz.setAttribute('aria-pressed', 'false');
      } else {
        btnUz.classList.add('active');
        btnUz.setAttribute('aria-pressed', 'true');
        btnRu.classList.remove('active');
        btnRu.setAttribute('aria-pressed', 'false');
      }
    }

    // Update all localized text elements
    const elements = document.querySelectorAll('.lang-text');
    elements.forEach(function (el) {
      const text = el.getAttribute('data-' + validLang);
      if (text !== null) {
        if (text.indexOf('<') !== -1) {
          el.innerHTML = text;
        } else {
          el.textContent = text;
        }
      }
    });
  }

  /**
   * Initializes interactive controls on DOMContentLoaded
   */
  document.addEventListener('DOMContentLoaded', function () {
    // 1. Initialize language
    const currentLang = getSavedLang();
    setLanguage(currentLang);

    // 2. Attach click handlers to language switch buttons
    const btnRu = document.getElementById('btn-ru');
    const btnUz = document.getElementById('btn-uz');

    if (btnRu) {
      btnRu.addEventListener('click', function () {
        setLanguage('ru');
      });
    }

    if (btnUz) {
      btnUz.addEventListener('click', function () {
        setLanguage('uz');
      });
    }

    // 3. Smooth scrolling for internal anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function (link) {
      link.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId && targetId !== '#') {
          const targetEl = document.querySelector(targetId);
          if (targetEl) {
            e.preventDefault();
            const headerOffset = 70;
            const elementPosition = targetEl.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
              top: offsetPosition,
              behavior: 'smooth'
            });
          }
        }
      });
    });

    // 4. Scroll Reveal Animations with IntersectionObserver
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const animElements = document.querySelectorAll('.animate-on-scroll');

    if ('IntersectionObserver' in window && !prefersReducedMotion) {
      const revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            revealObserver.unobserve(entry.target);
          }
        });
      }, {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
      });

      animElements.forEach(function (el) {
        revealObserver.observe(el);
      });
    } else {
      // Fallback: make all elements immediately visible
      animElements.forEach(function (el) {
        el.classList.add('animate');
      });
    }
  });
})();

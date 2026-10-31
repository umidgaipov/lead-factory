// Fast Bilingual Switcher (RU / UZ)
function switchLang(lang) {
  const ruBtn = document.getElementById('btn-ru');
  const uzBtn = document.getElementById('btn-uz');

  if (lang === 'uz') {
    ruBtn.classList.remove('active');
    uzBtn.classList.add('active');
  } else {
    uzBtn.classList.remove('active');
    ruBtn.classList.add('active');
  }

  const elements = document.querySelectorAll('.lang-text');
  elements.forEach((el) => {
    const text = el.getAttribute(`data-${lang}`);
    if (text) {
      el.textContent = text;
    }
  });

  try {
    localStorage.setItem('lead_factory_lang', lang);
  } catch (e) {}
}

// Auto-detect previous choice or system language
document.addEventListener('DOMContentLoaded', () => {
  try {
    const saved = localStorage.getItem('lead_factory_lang');
    if (saved === 'uz') {
      switchLang('uz');
    }
  } catch (e) {}
});

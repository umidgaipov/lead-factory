# Implementation Roadmap: 23:59 Barbershop (2359-barbershop)

> **Status**: Ready for Implementation  
> **Source of Truth**: `pipeline/data/leads/2359-barbershop.json`  
> **Target Output**: `D:\Work\сайты\2359-barbershop\`  
> **Author**: Lead Planner & Architect (via /plan skill)

---

## 1. Documentation & Architecture Summary
- **Бизнес**: 23:59 Barbershop, г. Ташкент (ул. Нукус, 5 / Минор, 90), тел. `+998 77 577 23 59`
- **Ниша**: Мужской барбершоп премиум-класса с уникальным УТП (работа до полуночи 23:59)
- **Стек**: Vanilla HTML5, CSS3 Custom Properties, ES6+ (Zero-dependency, First Contentful Paint < 0.8s)
- **Дизайн-направление**: Темная брутальная барбершоп-тема (глубокий угольный #111417, акцентный янтарь/золото #d4af37, чистый контрастный текст)
- **Интеграции**: Кнопка быстрой онлайн-записи в Telegram (@ServiceBookingDemo_bot), кликабельный телефон `tel:+998775772359`, маршрут в Яндекс.Картах

---

## 2. Global Acceptance Criteria
- [ ] 100% билингвальность: все текстовые узлы имеют корректные атрибуты `data-ru` и `data-uz`.
- [ ] Mobile-First: кнопки звонка и Telegram >= 44px, отсутствие горизонтального скролла на 360px+.
- [ ] Zero Hallucination: только реальные цены (от 60к до 200к сум), реальные адреса филиалов и телефон.
- [ ] Безопасность: плашка "Демо-концепт" и `robots.txt` с `Disallow: /`.
- [ ] 0 ошибок в консоли браузера и чистая валидация сборщика.

---

## 3. Milestones Roadmap

### Milestone 1: Foundations, Design Tokens & Palette
- **Goal**: Сформировать CSS-токены под визуальный стиль барбершопа (темная премиальная гамма).
- **Scope**: CSS переменные (--bg-dark: #121417, --surface: #1c1f24, --accent: #e5a93c, --accent-hover: #f5ba4c, --text: #f0f2f5, --text-muted: #9ba3af), типографика, плашка демо-версии.
- **Validation Checklist**:
  - [ ] Темный барбершоп-стиль подчеркивает работу до полуночи (23:59).
  - [ ] Контрастность текста по WCAG AA (коэффициент >= 4.5:1).
- **Definition of Done (DoD)**: Стили согласованы, палитра готова.

### Milestone 2: Structure, Markup & Bilingual Mapping
- **Goal**: Собрать семантическую разметку секций с синхронными RU и UZ текстами.
- **Scope**: Секции Header (языковой переключатель RU/UZ), Hero (H1 с гео, рейтинг 5.0, 695 отзывов), Trust Points (3 факта), Services & Prices (6 услуг от 60к сум), Reviews (реальные отзывы), Map & Contacts.
- **Validation Checklist**:
  - [ ] Каждый блок содержит валидные атрибуты `data-ru` и `data-uz`.
  - [ ] Никаких `undefined`, `NaN`, `{{ПЕРЕМЕННЫХ}}` или `Lorem ipsum`.
- **Definition of Done (DoD)**: Разметка полностью готова для генерации `index.html`.

### Milestone 3: Interactive Scripts & Bot Integration
- **Goal**: Обеспечить мгновенное переключение языка и привязку свободного Telegram-бота.
- **Scope**: Назначение бота `ServiceBookingDemo_bot` в `pipeline/bots_pool.json`, привязка к CTA-кнопкам, обработчики в `script.js`.
- **Validation Checklist**:
  - [ ] Кнопка [RU|UZ] мгновенно переключает все тексты без перезагрузки страницы.
  - [ ] Кнопка Telegram открывает `@ServiceBookingDemo_bot` с pre-filled сообщением.
- **Definition of Done (DoD)**: Все интерактивные элементы протестированы и работают.

### Milestone 4: Build, Asset Assembly & Sales Card
- **Goal**: Скомпилировать финальный проект сайта и карточку звонка.
- **Scope**: Запуск `python pipeline/build.py pipeline/data/leads/2359-barbershop.json`, размещение в `D:\Work\сайты\2359-barbershop\`.
- **Validation Checklist**:
  - [ ] Сгенерированы `index.html`, `style.css`, `script.js`, `robots.txt`, `звонок.md`.
  - [ ] Карточка `звонок.md` содержит персонализированный скрипт на RU и UZ.
- **Definition of Done (DoD)**: Директория сайта полностью готова к QA-проверке.

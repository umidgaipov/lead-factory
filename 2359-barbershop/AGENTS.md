# 23:59 Barbershop Site Development Rules

## Core Directives
1. **No Rigid Templates**: Write 100% bespoke, responsive Vanilla HTML5/CSS3/ES6+ from scratch. Never reuse generic boilerplate or AI slop layouts.
2. **Local Skills Priority (Skills First)**: Subagents and developers MUST read and apply local guidelines directly from `skills/`:
   - `skills/ui-ux-pro-max/` — dark theme tokens, high-contrast ratios (>=4.5:1), and mobile touch ergonomics.
   - `skills/frontend-design/` & `skills/no-ai-design-slop/` — authentic midnight barbershop aesthetic, bespoke typography, zero generic purple gradient blur circles, zero fake AI portraits.
   - `skills/landing-page/` & `skills/better-ui/` — single-intent conversion architecture, concentric border radii (`outer = inner + padding`), active button tactile scaling (`scale(0.96)`), explicit transitions (never `transition: all`), and 1px image depth outlines.
   - `skills/animation-on-scroll/` — lightweight vanilla IntersectionObserver reveals with reduced-motion compliance.
3. **8 Mandatory Sections**:
   - Section 1: Hero (Geo-H1, rating badge 5.0★, 2 CTAs: Telegram Bot + Phone, trust highlights).
   - Section 2: About Us (Authentic history, Japanese service concept, 4 stats cards).
   - Section 3: Why Us (6 benefit cards with icons).
   - Section 4: Services & Honest Pricing (10 verified services, unlisted strictly marked "уточняйте по телефону").
   - Section 5: Reviews (4 verbatim Yandex Maps reviews with author names + CTA to Yandex Maps).
   - Section 6: Cases / Portfolio (4 real work cards with Yandex CDN photos).
   - Section 7: Contacts & Hours (Nukus 5, landmarks, 10:00-00:00 schedule, 3 phone numbers, route CTA).
   - Section 8: Footer + Mobile Sticky Action Bar (<768px with Telegram and Call buttons >= 48px).
4. **Bilingual Synchronization [ RU | UZ ]**:
   - Every text element must have synchronized attributes: `data-ru="..."` and `data-uz="..."` with class `lang-text`.
   - Header must feature `<button id="btn-ru">` and `<button id="btn-uz">`.
5. **Zero Hallucination Guarantee**:
   - Prices, services, addresses, and telephone numbers must match `pipeline/data/leads/2359-barbershop.json` exactly.
   - Unlisted prices must strictly read «уточняйте по телефону» (RU) / «telefon orqali aniqlashtiring» (UZ).
   - Phone link must be valid `href="tel:+998775772359"`.
   - Telegram bot link must target `https://t.me/ServiceBookingDemo_bot`.
6. **Mobile Touch Targets & Accessibility**:
   - All interactive controls, telephone links, and buttons must have minimum touch targets of `44x44px` (`>= 48px` on mobile sticky bar).
   - Touch spacing between interactive targets must be `>= 8px`.
7. **SEO & Safety Shield**:
   - `<meta name="robots" content="noindex, nofollow">` must be present in `<head>`.
   - `robots.txt` must contain `User-agent: *\nDisallow: /`.
   - Footer must contain demo concept disclaimer and Lead Factory badge.

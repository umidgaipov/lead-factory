# 23:59 Barbershop Demo Site Instructions

## Language and Output
Think and plan in English without exposing private chain-of-thought. Reply in Russian.
Lead with the result; include only essential details, checks, or blockers. Skip introductions and long narratives.

## Project Index
Route tasks strictly to the relevant file:
- `index.html` — Primary bilingual landing page (RU / UZ).
- `style.css` — Design tokens, responsive grid, mobile-first styles (360px+).
- `script.js` — Client-side language switcher (`[data-lang]`, `data-ru`, `data-uz`) and Telegram CTA.
- `robots.txt` — Anti-indexing policy (`User-agent: *\nDisallow: /`).
- `звонок.md` — Sales script & instant messenger message template.
- `realisation.md` — Step-by-step implementation milestones and DoD checklists.
- Source of Truth: `D:\Work\lead-factory\pipeline\data\leads\2359-barbershop.json`.

## Search First, Frugal Reading, and Deny Noise
1. Open only target files (`index.html`, `style.css`, `script.js`).
2. Deny by default: `node_modules`, external dependencies, complex build tools, and autonomous browser verification (`browser_subagent`).
3. Work strictly inside `D:\Work\сайты\2359-barbershop\` and `pipeline/templates/bilingual-service/`.

## Project-Specific Rules
- **Zero Hallucination**: Use strictly verified facts from `lead.json`. Prices (from 60,000 to 200,000 UZS), phone `+998 77 577 23 59`, address `ул. Нукус, 5 / Минор, 90`.
- **Vanilla Stack**: Pure HTML5, CSS3 Custom Properties, and ES6+ only. Zero external frameworks, zero bundlers. Instant First Contentful Paint (<1s on 3G).
- **Bilingual Sync**: Every text element must provide synchronized `data-ru` and `data-uz` attributes.
- **Mobile Touch Targets**: All phone calls (`tel:`) and Telegram links (`https://t.me/ServiceBookingDemo_bot`) must have tap targets >= 44x44px.
- **Safety & Demo Banner**: Must contain visible "Демо-концепт" banner and `robots.txt` (`Disallow: /`).
- **Quota Saver**: Do NOT launch headless browsers or automated screenshot sessions.

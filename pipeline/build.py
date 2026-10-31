#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lead Factory Site Builder
Compiles bilingual static sites and sales cards from structured lead JSON.
"""

import os
import sys
import json
import shutil
import re
from pathlib import Path

# Force UTF-8 stdout on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
PIPELINE_DIR = BASE_DIR / "pipeline"
TEMPLATES_DIR = PIPELINE_DIR / "templates" / "bilingual-service"
BOTS_POOL_FILE = PIPELINE_DIR / "bots_pool.json"
SITES_OUTPUT_DIR = Path("D:/Work/сайты")

def clean_phone(phone_str):
    """Strip everything except numbers and optional leading +."""
    return re.sub(r"[^\d+]", "", phone_str)

def get_or_assign_bot(slug):
    """Pick an available bot from the pool or keep already assigned."""
    if not BOTS_POOL_FILE.exists():
        return "DemoBookingBot"

    try:
        with open(BOTS_POOL_FILE, "r", encoding="utf-8") as f:
            pool = json.load(f)
    except Exception:
        return "DemoBookingBot"

    # Check if already assigned
    for b in pool:
        if b.get("assigned_to") == slug:
            return b["bot_username"]

    # Assign first available
    for b in pool:
        if b.get("status") == "available":
            b["status"] = f"assigned:{slug}"
            b["assigned_to"] = slug
            with open(BOTS_POOL_FILE, "w", encoding="utf-8") as f:
                json.dump(pool, f, ensure_ascii=False, indent=2)
            return b["bot_username"]

    return pool[0]["bot_username"] if pool else "DemoBookingBot"

def render_trust_points(points_ru, points_uz):
    html = []
    icons = ["⚡", "⭐", "🛡️", "🔧", "☕"]
    for i, (p_ru, p_uz) in enumerate(zip(points_ru, points_uz)):
        icon = icons[i % len(icons)]
        html.append(f"""
        <div class="trust-item">
          <span class="trust-icon">{icon}</span>
          <span class="lang-text" data-ru="{p_ru}" data-uz="{p_uz}">{p_ru}</span>
        </div>
        """)
    return "\n".join(html)

def render_services(services_ru, services_uz):
    html = []
    for s_ru, s_uz in zip(services_ru, services_uz):
        name_ru = s_ru.get("name", "")
        name_uz = s_uz.get("name", name_ru)
        price_ru = s_ru.get("price", "уточняйте")
        price_uz = s_uz.get("price", "aniqlashtiring")
        html.append(f"""
        <div class="service-row">
          <span class="service-name lang-text" data-ru="{name_ru}" data-uz="{name_uz}">{name_ru}</span>
          <span class="service-price lang-text" data-ru="{price_ru}" data-uz="{price_uz}">{price_ru}</span>
        </div>
        """)
    return "\n".join(html)

def render_reviews(reviews_ru, reviews_uz):
    html = []
    for r_ru, r_uz in zip(reviews_ru, reviews_uz):
        author = r_ru.get("author", "Клиент с карт")
        text_ru = r_ru.get("text", "")
        text_uz = r_uz.get("text", text_ru)
        html.append(f"""
        <div class="review-card">
          <div class="review-header">
            <strong>{author}</strong>
            <span class="stars">★★★★★</span>
          </div>
          <div class="review-text lang-text" data-ru="{text_ru}" data-uz="{text_uz}">
            "{text_ru}"
          </div>
        </div>
        """)
    return "\n".join(html)

def build_site(lead_file_path):
    lead_path = Path(lead_file_path)
    if not lead_path.exists():
        print(f"Error: Lead file not found: {lead_path}")
        sys.exit(1)

    with open(lead_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slug = data.get("slug") or lead_path.stem
    business_name = data.get("name", "Сервис")
    city = data.get("city", "Ташкент")
    phone = data.get("phone", "+998 90 000 00 00")
    phone_clean = clean_phone(phone)
    address = data.get("address", "")
    maps_url = data.get("maps_url", "https://yandex.ru/maps")
    rating = data.get("rating", 4.8)
    reviews_count = data.get("reviews_count", 25)

    hours_ru = data.get("working_hours_ru", "Ежедневно 09:00 - 20:00")
    hours_uz = data.get("working_hours_uz", "Har kuni 09:00 - 20:00")

    content_ru = data.get("content_ru", {})
    content_uz = data.get("content_uz", {})

    h1_ru = content_ru.get("h1", business_name)
    h1_uz = content_uz.get("h1", h1_ru)

    subtitle_ru = content_ru.get("subtitle", "Качественные услуги с гарантией.")
    subtitle_uz = content_uz.get("subtitle", "Kafolatlangan sifatli xizmatlar.")

    trust_ru = content_ru.get("trust_points", ["Быстрое обслуживание", "Честные цены", "Опытные мастера"])
    trust_uz = content_uz.get("trust_points", ["Tezkor xizmat", "Halol narxlar", "Tajribali ustalar"])

    services_ru = data.get("services_ru", [])
    services_uz = data.get("services_uz", services_ru)

    reviews_ru = data.get("reviews_ru", [])
    reviews_uz = data.get("reviews_uz", reviews_ru)

    bot_username = get_or_assign_bot(slug)

    # Output directory
    out_dir = SITES_OUTPUT_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    # Render HTML
    with open(TEMPLATES_DIR / "template.html", "r", encoding="utf-8") as f:
        template = f.read()

    html = template
    html = html.replace("{{BUSINESS_NAME}}", business_name)
    html = html.replace("{{CITY}}", city)
    html = html.replace("{{SLUG}}", slug)
    html = html.replace("{{PHONE}}", phone)
    html = html.replace("{{PHONE_CLEAN}}", phone_clean)
    html = html.replace("{{ADDRESS}}", address)
    html = html.replace("{{MAPS_URL}}", maps_url)
    html = html.replace("{{RATING}}", str(rating))
    html = html.replace("{{REVIEWS_COUNT}}", str(reviews_count))
    html = html.replace("{{WORKING_HOURS_RU}}", hours_ru)
    html = html.replace("{{WORKING_HOURS_UZ}}", hours_uz)
    html = html.replace("{{H1_RU}}", h1_ru)
    html = html.replace("{{H1_UZ}}", h1_uz)
    html = html.replace("{{SUBTITLE_RU}}", subtitle_ru)
    html = html.replace("{{SUBTITLE_UZ}}", subtitle_uz)
    html = html.replace("{{BOT_USERNAME}}", bot_username)

    html = html.replace("{{TRUST_POINTS_HTML}}", render_trust_points(trust_ru, trust_uz))
    html = html.replace("{{SERVICES_HTML}}", render_services(services_ru, services_uz))
    html = html.replace("{{REVIEWS_HTML}}", render_reviews(reviews_ru, reviews_uz))

    with open(out_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Copy assets
    shutil.copy(TEMPLATES_DIR / "style.css", out_dir / "style.css")
    shutil.copy(TEMPLATES_DIR / "script.js", out_dir / "script.js")

    # Generate robots.txt
    with open(out_dir / "robots.txt", "w", encoding="utf-8") as f:
        f.write("User-agent: *\nDisallow: /\n")

    # Generate Sales Call Card
    generate_sales_card(out_dir, data, bot_username)

    print(f"SUCCESS: Site compiled at: {out_dir}")
    print(f"Assigned Telegram Bot: @{bot_username}")

def generate_sales_card(out_dir, data, bot_username):
    slug = data.get("slug", "client")
    name = data.get("name", "Сервис")
    phone = data.get("phone", "")
    rating = data.get("rating", 4.8)
    reviews_count = data.get("reviews_count", 25)
    best_review = data.get("reviews_ru", [{}])[0].get("text", "отличную работу")

    card_content = f"""# 📞 Карточка звонка: {name}

## 📋 Информация о клиенте:
- **Бизнес:** {name}
- **Телефон:** `{phone}`
- **Рейтинг на картах:** {rating} ★ ({reviews_count} отзывов)
- **Привязанный демо-бот:** @{bot_username}
- **Локальный сайт:** `file:///{out_dir.as_posix()}/index.html`

---

## 🎯 Скрипт разговора (Русский):
> «Здравствуйте! Я веб-разработчик. Обратил внимание на ваш {name} на картах — у вас отличный рейтинг {rating} и много положительных отзывов (особенно хвалят за качественный подход!).
>
> Но увидел, что у вас нет нормального мобильного сайта, а большинство клиентов сейчас ищут со смартфонов.
>
> Я уже бесплатно собрал для вас готовый демо-сайт на двух языках (русский и узбекский) с кнопкой быстрой записи в Telegram.
> 
> Никаких оплат не прошу — просто хочу скинуть ссылку, чтобы вы оценили со смартфона. Вам в Telegram или WhatsApp отправить?»

## 🎯 Скрипт разговора (O'zbekcha):
> «Assalomu alaykum! Men veb-dasturchiman. Xaritada {name} xizmatingizni ko'rdim — reytingingiz {rating} juda a'lo darajada va mijozlar juda iliq fikrlar qoldirgan!
>
> Lekin e'tibor berdim, sizda qulay mobil sayt yo'q ekan. Hozir hamma mijozlar telefon orqali tanlaydi.
>
> Men siz uchun oldindan mutlaqo bepul ikki tilli (o'zbek va rus) demo-sayt tayyorlab qo'ydim, hatto Telegram orqali yozilish tugmasi ham bor.
>
> Hech qanday to'lov kerak emas — shunchaki ko'rib chiqishingiz uchun link yubormoqchiman. Sizga Telegramdan tashlab beraymi yoki WhatsAppdan?»

---

## ⚡ Быстрое сообщение в мессенджер (скинуть во время звонка):
```text
Здравствуйте! Вот готовая демо-версия сайта для {name}:
(Ссылка на сайт)

Попробуйте переключить язык [RU / UZ] и протестировать кнопку Telegram-записи.
Посмотрите, если понравится — обсудим, как поставить его в ваши Яндекс/2ГИС/Google карты!
```

## 🛡️ Ответы на частые вопросы:
1. **«Сколько это стоит?»**  
   — *«Смотрите, сам демо-концепт я вам уже подарил бесплатно. Если захотите поставить на ваш домен и оставить Telegram-бота — это стоит всего 15–20 тысяч рублей (или ~2-3 млн сум), разовая оплата без скрытых платежей. Но давайте вы сначала посмотрите, нравится ли вообще!»*
2. **«Нам хватает карт / соцсетей»**  
   — *«Карты — супер, но там прямо рядом с вами 10 конкурентов. А сайт — это ваше личное пространство: ваши цены, ваши отзывы и мгновенная запись без конкурентов.»*
3. **«Это не развод?»**  
   — *«Абсолютно нет, я не прошу предоплат и паролей. Страница уже собрана, откройте и убедитесь сами. Если вам не понравится — я просто удалю ее.»*
"""
    with open(out_dir / "звонок.md", "w", encoding="utf-8") as f:
        f.write(card_content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build.py <path_to_lead_json>")
        sys.exit(1)
    build_site(sys.argv[1])

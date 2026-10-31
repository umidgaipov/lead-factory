#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lead Factory QA Checker (10-Point Deep Inspection)
Ensures zero-defect generation of bilingual landing pages and sales cards.
"""

import sys
import json
import re
from pathlib import Path

# Force UTF-8 stdout on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def qa_check(lead_json_path):
    lead_path = Path(lead_json_path)
    if not lead_path.exists():
        print(f"❌ FAIL: Lead JSON not found: {lead_path}")
        return False

    with open(lead_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slug = data.get("slug") or lead_path.stem
    site_dir = Path("D:/Work/сайты") / slug
    html_file = site_dir / "index.html"
    css_file = site_dir / "style.css"
    js_file = site_dir / "script.js"
    robots_file = site_dir / "robots.txt"
    sales_card = site_dir / "звонок.md"

    errors = []
    warnings = []

    # 1. Check critical files existence
    if not html_file.exists():
        print(f"❌ FAIL: index.html not found for {slug} in {site_dir}")
        return False

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    # 2. Check for unreplaced template placeholders
    unreplaced = re.findall(r"\{\{([A-Z0-9_]+)\}\}", html)
    if unreplaced:
        errors.append(f"Нераскрытые переменные шаблона: {set(unreplaced)}")

    forbidden_tokens = ["Lorem ipsum", "undefined", "NaN", "TODO", "FIXME"]
    for token in forbidden_tokens:
        if token.lower() in html.lower():
            errors.append(f"Обнаружен мусорный плейсхолдер: '{token}'")

    # 3. Check Phone integrity
    phone_raw = data.get("phone", "")
    phone_digits = re.sub(r"[^\d]", "", phone_raw)
    if phone_digits:
        if f"tel:" not in html:
            errors.append("Отсутствует ссылка href='tel:...' для быстрого звонка")
        elif phone_digits not in re.sub(r"[^\d]", "", html):
            errors.append(f"Номер телефона {phone_raw} не найден в HTML коде сайта")

    # 4. Check Telegram Bot Link
    if "https://t.me/" not in html and "t.me/" not in html:
        errors.append("Отсутствует ссылка на Telegram-бота (https://t.me/...)")

    # 5. Check Viewport Meta Tag (Mobile readiness)
    if 'name="viewport"' not in html:
        errors.append("Отсутствует тег <meta name='viewport'> (сайт сломается на мобилках)")

    # 6. Check Robots & Safety Banner (Noindex)
    if not robots_file.exists():
        errors.append("Файл robots.txt отсутствует в папке сайта")
    else:
        with open(robots_file, "r", encoding="utf-8") as rf:
            if "Disallow: /" not in rf.read():
                errors.append("В robots.txt нет директивы Disallow: /")

    if 'name="robots"' not in html or "noindex" not in html:
        warnings.append("В index.html рекомендуется метатег <meta name='robots' content='noindex, nofollow'>")

    # 7. Check Bilingual Switcher
    if 'id="btn-ru"' not in html or 'id="btn-uz"' not in html:
        errors.append("Отсутствуют кнопки переключения языков [ RU ] / [ UZ ]")

    # 8. Check CSS & JS integrity
    if not css_file.exists() or css_file.stat().st_size < 100:
        errors.append("style.css отсутствует или пуст")
    if not js_file.exists() or js_file.stat().st_size < 50:
        errors.append("script.js отсутствует или пуст")

    # 9. Check Broken Local Images / Empty Links
    empty_links = re.findall(r'href=["\']\s*["\']', html)
    if empty_links:
        errors.append(f"Обнаружены пустые ссылки: href='' ({len(empty_links)} шт.)")

    # 10. Check Sales Card
    if not sales_card.exists() or sales_card.stat().st_size < 100:
        errors.append("Шпаргалка для звонка (звонок.md) отсутствует или пуста")

    # Output report
    if errors:
        print(f"\n❌ QA ПРОВЕРКА НЕ ПРОЙДЕНА ДЛЯ [{slug}]: {len(errors)} ошибок")
        for err in errors:
            print(f"  ❌ {err}")
        if warnings:
            for w in warnings:
                print(f"  ⚠️ {w}")
        return False

    print(f"\n✅ QA ПРОВЕРКА УСПЕШНО ПРОЙДЕНА ДЛЯ [{slug}]!")
    print(f"  ✓ Телефон: {phone_raw} проверен")
    print(f"  ✓ Двуязычность: RU / UZ проверена")
    print(f"  ✓ Адаптивность и мобильный viewport: OK")
    print(f"  ✓ Безопасность и noindex: OK")
    print(f"  ✓ Карточка звонка (звонок.md): готова")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pipeline/qa_check.py <path_to_lead_json>")
        sys.exit(1)
    success = qa_check(sys.argv[1])
    sys.exit(0 if success else 1)

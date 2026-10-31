#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lead Factory - CRM Fetcher
Directly connects to LeadCRM database on Oracle VPS and pulls qualified candidates.
Generates structured pipeline/data/leads/{slug}.json
"""

import sys
import os
import json
import re
import argparse
import base64
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add LeadCRM to sys.path to borrow its Oracle SSH helper
sys.path.append("d:/projects/LeadCRM")
try:
    from deploy.sync_oracle import prepare_ssh_key, run_ssh
except ImportError:
    prepare_ssh_key = None
    run_ssh = None

LEADS_DIR = Path("d:/Work/lead-factory/pipeline/data/leads")
LEADS_DIR.mkdir(parents=True, exist_ok=True)

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text[:40] or "candidate"

def run_remote_python(code_str):
    if not prepare_ssh_key or not run_ssh:
        raise RuntimeError("deploy.sync_oracle not available in LeadCRM.")
    key = prepare_ssh_key()
    b64 = base64.b64encode(code_str.encode("utf-8")).decode("ascii")
    cmd = f"echo '{b64}' | base64 -d | /opt/leadcrm/.venv/bin/python3"
    res = run_ssh(key, cmd)
    return res

def list_qualified_candidates(limit=15):
    """List candidates with rating >= 4.3, reviews >= 15 and no active good website."""
    code = f"""
import sqlite3, json
con = sqlite3.connect('/opt/leadcrm/data/leadcrm.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute('''
    SELECT id, name, query, city, address, phone, rating, reviews_count, source_url, website, website_status, socials_json
    FROM lead_candidates
    WHERE (website IS NULL OR website = '' OR website_status = 'bad' OR website_status = 'none' OR website_status IS NULL)
      AND rating >= 4.3
      AND reviews_count >= 15
    ORDER BY reviews_count DESC
    LIMIT {limit}
''')
rows = [dict(r) for r in cur.fetchall()]
print('ROWS_START' + json.dumps(rows, default=str) + 'ROWS_END')
"""
    res = run_remote_python(code)
    if "ROWS_START" in res.stdout:
        return json.loads(res.stdout.split("ROWS_START")[1].split("ROWS_END")[0])
    return []

def fetch_candidate_by_id(candidate_id):
    """Fetch complete candidate record and format into lead.json."""
    code = f"""
import sqlite3, json
con = sqlite3.connect('/opt/leadcrm/data/leadcrm.db')
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute('SELECT * FROM lead_candidates WHERE id = {candidate_id}')
row = cur.fetchone()
if row:
    print('CAND_START' + json.dumps(dict(row), default=str) + 'CAND_END')
else:
    print('CAND_NONE')
"""
    res = run_remote_python(code)
    if "CAND_START" in res.stdout:
        raw = json.loads(res.stdout.split("CAND_START")[1].split("CAND_END")[0])
        return raw
    return None

def convert_to_lead_json(raw):
    name = raw.get("name") or "Сервис"
    slug = slugify(name)
    city = raw.get("city") or "Ташкент"
    phone = raw.get("phone") or ""
    address = raw.get("address") or ""
    rating = float(raw.get("rating") or 5.0)
    reviews_count = int(raw.get("reviews_count") or 15)
    source_url = raw.get("source_url") or raw.get("yandex_url") or "https://yandex.ru/maps"
    
    socials = {}
    if raw.get("socials_json"):
        try:
            socials = json.loads(raw["socials_json"])
        except Exception:
            socials = {}

    lead_data = {
        "crm_id": raw.get("id"),
        "slug": slug,
        "name": name,
        "niche": raw.get("query") or raw.get("categories") or "Услуги",
        "city": city,
        "phone": phone,
        "address": address,
        "maps_url": source_url,
        "rating": rating,
        "reviews_count": reviews_count,
        "socials": socials,
        "working_hours_ru": "Ежедневно 09:00 - 20:00",
        "working_hours_uz": "Har kuni 09:00 - 20:00",
        "content_ru": {
            "h1": f"{name} в {city}",
            "subtitle": "Качественные услуги с гарантией результата.",
            "trust_points": [
                f"Высокий рейтинг {rating} ★ на основе {reviews_count} отзывов",
                "Опытные мастера и гарантия на работу",
                "Удобная онлайн-запись через Telegram без звонков"
            ]
        },
        "content_uz": {
            "h1": f"{name} — {city}da",
            "subtitle": "Kafolatlangan sifatli xizmatlar.",
            "trust_points": [
                f"{reviews_count} ta mijoz fikri asosida yuqori {rating} ★ reyting",
                "Tajribali ustalar va kafolatlangan xizmat",
                "Telegram orqali qulay navbatsiz yozilish"
            ]
        },
        "services_ru": [
            {"name": "Базовая услуга", "price": "уточняйте по телефону"},
            {"name": "Комплексное обслуживание", "price": "уточняйте по телефону"}
        ],
        "services_uz": [
            {"name": "Asosiy xizmat", "price": "telefon orqali aniqlashtiring"},
            {"name": "Kafolatlangan to'liq xizmat", "price": "telefon orqali aniqlashtiring"}
        ],
        "reviews_ru": [
            {"author": "Клиент с карт", "text": "Отличный сервис, вежливый персонал и высокое качество работы! Рекомендую."}
        ],
        "reviews_uz": [
            {"author": "Xaritalar mijozi", "text": "A'lo darajadagi servis, xushmuomala xodimlar va sifatli ish! Tavsiya qilaman."}
        ]
    }
    return lead_data

def save_lead(lead_data):
    slug = lead_data["slug"]
    out_path = LEADS_DIR / f"{slug}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(lead_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Lead saved: {out_path}")
    return out_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch qualified candidates directly from LeadCRM server.")
    parser.add_argument("--list", action="store_true", help="List top qualified candidates from CRM")
    parser.add_argument("--id", type=int, help="Fetch candidate by CRM ID and save to pipeline/data/leads/{slug}.json")
    parser.add_argument("--limit", type=int, default=10, help="Number of candidates to list")
    args = parser.parse_args()

    if args.list or not args.id:
        print(f"🔍 Запрос кандидатов из LeadCRM на Oracle VPS (рейтинг >= 4.3, отзывы >= 15, без сайта)...")
        candidates = list_qualified_candidates(args.limit)
        print(f"\nНайдено кандидатов: {len(candidates)}")
        print("-" * 75)
        for c in candidates:
            print(f"ID {c['id']:<4} | {c['name']:<25} | {c['query'] or 'Услуги':<20} | {c['rating']} ★ ({c['reviews_count']} отз.) | {c['phone']}")
        print("-" * 75)
        print("Чтобы сгенерировать lead.json для кандидата, запустите:")
        print("  python pipeline/fetch_crm.py --id <ID>")
    
    if args.id:
        print(f"Загрузка кандидата ID {args.id} из CRM...")
        raw = fetch_candidate_by_id(args.id)
        if not raw:
            print(f"❌ Кандидат ID {args.id} не найден в CRM!")
            sys.exit(1)
        lead = convert_to_lead_json(raw)
        save_lead(lead)

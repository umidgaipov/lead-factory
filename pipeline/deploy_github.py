#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lead Factory - GitHub Pages Deployer
Pushes generated sites to GitHub repository gh-pages branch.
Provides live preview URL for sales calls and messengers.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Force UTF-8 stdout on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SITES_DIR = Path("D:/Work/сайты")
GITHUB_USER = "umidgaipov"
REPO_NAME = "lead-factory"
BRANCH = "gh-pages"

def run_git(args, cwd=SITES_DIR):
    cmd = ["git"] + args
    res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res

def deploy_site(slug):
    slug_dir = SITES_DIR / slug
    if not slug_dir.exists():
        print(f"❌ Ошибка: папка сайта не найдена: {slug_dir}")
        return None

    live_url = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/{slug}/"

    # Inject live URL into звонок.md if present
    sales_card = slug_dir / "звонок.md"
    if sales_card.exists():
        with open(sales_card, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("(Ссылка на сайт)", live_url)
        content = content.replace("file:///", f"Живой сайт: {live_url}\n- Локальный: file:///")
        with open(sales_card, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"🚀 Деплой сайта [{slug}] на GitHub Pages (ветка {BRANCH})...")
    run_git(["add", slug])
    run_git(["commit", "-m", f"Deploy demo site for {slug}"])
    
    push_res = run_git(["push", "origin", BRANCH])
    if push_res.returncode != 0 and "Everything up-to-date" not in push_res.stderr:
        print(f"⚠️ Предупреждение git push:\n{push_res.stderr}")

    print(f"\n🎉 САЙТ ОПУБЛИКОВАН!")
    print(f"🌐 Ссылка: {live_url}")
    return live_url

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy client site to GitHub Pages")
    parser.add_argument("--slug", required=True, help="Site directory slug (e.g. brookland)")
    args = parser.parse_args()

    deploy_site(args.slug)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lead Factory - GitHub Pages Deployer
Pushes generated sites to GitHub repository and generates live preview URL.
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
REPO_NAME = "lead-factory-sites"

def run_git(args, cwd=SITES_DIR):
    cmd = ["git"] + args
    res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res

def ensure_repo_initialized(remote_url=None):
    if not SITES_DIR.exists():
        SITES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if git is initialized
    if not (SITES_DIR / ".git").exists():
        print("Инициализация git в D:/Work/сайты...")
        run_git(["init", "-b", "main"])
    
    # Check remote
    remotes = run_git(["remote", "-v"]).stdout
    if "origin" not in remotes:
        if not remote_url:
            remote_url = f"git@github.com:{GITHUB_USER}/{REPO_NAME}.git"
        run_git(["remote", "add", "origin", remote_url])
        print(f"Привязан remote: {remote_url}")

def deploy_site(slug):
    slug_dir = SITES_DIR / slug
    if not slug_dir.exists():
        print(f"❌ Ошибка: папка сайта не найдена: {slug_dir}")
        return None

    ensure_repo_initialized()

    print(f"🚀 Деплой сайта [{slug}] на GitHub...")
    run_git(["add", slug])
    run_git(["commit", "-m", f"Deploy demo site for {slug}"])
    
    push_res = run_git(["push", "-u", "origin", "main"])
    if push_res.returncode != 0 and "Everything up-to-date" not in push_res.stderr:
        # Try pushing without -u if branch already exists
        push_res = run_git(["push", "origin", "main"])

    live_url = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/{slug}/"
    print(f"\n🎉 САЙТ ОПУБЛИКОВАН!")
    print(f"🌐 Ссылка: {live_url}")
    return live_url

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy client site to GitHub Pages")
    parser.add_argument("--slug", required=True, help="Site directory slug (e.g. brookland)")
    args = parser.parse_args()

    deploy_site(args.slug)


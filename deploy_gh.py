#!/usr/bin/env python3
"""Publicera ck-maleri på GitHub Pages (repo: oskarhellmer-dev/ck-maleri)."""
import json, os, re, subprocess, time, urllib.request
from pathlib import Path

ROOT = Path("/home/clawd/ck-maleri")
OWNER = "oskarhellmer-dev"
REPO = "ck-maleri"
TOKEN = re.search(r"https://[^:]+:([^@]+)@github\.com", Path("/home/clawd/.git-credentials").read_text()).group(1)
print("token:", len(TOKEN), "tecken")

def api(method, path, data=None):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        data=json.dumps(data).encode() if data else None,
        headers={"Authorization": f"token {TOKEN}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "hermes"}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")

def run(cmd, **kw):
    env = dict(os.environ, HOME="/home/clawd")
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, env=env, **kw)

(ROOT / ".nojekyll").write_text("")
(ROOT / "README.md").write_text(
    "# ckmaleri.se\n\nStatisk sajt för CK Måleri & Golv — golvslipning, måleri, "
    "microcement och plattsättning i Uddevalla och Trestad.\n\n"
    "Byggs med `python3 build.py` (ren stdlib, ingen beroendefil).\n")

run(["git", "init", "-q"])
run(["git", "add", "-A"])
run(["git", "-c", "user.email=oskarhellmer-dev@users.noreply.github.com",
     "-c", "user.name=oskarhellmer-dev",
     "commit", "-q", "-m", "CK Måleri & Golv: startsida, fyra tjänstesidor, video, SEO"])
run(["git", "branch", "-M", "main"])
run(["git", "remote", "remove", "origin"])
run(["git", "remote", "add", "origin", f"https://github.com/{OWNER}/{REPO}.git"])

st, body = api("POST", "/user/repos", {"name": REPO, "private": False,
                                       "description": "ckmaleri.se — statisk sajt för CK Måleri & Golv",
                                       "homepage": f"https://{OWNER}.github.io/{REPO}/"})
print("skapa repo:", st, body.get("full_name") if isinstance(body, dict) else str(body)[:120])

p = run(["git", "push", "-u", "origin", "main", "--force"])
print("push:", p.returncode, (p.stderr or p.stdout).strip()[-200:])

for payload in [{"source": {"branch": "main", "path": "/"}},
                {"build_type": "legacy", "source": {"branch": "main", "path": "/"}}]:
    st, body = api("POST", f"/repos/{OWNER}/{REPO}/pages", payload)
    print("aktivera pages:", st, body.get("html_url") if isinstance(body, dict) else str(body)[:160])
    if st in (201, 409, 422):
        break

URL = f"https://{OWNER}.github.io/{REPO}/"
for i in range(40):
    time.sleep(8)
    try:
        r = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "hermes"}), timeout=30)
        code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:
        code, = (0,)
        print("  väntar:", repr(e)[:80])
    print("  försök", i, "status", code)
    if code == 200:
        print("LIVE:", URL)
        break
for asset in ["assets/styles.css", "assets/app.js", "assets/video.mp4",
              "assets/img/hero.jpg", "assets/img/tjanst-golvslipning.jpg",
              "golvslipning.html", "sitemap.xml", "robots.txt"]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(URL + asset, headers={"User-Agent": "hermes"}), timeout=30)
        print("  %-38s %s  %d bytes" % (asset, r.status, len(r.read())))
    except urllib.error.HTTPError as e:
        print("  %-38s %s" % (asset, e.code))

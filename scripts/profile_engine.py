#!/usr/bin/env python3
"""Generate auditable, local SVG profile intelligence from GitHub public data.

Pure stdlib by design: no runtime package installation and no third-party data service.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "portfolio.json"
BASELINE_PATH = ROOT / "data" / "baseline.json"
LIVE_PATH = ROOT / "data" / "live.json"
OUT_DIR = ROOT / "assets" / "generated"

PALETTES = {
    "dark": {
        "bg": "#07101d", "panel": "#0f172a", "panel2": "#111c2f", "border": "#26364e",
        "text": "#f8fafc", "muted": "#94a3b8", "soft": "#cbd5e1",
        "blue": "#60a5fa", "teal": "#2dd4bf", "green": "#22c55e", "violet": "#a78bfa"
    },
    "light": {
        "bg": "#f8fafc", "panel": "#ffffff", "panel2": "#eff6ff", "border": "#cbd5e1",
        "text": "#0f172a", "muted": "#475569", "soft": "#334155",
        "blue": "#2563eb", "teal": "#0f766e", "green": "#15803d", "violet": "#7c3aed"
    },
}

@dataclass
class GitHubClient:
    owner: str
    api_version: str
    token: str = ""

    def _get(self, path: str) -> Any:
        url = f"https://api.github.com{path}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": self.api_version,
            "User-Agent": f"{self.owner}-profile-intelligence",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    def repo(self, name: str) -> dict[str, Any]:
        return self._get(f"/repos/{self.owner}/{name}")

    def latest_release(self, name: str) -> str:
        try:
            data = self._get(f"/repos/{self.owner}/{name}/releases/latest")
            return data.get("tag_name") or data.get("name") or "—"
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return "—"
            raise

    def readme(self, name: str) -> str:
        data = self._get(f"/repos/{self.owner}/{name}/readme")
        content = data.get("content", "").replace("\n", "")
        return base64.b64decode(content).decode("utf-8", errors="replace") if content else ""


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_live(config: dict[str, Any], token: str) -> dict[str, Any]:
    client = GitHubClient(config["owner"], config["api_version"], token)
    result: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "github-rest-api",
        "api_version": config["api_version"],
        "repos": {},
    }
    for project in config["flagships"]:
        name = project["repo"]
        meta = client.repo(name)
        readme = client.readme(name)
        license_info = meta.get("license") or {}
        claims = {
            claim["id"]: bool(re.search(claim["regex"], readme, flags=re.I | re.S))
            for claim in project.get("claim_patterns", [])
        }
        result["repos"][name] = {
            "name": name,
            "html_url": meta.get("html_url", f"https://github.com/{config['owner']}/{name}"),
            "description": meta.get("description") or "",
            "language": meta.get("language") or "—",
            "license": license_info.get("spdx_id") or "—",
            "stars": int(meta.get("stargazers_count", 0)),
            "forks": int(meta.get("forks_count", 0)),
            "pushed_at": meta.get("pushed_at") or meta.get("updated_at") or "",
            "latest_release": client.latest_release(name),
            "topics": meta.get("topics", []),
            "claims": claims,
        }
    return result


def iso_day(value: str) -> str:
    if not value:
        return "—"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%Y-%m-%d")
    except ValueError:
        return value[:10]


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def claim_summary(config: dict[str, Any], live: dict[str, Any]) -> tuple[int, int]:
    passed = total = 0
    for project in config["flagships"]:
        claims = live["repos"].get(project["repo"], {}).get("claims", {})
        for claim in project.get("claim_patterns", []):
            total += 1
            passed += 1 if claims.get(claim["id"], False) else 0
    return passed, total


def svg_header(width: int, height: int, title: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">'


def render_live_intelligence(config: dict[str, Any], live: dict[str, Any], theme: str) -> str:
    p = PALETTES[theme]
    passed, total = claim_summary(config, live)
    generated = iso_day(live.get("generated_at", ""))
    parts = [svg_header(1200, 410, "Live portfolio intelligence")]
    parts += [
        f'<rect width="1200" height="410" rx="26" fill="{p["bg"]}"/>',
        f'<text x="42" y="44" fill="{p["muted"]}" font-family="Arial" font-size="13" font-weight="700" letter-spacing="2">LIVE PORTFOLIO INTELLIGENCE</text>',
        f'<text x="42" y="70" fill="{p["soft"]}" font-family="Arial" font-size="12">{esc(("GitHub REST API · API " + str(live.get("api_version", config.get("api_version", "—")))) if str(live.get("source", "")).startswith("github") else "Bundled verified baseline · live refresh runs after workflow activation")} · snapshot {esc(generated)}</text>',
        f'<rect x="920" y="31" width="238" height="46" rx="12" fill="{p["panel"]}" stroke="{p["border"]}"/>',
        f'<circle cx="946" cy="54" r="7" fill="{p["green"] if passed == total else p["violet"]}"/>',
        f'<text x="966" y="60" fill="{p["text"]}" font-family="Arial" font-size="14" font-weight="700">CLAIMS VERIFIED {passed}/{total}</text>',
    ]
    x_positions = [42, 622]
    for idx, project in enumerate(config["flagships"]):
        repo = live["repos"].get(project["repo"], {})
        x = x_positions[idx]
        accent = p[project.get("accent", "blue")]
        parts += [
            f'<rect x="{x}" y="104" width="536" height="256" rx="21" fill="{p["panel"]}" stroke="{p["border"]}"/>',
            f'<rect x="{x}" y="104" width="7" height="256" rx="3" fill="{accent}"/>',
            f'<text x="{x+34}" y="145" fill="{p["text"]}" font-family="Arial" font-size="25" font-weight="800">{esc(project["repo"])}</text>',
            f'<text x="{x+34}" y="171" fill="{accent}" font-family="Arial" font-size="13" font-weight="700">{esc(project["label"].upper())}</text>',
            f'<text x="{x+34}" y="205" fill="{p["soft"]}" font-family="Arial" font-size="13">Language  {esc(repo.get("language", "—"))}</text>',
            f'<text x="{x+34}" y="229" fill="{p["soft"]}" font-family="Arial" font-size="13">Release   {esc(repo.get("latest_release", "—"))}</text>',
            f'<text x="{x+34}" y="253" fill="{p["soft"]}" font-family="Arial" font-size="13">Last push {esc(iso_day(repo.get("pushed_at", "")))}</text>',
            f'<text x="{x+300}" y="205" fill="{p["soft"]}" font-family="Arial" font-size="13">Stars  {repo.get("stars", 0)}</text>',
            f'<text x="{x+300}" y="229" fill="{p["soft"]}" font-family="Arial" font-size="13">Forks  {repo.get("forks", 0)}</text>',
            f'<text x="{x+300}" y="253" fill="{p["soft"]}" font-family="Arial" font-size="13">License {esc(repo.get("license", "—"))}</text>',
        ]
        claims = repo.get("claims", {})
        cx = x + 34
        for cidx, claim in enumerate(project.get("claim_patterns", [])):
            ok = claims.get(claim["id"], False)
            cy = 297 + cidx * 20
            parts += [
                f'<circle cx="{cx+5}" cy="{cy-4}" r="5" fill="{p["green"] if ok else p["violet"]}"/>',
                f'<text x="{cx+18}" y="{cy}" fill="{p["muted"]}" font-family="Arial" font-size="11">{esc(claim["label"])} · {"verified" if ok else "not found"}</text>'
            ]
    parts.append('</svg>')
    return "".join(parts)


def render_credential_matrix(config: dict[str, Any], theme: str) -> str:
    p = PALETTES[theme]
    creds = config["credentials"]
    thm = [c for c in creds if c["provider"] == "TryHackMe"]
    other = [c for c in creds if c["provider"] != "TryHackMe"]
    parts = [svg_header(1200, 390, "Credential matrix")]
    parts += [
        f'<rect width="1200" height="390" rx="26" fill="{p["bg"]}"/>',
        f'<text x="42" y="44" fill="{p["muted"]}" font-family="Arial" font-size="13" font-weight="700" letter-spacing="2">CREDENTIAL MATRIX · {len(creds)} DOCUMENTED PROGRAMS</text>',
        f'<rect x="42" y="80" width="720" height="265" rx="20" fill="{p["panel"]}" stroke="{p["border"]}"/>',
        f'<rect x="790" y="80" width="368" height="265" rx="20" fill="{p["panel"]}" stroke="{p["border"]}"/>',
        f'<text x="72" y="116" fill="{p["blue"]}" font-family="Arial" font-size="14" font-weight="700">TRYHACKME · {len(thm)}</text>',
        f'<text x="820" y="116" fill="{p["violet"]}" font-family="Arial" font-size="14" font-weight="700">ADDITIONAL · {len(other)}</text>',
    ]
    for i, cred in enumerate(thm):
        col = 0 if i < 5 else 1
        row = i if i < 5 else i - 5
        x = 72 + col * 335
        y = 153 + row * 36
        parts += [
            f'<text x="{x}" y="{y}" fill="{p["text"]}" font-family="Arial" font-size="12" font-weight="700">{esc(cred["name"][:42])}</text>',
            f'<text x="{x}" y="{y+15}" fill="{p["muted"]}" font-family="Consolas" font-size="9">{esc(cred["id"])} · {esc(cred["completed"])}</text>'
        ]
    for i, cred in enumerate(other):
        y = 154 + i * 53
        parts += [
            f'<text x="820" y="{y}" fill="{p["text"]}" font-family="Arial" font-size="11" font-weight="700">{esc(cred["name"][:45])}</text>',
            f'<text x="820" y="{y+17}" fill="{p["muted"]}" font-family="Arial" font-size="10">{esc(cred["provider"])} · {esc(cred["completed"])}</text>'
        ]
    parts.append('</svg>')
    return "".join(parts)


def semantic_snapshot(data: dict[str, Any]) -> dict[str, Any]:
    """Return only fields whose changes should create a profile commit."""
    return {
        "source": data.get("source"),
        "api_version": data.get("api_version"),
        "repos": data.get("repos", {}),
    }


def stabilize_generated_at(live: dict[str, Any]) -> dict[str, Any]:
    """Preserve snapshot time when public evidence has not meaningfully changed."""
    if not LIVE_PATH.exists():
        return live
    try:
        previous = load_json(LIVE_PATH)
    except Exception:
        return live
    if semantic_snapshot(previous) == semantic_snapshot(live):
        live["generated_at"] = previous.get("generated_at", live.get("generated_at"))
    return live


def write_outputs(config: dict[str, Any], live: dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for theme in PALETTES:
        (OUT_DIR / f"live-intelligence-{theme}.svg").write_text(render_live_intelligence(config, live, theme), encoding="utf-8")
        (OUT_DIR / f"credential-matrix-{theme}.svg").write_text(render_credential_matrix(config, theme), encoding="utf-8")
    passed, total = claim_summary(config, live)
    manifest = {
        "schema": 1,
        "generated_at": live.get("generated_at"),
        "source": live.get("source"),
        "api_version": live.get("api_version", config.get("api_version")),
        "role": config.get("role"),
        "flagships": live.get("repos", {}),
        "credential_count": len(config.get("credentials", [])),
        "tryhackme_credential_count": sum(1 for c in config.get("credentials", []) if c.get("provider") == "TryHackMe"),
        "verified_claims": {"passed": passed, "total": total},
    }
    (OUT_DIR / "portfolio-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Fetch current public data from GitHub REST API")
    parser.add_argument("--offline", action="store_true", help="Use bundled baseline snapshot")
    args = parser.parse_args()
    config = load_json(CONFIG_PATH)
    if args.live and not args.offline:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
        try:
            live = stabilize_generated_at(collect_live(config, token))
            LIVE_PATH.write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        except Exception as exc:
            print(f"live collection failed: {exc}; using baseline", file=sys.stderr)
            live = load_json(BASELINE_PATH)
            live["source"] = "baseline-fallback"
            live["api_version"] = config.get("api_version")
            live = stabilize_generated_at(live)
            LIVE_PATH.write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        live = load_json(BASELINE_PATH)
    write_outputs(config, live)
    passed, total = claim_summary(config, live)
    print(f"profile intelligence generated: {passed}/{total} claims verified; {len(config['credentials'])} credentials")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

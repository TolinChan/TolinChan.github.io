#!/usr/bin/env python3
"""Verify migrated content, built routes, media integrity, and secret hygiene."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "src" / "data" / "migration-report.json"
EXPECTED = {
    "publishedPosts": 42,
    "effectivePublishedPages": 5,
    "friends": 26,
    "galleryImages": 31,
    "approvedComments": 2,
    "selectedMediaFiles": 157,
}
FORBIDDEN_TEXT = (
    "116.62.4.97",
    "http://blog.tolinchan.xyz",
    "<wp:author_email>",
    "<wp:comment_author_email>",
    "<wp:comment_author_IP>",
    "CREATE TABLE `wp_users`",
)
FORBIDDEN_SUFFIXES = (
    ".sql",
    ".sql.gz",
    ".tar",
    ".tar.gz",
    ".wordpress.2025-07-05.xml",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def route_file(dist: Path, route: str) -> Path:
    relative = PurePosixPath(route.strip("/"))
    return dist.joinpath(*relative.parts, "index.html")


def iter_project_files() -> list[Path]:
    excluded = {"node_modules", "dist", ".astro", ".git"}
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in excluded for part in path.parts)
    ]


def verify() -> None:
    if not REPORT.is_file():
        fail("migration report is missing; run npm.cmd run migrate")
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    for key, expected in EXPECTED.items():
        if report.get(key) != expected:
            fail(f"{key}: expected {expected}, got {report.get(key)}")
    if report.get("illegalXmlCharactersRemoved") != {"0x02": 42}:
        fail("unexpected illegal XML character cleanup result")

    posts = sorted((ROOT / "src" / "content" / "blog").glob("legacy-*.md"))
    if len(posts) != EXPECTED["publishedPosts"]:
        fail(f"expected 42 legacy Markdown files, found {len(posts)}")

    media_root = ROOT / "public" / "wp-content" / "uploads"
    media = [path for path in media_root.rglob("*") if path.is_file()]
    if len(media) != EXPECTED["selectedMediaFiles"]:
        fail(f"expected 157 selected media files, found {len(media)}")

    for path in iter_project_files():
        lower_name = path.name.lower()
        if any(lower_name.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
            fail(f"backup-like file is inside the site: {path.relative_to(ROOT)}")
        if path.suffix.lower() not in {".md", ".html", ".json", ".ts", ".js", ".mjs", ".astro", ".txt", ".yml", ".yaml"}:
            continue
        value = path.read_text(encoding="utf-8", errors="ignore")
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in value:
                fail(f"forbidden backup or old-host text in {path.relative_to(ROOT)}: {forbidden}")

    dist = ROOT / "dist"
    if not dist.is_dir():
        fail("dist is missing; run npm.cmd run build before verification")
    routes = report["postRoutes"] + report["legacyPageRoutes"]
    for route in routes:
        if not route_file(dist, route).is_file():
            fail(f"built legacy route is missing: {route}")

    for path in dist.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".html", ".xml", ".txt", ".js", ".css"}:
            continue
        value = path.read_text(encoding="utf-8", errors="ignore")
        for forbidden in FORBIDDEN_TEXT[:2]:
            if forbidden in value:
                fail(f"old host remains in built output: {path.relative_to(dist)}")
        for match in re.findall(r"[\"'](/wp-content/uploads/[^\"'?#]+)", value):
            target = dist.joinpath(*PurePosixPath(match.lstrip("/")).parts)
            if not target.is_file():
                fail(f"built page references missing media: {match}")

    cname = (dist / "CNAME").read_text(encoding="utf-8").strip()
    if cname != "blog.tolinchan.xyz":
        fail(f"unexpected CNAME: {cname}")

    print(
        "PASS: 42 posts, 5 pages, 26 friends, 31 gallery images, "
        "2 comments, 157 media files, routes and secret hygiene verified"
    )


if __name__ == "__main__":
    verify()

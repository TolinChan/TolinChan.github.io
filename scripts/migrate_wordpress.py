#!/usr/bin/env python3
"""Deterministically migrate the local WordPress backups into the Astro site.

The three input archives are read-only. Only explicitly selected public content
and media are written below the requested Astro output directory.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import html
import json
import re
import shutil
import tarfile
import urllib.parse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath


NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}
INTERNAL_HOSTS = ("116.62.4.97", "blog.tolinchan.xyz")
ILLEGAL_XML = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")
INTERNAL_URL = re.compile(
    r"https?://(?:116\.62\.4\.97|blog\.tolinchan\.xyz)/[^\s\"'<>),]+",
    re.IGNORECASE,
)
IMAGE_URL = re.compile(
    r"(?:src|href)=[\"'](https?://[^\"']+)[\"']", re.IGNORECASE
)


def text(node: ET.Element, path: str) -> str:
    child = node.find(path, NS)
    return (child.text or "") if child is not None else ""


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.hidden_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.hidden_depth += 1
        elif tag in {"p", "br", "div", "li", "h1", "h2", "h3", "h4"}:
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.hidden_depth:
            self.hidden_depth -= 1
        elif tag in {"p", "div", "li"}:
            self.parts.append(" ")

    def handle_data(self, data: str) -> None:
        if not self.hidden_depth:
            self.parts.append(data)

    def value(self) -> str:
        return re.sub(r"\s+", " ", "".join(self.parts)).strip()


class ImageExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "img":
            return
        values = {key.lower(): value or "" for key, value in attrs}
        source = (
            values.get("data-original")
            or values.get("data-src")
            or values.get("src")
        )
        if source:
            self.images.append(
                {
                    "src": rewrite_internal_urls(source),
                    "alt": values.get("alt", "").strip(),
                    "title": values.get("title", "").strip(),
                }
            )


def plain_text(value: str) -> str:
    parser = TextExtractor()
    parser.feed(value)
    parser.close()
    return parser.value()


def description_from_html(value: str, limit: int = 180) -> str:
    result = plain_text(value)
    if len(result) <= limit:
        return result
    return result[: limit - 1].rstrip() + "…"


def rewrite_internal_urls(value: str) -> str:
    value = re.sub(
        r"https?://(?:116\.62\.4\.97|blog\.tolinchan\.xyz)(?=/|$)",
        "",
        value,
        flags=re.IGNORECASE,
    )
    return re.sub(
        r"\[toc\]",
        '<nav class="post-toc" data-auto-toc aria-label="文章目录"></nav>',
        value,
        flags=re.IGNORECASE,
    )


def clean_xml(path: Path) -> tuple[ET.Element, dict[str, int]]:
    source = path.read_text(encoding="utf-8", errors="replace")
    removed = collections.Counter(ord(match.group()) for match in ILLEGAL_XML.finditer(source))
    source = ILLEGAL_XML.sub("", source)
    return ET.fromstring(source), {f"0x{key:02x}": value for key, value in removed.items()}


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(values: list[str]) -> str:
    return json.dumps(values, ensure_ascii=False)


def route_for_post(item: ET.Element) -> str:
    date = text(item, "wp:post_date").strip()
    slug = urllib.parse.unquote(text(item, "wp:post_name").strip())
    slug = slug.strip("/").replace("/", "-")
    if not slug:
        slug = f"post-{text(item, 'wp:post_id').strip()}"
    year, month, day = date[:10].split("-")
    return f"/{year}/{month}/{day}/{slug}/"


def iso_shanghai(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    return value.replace(" ", "T") + "+08:00"


def post_terms(item: ET.Element, domain: str) -> list[str]:
    values: list[str] = []
    for category in item.findall("category"):
        if category.attrib.get("domain") == domain and (category.text or "").strip():
            values.append(html.unescape((category.text or "").strip()))
    return list(dict.fromkeys(values))


def write_post(item: ET.Element, content_dir: Path) -> dict[str, object]:
    legacy_id = int(text(item, "wp:post_id").strip())
    title = html.unescape(text(item, "title").strip())
    body = rewrite_internal_urls(text(item, "content:encoded")).strip()
    published = iso_shanghai(text(item, "wp:post_date"))
    updated = iso_shanghai(text(item, "wp:post_modified"))
    route = route_for_post(item)
    categories = post_terms(item, "category")
    tags = post_terms(item, "post_tag")
    frontmatter = [
        "---",
        f"title: {yaml_string(title)}",
        f"description: {yaml_string(description_from_html(body))}",
        f"publishedAt: {yaml_string(published)}",
    ]
    if updated and updated != published:
        frontmatter.append(f"updatedAt: {yaml_string(updated)}")
    frontmatter.extend(
        [
            f"route: {yaml_string(route)}",
            f"categories: {yaml_list(categories)}",
            f"tags: {yaml_list(tags)}",
            f"legacyId: {legacy_id}",
            "draft: false",
            "---",
            "",
            body,
            "",
        ]
    )
    (content_dir / f"legacy-{legacy_id}.md").write_text(
        "\n".join(frontmatter), encoding="utf-8", newline="\n"
    )
    return {
        "legacyId": legacy_id,
        "title": title,
        "route": route,
        "publishedAt": published,
    }


def mysql_columns(sql: str, table: str) -> list[str]:
    match = re.search(
        rf"CREATE TABLE `{re.escape(table)}` \((.*?)\) ENGINE=", sql, re.DOTALL
    )
    if not match:
        raise ValueError(f"Missing schema for {table}")
    return re.findall(r"^\s*`([^`]+)`", match.group(1), re.MULTILINE)


def mysql_unescape(value: str) -> str:
    replacements = {
        "0": "\0",
        "b": "\b",
        "n": "\n",
        "r": "\r",
        "t": "\t",
        "Z": "\x1a",
        "\\": "\\",
        "'": "'",
        '"': '"',
    }
    result: list[str] = []
    index = 0
    while index < len(value):
        if value[index] == "\\" and index + 1 < len(value):
            index += 1
            result.append(replacements.get(value[index], value[index]))
        else:
            result.append(value[index])
        index += 1
    return "".join(result)


def split_mysql_rows(body: str) -> list[str]:
    rows: list[str] = []
    current: list[str] = []
    depth = 0
    quoted = False
    escaped = False
    for char in body:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if quoted and char == "\\":
            current.append(char)
            escaped = True
            continue
        if char == "'":
            quoted = not quoted
            current.append(char)
            continue
        if not quoted and char == "(":
            if depth:
                current.append(char)
            else:
                current = []
            depth += 1
            continue
        if not quoted and char == ")":
            depth -= 1
            if depth == 0:
                rows.append("".join(current))
            else:
                current.append(char)
            continue
        if depth:
            current.append(char)
    return rows


def split_mysql_fields(row: str) -> list[str | None]:
    raw_fields: list[str] = []
    current: list[str] = []
    quoted = False
    escaped = False
    for char in row + ",":
        if escaped:
            current.append(char)
            escaped = False
            continue
        if quoted and char == "\\":
            current.append(char)
            escaped = True
            continue
        if char == "'":
            quoted = not quoted
            continue
        if char == "," and not quoted:
            raw_fields.append("".join(current))
            current = []
        else:
            current.append(char)
    result: list[str | None] = []
    for value in raw_fields:
        stripped = value.strip()
        result.append(None if stripped == "NULL" else mysql_unescape(stripped))
    return result


def mysql_rows(sql: str, table: str) -> list[dict[str, str | None]]:
    columns = mysql_columns(sql, table)
    matches = re.finditer(
        rf"INSERT INTO `{re.escape(table)}`(?:\s*\([^)]*\))? VALUES\s*(.*?);\s*(?:\n|$)",
        sql,
        re.DOTALL,
    )
    rows: list[dict[str, str | None]] = []
    for match in matches:
        for raw_row in split_mysql_rows(match.group(1)):
            values = split_mysql_fields(raw_row)
            if len(values) == len(columns):
                rows.append(dict(zip(columns, values)))
    return rows


def extract_friends(sql_path: Path) -> list[dict[str, str]]:
    with gzip.open(sql_path, "rt", encoding="utf-8", errors="replace") as stream:
        sql = stream.read()
    friends: list[dict[str, str]] = []
    for row in mysql_rows(sql, "wp_links"):
        if row.get("link_visible") != "Y":
            continue
        friends.append(
            {
                "name": html.unescape(str(row.get("link_name") or "")).strip(),
                "url": str(row.get("link_url") or "").strip(),
                "description": plain_text(str(row.get("link_description") or "")),
            }
        )
    return friends


def extract_comments(channel: ET.Element, routes: dict[int, str]) -> list[dict[str, object]]:
    comments: list[dict[str, object]] = []
    for item in channel.findall("item"):
        legacy_id_text = text(item, "wp:post_id").strip()
        if not legacy_id_text:
            continue
        legacy_id = int(legacy_id_text)
        if legacy_id not in routes:
            continue
        for comment in item.findall("wp:comment", NS):
            if text(comment, "wp:comment_approved").strip() != "1":
                continue
            comment_type = text(comment, "wp:comment_type").strip()
            if comment_type not in {"", "comment"}:
                continue
            comments.append(
                {
                    "legacyPostId": legacy_id,
                    "route": routes[legacy_id],
                    "author": html.unescape(
                        text(comment, "wp:comment_author").strip()
                    ),
                    "date": iso_shanghai(text(comment, "wp:comment_date")),
                    "content": plain_text(text(comment, "wp:comment_content")),
                }
            )
    return comments


def internal_archive_path(url: str) -> str | None:
    parsed = urllib.parse.urlparse(html.unescape(url))
    if parsed.hostname not in INTERNAL_HOSTS:
        return None
    path = urllib.parse.unquote(parsed.path).lstrip("/")
    posix = PurePosixPath(path)
    if not path.startswith("wp-content/uploads/") or ".." in posix.parts:
        return None
    return posix.as_posix()


def selected_media(channel: ET.Element) -> set[str]:
    selected: set[str] = set()
    for item in channel.findall("item"):
        post_type = text(item, "wp:post_type").strip()
        status = text(item, "wp:status").strip()
        if post_type == "attachment":
            path = internal_archive_path(text(item, "wp:attachment_url").strip())
            if path:
                selected.add(path)
        if post_type in {"post", "page"} and status == "publish":
            for url in INTERNAL_URL.findall(text(item, "content:encoded")):
                path = internal_archive_path(url)
                if path:
                    selected.add(path)
    return selected


def extract_media(archive_path: Path, output: Path, selected: set[str]) -> int:
    upload_root = output / "public" / "wp-content" / "uploads"
    if upload_root.exists():
        shutil.rmtree(upload_root)
    total_size = 0
    found: set[str] = set()
    with tarfile.open(archive_path, "r:gz") as archive:
        for member in archive:
            if not member.isfile() or member.name not in selected:
                continue
            source = archive.extractfile(member)
            if source is None:
                continue
            destination = output / "public" / PurePosixPath(member.name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("wb") as target:
                shutil.copyfileobj(source, target)
            total_size += member.size
            found.add(member.name)
    missing = sorted(selected - found)
    if missing:
        raise RuntimeError(f"Missing {len(missing)} selected media files: {missing[:5]}")
    return total_size


def external_image_hosts(channel: ET.Element) -> dict[str, int]:
    hosts: collections.Counter[str] = collections.Counter()
    for item in channel.findall("item"):
        if text(item, "wp:post_type").strip() not in {"post", "page"}:
            continue
        if text(item, "wp:status").strip() != "publish":
            continue
        for url in IMAGE_URL.findall(text(item, "content:encoded")):
            parsed = urllib.parse.urlparse(html.unescape(url))
            if parsed.hostname and parsed.hostname not in INTERNAL_HOSTS:
                if re.search(r"\.(?:png|jpe?g|gif|webp|svg)(?:$|\?)", url, re.I):
                    hosts[parsed.hostname] += 1
    return dict(sorted(hosts.items()))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def migrate(args: argparse.Namespace) -> None:
    wxr_path = args.wxr.resolve()
    sql_path = args.sql.resolve()
    archive_path = args.archive.resolve()
    output = args.output.resolve()
    for path in (wxr_path, sql_path, archive_path):
        if not path.is_file():
            raise FileNotFoundError(path)

    root, removed = clean_xml(wxr_path)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("WXR channel not found")

    content_dir = output / "src" / "content" / "blog"
    content_dir.mkdir(parents=True, exist_ok=True)
    for stale in content_dir.glob("legacy-*.md"):
        stale.unlink()

    posts: list[dict[str, object]] = []
    routes: dict[int, str] = {}
    pages: dict[str, ET.Element] = {}
    for item in channel.findall("item"):
        post_type = text(item, "wp:post_type").strip()
        status = text(item, "wp:status").strip()
        if post_type == "post" and status == "publish":
            record = write_post(item, content_dir)
            posts.append(record)
            routes[int(record["legacyId"])] = str(record["route"])
        if post_type == "page" and status == "publish":
            pages[text(item, "wp:post_name").strip()] = item

    about = next(
        (
            item
            for item in pages.values()
            if text(item, "title").strip() == "About To1in"
        ),
        None,
    )
    if about is None:
        raise ValueError("Published About To1in page not found")
    (output / "src" / "data" / "about.html").write_text(
        rewrite_internal_urls(text(about, "content:encoded")).strip() + "\n",
        encoding="utf-8",
        newline="\n",
    )

    gallery_page = next(
        (
            item
            for item in pages.values()
            if text(item, "title").strip() == "旅游相册"
        ),
        None,
    )
    if gallery_page is None:
        raise ValueError("Published gallery page not found")
    gallery_parser = ImageExtractor()
    gallery_parser.feed(text(gallery_page, "content:encoded"))
    gallery: list[dict[str, str]] = []
    seen_gallery: set[str] = set()
    for image in gallery_parser.images:
        if image["src"] not in seen_gallery:
            gallery.append(image)
            seen_gallery.add(image["src"])

    friends = extract_friends(sql_path)
    comments = extract_comments(channel, routes)
    media = selected_media(channel)
    media_bytes = extract_media(archive_path, output, media)

    write_json(output / "src" / "data" / "friends.json", friends)
    write_json(output / "src" / "data" / "gallery.json", gallery)
    write_json(output / "src" / "data" / "legacy-comments.json", comments)

    report = {
        "inputs": {
            "wxrSha256": sha256(wxr_path),
            "sqlSha256": sha256(sql_path),
            "archiveSha256": sha256(archive_path),
        },
        "illegalXmlCharactersRemoved": removed,
        "publishedPosts": len(posts),
        "effectivePublishedPages": 5,
        "friends": len(friends),
        "galleryImages": len(gallery),
        "approvedComments": len(comments),
        "selectedMediaFiles": len(media),
        "selectedMediaBytes": media_bytes,
        "externalImageHosts": external_image_hosts(channel),
        "postRoutes": sorted(str(post["route"]) for post in posts),
        "legacyPageRoutes": [
            "/友情链接/",
            "/about-to1in/",
            "/时光轴/",
            "/文章/",
            "/旅游相册/",
            "/163-2/",
        ],
    }
    write_json(output / "src" / "data" / "migration-report.json", report)

    print(
        json.dumps(
            {
                "posts": len(posts),
                "friends": len(friends),
                "gallery": len(gallery),
                "comments": len(comments),
                "media": len(media),
                "mediaMiB": round(media_bytes / 1024 / 1024, 1),
                "removedXmlCharacters": removed,
            },
            ensure_ascii=False,
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wxr", required=True, type=Path)
    parser.add_argument("--sql", required=True, type=Path)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    migrate(parse_args())

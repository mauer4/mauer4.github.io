import argparse
import os
import re
from datetime import datetime

import feedparser
import requests
import sys


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\-\s]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:80]


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_post(root: str, entry) -> bool:
    link = entry.get("link")
    title = entry.get("title", "Untitled")
    published = entry.get("published") or entry.get("updated")
    summary = entry.get("summary", "").strip()
    content_html = ""
    if entry.get("content"):
        # Prefer full HTML content from feed
        content_html = entry["content"][0].get("value", "")
    elif summary:
        content_html = summary

    # Fallback date
    try:
        if entry.get("published_parsed"):
            dt = datetime(*entry.published_parsed[:6])
        elif entry.get("updated_parsed"):
            dt = datetime(*entry.updated_parsed[:6])
        else:
            dt = datetime.utcnow()
    except Exception:
        dt = datetime.utcnow()

    slug = slugify(title or link or dt.strftime("%Y%m%d%H%M%S"))
    post_dir = os.path.join(root, "content", "post", slug)
    index_md = os.path.join(post_dir, "index.md")

    # Skip if already imported (idempotent): check existing file for medium_link
    if os.path.exists(index_md):
        try:
            with open(index_md, "r", encoding="utf-8") as f:
                existing = f.read()
            if link and ("medium_link: " in existing or "canonical_url:" in existing) and link in existing:
                return False
        except Exception:
            pass

    ensure_dir(post_dir)

    fm = []
    fm.append("---")
    fm.append(f"title: {title!r}")
    fm.append(f"date: {dt.isoformat()}")
    fm.append("authors: ['admin']")
    if summary:
        # Trim long summaries
        clean = re.sub(r"<[^>]+>", "", summary)
        fm.append(f"summary: {clean[:240]!r}")
    if link:
        fm.append(f"canonical_url: {link}")
        fm.append(f"medium_link: {link}")
    fm.append("tags: ['medium']")
    fm.append("draft: false")
    fm.append("---\n")

    body = content_html or ""
    # Ensure relative headings don't break; Medium feeds are HTML already.
    content = "\n".join(fm) + body + "\n"
    with open(index_md, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def main():
    parser = argparse.ArgumentParser(description="Sync Medium RSS to Hugo content")
    parser.add_argument("--feed", required=True, help="Medium RSS feed URL, e.g. https://medium.com/feed/@your_handle")
    parser.add_argument("--root", default=os.getcwd(), help="Site root (default: CWD)")
    args = parser.parse_args()

    # Fetch the feed first to provide clearer errors (status, content-type)
    try:
        resp = requests.get(
            args.feed,
            headers={"User-Agent": "medium-sync/1.0 (+https://github.com/mauer4/mauer4.github.io)"},
            timeout=30,
        )
    except Exception as e:
        raise SystemExit(f"Failed to request feed: {e}")

    if resp.status_code != 200:
        raise SystemExit(f"Failed to fetch feed: HTTP {resp.status_code} from {args.feed}")

    ctype = (resp.headers.get("content-type") or "").lower()
    if "xml" not in ctype and not resp.text.lstrip().startswith("<?xml"):
        print("Warning: Response does not look like RSS/Atom XML (content-type=", ctype, ")", file=sys.stderr)

    d = feedparser.parse(resp.content)
    if d.bozo:
        raise SystemExit(f"Failed to parse feed: {getattr(d, 'bozo_exception', '')}")
    if not getattr(d, 'entries', None):
        raise SystemExit("Parsed feed but found no entries. Is the URL a valid Medium RSS? Expected formats: https://medium.com/feed/@handle or https://handle.medium.com/feed")

    created = 0
    for entry in d.entries:
        if write_post(args.root, entry):
            created += 1

    print(f"Imported {created} new Medium posts.")


if __name__ == "__main__":
    main()

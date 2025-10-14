import base64
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional

import requests
import yaml


@dataclass
class RepoSpec:
    owner: str
    name: str
    featured: bool = False
    summary: Optional[str] = None


GITHUB_API = "https://api.github.com"


def read_config(path: str) -> List[RepoSpec]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    repos = []
    for item in data.get("repos", []):
        full = item.get("repo", "")
        if "/" not in full:
            continue
        owner, name = full.split("/", 1)
        repos.append(
            RepoSpec(
                owner=owner.strip(),
                name=name.strip(),
                featured=bool(item.get("featured", False)),
                summary=item.get("summary"),
            )
        )
    return repos


def gh_headers(token: Optional[str]):
    h = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-readme-sync",
    }
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def get_repo(owner: str, name: str, token: Optional[str]):
    r = requests.get(f"{GITHUB_API}/repos/{owner}/{name}", headers=gh_headers(token), timeout=30)
    r.raise_for_status()
    return r.json()


def get_readme(owner: str, name: str, token: Optional[str]):
    r = requests.get(f"{GITHUB_API}/repos/{owner}/{name}/readme", headers=gh_headers(token), timeout=30)
    r.raise_for_status()
    j = r.json()
    content_b64 = j.get("content", "")
    encoding = j.get("encoding", "base64")
    path = j.get("path", "README.md")
    download_url = j.get("download_url")
    if content_b64 and encoding == "base64":
        raw = base64.b64decode(content_b64).decode("utf-8", errors="replace")
    elif download_url:
        raw = requests.get(download_url, headers=gh_headers(token), timeout=30).text
    else:
        raw = ""
    return raw, path


def rewrite_relative_assets(markdown: str, owner: str, name: str, default_branch: str) -> str:
    # Rewrite relative image and link URLs to raw GitHub URLs so they render on the site
    def repl_img(m):
        alt, url, title = m.group(1), m.group(2), m.group(3) or ""
        if url.startswith("http") or url.startswith("#"):
            return m.group(0)
        url2 = url.lstrip("./")
        raw = f"https://raw.githubusercontent.com/{owner}/{name}/{default_branch}/{url2}"
        return f"![{alt}]({raw}{title})"

    def repl_link(m):
        text, url, title = m.group(1), m.group(2), m.group(3) or ""
        if url.startswith("http") or url.startswith("#"):
            return m.group(0)
        url2 = url.lstrip("./")
        web = f"https://github.com/{owner}/{name}/blob/{default_branch}/{url2}"
        return f"[{text}]({web}{title})"

    # Images: ![alt](url "title")
    markdown = re.sub(r"!\[([^\]]*)\]\(([^\s\)]+)(\s+\"[^\"]*\")?\)", repl_img, markdown)
    # Links: [text](url "title")
    markdown = re.sub(r"\[([^\]]+)\]\(([^\s\)]+)(\s+\"[^\"]*\")?\)", repl_link, markdown)
    return markdown


def write_project(root: str, repo: dict, readme_md: str, featured: bool, summary_override: Optional[str]):
    owner = repo["owner"]["login"]
    name = repo["name"]
    default_branch = repo.get("default_branch", "main")
    title = repo.get("name", name)
    summary = summary_override or repo.get("description", "") or ""

    readme_md = rewrite_relative_assets(readme_md, owner, name, default_branch)

    dest_dir = os.path.join(root, "content", "project", name)
    os.makedirs(dest_dir, exist_ok=True)
    index_md = os.path.join(dest_dir, "index.md")

    fm = []
    fm.append("---")
    fm.append(f"title: {title!r}")
    if summary:
        fm.append(f"summary: {summary!r}")
    fm.append(f"date: {repo.get('created_at', '')}")
    fm.append(f"lastmod: {repo.get('pushed_at', '')}")
    topics = repo.get("topics") or []
    if topics:
        fm.append("tags: [" + ", ".join(repr(t) for t in topics) + "]")
    fm.append(f"external_link: https://github.com/{owner}/{name}")
    fm.append(f"featured: {str(bool(featured)).lower()}")
    fm.append("---\n")

    with open(index_md, "w", encoding="utf-8") as f:
        f.write("\n".join(fm))
        f.write(readme_md.strip())
        f.write("\n")


def main():
    site_root = os.getcwd()
    cfg = os.path.join(site_root, "data", "github_projects.yaml")
    if not os.path.exists(cfg):
        print("Config data/github_projects.yaml not found", file=sys.stderr)
        sys.exit(1)
    specs = read_config(cfg)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    for spec in specs:
        repo = get_repo(spec.owner, spec.name, token)
        readme_md, _ = get_readme(spec.owner, spec.name, token)
        if not readme_md:
            print(f"Skipping {spec.owner}/{spec.name}: no README found", file=sys.stderr)
            continue
        write_project(site_root, repo, readme_md, spec.featured, spec.summary)
        print(f"Updated project: {spec.owner}/{spec.name}")


if __name__ == "__main__":
    main()


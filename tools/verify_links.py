#!/usr/bin/env python3
"""
tools/verify_links.py - Link, Image, Wikilink, and Local Path Leak Auditor

Scans the repository to ensure:
1. 100% of images (![...](...)) resolve to existing files on disk (zero 404s).
2. 100% of relative markdown links ([...](...)) resolve to valid local targets.
3. 100% of Obsidian wikilinks ([[...]]) resolve to indexed file stems or frontmatter aliases.
4. Zero machine-specific path leaks (e.g., /Users/jang/ or file:///Users/...).

Exit code 0 on success, 1 on any failure.
"""

import os
import re
import sys
from pathlib import Path


def audit_repository(repo_root: str = None) -> bool:
    if repo_root is None:
        # Default to repo root relative to this tool
        repo_root = str(Path(__file__).resolve().parent.parent)

    md_files = []
    filename_map = set()
    alias_map = {}

    for root, dirs, files in os.walk(repo_root):
        if ".git" in root or "node_modules" in root:
            continue
        for f in files:
            if f.endswith(".md"):
                full_p = os.path.join(root, f)
                md_files.append(full_p)
                stem = f[:-3].lower()
                filename_map.add(stem)

                # Index aliases & ids from frontmatter
                try:
                    with open(full_p, "r", encoding="utf-8") as file:
                        text = file.read()
                        m_id = re.search(r"^id:\s*([^\n]+)", text, re.MULTILINE)
                        if m_id:
                            clean_id = m_id.group(1).strip(" \"'").lower()
                            filename_map.add(clean_id)
                        
                        m_title = re.search(r"^title:\s*([^\n]+)", text, re.MULTILINE)
                        if m_title:
                            clean_title = m_title.group(1).strip(" \"'").lower()
                            filename_map.add(clean_title)

                        aliases = re.findall(r"aliases:\s*\n((?:\s*-\s*\"?[^\n]+\"?\n?)+)", text)
                        if aliases:
                            for line in aliases[0].split("\n"):
                                line = line.strip().strip("-").strip(" \"'").lower()
                                if line:
                                    filename_map.add(line)
                except Exception as e:
                    print(f"Warning reading {full_p}: {e}")

    broken_images = []
    broken_rel_links = []
    unresolved_wikilinks = []
    path_leaks = []

    img_regex = re.compile(r"\!\[(.*?)\]\((.*?)\)")
    link_regex = re.compile(r"(?<!!)\[(.*?)\]\((.*?)\)")
    wikilink_regex = re.compile(r"\[\[(.*?)\]\]")

    for fpath in md_files:
        rel_path = os.path.relpath(fpath, repo_root)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for local machine path leaks
        if "/Users/jang/" in content or "file:///Users/" in content:
            for line_no, line in enumerate(content.splitlines(), 1):
                if ("/Users/jang/" in line or "file:///Users/" in line) and "git clone" not in line:
                    path_leaks.append((rel_path, line_no, line.strip()[:90]))

        # Check images
        for alt, target in img_regex.findall(content):
            target_path = target.split("#")[0].split("?")[0]
            if target_path.startswith("http://") or target_path.startswith("https://"):
                continue
            abs_img = os.path.normpath(os.path.join(os.path.dirname(fpath), target_path))
            if not os.path.exists(abs_img):
                broken_images.append((rel_path, target))

        # Check relative markdown links
        for text, target in link_regex.findall(content):
            if (
                target.startswith("http://")
                or target.startswith("https://")
                or target.startswith("#")
                or target.startswith("mailto:")
            ):
                continue
            target_path = target.split("#")[0].split("?")[0]
            if not target_path:
                continue
            abs_target = os.path.normpath(os.path.join(os.path.dirname(fpath), target_path))
            if not os.path.exists(abs_target):
                broken_rel_links.append((rel_path, target))

        # Check wikilinks (ignoring fenced code blocks and inline backtick spans)
        non_code_content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        non_code_content = re.sub(r"`[^`\n]+`", "", non_code_content)

        for link in wikilink_regex.findall(non_code_content):
            target = link.split("|")[0].split("#")[0].strip()
            if target == "..." or not target:
                continue
            if target.lower() not in filename_map:
                unresolved_wikilinks.append((rel_path, link))


    print("=" * 60)
    print(f"🔍 AUDIT REPORT: {len(md_files)} Markdown Files Verified")
    print("=" * 60)
    print(f"• Broken Image Links (404s):      {len(broken_images)}")
    for item in broken_images:
        print(f"  ❌ {item[0]} -> {item[1]}")

    print(f"• Broken Relative File Links:     {len(broken_rel_links)}")
    for item in broken_rel_links:
        print(f"  ❌ {item[0]} -> {item[1]}")

    print(f"• Unresolved Wikilinks ([[...]]): {len(unresolved_wikilinks)}")
    for item in unresolved_wikilinks:
        print(f"  ❌ {item[0]} -> [[{item[1]}]]")

    print(f"• Local Path Leaks (/Users/jang): {len(path_leaks)}")
    for item in path_leaks:
        print(f"  ❌ {item[0]}:{item[1]} -> {item[2]}")

    print("=" * 60)

    success = (
        len(broken_images) == 0
        and len(broken_rel_links) == 0
        and len(unresolved_wikilinks) == 0
        and len(path_leaks) == 0
    )

    if success:
        print("✅ 100% HEALTHY: All images, links, wikilinks, and paths verified clean.")
    else:
        print("❌ FAILURES DETECTED: Review items above before committing.")

    return success


if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    passed = audit_repository(target_dir)
    sys.exit(0 if passed else 1)

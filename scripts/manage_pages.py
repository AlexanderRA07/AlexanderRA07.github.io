#!/usr/bin/env python3
"""Manage project pages: new, populate, archive, delete.

Keeps projects/, archive/, and the featured cards on index.html in sync,
so a page and its home page card are never edited by hand separately.
"""
import argparse
import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT / "projects"
ARCHIVE_DIR = ROOT / "archive"
TEMPLATE = PROJECTS_DIR / "_template.html"
INDEX = ROOT / "index.html"


def find_page(name):
    for d in (PROJECTS_DIR, ARCHIVE_DIR):
        p = d / f"{name}.html"
        if p.exists():
            return p
    return None


def check_name(name):
    if name.startswith("_") or "/" in name or name == "index":
        sys.exit(f"error: invalid page name '{name}'")


def card_pattern(name):
    return re.compile(r"[ \t]*<!-- card:%s -->\n.*?</a>\n" % re.escape(name), re.DOTALL)


def remove_card(name):
    text = INDEX.read_text()
    new_text, n = card_pattern(name).subn("", text)
    if n == 0:
        print(f"note: no home page card found for '{name}', nothing to remove")
        return
    INDEX.write_text(new_text)
    print("removed home page card")


def upsert_card(name, title, description, href):
    text = INDEX.read_text()
    block = (
        f'      <!-- card:{name} -->\n'
        f'      <a class="project-card" href="{href}">\n'
        f'        <h3>{html.escape(title)}</h3>\n'
        f'        <p>{html.escape(description)}</p>\n'
        f'      </a>\n'
    )
    pattern = card_pattern(name)
    if pattern.search(text):
        text = pattern.sub(block, text)
        print("updated existing home page card")
    else:
        marker = '<div class="project-grid">'
        idx = text.index(marker)
        end_div = re.search(r"\n([ \t]*)</div>", text[idx:])
        insert_at = idx + end_div.start(1)
        text = text[:insert_at] + block + text[insert_at:]
        print("added new home page card")
    INDEX.write_text(text)


def cmd_new(args):
    check_name(args.name)
    if find_page(args.name):
        sys.exit(f"error: '{args.name}.html' already exists")
    target_dir = ARCHIVE_DIR if args.archive else PROJECTS_DIR
    target = target_dir / f"{args.name}.html"
    text = TEMPLATE.read_text()
    if text.lstrip().startswith("<!--"):
        text = text.split("-->", 1)[1].lstrip("\n")
    target.write_text(text)
    print(f"created {target.relative_to(ROOT)}")
    print("next: run 'populate' to fill it in with real content")


def cmd_populate(args):
    check_name(args.name)
    path = find_page(args.name)
    if not path:
        sys.exit(f"error: no page named '{args.name}.html' found in projects/ or archive/")
    title = html.escape(args.title)
    description = html.escape(args.description)
    live_url = args.live_url or "#"
    live_label = html.escape(args.live_label or "Live site")
    repo_url = args.repo_url or "#"

    text = path.read_text()
    text, n_title = re.subn(
        r"<title>.*? — Alexander</title>", f"<title>{title} — Alexander</title>", text, count=1
    )
    text, n_body = re.subn(
        r"<h1>.*?</h1>\s*<p>.*?</p>",
        f"<h1>{title}</h1>\n    <p>{description}</p>",
        text, count=1, flags=re.DOTALL,
    )
    text, n_links = re.subn(
        r'<div class="project-links">.*?</div>',
        (
            f'<div class="project-links">\n'
            f'      <a href="{live_url}">{live_label}</a>\n'
            f'      <a href="{repo_url}">GitHub repo</a>\n'
            f'    </div>'
        ),
        text, count=1, flags=re.DOTALL,
    )
    if not (n_title and n_body and n_links):
        sys.exit(f"error: '{path.name}' doesn't match the expected page structure — populate expects it to still follow _template.html's layout")
    path.write_text(text)
    print(f"populated {path.relative_to(ROOT)}")

    if path.parent == PROJECTS_DIR:
        upsert_card(args.name, args.title, args.description, f"projects/{args.name}.html")
    else:
        print("page is in archive/ — not linked from the home page")


def cmd_archive(args):
    check_name(args.name)
    src = PROJECTS_DIR / f"{args.name}.html"
    if not src.exists():
        sys.exit(f"error: '{args.name}.html' is not an active page in projects/")
    dst = ARCHIVE_DIR / f"{args.name}.html"
    if dst.exists():
        sys.exit(f"error: '{args.name}.html' already exists in archive/")
    shutil.move(str(src), str(dst))
    print(f"moved projects/{args.name}.html -> archive/{args.name}.html")
    remove_card(args.name)
    print("reminder: add/populate a new featured project to fill its spot on the home page")


def cmd_delete(args):
    check_name(args.name)
    path = find_page(args.name)
    if not path:
        sys.exit(f"error: no page named '{args.name}.html' found in projects/ or archive/")
    if not args.yes:
        answer = input(f"delete {path.relative_to(ROOT)}? [y/N] ").strip().lower()
        if answer != "y":
            print("aborted")
            return
    was_active = path.parent == PROJECTS_DIR
    path.unlink()
    print(f"deleted {path.relative_to(ROOT)}")
    if was_active:
        remove_card(args.name)


def main():
    parser = argparse.ArgumentParser(description="Manage project pages")
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="scaffold a new page from the template")
    p_new.add_argument("name", help="page name without .html, e.g. project-4")
    p_new.add_argument("--archive", action="store_true", help="create it in archive/ instead of projects/")
    p_new.set_defaults(func=cmd_new)

    p_pop = sub.add_parser("populate", help="fill a page's placeholders with real content")
    p_pop.add_argument("name")
    p_pop.add_argument("--title", required=True)
    p_pop.add_argument("--description", required=True)
    p_pop.add_argument("--live-url", help="live URL / demo / notebook link (default: '#')")
    p_pop.add_argument("--live-label", help="link text for the live URL (default: 'Live site')")
    p_pop.add_argument("--repo-url", help="GitHub repo URL (default: '#')")
    p_pop.set_defaults(func=cmd_populate)

    p_arc = sub.add_parser("archive", help="move an active page to archive/ and unlink it from the home page")
    p_arc.add_argument("name")
    p_arc.set_defaults(func=cmd_archive)

    p_del = sub.add_parser("delete", help="delete a page (active or archived)")
    p_del.add_argument("name")
    p_del.add_argument("-y", "--yes", action="store_true", help="skip confirmation prompt")
    p_del.set_defaults(func=cmd_delete)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

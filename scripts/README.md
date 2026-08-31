# scripts/

Run `python3 scripts/manage_pages.py <command> ...` from the repo root to add, fill in, archive, or delete project pages. It keeps `projects/`, `archive/`, and the featured cards on `index.html` in sync, so you never have to hand-edit `index.html` when a page is added, demoted, or removed.

A page `<name>` refers to the filename without `.html`, e.g. `project-4` for `projects/project-4.html`.

## Commands

### `new <name> [--archive]`
Scaffolds a new page from `projects/_template.html`.

```
python3 scripts/manage_pages.py new project-4
python3 scripts/manage_pages.py new project-4 --archive   # create directly in archive/
```

### `populate <name> --title T --description D [options]`
Fills in a page's `{{PLACEHOLDER}}` tokens with real content. If the page lives in `projects/`, its home page card is added/updated automatically; pages in `archive/` don't touch `index.html`.

```
python3 scripts/manage_pages.py populate project-4 \
  --title "My New Project" \
  --description "One-line summary for the card and the detail page." \
  --live-url "https://example.com" \
  --live-label "Live site" \
  --repo-url "https://github.com/AlexanderRA07/my-new-project"
```

`--live-url`, `--live-label`, and `--repo-url` are optional and default to a `#` link / "Live site" label if omitted.

### `archive <name>`
Moves an active page from `projects/` to `archive/` and removes its home page card (demote). Add a replacement featured project with `new` + `populate` afterward.

```
python3 scripts/manage_pages.py archive project-2
```

### `delete <name> [-y]`
Deletes a page, active or archived, removing its home page card if it had one. Prompts for confirmation unless `-y`/`--yes` is passed.

```
python3 scripts/manage_pages.py delete project-4
python3 scripts/manage_pages.py delete project-4 -y   # skip the prompt
```

## Notes
- There's no `promote` command (archive → projects) yet — do it manually by moving the file and running `populate`.
- Names starting with `_` (like `_template`) are reserved and rejected.
- All changes are plain file edits — nothing is committed or pushed automatically.

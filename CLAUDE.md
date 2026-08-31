# Portfolio Website — Project Brief

Note that my github username is AlexanderRA07

## Overview
A personal portfolio website to advertise on a resume and demonstrate projects. Hosted on GitHub Pages at `username.github.io` (repo must be named exactly `<username>.github.io`).

## Tech Stack
- **Languages:** HTML, CSS only — no frameworks, no build tools
- **Hosting:** GitHub Pages (free, auto-deploys on push to main)
- **Dev environment:** Docker devcontainer — do NOT run a local dev server; push to GitHub and preview via the live URL instead

## Design
- Dark themed, clean, professional
- Built from scratch (no templates)
- Mobile responsive (assumed — confirm with user)

## Site Structure

### Pages
```
index.html               ← Home page
projects/
  project-1.html         ← Detail page for featured project 1
  project-2.html         ← Detail page for featured project 2
  project-3.html         ← Detail page for featured project 3
archive/
  project-a.html         ← Archived projects (not linked from home)
  project-b.html
  ...
```

### Home Page Sections
1. Hero / welcome section — aesthetic, introduces the developer
2. Featured Projects — 3 cards, each linking to their detail page
3. (Optional) About, Contact, links to GitHub/LinkedIn — TBD

### Project Detail Pages
Each contains:
- Project title and description
- Links to live URL (if applicable)
- Link to GitHub repository
- Any other relevant resources

### Archive
- Archive pages live in `/archive/` and are not linked from the home page by default
- To **promote** an archived project to the home page: move it to `/projects/`, update the card on `index.html`
- To **demote** a featured project to the archive: move it to `/archive/`, replace its card on `index.html` with the new project
- Future option: add an `/archive/index.html` listing page accessible from the home page nav

## Content (To Be Filled In)
- GitHub username: AlexanderRA07
- Repo: `AlexanderRA07.github.io` (renamed to match GitHub Pages user-site convention; remote is `origin`)
- Project 1: Nutrition App (github hosted website)
- Project 2: Neural Net Number Identifier (google colab)
- Project 3: Data Analysis on Steam User/Critic Review
- Developer name: Alexander
- Tagline: "Software Developer"
- Contact info / social links: TBD — footer currently has a placeholder plus a GitHub link
- Page content (project descriptions, live URLs, repo links): all placeholders for now, to be filled in later

## Decisions Made
- **Navigation bar:** none in v1. Each page includes a commented-out `<nav class="site-nav">` block (Home / Archive links) so a nav can be turned on quickly later by uncommenting it across pages.
- **About / Contact:** no separate section/page — folded into the home page (hero acts as the "about", footer holds contact/social placeholders).
- **Responsiveness:** engineered web-first; `styles.css` has one basic mobile media query as a fallback, not a full responsive pass.
- **Fonts:** placeholder system font stack (`system-ui, sans-serif`) via a CSS variable — swap later in one place.
- **Favicon:** placeholder inline SVG data URI (dark square, "A") — swap later.
- **Page management script:** `scripts/manage_pages.py` handles the full lifecycle and keeps `index.html`'s featured cards in sync automatically:
  - `new <name> [--archive]` — scaffold a page from `_template.html` into `projects/` (or `archive/`)
  - `populate <name> --title T --description D [--live-url U] [--live-label L] [--repo-url R]` — fill placeholders; if the page is in `projects/`, adds/updates its home page card
  - `archive <name>` — move an active page to `archive/` and remove its home page card (demote)
  - `delete <name> [-y]` — delete a page (active or archived), removing its home page card if it had one
  - (promoting archive → projects isn't implemented yet — currently a manual `mv` + `populate`)

## Still To Decide
- Social links — GitHub profile is linked; LinkedIn / email still TBD
- Whether/when to build `archive/index.html` (currently just an empty directory with real content still to come)
- Final fonts and favicon (currently placeholders, see Decisions Made)

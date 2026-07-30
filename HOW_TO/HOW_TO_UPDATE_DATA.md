# How to update the website (new streamlined workflow)

The old workflow (data-entry form → copy text → paste to Claude → Python scripts → commit)
is replaced by **one page**: `admin.html`. It loads the live data, recalculates every
statistic automatically, and publishes straight to GitHub.

## Daily update — 2 minutes

1. Open **https://shashanktamaskar.github.io/science-on-wheels/admin.html**
2. Pick the **date**, **state** and **vehicle**.
3. For each school: name, Google Maps link (coordinates are extracted automatically —
   wait for the ✅), district (dropdown), girls + boys (total auto-fills), and optionally
   the gallery link and collage filename.
4. Distance: leave blank to auto-estimate, or type the odometer figure.
5. Click **🧮 Calculate & preview update** — check the summary line.
6. Click **🚀 Publish to website (GitHub)**. Done. The site refreshes in ~1–2 minutes.

Everything else is computed for you: total schools, students, girls/boys, districts,
states, distance, `lastUpdated`, the dashboard table and the map markers.

## One-time setup (per browser)

The publish button needs a GitHub token (stored only in your browser's localStorage):

1. Go to https://github.com/settings/personal-access-tokens/new
2. Token name: `science-on-wheels-admin` · Expiration: 1 year
3. Repository access: **Only select repositories** → `shashanktamaskar/science-on-wheels`
4. Permissions → Repository permissions → **Contents: Read and write**
5. Generate, copy the token, paste it under **⚙️ GitHub settings** in `admin.html`,
   click **Save settings**.

## No token? Fallback in 1 minute

Click **⬇️ Download data-v2.json** instead, then on github.com open `data-v2.json` →
✏️ Edit → select-all, paste the downloaded file's contents → Commit changes.

## Fixing a mistake

Re-enter the same **date + vehicle** and publish again — the day's entry is replaced,
not duplicated, and all totals are recomputed from scratch.

## What about the old Punjab site?

`punjab.html` + `data.json` are the archived Punjab 2025–26 phase. They are frozen —
don't edit them. The new tools only touch `data-v2.json`.

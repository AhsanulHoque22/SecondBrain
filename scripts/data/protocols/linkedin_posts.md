## LINKEDINPOSTS PROTOCOL

Triggered by: `"LinkedInPosts"` / "write my next LinkedIn post" / "start a new LinkedIn series on [X]" / "brainstorm LinkedIn post ideas" / "post about [topic]" (LinkedIn context).

Home folder: `08_LinkedIn/`. Index: `08_LinkedIn/_index.md`. Each series lives in `08_LinkedIn/Series_[Name]/` with a `_series.md` tracker and one file per post.

### Step 0 — Classify the request
Figure out which mode this is before doing anything else:
- **New series** — user names a new topic that isn't in `08_LinkedIn/_index.md` yet.
- **Next post** — user wants the next post in an existing series.
- **Standalone post** — one-off, not part of any series.
- **Brainstorm only** — user wants ideas, no draft yet.
- **Research only** — user wants source material gathered before writing.

### Step 1 — New series setup (skip if series already exists)
1. Create `08_LinkedIn/Series_[Name]/`.
2. Write `_series.md`: status, start date, angle (one sentence — what makes this series distinct), target audience, cadence (leave open until a rhythm exists), a "Planned posts" table, and a "Backlog / brainstormed angles" list for ideas not yet sequenced.
3. Add the series to the table in `08_LinkedIn/_index.md`.

### Step 2 — Brainstorm
Generate 4-6 candidate angles/hooks for the post in question (not generic — specific to what's actually in this vault: exam-mentor system, protocols, wiki layer, Livora build-in-public, spaced repetition, the Telegram bot, mistakes and fixes). Present the shortlist, note which one was picked and why, and file the rest into the series' backlog so they aren't lost.

### Step 3 — Research
Pull supporting material before writing, in this order:
1. **Vault first** — grep/search this repo for relevant existing notes (course wiki pages, `04_Livora/`, daily logs, `01_Master_Plan.md`) via `obsidian-cli` vault search or `grep`. Never re-derive something the vault already has written down.
2. **External** — if the post needs outside context (a framework name, a stat, a technique), use `WebSearch`/`defuddle`, not memory.
3. Note every vault source used so it can be wikilinked in Step 5.

### Step 4 — Draft the post
Write `08_LinkedIn/Series_[Name]/[NN]_[Slug].md` (or `08_LinkedIn/Standalone/[date]_[Slug].md` for one-offs). Use the `obsidian-markdown` skill for syntax. Structure:

```yaml
---
series: "[Name or 'standalone']"
status: draft        # draft -> scheduled -> posted
target_publish_date:
tags:
  - linkedin-post
---
```
- **Hook** — first 1-2 lines, must stand alone in the LinkedIn feed preview.
- **Body** — short paragraphs (1-3 lines each), concrete detail over abstraction, one real example from the vault/life, not generic advice.
- **Close** — a question, takeaway, or soft CTA.
- **Hashtags** — 3-5, relevant, no spam.
- A `## Sources` section at the bottom with wikilinks to whatever vault notes were used in Step 3.

### Step 5 — Link everything
- Update the series' `_series.md` Planned Posts table: status → drafted, wikilink to the new post.
- Update `08_LinkedIn/_index.md` if this is a new series or changes the active list.
- Add wikilinks from the post to any vault notes it draws on (Step 3 sources) — this is what makes research reusable for the *next* post instead of starting cold each time.

### Step 6 — Evolve this protocol
After each run, check whether something about *how* this task gets done changed or repeated (a post structure that worked well, a research shortcut, a recurring series-planning question). If so, append a dated entry under **Protocol Evolution Log** below — don't silently repeat undocumented tribal knowledge next time. Keep entries terse (1-2 lines). If a pattern shows up 2+ times, fold it into the steps above instead of leaving it as a log entry.

### Step 7 — Git commit
```bash
git add -A && git commit -m "linkedin: [series/post] — [one-line description]"
```

---

## Protocol Evolution Log
- 2026-07-08 — Protocol created. First series ("Second Brain") and first post ("Introduction") drafted as the initial run.

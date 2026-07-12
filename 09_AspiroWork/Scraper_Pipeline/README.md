# Scraper Pipeline

## Introduction

Before this pipeline existed, scraping study-abroad program data (Netherlands,
Malta — see `../Data Collection/`) was a manual process: fetch search-result
pages by hand, extract program links, dispatch parallel agents to read each
page and fill in a CSV row, then run a second verification pass to catch
mistakes. It worked, but it didn't scale past a couple of countries and had
no reusable code behind it.

This pipeline replaces that manual process with three small, single-purpose
Python scripts — collect, extract, clean — chained by one CLI orchestrator.
Point it at a list of program-page URLs and it produces the same 17-column
CSV the manual process did, without a human reading every page.

## What this pipeline does

Given one or more URLs to individual master's-program pages, it:

1. Fetches and caches the raw HTML for each URL (clearing Cloudflare/WAF
   bot-protection automatically where needed).
2. Extracts the Appendix A program fields (university, level, program name,
   tuition, deadlines, requirements, tags, etc.) using an LLM cascade that
   generalizes across arbitrary site layouts — no per-site selectors to
   maintain — with a zero-setup heuristic fallback if no LLM is reachable.
3. Normalizes, validates, and de-duplicates each record, then appends it to
   a flat output CSV in the same schema already used across
   `Data Collection/`.

## What it's used for

Feeding `09_AspiroWork/Data Collection/` — the source data for AspiroBrain's
study-abroad advisory database. Previously that data was scraped from
mastersportal.com only, one country at a time, entirely by hand. This
pipeline is the automated replacement: it's designed to work on
mastersportal.com pages *and* on individual university sites directly (e.g.
ox.ac.uk course pages) — anywhere a program's details live on one page.

## Architecture

```
   ┌───────────────────────────────────────────┐
   │  0. DISCOVER (optional, mastersportal.com)  │
   │  discover.py                                │
   │                                              │
   │  listing/search URL  →  collector.fetch_html │
   │  → regex for /studies/<id>/<slug>.html links │
   │  → walk page=1..N  →  dedupe  →  urls.txt    │
   └─────────────────────┬───────────────────────┘
                         │  urls.txt
                         ▼
                    ┌─────────────────────────────────────────────┐
                    │              pipeline.py (CLI)               │
                    │   --url / --url-file  →  loop over URLs      │
                    └─────────────────────┬─────────────────────────┘
                                          │  for each URL
                                          ▼
   ┌─────────────────┐   ┌──────────────────────────────┐   ┌──────────────────┐
   │  1. COLLECT      │   │  2. EXTRACT                    │   │  3. CLEAN         │
   │  collector.py    │──▶│  extractor.py                  │──▶│  cleaner.py       │
   │                  │   │                                 │   │                  │
   │  requests GET    │   │  clean_text_from_html()         │   │  normalize fields │
   │       │403       │   │       │                          │   │  currency split   │
   │       ▼           │   │       ▼                          │   │  flatten repeats  │
   │  Playwright        │   │  ┌─ Haiku 4.5  ──validator──┐   │   │  validate required │
   │  headless fallback │   │  │ Sonnet 5   (on failure)  │   │   │  dedupe + append   │
   │       │           │   │  │ Opus 4.8   (on failure)   │   │   │  to output CSV     │
   │       ▼           │   │  └───────────┬───────────────┘   │   │                  │
   │  cache to raw/     │   │              │ all tiers failed  │   │                  │
   │  (.html+.meta.json)│   │              ▼                  │   │                  │
   │                  │   │       heuristic fallback        │   │                  │
   │                  │   │  (JSON-LD / og:tags / regex)    │   │                  │
   └─────────────────┘   └──────────────────────────────┘   └──────────────────┘
```

| File | Stage | Responsibility |
|---|---|---|
| `schema.py` | — | Canonical 17-field list + which 3 are required |
| `discover.py` | Discover (optional) | Extract individual program links from a mastersportal.com listing page, walk pagination, write a URL list |
| `collector.py` | Collect | Fetch raw HTML, clear Cloudflare/WAF via a headless-browser fallback, cache to disk |
| `extractor.py` | Extract | Haiku → Sonnet → Opus cascade with a free validator gate; heuristic fallback if no LLM is reachable |
| `cleaner.py` | Clean | Normalize, validate required fields, dedupe, append to CSV |
| `pipeline.py` | — | CLI orchestrator; chains the three stages per URL, keeps going on per-URL failure |

## How to use it

### Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/playwright install chromium
```

For LLM-based extraction (recommended — generalizes across arbitrary site
layouts instead of relying on the weaker heuristic path), set
`ANTHROPIC_API_KEY` or run `ant auth login`. Without either, every page falls
straight through the LLM cascade to heuristic extraction — lower recall, but
works with zero setup.

The `playwright install chromium` step downloads the headless browser used
only as the Cloudflare/WAF fallback (see Known limitations below). Skipping
it is fine — the collector still works for any site that doesn't block plain
`requests`; it just can't clear a bot-protection wall without it.

### Run

```bash
./.venv/bin/python pipeline.py --url "https://example.com/msc-program-page"
./.venv/bin/python pipeline.py --url-file urls.txt
./.venv/bin/python pipeline.py --url-file urls.txt --output output/my_batch.csv --raw-dir raw/my_batch
```

Output: `output/programs.csv` by default. Raw HTML snapshots are cached in
`raw/` (one `.html` + `.meta.json` per URL, keyed by a hash of the URL), so
extraction can be re-run later without re-fetching. Each line printed during
a run is one of `OK` / `DUPLICATE` / `SKIPPED` / `FAILED`, followed by a
summary count.

### Discover (optional — mastersportal.com only, for now)

If you have a search/listing page URL instead of individual program URLs,
generate a `urls.txt` first and feed it straight into the run above:

```bash
./.venv/bin/python discover.py --url "https://www.mastersportal.com/search/master/2-years/netherlands" --pages 5 --output urls.txt
./.venv/bin/python pipeline.py --url-file urls.txt
```

`--pages N` walks `page=1..N` of the same search (20 results per page on
mastersportal.com) and de-duplicates across pages. This only works for
mastersportal.com right now — see Drawbacks below.

## Challenges faced, and how they were solved

**1. Cloudflare/WAF blocked the collector outright.**
mastersportal.com and ox.ac.uk both return 403 to a plain `requests` call
with a real User-Agent header — the same wall that forced the original
scraping work to be done by hand. Fixed by adding a headless-browser
(Playwright) fallback that fires specifically on a 403: it executes the
page's JavaScript, which clears most "checking your browser" challenges,
then hands the resulting HTML back to the same caching path. Verified live
against mastersportal.com: the plain-`requests` call 403s as expected, the
fallback then pulls the real page (145KB of HTML) successfully.

**2. A mid-edit annotation pass had broken the collector.**
Before this session's changes, `collector.py` had two live syntax errors
from an in-progress pass of explanatory comments — `import return` instead
of `import requests`, and an unterminated docstring at the end of the file.
The module couldn't even be imported. Fixed both while keeping the
educational comments intact.

**3. The headless-browser fallback had no retry of its own.**
Running the pipeline against a real 13-URL batch of Oxford course pages
surfaced two `net::ERR_NETWORK_CHANGED` failures — a one-off network blip,
confirmed transient by re-fetching the same two URLs directly and getting
them on the first try. The plain-`requests` path already retried transient
failures; the Playwright fallback didn't. Fixed by giving it the same
retry-with-backoff budget.

**4. The heuristic extractor returned nothing on real (non-mastersportal)
pages.** With no `ANTHROPIC_API_KEY` configured, extraction falls through to
a heuristic path — and on the same 13-URL Oxford batch, every single row
came back with the three *required* fields empty, because that path only
ever read `university_name`/`program_name` from `schema.org` JSON-LD Course
markup, which ox.ac.uk (and most ordinary sites) doesn't have. The data was
sitting right there in standard `<title>`/`og:title`/`og:site_name` meta
tags the heuristic never looked at. Fixed by adding those as fallbacks, plus
a degree-prefix regex (`MSc`, `MPhil`, `MSt`, …) to backfill `level` from the
program name.

**5. A regex false-positive corrupted `application_fee`.** Once the fields
above were being populated, `application_fee` on several Oxford rows came
back as `"applicants from low-income countries;"` — an unrelated sentence
elsewhere on the page that happened to sit after a colon. The label-to-colon
gap in that regex was unbounded, so it matched the *nearest colon anywhere
in the text* rather than one actually attached to the label. Fixed by
capping the gap at 30 characters and rejecting any captured value with no
digit in it (these fields are always numeric/currency, so a non-numeric
capture is prose, not data).

**6. Extraction always called the most expensive model, with no check on
its output.** The extractor originally hardcoded `claude-opus-4-8`
($5/$25 per MTok) for every single page, and accepted whatever it returned
with no semantic validation — a "successful" API call with an empty required
field went straight to the CSV uncaught. Redesigned as a 3-tier cascade
(Haiku 4.5 → Sonnet 5 → Opus 4.8), cheapest first, gated by a free
deterministic validator (checks required fields aren't empty/placeholder,
numeric fields contain a digit). A page only pays for a stronger model if
the cheaper one's output actually fails validation, and the escalation
prompt carries the validator's specific complaints so the retry is a
correction rather than a second blind guess.

**7. Feeding the pipeline a search-results page silently produced nothing
useful.** Pointing `pipeline.py` directly at a mastersportal.com search URL
"worked" (no crash) but every URL came back `SKIPPED` — a search page lists
~20 different programs, so there's no single `university_name`/`level`/
`program_name` for it to extract, and both the LLM tiers and the heuristic
path correctly refused to fabricate one. The real need was a separate
discovery step. First attempt at building it used the wrong link pattern
(`href="/studies/..."`) and found zero links on a page that plainly had real
listings on it (confirmed via screenshot); the actual links turned out to be
embedded as JSON data (`"url":"/studies/8997/....html"`), not `<a href>`
tags — a bare regex on the raw HTML found all of them. Landed as `discover.py`,
reusing `collector.py`'s existing fetch (no new dependency needed).

## Tests done, and what came out of them

- **Playwright fallback, live:** fetched a real mastersportal.com program
  page through the full `collect()` path — plain `requests` returned 403 as
  expected, the headless-browser fallback then returned 145,058 bytes of
  real HTML, correctly cached to disk.
- **Full pipeline, live, real batch:** ran `pipeline.py` end-to-end against
  13 real Oxford graduate-course URLs (deliberately chosen: a genuinely
  Cloudflare-blocked, non-mastersportal site, spanning CS, physics,
  education, migration studies, theology, linguistics, and music — not a toy
  set). Result after the fixes above: **13/13 collected, 13/13 written to
  the output CSV**, all with correct `university_name` ("Oxford
  University"), `level` (MSc/MPhil/MSt), and `program_name` — via the
  heuristic path, since this environment has no `ANTHROPIC_API_KEY`
  configured. Re-ran a second time after the `application_fee` regex fix to
  confirm the garbage value was gone and every other field stayed intact.
- **Cascade/escalation logic:** since this environment can't reach the live
  LLM tiers, the new Haiku→Sonnet→Opus logic was verified with mocked model
  responses instead of a real API batch: a clean tier-1 (Haiku) result makes
  **exactly one** API call and returns tagged `llm-haiku`; a tier-1 result
  missing a required field is correctly rejected by the validator, escalates
  to tier 2 (Sonnet) **with the validator's exact complaint attached to the
  retry prompt**, and the corrected result returns tagged `llm-sonnet`.
  Re-ran the same 13-URL Oxford batch afterward to confirm the cascade still
  falls through cleanly to the heuristic path end-to-end when no credentials
  are present.
- **Discover, live:** ran `discover.py` against a real mastersportal.com
  Netherlands search, 2 pages — **40 unique program links** written to a
  URL file, 20 per page, correctly de-duplicated across pages. Fed a 3-URL
  sample of that output straight into `pipeline.py --url-file`: all 3
  cleared the Cloudflare 403 wall and collected successfully (proving the
  full discover → urls.txt → pipeline chain the user asked for actually
  works end-to-end). Extraction on those 3 came back `SKIPPED` for `level`
  under the heuristic-only path — mastersportal's titles don't follow the
  "MSc in X" pattern the degree-prefix regex looks for, a known instance of
  the heuristic-recall drawback below, not a discovery-stage bug.

## Drawbacks / known limitations

- **The Haiku/Sonnet/Opus cascade has never been run against the live API.**
  Everything above about it is verified via mocked responses, not a real
  batch — actual accuracy, actual escalation rate, and actual cost per page
  are unmeasured until it's run with a real `ANTHROPIC_API_KEY`.
- **The zero-setup heuristic path has real gaps.** Even after the
  `og:title`/`og:site_name` fix, it still can't reliably pull
  `tuition_1st_year`, `duration`, `success_rate`, or `program_image_url` on
  sites that don't expose them in a plain "Label: value" line — confirmed
  empty on all 13 rows of the Oxford test batch. The `level` backfill regex
  is similarly narrow: it only catches a degree abbreviation at the very
  start of the program name ("MSc in X"), so it missed `level` on all 3
  mastersportal.com pages tested, whose titles read like "Joint Master in X
  ... at University Y" instead. This is the expected trade-off of the
  zero-setup path, not a bug, but it means heuristic-only runs produce thin
  data outside the required fields, and even those three aren't guaranteed
  on every site's title convention.
- **No coverage for a WAF that also fingerprints headless Chromium.** The
  Playwright fallback has only been proven against sites that block plain
  `requests` but don't detect a real browser. A site that blocks *both*
  would still show up as `FAILED` — untested, unknown how common this is.
- **URL discovery only covers mastersportal.com.** `discover.py`'s link
  pattern (`/studies/<id>/<slug>.html`) and pagination (`page=N`) are
  specific to that site. Oxford's own course-listing page, for example,
  renders results via a JS widget that isn't captured the same way (a plain
  Playwright fetch of it comes back empty even with a network-idle wait) —
  discovering URLs for a new, non-mastersportal site is still a manual step.
- **No real rate limiting anywhere in the pipeline** — `collector.py` has no
  delay between URLs in a batch at all, and `discover.py` only has a flat
  1.5s delay between listing pages. mastersportal.com's Cloudflare
  protection was observed to intermittently hard-block (not just
  soft-challenge) this same IP during this session's testing, for reasons
  that weren't isolated — possibly request-volume-based, since it happened
  after repeated testing in a short window. A run on a fresh IP/session may
  behave differently than what was tested here, and a large batch on one IP
  risks tripping a stricter response than the ones already seen.
- **The validator is itself heuristic**, not a ground-truth check — it
  confirms a field is present and numeric-looking, not that the *value* is
  actually correct. A plausible-but-wrong number would still pass.
- **Escalation adds latency, worst case 3x.** A page that fails validation
  twice makes three sequential API calls before falling back to heuristic;
  this should be rare in practice but hasn't been measured on a real batch.
- **Flat CSV output only.** No structured/database storage, no Bronze-style
  immutable snapshotting — both were flagged as future work in
  `../AspiroBrain_Data_Pipeline_Plan.md` but aren't part of this pipeline.

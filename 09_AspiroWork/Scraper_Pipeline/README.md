# Scraper Pipeline

A small, self-contained pipeline that turns program-listing pages and
individual program pages into a clean, deduplicated CSV — without a human
reading every page by hand. Point it at one URL, a file of URLs, or a
search/listing page, and it fetches, extracts, normalizes, and writes the
data for you.

It ships with **no fixed AI vendor or model** — you choose which LLM
provider to use (or none at all) via configuration, described in the
[User Manual](#user-manual) below.

## Features

- **Four independently runnable stages** — discover, collect, extract,
  clean — chained by one CLI orchestrator (`pipeline.py`), so you can run
  the whole thing end-to-end or use any stage on its own.
- **Multi-provider LLM extraction.** Structured-field extraction works
  against Anthropic, OpenAI, or Google Gemini, selected by an environment
  variable — no code changes needed to switch providers or models.
  See [Provider status](#provider-status) for what's been verified.
- **Cost-aware multi-tier model cascade.** Configure a list of models from
  cheapest/fastest to most capable; a deterministic validator gates each
  tier's output, and a page only escalates to a stronger (pricier) model
  when the cheaper one's output actually fails validation.
- **Zero-setup heuristic fallback.** With no LLM configured at all — or if
  every configured tier fails — extraction falls back to JSON-LD, Open
  Graph, and regex-based heuristics. Lower recall, but the pipeline never
  simply stops.
- **Deterministic output validation.** Every LLM extraction is checked for
  required fields, correct numeric shape, and source-text grounding (a
  numeric value's digits must actually appear on the page) before it's
  accepted — catches empty and hallucinated fields without a second LLM
  call.
- **Cloudflare/WAF bypass.** Sites that return 403 to a plain HTTP request
  are retried automatically through a headless-browser (Playwright)
  fallback that executes the page's JavaScript.
- **Hard-block detection.** A Cloudflare "you have been blocked" page is
  detected and treated as a failure, not silently cached as if it were real
  page content.
- **Site discovery with pagination.** Turn a search/listing page into a
  list of individual program URLs, walking multiple result pages and
  de-duplicating as it goes.
- **Optional LLM-based discovery (`--llm-discovery`), for any site.** The
  default discovery path needs a small regex pattern registered per site
  (see [Limitations](#limitations)). `--llm-discovery` instead does a free,
  generic pass to collect every same-domain URL-shaped candidate on the
  page, then a small, cheap LLM call classifies which candidates are real
  program pages — works on an unregistered site with no code changes, at a
  fraction of a cent per listing page. See [Estimating discovery
  cost](#estimating-discovery-cost).
- **Cross-run discovery memory.** Every URL ever discovered is kept in a
  persistent manifest, so re-running discovery against an overlapping
  search only reports what's genuinely new.
- **Change detection (`--refresh`).** Re-check an already-scraped URL
  cheaply via a content hash, and only pay for re-extraction if the page's
  content actually changed — the existing CSV row is updated in place, not
  duplicated.
- **Resume by default.** Interrupt a batch at any point (crash, block,
  closed laptop) and rerun the same command — URLs already written to the
  output CSV are skipped automatically.
- **Rate limiting and block cooldown.** Configurable delay between
  requests, plus a longer cooldown specifically after a hard block is
  detected, before continuing to the next URL.
- **Atomic, crash-safe writes.** Both the output CSV and all JSON state
  files are written via a temp-file-then-rename pattern, so a crash
  mid-write can never leave a corrupted file.
- **Per-batch cost/token reporting.** Every LLM call's real token usage is
  tracked and summarized per model at the end of a run, priced at standard
  list rates.
- **Deterministic, no-network test suite.** 92 `pytest` tests cover every
  pure-logic component (validators, normalizers, regex tiers, schema
  translation, cascade/escalation logic) with all network and LLM calls
  mocked.
- **Smoke-test script (`canary.py`).** Runs the real collect → extract path
  against a small set of known-good URLs, so a supported site quietly
  changing its layout gets caught before a real batch comes back empty.
- **Optional `.env` support.** Configuration can be set as real environment
  variables or in a local `.env` file (auto-loaded if `python-dotenv` is
  installed).

## Limitations

- **Only the Anthropic provider has been run against a live API in this
  project.** The OpenAI and Google Gemini adapters are implemented against
  each vendor's documented API contract but have not been exercised against
  a live account. Review their output on a handful of real pages before
  trusting either for a full batch. See [Provider status](#provider-status).
- **The heuristic fallback has real gaps.** It reliably reads
  `university_name`, `program_name`, and a heuristic `level` guess, but
  fields like `tuition_1st_year`, `duration`, `success_rate`, and
  `program_image_url` are only picked up if the page exposes them as a
  plain "Label: value" line or standard JSON-LD/Open Graph metadata. A page
  with a genuinely different layout convention can come back with those
  fields empty. This is the expected trade-off of a zero-setup fallback,
  not a bug — it exists so the pipeline never simply stops, not to match
  LLM-tier recall.
- **No defense against a WAF that also fingerprints headless browsers.**
  The Playwright fallback clears sites that block plain HTTP requests but
  don't detect a real (if headless) browser. A site that blocks both will
  still fail collection.
- **URL discovery ships with one site pattern (mastersportal.com)
  registered** for the free, deterministic path. Adding a second pattern is
  meant to be a small, contained change — see [Adding a new discovery
  site](#adding-a-new-discovery-site) — but no second pattern has been
  built or tested. `--llm-discovery` (see
  [Features](#features)/[Estimating discovery
  cost](#estimating-discovery-cost)) works on an unregistered domain
  without a pattern, at a small LLM cost — but multi-page pagination there
  still needs a registered pattern to know the site's query-string
  convention, so an unregistered domain with `--llm-discovery` and
  `--pages > 1` collapses to fetching page 1 only rather than guessing a
  pagination scheme. Pointing plain `discover.py` (no `--llm-discovery`) at
  an unregistered domain still raises a clear error rather than silently
  returning nothing.
- **Rate limiting is a flat delay, not adaptive.** `--delay` and
  `--block-cooldown` are fixed values you set upfront, not a backoff that
  tunes itself to how a site is actually responding.
- **Source-grounding validation isn't perfect.** It only checks whether a
  numeric value's digits appear somewhere on the page — a value the model
  legitimately computed or reformatted (rather than copied verbatim) could
  be flagged as "not grounded" even when it's correct, triggering an
  unnecessary but harmless escalation.
- **Resume keys on exact source URL only**, which is coarser than the
  cleaner's own duplicate check (university + program name + URL). Two
  different URLs describing the same program won't be caught by resume,
  though they'd still be caught as a duplicate if actually reprocessed.
- **`--refresh` change detection can occasionally report a false positive.**
  It hashes the page's cleaned text, not the raw HTML — in testing, two
  fetches of a genuinely unchanged real page landed on different hashes
  once, most likely because of headless-browser render-timing variance
  rather than an actual page change. Not reliably reproduced across
  follow-up controlled fetches. The failure direction is the safer one
  (occasionally re-extracts something that didn't change; should never
  silently miss a real change), but the real false-positive rate on a large
  batch is unmeasured. See `state/README.md` for the full design notes.
- **Atomic CSV writes rewrite the whole file per append** — fine at the
  scale this pipeline targets (hundreds to low thousands of rows), but
  would need a real database well before tens of thousands of rows.
- **Escalation adds latency, worst case one API call per cascade tier.** A
  page that fails validation at every tier makes one sequential call per
  tier before falling back to the heuristic path.
- **`canary.py` isn't wired into a scheduler.** It exists and works, but
  something has to actually run it — cron, CI, or manually — for it to
  catch a layout regression.
- **Flat CSV output only.** No structured database storage and no
  versioned/immutable snapshotting of raw pages beyond the `raw/` HTML
  cache.

## Architecture

```
   ┌───────────────────────────────────────────┐
   │  0. DISCOVER (optional, mastersportal.com)  │
   │  discover.py                                │
   │                                              │
   │  listing/search URL  →  collector.fetch_html │
   │  → site-specific link regex (SITE_PATTERNS)  │
   │  → walk page=1..N  →  merge into             │
   │    state/discovered_urls.json (cross-run)    │
   │  → urls.txt = only new links this run        │
   └─────────────────────┬───────────────────────┘
                         │  urls.txt
                         ▼
                    ┌─────────────────────────────────────────────┐
                    │              pipeline.py (CLI)               │
                    │  --url / --url-file  →  loop, delay+jitter   │
                    │  skip already-in-output (resume) per URL,    │
                    │  or (--refresh) re-check via content hash    │
                    │  in state/extraction_state.json              │
                    └─────────────────────┬─────────────────────────┘
                                          │  for each new/changed URL
                                          ▼
   ┌─────────────────┐   ┌──────────────────────────────┐   ┌──────────────────┐
   │  1. COLLECT      │   │  2. EXTRACT                    │   │  3. CLEAN         │
   │  collector.py    │──▶│  extractor.py + llm_providers.py│──▶│  cleaner.py       │
   │                  │   │                                 │   │                  │
   │  requests GET    │   │  clean_text_from_html()         │   │  normalize fields │
   │       │403       │   │       │                          │   │  currency split   │
   │       ▼           │   │       ▼                          │   │  flatten repeats  │
   │  Playwright        │   │  ┌─ model tier 1 ──validator─┐   │   │  validate required │
   │  headless fallback │   │  │ model tier 2  (on failure) │   │   │  dedupe + append   │
   │       │           │   │  │ model tier N  (on failure) │   │   │  (atomic write)    │
   │       ▼           │   │  └───────────┬───────────────┘   │   │                  │
   │  hard-block check  │   │              │ all tiers failed  │   │                  │
   │       │           │   │              ▼                  │   │                  │
   │       ▼           │   │       heuristic fallback        │   │                  │
   │  cache to raw/     │   │  (JSON-LD / og:tags / regex)    │   │                  │
   └─────────────────┘   └──────────────────────────────┘   └──────────────────┘

   Also: canary.py (smoke test against known-good real URLs) and
   tests/ (pytest — pure-logic tests, no network) run independently of
   the pipeline itself, not part of the per-URL flow above.
```

| File | Stage | Responsibility |
|---|---|---|
| `schema.py` | — | Canonical output field list + which are required |
| `discover.py` | Discover (optional) | Extract individual program links from a listing page — site-pattern registry by default, or `--llm-discovery` (generic candidate scan + LLM classification, any site) — walk pagination, merge into a persistent cross-run manifest, write only new links |
| `collector.py` | Collect | Fetch raw HTML, clear Cloudflare/WAF via a headless-browser fallback, detect hard blocks, cache to disk |
| `extractor.py` | Extract | Multi-tier model cascade with a deterministic validator gate (required fields, numeric shape, source-grounding); heuristic fallback if no LLM is reachable |
| `llm_providers.py` | Extract, Discover | Provider adapter layer — dispatches a structured-output call to Anthropic, OpenAI, or Google Gemini behind one common interface; used by both `extractor.py` (field extraction) and `discover.py` (`--llm-discovery` link classification) |
| `cleaner.py` | Clean | Normalize, validate required fields, dedupe, atomically append to CSV |
| `pipeline.py` | — | CLI orchestrator: delay/jitter, hard-block cooldown, resume-skip or `--refresh` change-check, cost/token report |
| `canary.py` | — | Smoke test: known-good real URLs, run periodically to catch silent site-layout breakage |
| `tests/` | — | `pytest` suite for every pure-logic piece above (92 tests, no network) |
| `pytest.ini` | — | Points `pytest` at `tests/` |
| `.env.example` | — | Template for the environment variables described below |
| `state/discovered_urls.json` | — | Persistent cross-run discovery manifest, written/merged by `discover.py`. Git-tracked (see `state/README.md`) |
| `state/extraction_state.json` | — | Per-URL content-hash record, written by `extractor.record_extraction_state()`, read by `pipeline.py --refresh`. Git-tracked (see `state/README.md`) |

## User Manual

### Requirements

- Python 3.10+
- An API key for whichever LLM provider you choose (optional — see
  [Running with no LLM configured](#running-with-no-llm-configured))

### Installation

```bash
git clone <this repository's URL>
cd Scraper_Pipeline

python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/playwright install chromium
```

`playwright install chromium` downloads the headless browser used only as
the Cloudflare/WAF fallback. Skipping it is fine — the collector still
works for any site that doesn't block plain HTTP requests; it just can't
clear a bot-protection wall without it.

`requirements.txt` installs the `anthropic` SDK by default (Anthropic is
the provider with a built-in default model cascade — see below). If you
plan to use OpenAI or Google Gemini instead, also install that vendor's
SDK:

```bash
./.venv/bin/pip install openai              # if using LLM_PROVIDER=openai
./.venv/bin/pip install google-generativeai # if using LLM_PROVIDER=google
```

### Configuration

Copy `.env.example` to `.env` and fill in your values (auto-loaded on every
run if `python-dotenv` is installed, which it is by default):

```bash
cp .env.example .env
```

| Variable | Required | Purpose |
|---|---|---|
| `LLM_PROVIDER` | No (defaults to `anthropic`) | Which vendor to use: `anthropic`, `openai`, or `google` |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GOOGLE_API_KEY` | Yes, for the provider you chose | Credential for that vendor's SDK |
| `EXTRACTION_MODEL_CASCADE` | Yes, unless `LLM_PROVIDER=anthropic` | Comma-separated model IDs, cheapest/fastest first |
| `DISCOVERY_MODEL` | Only if using `--llm-discovery` with a non-`anthropic` provider | Single model ID used to classify candidate links (no cascade — see [Estimating discovery cost](#estimating-discovery-cost)) |

**Model IDs are never hardcoded for OpenAI or Google in this project** —
only the Anthropic cascade ships with a built-in default, because it's the
only provider this pipeline has actually been run against. For any other
provider, check that vendor's current documentation for valid model names
and set `EXTRACTION_MODEL_CASCADE` yourself, for example:

```bash
LLM_PROVIDER=openai
EXTRACTION_MODEL_CASCADE=<your-cheap-model>,<your-strong-model>
```

Each configured model is tried in order; a model only escalates to the
next one in the list if the deterministic validator rejects its output
(missing required field, non-numeric value in a numeric field, or a value
that doesn't appear anywhere in the source page).

#### Provider status

| Provider | Status |
|---|---|
| Anthropic | Exercised against the live API during this pipeline's development. Has a built-in default model cascade. |
| OpenAI | Implemented against OpenAI's documented strict function-calling contract. Not exercised against a live account — verify on real pages before trusting it for a full batch. |
| Google Gemini | Implemented against the documented `google-generativeai` structured-output contract, including a schema-translation step (Gemini's schema dialect differs from plain JSON Schema). The least-verified of the three — review carefully before relying on it. |

#### Estimating cost

Because each page is one independent, stateless API call — a page's cost
never depends on how many other pages are in the batch, and nothing
accumulates across a run — total cost scales linearly with page count and
is straightforward to estimate: `(input tokens × input price) + (output
tokens × output price)`, summed per model tier actually used, then across
the batch. `pipeline.py` prints this automatically at the end of every run
that made LLM calls (see [Reading a run's output](#reading-a-runs-output)).

As a concrete, measured example using Anthropic's list pricing: a typical
program page's cleaned text plus the extraction schema and prompt runs
roughly 4,000–4,500 input tokens, and a typical structured extraction
response is roughly 250 output tokens. At Claude Haiku pricing ($1/$5 per
million input/output tokens) that's well under a cent per page when the
cheapest tier resolves it; escalating to a stronger tier costs proportionally
more per that tier's list price, but only fires on the pages the validator
actually rejects. The exact numbers depend entirely on which provider and
models you configure — check that vendor's current pricing.

#### Estimating discovery cost

`--llm-discovery` is a single, small classification call per listing page —
much cheaper than extraction, by design. It never sends the raw page to the
model: `extract_candidate_links` first does a free regex pass that pulls
out every same-domain, page-like URL on the page (capped at 300
candidates), and only that short list of paths — not the page content — is
what gets sent to the LLM to classify. A page with zero link-shaped
candidates makes no LLM call at all.

At roughly 100–300 short candidate paths per listing page, that's typically
under 5,000 input tokens and a few hundred output tokens (the ~20 selected
program links) — at Claude Haiku pricing, **a fraction of a cent per
listing page**, and each listing page typically discovers ~20 program URLs,
so the marginal cost per discovered program is well under what extracting
that program's page costs. `discover.py` prints its own per-model cost
report at the end of any run that made an LLM call, the same way
`pipeline.py` does for extraction.

### Running with no LLM configured

The pipeline never hard-requires an LLM. With no API key set for the
configured provider (or with every configured tier failing for any other
reason — network error, invalid key, rate limit), extraction falls through
to the heuristic path automatically: JSON-LD (`schema.org` Course /
EducationalOccupationalProgram markup), Open Graph tags, and label-based
regex matching. Lower recall (see [Limitations](#limitations)), but zero
setup and it never blocks a batch.

### Quick start

```bash
./.venv/bin/python pipeline.py --url "https://example.com/programs/some-masters-degree"
```

This fetches the page, extracts the fields, cleans and validates them, and
appends one row to `output/programs.csv`.

### Use cases

**Process a single URL:**

```bash
./.venv/bin/python pipeline.py --url "https://example.com/programs/some-masters-degree"
```

**Process a batch from a file** (one URL per line, `#`-prefixed lines
ignored):

```bash
./.venv/bin/python pipeline.py --url-file urls.txt
```

**Custom output location and raw-HTML cache directory:**

```bash
./.venv/bin/python pipeline.py --url-file urls.txt --output output/my_batch.csv --raw-dir raw/my_batch
```

**Tune request pacing** — `--delay` (default 1.5s + up to 1s random
jitter) between URLs, `--block-cooldown` (default 30s) as an extra sleep
specifically after a hard block is detected:

```bash
./.venv/bin/python pipeline.py --url-file urls.txt --delay 2.0 --block-cooldown 60
```

**Reprocess URLs already in the output CSV** (resume is on by default —
this opts out of it for one run):

```bash
./.venv/bin/python pipeline.py --url-file urls.txt --no-resume
```

**Re-check already-scraped URLs for source-page changes** instead of
skipping them outright:

```bash
./.venv/bin/python pipeline.py --url-file urls.txt --refresh
```

Each already-done URL is re-fetched and its content hash compared against
`state/extraction_state.json`. Unchanged → reported `UNCHANGED`, no LLM
call, no CSV write. Changed → re-extracted and the existing row **replaced
in place** (not appended as a duplicate) → reported `UPDATED`. Point
`--extraction-state` elsewhere to use a different state file (default:
`state/extraction_state.json`).

**Discover program URLs from a search/listing page** (currently supports
mastersportal.com — see [Adding a new discovery
site](#adding-a-new-discovery-site) to extend it):

```bash
./.venv/bin/python discover.py --url "https://www.mastersportal.com/search/master/2-years/netherlands" --pages 5 --output urls.txt
./.venv/bin/python pipeline.py --url-file urls.txt
```

`--pages N` walks `page=1..N` of the same search and de-duplicates across
pages. Every link found is also merged into `state/discovered_urls.json` (a
persistent manifest, not overwritten between runs — `--state` to point it
elsewhere); `urls.txt` only ever contains links that are *new* as of the
most recent run, so running `discover.py` again against the same or an
overlapping search correctly reports 0 new links for anything already
known. See `state/README.md` for the full design.

**Discover on a site with no registered pattern**, using `--llm-discovery`
instead of extending `SITE_PATTERNS`:

```bash
./.venv/bin/python discover.py --url "https://example.com/programs?country=netherlands" --llm-discovery --output urls.txt
```

Works on any site, no code changes — see [Estimating discovery
cost](#estimating-discovery-cost) for what this actually costs, and
[Limitations](#limitations) for the pagination caveat (`--pages > 1` on an
unregistered domain collapses to page 1 only, since there's no known
query-string convention to walk without guessing one). Override the model
with `--llm-discovery-model` or the `DISCOVERY_MODEL` environment variable.

**Run the test suite** (pure logic only, no network, no live LLM calls):

```bash
./.venv/bin/python -m pytest
```

Run this after any change to a regex, validator, normalizer, or provider
adapter — it's what catches a regression before it ships in a real batch.

**Run the smoke test** against known-good real URLs (hits the network,
uses whichever LLM provider is currently configured):

```bash
./.venv/bin/python canary.py --verbose
```

There's no scheduler wired up for this — run it manually, or wire it into
your own cron job or CI pipeline, periodically to catch a supported site
quietly changing its layout before a real batch comes back empty.

### Reading a run's output

Each line printed during a run is one of:

| Status | Meaning |
|---|---|
| `OK` | New row written |
| `DUPLICATE` | Extracted successfully but an equivalent row already existed |
| `UPDATED` | (`--refresh` only) Existing row replaced with changed data |
| `UNCHANGED` | (`--refresh` only) No content change detected, nothing re-extracted |
| `RESUMED` | URL already in the output CSV, skipped entirely |
| `SKIPPED` | Extraction ran but a required field came back empty |
| `BLOCKED` | A hard bot-protection block was detected |
| `FAILED` / `ERROR` | Collection or an unexpected error stopped this URL |

Followed by a summary count, and — if any LLM calls were made — a per-model
token/cost report, priced at each configured model's standard list rate
(models with no known price are reported at $0.00 rather than a guessed
number).

### Output format

`output/programs.csv` (or wherever `--output` points) has one row per
program with the columns defined in `schema.FIELDNAMES` — identity fields
(university, level, program name), location, cost, dates, and repeatable
sections (intake terms, deadlines, prerequisites, requirements, tags)
flattened into semicolon-separated cells. `schema.REQUIRED_FIELDS`
(`university_name`, `level`, `program_name`) must be non-empty for a row to
be written at all; anything else missing is left blank.

Raw HTML snapshots are cached in `raw/` (one `.html` + `.meta.json` per
URL, keyed by a hash of the URL), so extraction can be re-run later without
re-fetching the page.

### Adding a new discovery site

Two options, depending on whether you want a free/deterministic pattern or
zero setup:

- **Register a `SitePattern`** (free, deterministic, requires inspecting
  the site's HTML once). `discover.py`'s `SITE_PATTERNS` registry maps a
  domain to a small `SitePattern` entry: a regex for extracting program
  links out of a fetched listing page, and the pagination query-parameter
  name for that site. Add one more entry with that site's own link pattern
  — no other code needs to change.
- **Use `--llm-discovery`** (small LLM cost, zero setup — see [Discover on
  a site with no registered pattern](#use-cases) and [Estimating discovery
  cost](#estimating-discovery-cost)). No `SitePattern` needed at all;
  multi-page pagination is the one thing it can't do without a registered
  pattern's `page_param`.

Pointing plain `discover.py` (no `--llm-discovery`) at a domain with no
registered pattern raises a clear error rather than silently returning
nothing.

### Troubleshooting

- **Every row comes back `SKIPPED`.** You likely pointed `--url`/
  `--url-file` at a search/listing page instead of individual program
  pages — a listing page has no single program's data to extract. Run
  `discover.py` on it first to get individual program URLs.
- **A batch comes back mostly `FAILED`/`BLOCKED`.** The target site may
  have escalated to a harder block than the Playwright fallback can clear,
  or its layout may not match this pipeline's assumptions. Try increasing
  `--delay` and `--block-cooldown` first; if that doesn't help, the site is
  likely outside what this pipeline currently supports (see
  [Limitations](#limitations)).
- **Extraction always uses the heuristic path even with a provider
  configured.** Check that the correct API key environment variable is set
  for your `LLM_PROVIDER`, that the SDK for that provider is installed, and
  check stderr output during the run — every LLM-tier failure is logged
  there with the reason.
- **`RuntimeError: ... has no built-in default model cascade`.** You set
  `LLM_PROVIDER` to something other than `anthropic` without also setting
  `EXTRACTION_MODEL_CASCADE`. Set it to a comma-separated list of that
  provider's model IDs.
- **`RuntimeError: ... has no built-in default discovery model`.** Same
  cause as above, for `--llm-discovery`: set `DISCOVERY_MODEL` to a single
  model ID for your configured provider.
- **`--llm-discovery` finds 0 links on a page you can see has listings.**
  Check stderr for how many *candidates* were found before classification —
  zero candidates means `extract_candidate_links`'s regex pass found
  nothing URL-shaped on the page at all (possible on a heavily
  client-rendered page that Playwright didn't fully render); a nonzero
  candidate count with zero selected means the LLM classified all of them
  as non-program links, worth spot-checking manually.

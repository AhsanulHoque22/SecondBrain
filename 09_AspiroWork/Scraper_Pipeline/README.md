# Scraper Pipeline

## Introduction

Before this pipeline existed, scraping study-abroad program data was a
manual process: fetch search-result pages by hand, extract program links,
then read each page — manually or with AI assistance — and fill in a CSV
row, then run a second verification pass to catch mistakes. It worked, but
it didn't scale past a couple of countries and had no reusable code behind
it.

This pipeline replaces that manual process with small, single-purpose
Python scripts — discover, collect, extract, clean — chained by one CLI
orchestrator. Point it at a list of program-page URLs and it produces the
same 17-column CSV the manual process did, without a human reading every
page.

## What this pipeline does

Given one or more URLs to individual program pages, it:

1. Fetches and caches the raw HTML for each URL (clearing Cloudflare/WAF
   bot-protection automatically where needed).
2. Extracts the Appendix A program fields (university, level, program name,
   tuition, deadlines, requirements, tags, etc.) using an LLM cascade that
   generalizes across arbitrary site layouts — no per-site selectors to
   maintain — with a zero-setup heuristic fallback if no LLM is reachable.
3. Normalizes, validates, and de-duplicates each record, then appends it to
   a flat output CSV in the same schema already used across
   `Data Collection/`.

It can also turn a search/listing page into that URL list for you first
(mastersportal.com only, for now) — see Discover below.

## What it's used for

Feeding `09_AspiroWork/Data Collection/` — the source data for AspiroBrain's
study-abroad advisory database. Previously that data was scraped one country
at a time, entirely by hand. This pipeline is the automated replacement:
it's designed to work on sites like mastersportal.com *and* on individual
university sites directly (e.g. ox.ac.uk course pages) — anywhere a
program's details live on one page.

## Architecture

```
   ┌───────────────────────────────────────────┐
   │  0. DISCOVER (optional, mastersportal.com)  │
   │  discover.py                                │
   │                                              │
   │  listing/search URL  →  collector.fetch_html │
   │  → site-specific link regex (SITE_PATTERNS)  │
   │  → walk page=1..N  →  dedupe  →  urls.txt    │
   └─────────────────────┬───────────────────────┘
                         │  urls.txt
                         ▼
                    ┌─────────────────────────────────────────────┐
                    │              pipeline.py (CLI)               │
                    │  --url / --url-file  →  loop, delay+jitter   │
                    │  skip already-in-output (resume) per URL     │
                    └─────────────────────┬─────────────────────────┘
                                          │  for each new URL
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
   │       │           │   │  │ Opus 4.8   (on failure)   │   │   │  (atomic write)    │
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
| `schema.py` | — | Canonical 17-field list + which 3 are required |
| `discover.py` | Discover (optional) | Extract individual program links from a listing page (site-pattern registry), walk pagination, write a URL list |
| `collector.py` | Collect | Fetch raw HTML, clear Cloudflare/WAF via a headless-browser fallback, detect hard blocks, cache to disk |
| `extractor.py` | Extract | Haiku → Sonnet → Opus cascade with a free validator gate (required fields, numeric shape, source-grounding); heuristic fallback if no LLM is reachable |
| `cleaner.py` | Clean | Normalize, validate required fields, dedupe, atomically append to CSV |
| `pipeline.py` | — | CLI orchestrator: delay/jitter, hard-block cooldown, resume-skip, cost/token report |
| `canary.py` | — | Smoke test: known-good real URLs, run periodically to catch silent site-layout breakage |
| `tests/` | — | `pytest` suite for every pure-logic piece above (56 tests, no network) |
| `pytest.ini` | — | Points `pytest` at `tests/` |

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
./.venv/bin/python pipeline.py --url "https://www.mastersportal.com/studies/8798/legal-research.html"
./.venv/bin/python pipeline.py --url-file urls.txt
./.venv/bin/python pipeline.py --url-file urls.txt --output output/my_batch.csv --raw-dir raw/my_batch
./.venv/bin/python pipeline.py --url-file urls.txt --delay 2.0 --block-cooldown 60
./.venv/bin/python pipeline.py --url-file urls.txt --no-resume   # reprocess URLs already in the output CSV
```

Output: `output/programs.csv` by default. Raw HTML snapshots are cached in
`raw/` (one `.html` + `.meta.json` per URL, keyed by a hash of the URL), so
extraction can be re-run later without re-fetching. Each line printed during
a run is one of `OK` / `DUPLICATE` / `RESUMED` / `SKIPPED` / `BLOCKED` /
`FAILED`, followed by a summary count and — if any LLM calls were made — a
per-model token/cost report.

`--url` expects an individual program page. Pointing it at a search/listing
page instead (e.g. `mastersportal.com/search/master/...`) will "succeed"
with no crash but produce `SKIPPED` on every row — a listing page has no
single `university_name`/`level`/`program_name` for the pipeline to
extract. Use Discover below to turn a listing page into individual URLs
first.

**Resuming a batch.** By default, any URL already present in the output
CSV's `source_url` column is skipped entirely — no re-fetch, no
re-extraction, no LLM spend — reported as `RESUMED`. This makes it cheap to
rerun a batch that got interrupted partway (crash, hard block, closed
laptop). Pass `--no-resume` to force reprocessing every URL regardless.

**Politeness delay.** `--delay` (default 1.5s, plus up to 1s of random
jitter) is applied between URLs in a batch. `--block-cooldown` (default 30s)
is an *extra*, one-time sleep applied specifically after a hard Cloudflare
block is detected, before continuing to the next URL — see Failproofing
below for why this exists.

### Discover (optional — mastersportal.com only, for now)

If you have a search/listing page URL instead of individual program URLs,
generate a `urls.txt` first and feed it straight into the run above:

```bash
./.venv/bin/python discover.py --url "https://www.mastersportal.com/search/master/2-years/netherlands" --pages 5 --output urls.txt
./.venv/bin/python pipeline.py --url-file urls.txt
```

`--pages N` walks `page=1..N` of the same search (20 results per page on
mastersportal.com) and de-duplicates across pages. Site support is a small
registry (`SITE_PATTERNS` in `discover.py`) — only mastersportal.com is
registered today; pointing it at an unregistered domain raises a clear
error rather than silently finding nothing.

### Testing

```bash
./.venv/bin/python -m pytest              # 56 pure-logic tests, no network, ~2s
./.venv/bin/python canary.py --verbose    # smoke test against real known-good URLs, hits the network
```

Run `pytest` after any change to a regex, validator, or normalizer — it's
what catches a regression before it silently ships in a real batch. Run
`canary.py` periodically (there's no cron job wired up for it — see
Failproofing below) to catch a supported site changing its layout before a
real batch quietly comes back empty.

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
tags — a bare regex on the raw HTML found all of them. Landed as
`discover.py`, reusing `collector.py`'s existing fetch (no new dependency
needed).

**8. The `level` degree-prefix regex from #4 still missed most real
mastersportal.com titles.** It only matched an abbreviation (`MSc`, `MPhil`,
…) anchored at the very start of the program name — Oxford's convention
("MSc in X"). mastersportal.com titles read differently, e.g. "Joint Master
in Applied XR … at USTP" (unabbreviated "Master", not at the start) and
"Legal Research LL.M. at Utrecht University" (a dotted abbreviation, also
not at the start). Widened `level` backfill to three tiers, tried in order:
the original anchored abbreviation match; a dotted-abbreviation search
anywhere in the title (`LL.M`, `M.Sc`, …) — safe to search anywhere because
the literal period makes false positives very unlikely; then a plain-word
search anywhere (`Master`, `Bachelor`, `Doctorate`, …) — also safe as whole
words. Deliberately did *not* widen the original anchored tier's bare
2-letter forms (`MA`, `BA`) to search-anywhere, since those really do
collide with normal English/place-name text (verified: "University of
Massachusetts (MA)" does not falsely match `MA` under any tier).

**9. mastersportal.com escalated from a soft challenge to a hard block
mid-session.** While testing `discover.py` against the same site
repeatedly, a Playwright fetch that had previously succeeded came back with
an actual Cloudflare "Sorry, you have been blocked" page — a real,
different HTML document, served with a normal 200 status, that the
collector was silently treating as a successful fetch (it would have been
cached and handed to the extractor as if it were program content). This is
the concrete failure that motivated most of the Failproofing work below:
`collector.py` had no way to tell "fetched real content" apart from
"fetched a block page that happens to be valid HTML."

## Failproofing (this round)

After the fixes above, the question became "what else can go wrong" —
these ten items were brainstormed from the actual gaps already known at
that point, then implemented and verified in this same session.

1. **Detect a hard Cloudflare block distinctly from a soft 403.** `collector.py`
   now checks fetched HTML against known block-page markers ("Sorry, you
   have been blocked", "Attention Required! | Cloudflare", `cf-error-details`)
   and raises `HardBlockError` — a `CollectionError` subclass — instead of
   silently returning the block page as if it were content. Applied to
   *both* fetch paths (plain `requests` 200s and the Playwright fallback),
   since a block page isn't guaranteed to arrive with a 403. Verified: unit
   test reproduces the exact real block-page text seen mid-session and
   confirms it's caught; a second test confirms real page HTML never
   false-positives.
2. **Rate limiting + hard-block cooldown in `pipeline.py`.** There was
   previously zero delay between URLs in a batch — the leading suspect for
   why #9 above happened. Added `--delay` (default 1.5s + up to 1s jitter)
   between every URL, and a separate, much longer `--block-cooldown`
   (default 30s) that fires once when a `HardBlockError` is caught, before
   continuing to the next URL — retrying immediately into an active block
   just deepens it. Verified live (delay measurably slows a 2-URL batch)
   and with a mocked `HardBlockError` (cooldown sleep fires, batch
   continues afterward, `BLOCKED` is reported distinctly in the summary).
3. **Resume / skip-already-done.** Before processing a URL, `pipeline.py`
   now checks whether it's already in the output CSV's `source_url` column
   and skips it immediately if so (`RESUMED`, no network/LLM call at all).
   `--no-resume` forces reprocessing. Verified live: an identical 2-URL
   batch took ~22s fresh and ~1.8s on rerun, both URLs correctly skipped;
   `--no-resume` on the same batch correctly re-fetched both and fell
   through to `cleaner.py`'s own content-based dedup (`DUPLICATE`).
4. **Source-text grounding check in the validator.** `validate_extraction()`
   previously only checked *shape* (non-empty, contains a digit) — a
   plausible-but-wrong number would sail through untouched. Now, for any
   numeric field with a 3+ digit value, it strips all extracted values and
   the page's clean text down to digits-only and checks the value's digits
   actually appear somewhere on the page; a value with no match is flagged
   as "not grounded in the page — possible hallucination" and triggers
   escalation, same as any other validation failure. Digit-only comparison
   sidesteps formatting noise ("£15,000" vs "15000"); the 3-digit floor
   avoids flagging every short number (a duration of "7 years") as a
   coincidental non-match. Verified with unit tests: a grounded value
   passes, an identical-shape ungrounded value is flagged, a short digit
   run is correctly *not* flagged either way.
5. **Live cascade test — still blocked.** Actually running the
   Haiku→Sonnet→Opus cascade against the real API on a real batch needs
   `ANTHROPIC_API_KEY`, which is not available in this environment (checked
   again at the start of this round — still unset, no `ant` CLI either).
   Real accuracy, real escalation rate, and real $ per program remain
   unmeasured. Item 6 below (cost tracking) is ready to report on this the
   moment credentials are available.
6. **Per-call cost/token tracking + end-of-batch report.** `extract_via_llm`
   now returns the API response's real `usage` (input/output tokens)
   alongside the extracted fields; `extract()` attaches it as `data["_usage"]`
   (model + token counts, or `None` on the heuristic path — no API call, no
   cost). `pipeline.py` accumulates this across a batch and prints a
   per-model breakdown plus a total, priced at standard list rates (not the
   temporary Sonnet 5 introductory discount — a cost *estimate* that
   silently goes wrong the day a discount expires is worse than one that's
   always a few cents pessimistic). Verified with unit tests covering the
   summing/formatting logic; can't be verified against real dollars without
   #5 above.
7. **A `pytest` suite for every pure-logic piece.** Every fix in this
   session up to this point was verified with a one-off script written,
   run, and thrown away — real confirmation in the moment, but nothing
   stopping a future change from quietly breaking the same thing again.
   Added `tests/` (56 tests) covering: the `level` three-tier regex
   (including both real titles that exposed gaps #4/#8 and both
   adversarial cases), the `application_fee` false-positive regression
   from #5, the validator's required/numeric/grounding checks from #4
   above, the full escalation cascade (mocked — tests never touch the live
   API), `discover.py`'s link extraction + pagination + site registry,
   `cleaner.py`'s normalizers + atomic-write behavior (#9 below), and
   `collector.py`'s hash + hard-block detection. Small refactor alongside
   this: the inline three-tier level-detection logic in
   `extract_via_heuristics` was pulled out into its own `backfill_level()`
   function so it could be tested directly instead of only indirectly
   through a full HTML fixture. `pytest` added to `requirements.txt`.
   Verified: `pytest` — 56 passed in ~2s.
8. **A canary/smoke-test script.** `canary.py` hits one known-good real URL
   per supported site (mastersportal.com, ox.ac.uk) through the actual
   `collect()` → `extract()` path, using a throwaway temp directory so it
   never touches the real `raw/` cache or output CSV, and exits non-zero if
   either one stops producing the required fields — meant to catch a site
   silently changing its layout before a real batch quietly comes back
   empty. Not wired into cron or any scheduler (that would be a separate,
   explicit ask). Verified live: both real canary URLs pass today; a mocked
   failure correctly exits 1 with a clear stderr message, and an empty
   canary list correctly exits 0.
9. **Atomic CSV writes.** `cleaner.append_to_csv` previously opened the
   output file in append mode and wrote directly — a crash or kill
   mid-write could leave a truncated or partially-written row. Rewritten to
   write the full file (existing rows + the new row) to a temp file in the
   same directory, then swap it in with `os.replace()`, which is atomic on
   both POSIX and Windows. Trade-off: this is an O(rows) rewrite per append
   rather than true O(1) append — the right call at this pipeline's scale
   (hundreds to low thousands of rows), not for a much larger file.
   Verified with a unit test that injects a `RuntimeError` mid-write via a
   monkeypatched `csv.DictWriter` and confirms the original file is
   byte-for-byte unchanged afterward, with no leftover temp file.
10. **`discover.py` refactored for multi-site extensibility.** The
    mastersportal-only regex and `page=` pagination param were hardcoded
    inline. Replaced with a `SITE_PATTERNS` registry keyed by domain (each
    entry: link regex + pagination param name), so adding a second site
    later is meant to be a small addition, not a rewrite — though no second
    site's actual pattern has been discovered/tested yet, so only
    mastersportal.com is registered. Pointing `discover.py` at an
    unregistered domain now raises a clear, actionable error instead of
    silently returning zero links. Verified live (same 20-links-per-page
    result as before the refactor) and with unit tests, including the new
    error path.

## Cost estimation: old manual/agent system vs. this pipeline

The old manual process (Netherlands/Malta CSVs — see `../Data Collection/`)
ran into a hard **session/context limit**: a single agent session trying to
work through 100 programs in one go accumulated too much context (fetched
page content + reasoning + CSV-row output, for every program processed so
far, all staying in the same conversation) and became unworkable well before
finishing — which is why that process had to be split into 5 parallel
agents of 20 programs each, run in two full passes (an initial scrape, then
a full re-verification pass that re-fetched every page live).

**The structural fix, not just the cost fix:** this pipeline's `extract()`
call is stateless per page — each program is one isolated API call with
just that page's text (capped at 15,000 characters) and zero memory of the
other 99. Batch size and context limits are completely decoupled: 100
programs and 10,000 programs cost the same *per program*, and neither can
hit a session ceiling, because there's nothing accumulating across the
batch to begin with.

### Dollar cost, grounded in real numbers

Measured against the actual code and actual pricing, not estimated in the
abstract: both real pages fetched during this session (mastersportal.com,
ox.ac.uk) exceeded the 15,000-char input cap, so that's the realistic
per-call input size, not a hopeful average. System prompt + tool schema +
URL wrapper + the capped page text ≈ 17,450 characters ≈ **~4,364 input
tokens** per call (~4 chars/token); a typical structured extraction (17
fields, a handful of list items) runs **~250 output tokens**.

| Tier | Cost per program | Cost per 100 programs |
|---|---|---|
| Haiku 4.5 (typical, no escalation) | $0.0056 | **$0.56** |
| Sonnet 5 (if escalated) | $0.0168 | $1.68 |
| Opus 4.8 (if double-escalated) | $0.0281 | $2.81 |

**Realistic range for a 100-program batch**, depending on how often the
free validator (Failproofing #4) rejects the cheap tier's output:

- **Best case** (everything resolves on Haiku): **~$0.56**
- **Moderate case** (~20% need one escalation to Sonnet): **~$0.90**
- **Absolute worst case** (every page fails twice, needs Opus): **~$5.00**
  — a pessimistic ceiling, not an expectation

For the old system there's no log to measure against (it ran in a prior
session), so this is a reasoned estimate rather than a measured one, unlike
the table above: those were general-purpose agent calls doing WebFetch +
reasoning + CSV-writing per program, at Opus-tier pricing (the environment's
default model), across **two full passes** — so whatever the per-program
cost actually was, it was paid roughly twice, at the most expensive tier,
with no cheap-first cascade at all. Order-of-magnitude, that plausibly lands
in the **$3–$8+ range for 100 programs**.

**Bottom line:** even this pipeline's worst-case ceiling (~$5) sits in the
same ballpark as a *conservative* estimate of the old system's typical cost,
and the realistic case (~$0.56–$0.90) is roughly 5–10x cheaper — on top of
removing the session-limit problem entirely rather than just making it
cheaper to hit.

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
  cleared the Cloudflare 403 wall and collected successfully.
- **`level` regex widening, live:** re-ran the same 3-URL mastersportal
  sample after fix #8. Before: **2/3 written**, one `SKIPPED` on `level`
  (the `LL.M.` title). After: **3/3 written** — the "Joint Master…" page
  picked up `M.Sc` (found later in its own title, more precise than the
  generic "Master" match), the other "Joint Master…" page got `Master`, and
  the `LL.M.` page got `LL.M`. Also re-ran the isolated regex cases,
  including both adversarial ones from the design (`"University of
  Massachusetts (MA)"` and a title with no degree word at all,
  `"Legal Research"`) — both still correctly return no match.
- **Failproofing round, live + unit:** every item in that section above was
  individually verified as described there. Full regression after all ten
  items landed: `pytest` — **56 passed**, `canary.py --verbose` — **both
  real URLs PASS**, all seven `.py` files parse cleanly.

## Drawbacks / known limitations

- **The Haiku/Sonnet/Opus cascade has never been run against the live API.**
  Everything about it is verified via mocked responses, not a real batch —
  actual accuracy, actual escalation rate, and actual cost per page are
  unmeasured until it's run with a real `ANTHROPIC_API_KEY`. Cost tracking
  (Failproofing #6) is ready to report on this the moment it happens.
- **The zero-setup heuristic path still has real gaps**, even after fixes
  #4 and #8: it can't reliably pull `tuition_1st_year`, `duration`,
  `success_rate`, or `program_image_url` on sites that don't expose them in
  a plain "Label: value" line (confirmed empty on all 13 rows of the Oxford
  test batch), and `level` backfill only covers the degree-naming patterns
  actually seen in testing (Oxford- and mastersportal-style) — a site with a
  genuinely different convention could still come back empty. This is the
  expected trade-off of the zero-setup path, not a bug, but it means
  heuristic-only runs produce thinner data than the LLM cascade would.
- **No coverage for a WAF that also fingerprints headless Chromium.** The
  Playwright fallback has only been proven against sites that block plain
  `requests` but don't detect a real browser. A site that blocks *both*
  would still show up as `FAILED` — untested, unknown how common this is.
- **URL discovery only covers mastersportal.com.** The `SITE_PATTERNS`
  registry (Failproofing #10) makes adding a second site a smaller change
  than before, but no second site's actual link pattern has been
  discovered or tested — Oxford's own course-listing page, for example,
  renders results via a JS widget that isn't captured the same way (a plain
  Playwright fetch of it comes back empty even with a network-idle wait).
- **Rate limiting is a flat delay, not adaptive.** `--delay`/`--block-cooldown`
  (Failproofing #2) are fixed values you set upfront, not a backoff that
  tunes itself to how a site is actually responding. A batch large enough
  or fast enough could still trigger a hard block; the pipeline now detects
  and reports that when it happens (Failproofing #1) rather than silently
  caching a block page, but it doesn't prevent it outright.
- **The source-grounding validator check (Failproofing #4) can't tell a
  legitimately-derived number from a hallucinated one.** It only checks
  whether a value's digits appear *somewhere* on the page — a genuinely
  correct value the model computed or reformatted from other numbers on the
  page (rather than copied verbatim) could be flagged as "not grounded"
  even though it's right, triggering an unnecessary (but harmless, since
  it's still validated with the *shape* check either way) escalation.
- **Resume (Failproofing #3) keys on the exact source URL only** — coarser
  than `cleaner.py`'s own dedup, which matches on university + program name
  + URL. Two different URLs that happen to describe the same program won't
  be caught by resume (though they'd still be caught as a `DUPLICATE` by
  `cleaner.py` if actually reprocessed).
- **Atomic CSV writes (Failproofing #9) rewrite the whole file per append**
  — safe and fine at this pipeline's real scale, but would need revisiting
  (e.g. a real database) well before reaching tens of thousands of rows.
- **Escalation adds latency, worst case 3x.** A page that fails validation
  twice makes three sequential API calls before falling back to heuristic;
  this should be rare in practice but hasn't been measured on a real batch.
- **`canary.py` isn't wired into any scheduler.** It exists and works, but
  someone (or some cron job) has to actually run it for it to catch
  anything — it's a tool, not yet a monitor.
- **Flat CSV output only.** No structured/database storage, no Bronze-style
  immutable snapshotting — both were flagged as future work in
  `../AspiroBrain_Data_Pipeline_Plan.md` but aren't part of this pipeline.

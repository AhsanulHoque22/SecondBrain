# State

Two mechanisms live here. **Both are now implemented.**

## `discovered_urls.json` — implemented

Fixes a real bug: `discover.py` used to write `urls.txt` with
`Path.write_text(...)` — a full overwrite. Running it again against the
same (or an overlapping) search replaced the file entirely, with no memory
of links found in a previous run.

Now `discover.py` loads this manifest at the start of every run, merges
newly-found links into it (dedup key: **exact URL match** — mastersportal's
program links, `/studies/<id>/<slug>.html` resolved to absolute, carry no
tracking params or fragments, so there's nothing to normalize), and writes
it back atomically (temp file + `os.replace`, same pattern as
`cleaner.append_to_csv`'s crash-safety fix). A URL already in the manifest
gets `last_discovered_at` bumped, not duplicated — useful later as a signal
for whether a listing still shows a program or it's been pulled.

**Deliberately no `status` field.** `pipeline.py` already has a resume
mechanism (Failproofing #3) that skips any URL already in the output CSV —
that's the real, single source of truth for "has this been processed."
Tracking a second "processed" flag here would just be a second fact that
could drift out of sync with the CSV; better to have one place that
answers that question.

Given that, the role split is:
- **`discovered_urls.json`** = the full history of every URL ever found,
  never pruned.
- **`urls.txt`** (`discover.py`'s `--output`, unchanged path/flag) = only
  the URLs that were *new* as of the most recent run — the small,
  immediately-actionable batch to hand to `pipeline.py --url-file`.
  Running `discover.py` twice against overlapping searches now correctly
  produces a second `urls.txt` containing only what's actually new,
  instead of the same 20 links all over again.

```jsonc
{
  "https://www.mastersportal.com/studies/8798/legal-research.html": {
    "first_discovered_at": "2026-07-13T10:00:00Z",
    "last_discovered_at": "2026-07-20T09:15:00Z",
    "discovered_via": "https://www.mastersportal.com/search/master/2-years/netherlands"
  }
}
```

## `extraction_state.json` — implemented

Keyed by program URL. Written by `extractor.record_extraction_state()`
after every successful extraction (new URL or a refreshed one), holding a
hash of `extractor.clean_text_from_html()`'s output (not the raw HTML —
see "Hash target" below, this decision is now made and confirmed live, not
just reasoned about). `pipeline.py --refresh` re-fetches an already-done
URL, hashes the new content via `extractor.has_content_changed()`, and
compares: unchanged → reported `UNCHANGED`, no LLM call, no CSV write;
changed → re-extracted and the existing row replaced in place via
`cleaner.upsert_to_csv()` (not appended as a duplicate — `append_to_csv`'s
dedup key would otherwise just see the same university+program+URL and
silently refuse to write the updated data).

```jsonc
{
  "https://www.mastersportal.com/studies/8798/legal-research.html": {
    "last_extracted_at": "2026-07-13T10:05:00Z",
    "content_hash": "sha256:9f2b1e...",
    "extraction_method": "llm-haiku"
  }
}
```

**Merge key:** exact URL match — same as `discovered_urls.json`.

**Hash target — decided, and the tradeoff is now confirmed live, not just
theoretical.** Hashing raw HTML was rejected (too noisy — ads, trackers,
per-request markup variance). Hashing `clean_text_from_html()`'s output was
chosen as the middle ground. Verified live: re-extracting the same real
mastersportal.com page after a tuition change correctly triggered `UPDATED`
with the new value upserted in place (the feature's actual purpose,
working). But also, in the same round of live testing, two real fetches of
the identical page — genuinely unchanged, confirmed by three separate
controlled follow-up fetches (including one with a deliberate 90-second
gap) all matching — one time landed on *different* hashes. The most likely
cause: `collector.fetch_html_playwright`'s `networkidle` wait doesn't
always settle by the same point (it's wrapped in a try/except that just
moves on — see collector.py), so two fetches of the same page can capture
slightly different DOM-render-completeness snapshots, independent of
whether the underlying data changed at all. Net effect: `--refresh` can
occasionally report a false `UPDATED` (wasted LLM cost on a page that
didn't really change) but should never *miss* a real change — the failure
mode leans toward "extra work," not "silently stale data," which is the
safer side to be wrong on. Not reproduced reliably enough to fix with
confidence right now; flagged in the main README's Drawbacks instead of
guessed at.

**Field-level change detection** (compare the actual extracted values
before/after, not page content) would sidestep this entirely, but needs
running extraction on every "pending recheck" URL regardless of whether
anything changed — which defeats the purpose of a cheap pre-check hash. Not
pursued for that reason.

**Git tracking:** tracked, not gitignored — same reasoning as
`discovered_urls.json` below: small, and the accumulated history is the
whole point.

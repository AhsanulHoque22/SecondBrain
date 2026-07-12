# State

Two mechanisms live here. **Discovery dedup is implemented.**
**Change-detection is still just a scaffold.**

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

## `extraction_state.json` — scaffold only, not yet implemented

Keyed by program URL. Written after a successful extraction, holding a
content hash of the fetched page (raw HTML or `clean_text` — the exact
choice is an implementation decision for later, not made here) so a future
run can re-fetch a previously-processed URL, hash the new content, and
compare: unchanged → stays resumed/skipped as today; changed → treated as
needing re-extraction instead of being silently skipped.

```jsonc
{
  "https://www.mastersportal.com/studies/8798/legal-research.html": {
    "last_extracted_at": "2026-07-13T10:05:00Z",
    "content_hash": "sha256:9f2b1e...",
    "extraction_method": "llm-haiku"
  }
}
```

## Open decisions for whoever builds `extraction_state.json` next

(The equivalent decision for `discovered_urls.json` — merge key — is
resolved: exact URL match, see above.)

- **Hash target:** hashing the full raw HTML will flag on *any* page change,
  including irrelevant ones (ads, a changed timestamp in the footer,
  a/b-tested markup) — hashing `extractor.clean_text_from_html()`'s output
  instead is noisier-content-resistant but still not field-level (a change
  to `program_name` and a change to unrelated body copy both trip it).
  Field-level change detection (compare the actual extracted values, not
  page content) would need running extraction on every "pending recheck"
  URL regardless, which defeats the purpose of a cheap pre-check hash.

**Git tracking, decided for `discovered_urls.json`:** tracked, not
gitignored — unlike `raw/` (bulky, trivially regenerable) or `output/`
(copied elsewhere; see main README), this manifest is small and its whole
value *is* the accumulated history — gitignoring it would defeat the
purpose the moment this runs from a second machine or a fresh clone.
`extraction_state.json` doesn't do anything yet, so its own git-tracking
call is still open until it's actually implemented (it'll likely follow
the same reasoning, but isn't decided here).

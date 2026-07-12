# State — scaffold only, not yet implemented

This directory is the planned home for two mechanisms `discover.py` and
`pipeline.py` don't have yet:

1. **Duplicate-safe, cross-run discovery storage.** Right now `discover.py`
   writes `urls.txt` with `Path.write_text(...)` — a full overwrite. Running
   it again against the same (or an overlapping) search replaces the file
   entirely; there's no memory of links found in a previous run.
2. **Change-detection for already-extracted programs.** `pipeline.py`'s
   resume feature skips any URL already present in the output CSV,
   unconditionally. If a program's tuition, deadline, or requirements
   change on the source page after it's been scraped once, nothing here
   will ever notice or re-extract it — resume and "did this change" are
   different questions, and only the first one is currently answered.

Neither file below is read or written by any code yet. This is file/schema
scaffolding only, so the logic has an obvious place to live when it's
built — see the main README's Drawbacks section for the current gap this
fills.

## `discovered_urls.json`

Keyed by program URL. `discover.py` would **merge** into this file instead
of overwriting `urls.txt` from scratch — a URL already present gets
`last_discovered_at` bumped, not duplicated; a new one gets an entry with
`status: "pending"`. `pipeline.py --url-file` would eventually be able to
read straight from this manifest (filtered to `status == "pending"`)
instead of a flat text file.

```jsonc
{
  "https://www.mastersportal.com/studies/8798/legal-research.html": {
    "first_discovered_at": "2026-07-13T10:00:00Z",
    "last_discovered_at": "2026-07-20T09:15:00Z",
    "discovered_via": "https://www.mastersportal.com/search/master/2-years/netherlands",
    "status": "pending"   // "pending" | "processed" | "failed"
  }
}
```

## `extraction_state.json`

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

## Open decisions for whoever builds this next

- **Merge key:** exact URL match (simplest, matches how resume already
  works) vs. something looser (e.g. normalizing tracking params) — exact
  match is the safer default.
- **Hash target:** hashing the full raw HTML will flag on *any* page change,
  including irrelevant ones (ads, a changed timestamp in the footer,
  a/b-tested markup) — hashing `extractor.clean_text_from_html()`'s output
  instead is noisier-content-resistant but still not field-level (a change
  to `program_name` and a change to unrelated body copy both trip it).
  Field-level change detection (compare the actual extracted values, not
  page content) would need running extraction on every "pending recheck"
  URL regardless, which defeats the purpose of a cheap pre-check hash.
- **Git tracking:** `raw/`, `output/`, and `urls.txt` are all gitignored
  today (this is currently a local, single-machine tool). Whether
  `state/*.json` should be gitignored too, or actually committed so the
  discovery/change history survives a fresh clone, is worth deciding
  explicitly once this pipeline has a real shared home — not decided here.

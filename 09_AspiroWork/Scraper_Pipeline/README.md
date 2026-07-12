# Scraper Pipeline

Three stages, three files, one CSV — collect, extract, clean. Schema matches
Appendix A (Program Entry Schema) plus `tuition_currency` and
`last_verified_date`.

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/playwright install chromium
```

For LLM-based extraction (recommended — generalizes across arbitrary site
layouts), set `ANTHROPIC_API_KEY` or run `ant auth login`. Without either,
the pipeline automatically falls back to heuristic extraction (JSON-LD +
label matching) — lower recall, but works with zero setup.

Extraction is a cost/accuracy cascade, cheapest model first: Haiku 4.5 tries
each page, a deterministic (free, no LLM call) validator checks the output,
and only pages that fail validation escalate to Sonnet 5 then Opus 4.8 — the
escalation prompt includes exactly what the validator rejected, so it's a
correction, not a blind re-roll. Most pages should resolve on Haiku alone;
`_extraction_method` in the output records which tier actually served each
row (`llm-haiku` / `llm-sonnet` / `llm-opus` / `heuristic`).

The `playwright install chromium` step downloads a headless browser used
only as a fallback (see Known limitation below). Skipping it is fine — the
collector still works for any site that doesn't block plain `requests`;
it just can't clear a Cloudflare/WAF wall without it.

## Run

```bash
./.venv/bin/python pipeline.py --url "https://example.com/msc-program-page"
./.venv/bin/python pipeline.py --url-file urls.txt
```

Output: `output/programs.csv`. Raw HTML snapshots cached in `raw/` (one
`.html` + `.meta.json` per URL, keyed by URL hash) so extraction can be
re-run without re-fetching.

## Known limitation

Sites behind Cloudflare/WAF bot-protection (mastersportal.com, ox.ac.uk
confirmed) return 403 to this collector's plain `requests` calls — same wall
hit during the original manual scraping work. On a 403, the collector now
automatically retries once with a headless browser (Playwright), which
executes the page's JS and clears most "checking your browser" challenges.
If Playwright isn't installed (see Setup) or the fallback is also blocked,
the pipeline reports the URL as `FAILED` per-URL and keeps going rather
than crashing the batch.

## Files

| File | Stage |
|---|---|
| `schema.py` | Canonical field list + required fields |
| `collector.py` | Collect — fetch + cache raw HTML |
| `extractor.py` | Extract — Haiku→Sonnet→Opus cascade (strict tool schema, validated) with heuristic fallback |
| `cleaner.py` | Clean — normalize, validate, dedupe, append to CSV |
| `pipeline.py` | CLI orchestrator |

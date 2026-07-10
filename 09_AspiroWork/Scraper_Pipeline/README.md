# Scraper Pipeline

Three stages, three files, one CSV — collect, extract, clean. Schema matches
Appendix A (Program Entry Schema) plus `tuition_currency` and
`last_verified_date`.

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

For LLM-based extraction (recommended — generalizes across arbitrary site
layouts), set `ANTHROPIC_API_KEY` or run `ant auth login`. Without either,
the pipeline automatically falls back to heuristic extraction (JSON-LD +
label matching) — lower recall, but works with zero setup.

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
hit during the original manual scraping work. A headless-browser fallback
(Playwright) would clear it but is intentionally out of scope here to keep
the collector to one job: fetch and cache. The pipeline reports these as
`FAILED` per-URL and keeps going rather than crashing the batch.

## Files

| File | Stage |
|---|---|
| `schema.py` | Canonical field list + required fields |
| `collector.py` | Collect — fetch + cache raw HTML |
| `extractor.py` | Extract — LLM (Claude, strict tool schema) with heuristic fallback |
| `cleaner.py` | Clean — normalize, validate, dedupe, append to CSV |
| `pipeline.py` | CLI orchestrator |

## BLOCK STUDY GUIDE PROTOCOL

Triggered by: "starting block [N]" / "I'm starting block [N]" / "ready for block [N]"

### Step 1 — Identify topics
- Read `scripts/data/wiki_state.md` → active course, phase, carry-forward
- Read `01_Master_Plan.md` → find block's topics

### Step 2 — Wiki-first check (LLM Wiki rule)
For each topic in the block:
- Check `02_Courses/[active course]/wiki/[topic-slug].md`
- **EXISTS** → use it directly. Do NOT read the raw PDF. Jump to Step 3.
- **MISSING** → trigger Wiki Ingest now (read `scripts/data/protocols/wiki_ingest.md`), then continue.

### Step 3 — Generate the study guide
From wiki page content (or freshly ingested content):

```
## Block [N] Study Guide — [Topic Names]

| Pages | What's there | Why study it |
|-------|-------------|--------------|
| p.X-Y | [content]   | [exam relevance + past paper link] |

SKIP: p.A-B — [reason]

Past paper questions:
| Topic | Questions | What they ask |
|-------|-----------|---------------|
| [topic] | 20XX Q[N] | [trace/compare/prove/define] |

Block [N] plan ([time range]):
1. [topic] — p.X-Y — [N] min
...
[After each algorithm: "close notes and trace on paper"]
```

### Step 4 — Link to exact past paper questions
Tell the user the exact exam format expected (e.g. "Show the fringe as a sorted list at every step").

Rule: guide fits one screen — tables and bullets only.

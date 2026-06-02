## WIKI INGEST PROTOCOL

**Trigger:** Block Study Guide started for a topic with no wiki page, OR topic first reaches ✅/📖.

**Purpose:** Compile raw source material into a dense wiki page. Run ONCE per topic. After this the wiki page is the source of truth — never re-read the raw PDF for this topic again.

### Step 1 — Identify
- Course: from `scripts/data/wiki_state.md`
- Topic: from block plan or trigger message
- Topic slug: lowercase, hyphens (e.g. `forward-chaining`, `alpha-beta-pruning`)
- Source file: check `02_Courses/[course]/` for the relevant PDF (lecture slides or textbook chapter)

### Step 2 — Read raw source (ONCE)
- Read the PDF pages for this topic only (use page range from `_TopicQuestionMap.md` or `_Syllabus.md`)
- For each page: extract definitions, algorithms, worked examples — skip admin/title pages

### Step 3 — Read past paper questions (ONCE)
- Read `02_Courses/[course]/_TopicQuestionMap.md` for this topic's rows
- Read the exact past-paper PDF pages listed for each question
- Extract verbatim question wording — word for word, all sub-parts

### Step 4 — Write `02_Courses/[course]/wiki/[topic-slug].md`
Use this EXACT structure (fits one screen):

```markdown
# [Topic Name]
> [[wiki/_index|← Course Index]] · [[_Topics]] · [[00_Dashboard]]

## Definition
[One sentence, exam-ready phrasing]

## Key steps / algorithm
1. [Step 1]
2. [Step 2]
...

## Exam pattern
| Year | Q# | What it asks |
|---|---|---|
| 2024 | A-Q1 | [verbatim question ≤100 chars] |
| 2023 | A-Q1 | [verbatim question ≤100 chars] |
🔁 Repeats every year: [what the recurring ask is — one line]

## Weak spots / common mistakes
- [mistake or gotcha 1]
- [mistake or gotcha 2]

## Related topics
[[topic-a]] · [[topic-b]]
```

### Step 5 — Update `02_Courses/[course]/wiki/_index.md`
Append: `- [[wiki/[topic-slug]|[Topic Name]]] — [one-line description]`
If `_index.md` doesn't exist, create it:
```markdown
# [Course Code] Wiki Index
> [[_Topics]] · [[_TopicQuestionMap]] · [[00_Dashboard]]

## Topics
- [[wiki/[topic-slug]|[Topic Name]]] — [one-line description]
```

### Step 6 — Confirm and continue
Output: `✅ Wiki page created: wiki/[topic-slug].md — proceeding to study guide.`
Then continue with Block Study Guide Step 3.

**Hard rule:** After Step 4 is written, this PDF is never opened again for this topic.

## RECALL GAPS TRACKING PROTOCOL

Data store: `scripts/data/recall_gaps.json`
Fields per gap: topic, course, source_block, date_identified, question_missed, revised (bool), revision_date

Adding a gap (after active recall):
```bash
python3 scripts/recall_gaps.py add COURSE "topic" "question missed" "Block N"
```

Marking revised — triggered by "revised [topic]" or "done revising [topic]":
```bash
python3 scripts/recall_gaps.py mark-revised COURSE "topic"
python3 scripts/spaced_rep.py recalled COURSE "topic" [confidence]
```

End-of-day reminder (part of 🔵 end-of-session):
```bash
python3 scripts/recall_gaps.py reminder
```
If unrevised gaps: send Telegram reminder + add to tomorrow's Block 1.
For gaps older than 2 days: escalate to Block 1 AND morning reminder.

Listing: `python3 scripts/recall_gaps.py list` / `list --today-only`

## QUIZ MODE PROTOCOL

Triggered by: "Quiz me on [topic]" / "Test me on [topic]"

1. Check `02_Courses/[active course]/wiki/[topic-slug].md` first — if it exists, use it for questions. Fall back to `_TopicQuestionMap.md` only if no wiki page.
2. Select 3–5 questions, easiest first.
3. Send the FIRST question only. Wait for the answer.
4. On answer: grade ✅/⚠️/❌, give correct answer if wrong/partial, ask "Confidence? (1–5)"
5. Send next question. Repeat until done.
6. Final summary: score X/Y, weakest point. Update `_Topics.md` confidence. Run `python3 scripts/spaced_rep.py`

Rules: one question at a time; exam-style format.

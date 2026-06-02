## CONFIDENCE UPDATE PROTOCOL

Triggered by: "Confidence on [topic]: [1-5]" / after any quiz

1. Find topic in `_Topics.md` (fuzzy match OK)
2. Update 'Conf' column
3. Run `python3 scripts/spaced_rep.py`
4. If confidence ≤ 2: add topic to tomorrow's Block 1
5. Update `wiki/[topic-slug].md` — adjust "Weak spots" section if confidence ≤ 2
6. Confirm: "Updated confidence for [topic]: [N]/5"

Scale: 1=barely remember | 2=blank in exam | 3=explain but detail errors | 4=cold explain + past papers | 5=bulletproof

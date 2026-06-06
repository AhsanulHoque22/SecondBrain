# videoTopicYear Protocol

**Trigger:** User says `"[Topic Name] videoTopicYear [playlist URL]"` — or — pastes a YouTube playlist URL and asks which videos to watch for a topic / for the exam.

**Purpose:** Given a YouTube playlist and a course topic, produce a prioritised watch list by mapping each video to slide subtopics and past-paper questions. Answers: which videos matter, why, and in what order.

**Tools required:** `yt-dlp` (pre-installed at `/home/ahsanul-hoque/.local/bin/yt-dlp`)

---

## Steps to Execute

### Step 1 — Fetch Playlist Titles
```bash
yt-dlp --flat-playlist --print "%(playlist_index)s. %(title)s" "<PLAYLIST_URL>" 2>/dev/null
```
- This produces a numbered list of all video titles without downloading anything.
- If yt-dlp is not installed: ask user to run `pip install yt-dlp` or paste titles manually.

### Step 2 — Load Topic Subtopics
- Read `02_Courses/[course]/wiki/[topic].md` — this is the authoritative subtopic list.
- If no wiki page exists: read the source slide PDF (see `question_analysis.md` for the source PDF map) and extract all subtopics.
- Do NOT re-read the raw PDF if a wiki page already exists.

### Step 3 — Load Past Paper Questions for the Topic
- Read `02_Courses/[course]/_TopicQuestionMap.md`.
- Extract every question entry for this topic (2020–2024).
- Build a list of **subtopics that appeared** vs **subtopics that never appeared**.

### Step 4 — Map Each Video to Subtopics
For every video title from Step 1:
- Classify which slide subtopic(s) it covers (by title keywords).
- Tag it with the past paper appearance status:
  - ✅ **Appeared in past papers** — high priority
  - 📖 **In slides, not yet in past papers** — medium priority (may appear)
  - ❌ **Not in slides / not in syllabus** — skip

### Step 5 — Output the Watch List
Produce three tables:

**Table A — Priority 1: Watch these** (subtopic appeared in past papers)
| # | Video title | Subtopic | Past paper appearances |

**Table B — Priority 2: Watch if time allows** (subtopic in slides, not yet tested)
| # | Video title | Subtopic | Risk assessment |

**Table C — Skip** (outside syllabus or already better covered by wiki/solutions PDF)
| # | Video title | Reason |

### Step 6 — Subtopic Coverage Map
Produce a final master table showing every subtopic from the slides:

| Subtopic | In slides? | Appeared in papers? | Video # covering it |
|----------|-----------|--------------------|--------------------|

Rows where "Appeared in papers = Yes" but "Video = None" → flag as a gap the user should fill from the solutions PDF, not videos.

### Step 7 — Hard Cap Recommendation
State the maximum time to spend on these videos, based on:
- Days until exam
- Status of the topic in `_Topics.md` (🔲 / 📖 / ✅)
- Whether a solutions PDF already exists for this topic

If topic is ✅ or solutions PDF exists → cap at 45 min (recall reinforcement only).
If topic is 📖 → cap at 90 min (selective watching, then do active recall).
If topic is 🔲 → cap at 2 hours, then immediately trigger Block Study Guide.

### Step 8 — Git Commit (only if _TopicQuestionMap.md or _Topics.md were updated during this workflow)
```bash
git add -A
git commit -m "study: [topic] videoTopicYear map generated"
```

---

## Decision Rules for Classifying Videos

| Video title contains… | Likely subtopic | Priority |
|-----------------------|----------------|----------|
| "Uncertainty" / "Doorbell" / "Reasoning under uncertainty" | Uncertainty concept | ✅ High (2020, 2021) |
| "Bayesian Belief Network" / "BBN" / "Burglary Alarm" | BN joint factorization | ✅ High (2021–2023) |
| "Naive Bayes Theorem" / "MAP" / "posterior" | Extended Bayes Form 1 | ✅ High (2020, 2024) |
| "Inference" + "Bayesian" | 4 BN inference types | 📖 Medium |
| "Naive Bayes Classifier" / "classification" / "feature" | ML classifier (not AI exam) | ❌ Skip |
| "Gaussian Naive Bayes" | ML classifier variant | ❌ Skip |
| "Text Classification" / "Spam" / "TF-IDF" | ML NLP (not AI exam) | ❌ Skip |
| "Hidden Markov" / "HMM" / "Temporal" | HMM (not in CSE 713) | ❌ Skip |
| "Laplace smoothing" / "Add-1" | ML preprocessing | ❌ Skip |
| "Backpropagation" / "sigmoid" | Neural Networks (diff topic) | ❌ Skip for Bayes |
| "Alpha-Beta" / "Minimax" | Game Playing (diff topic) | ❌ Skip for Bayes |
| "Forward Chaining" / "Backward Chaining" | Rule-Based (diff topic) | ❌ Skip for Bayes |

---

## Output Format Rules
- Always state how many videos total vs how many to actually watch.
- Always give the time estimate for Priority 1 + Priority 2 videos combined.
- Always end with the hard cap recommendation and what to do after the videos.
- Never recommend watching a video that covers only content fully solved in the topic's solutions PDF — the PDF is faster and exam-targeted.

---

## Example Trigger Commands
```
Bayes videoTopicYear https://youtube.com/playlist?list=PLxxx
Neural Networks videoTopicYear https://youtube.com/playlist?list=PLyyy
Planning videoTopicYear https://youtube.com/playlist?list=PLzzz
```

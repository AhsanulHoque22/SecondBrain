## OBSIDIAN WIKILINK PROTOCOL

Every markdown file must have ≥1 `[[wikilink]]`.

Navigation line (line 2, after title):
```
> [[00_Dashboard]] · [[relevant_file]] · [[another_relevant_file]]
```

Standard links by file type:
- Daily logs → `[[00_Dashboard]]` + `[[active course _Topics]]` + `[[01_Master_Plan]]`
- Course _Topics.md → `[[_Syllabus]]` + `[[_TopicQuestionMap]]` + `[[00_Dashboard]]`
- Course _Syllabus.md → `[[_Topics]]` + `[[_TopicQuestionMap]]`
- Wiki pages → `[[wiki/_index|← Course Index]]` + `[[_Topics]]` + `[[00_Dashboard]]`
- Any new topic note → link to course file + `[[_Topics]]`

Course wikilinks: AI=`[[02_Courses/CSE713_AI/_Topics|AI]]`, InfoSec=`[[02_Courses/CSE717_InfoSec/README|InfoSec]]`, Compiler=`[[02_Courses/CSE711_Compiler/README|Compiler]]`, Distributed=`[[02_Courses/CSE719_Distributed/README|Distributed]]`, Graphics=`[[02_Courses/CSE715_Graphics/README|Graphics]]`

In daily logs: always `[[link]]` every topic name to its course file.

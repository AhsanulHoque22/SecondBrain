#!/bin/bash
# NotebookLM Prep Script
# Finds all PDFs in each course folder and creates upload checklists
# Run from vault root: bash scripts/notebooklm_prep.sh

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
COURSES_DIR="$VAULT_DIR/02_Courses"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  NotebookLM Source Preparation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Go to: notebooklm.google.com"
echo "Create one notebook per course, then upload the files listed below."
echo ""

for course_dir in "$COURSES_DIR"/*/; do
    course_name=$(basename "$course_dir")
    output_file="$course_dir/NotebookLM_Sources.md"

    echo "━━━━ $course_name ━━━━"

    # Find all PDFs and markdown notes
    pdfs=$(find "$course_dir" -name "*.pdf" 2>/dev/null | sort)
    mds=$(find "$course_dir" -name "*.md" ! -name "_Topics.md" ! -name "NotebookLM_Sources.md" 2>/dev/null | sort)

    # Write the source file
    {
        echo "# NotebookLM Sources — $course_name"
        echo ""
        echo "> Upload all files below to the **$course_name** notebook at notebooklm.google.com"
        echo "> Last updated: $(date '+%Y-%m-%d')"
        echo ""
        echo "## PDFs to upload"
        echo ""
        if [ -n "$pdfs" ]; then
            while IFS= read -r pdf; do
                filename=$(basename "$pdf")
                size=$(du -h "$pdf" 2>/dev/null | cut -f1)
                echo "- [ ] \`$filename\` ($size)"
            done <<< "$pdfs"
        else
            echo "- (no PDFs found yet — add your lecture slides and textbook chapters here)"
        fi

        echo ""
        echo "## Notes to paste as text"
        echo ""
        if [ -n "$mds" ]; then
            while IFS= read -r md; do
                filename=$(basename "$md")
                echo "- [ ] \`$filename\` — paste contents into NotebookLM as a text source"
            done <<< "$mds"
        fi

        echo ""
        echo "## Recommended NotebookLM prompts (use after upload)"
        echo ""
        echo '```'
        echo '"Generate 15 exam-style questions based on past paper patterns"'
        echo '"Create a 1-page cheat sheet for this course"'
        echo '"What topics from my syllabus are covered in the uploaded materials?"'
        echo '"Explain [topic] step by step as if preparing me for an exam"'
        echo '"Generate an Audio Overview focusing on the most important exam topics"'
        echo '```'
    } > "$output_file"

    # Print summary
    pdf_count=$(echo "$pdfs" | grep -c . || echo 0)
    echo "  PDFs found: $pdf_count"
    echo "  Upload list: $output_file"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Done. Open each NotebookLM_Sources.md for the upload checklist."
echo "Priority: do CSE713_AI first — that's your next exam."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

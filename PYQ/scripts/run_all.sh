#!/usr/bin/env bash
# Rebuild the question bank from the public assignment PDFs.
# Needs: .venv with pymupdf (see ../../requirements.txt). Run from the repo root.
set -euo pipefail
PY=${PY:-.venv/bin/python}
W=$(mktemp -d)
BASE=https://raw.githubusercontent.com/Shivammittal13ai/Big-Data-Computing_NPTEL-2025/main/Assignments
mkdir -p "$W/pdfs" "$W/draft"
for f in "2019_A-0-2,5-8_solu.pdf" "2019_A-4.pdf" "2021_A-0 to 8_solu.pdf" "2022_A-1 to 8_solu.pdf" \
         "2023_A-0 to 8_solu.pdf" "2024_A-0 to 8_solu.pdf" "2025_A-0 to 8_solu.pdf"; do
  curl -fsSL --max-time 90 --retry 3 "$BASE/$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$f")" -o "$W/pdfs/$f"
done
P=PYQ/scripts; D=$W/draft; F=$W/pdfs
# portal printouts (question + options + "Accepted Answers"); last arg = pages that hold week 0
$PY $P/parse_portal.py "$F/2019_A-0-2,5-8_solu.pdf" 2019 $D/2019a.json
$PY $P/parse_portal.py "$F/2019_A-4.pdf" 2019 $D/2019b.json
$PY $P/parse_portal.py "$F/2023_A-0 to 8_solu.pdf" 2023 $D/2023w0.json 3
$PY $P/parse_portal.py "$F/2024_A-0 to 8_solu.pdf" 2024 $D/2024w0.json 5
$PY $P/parse_portal.py "$F/2025_A-0 to 8_solu.pdf" 2025 $D/2025w0.json 1
# solution documents (weeks 1-8); last arg = first page of the solutions
$PY $P/parse_solutions.py "$F/2021_A-0 to 8_solu.pdf" 2021 $D/2021s.json 4
$PY $P/parse_solutions.py "$F/2022_A-1 to 8_solu.pdf" 2022 $D/2022s.json 1
$PY $P/parse_solutions.py "$F/2023_A-0 to 8_solu.pdf" 2023 $D/2023s.json 4
$PY $P/parse_solutions.py "$F/2024_A-0 to 8_solu.pdf" 2024 $D/2024s.json 6
$PY $P/parse_solutions.py "$F/2025_A-0 to 8_solu.pdf" 2025 $D/2025s.json 2
$PY $P/resolve_2024.py $D/2024s.json
PYQ_DRAFTS=$D $PY $P/build_bank.py
$PY $P/validate.py
$PY $P/build_outputs.py

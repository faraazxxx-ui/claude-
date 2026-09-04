#!/usr/bin/env bash
# Render a self-contained HTML file to PDF using the Playwright-bundled Chromium
# already present in this environment. No Playwright python package needed —
# Chromium's own --headless --print-to-pdf flag does the work.
#
# Usage: render_pdf.sh <input.html> <output.pdf>
set -euo pipefail

IN="${1:?usage: render_pdf.sh <input.html> <output.pdf>}"
OUT="${2:?usage: render_pdf.sh <input.html> <output.pdf>}"

CHROME="$(find /opt/pw-browsers -maxdepth 3 -type f -iname chrome 2>/dev/null | head -1)"
if [ -z "$CHROME" ]; then
  echo "No bundled Chromium found under /opt/pw-browsers — fall back to the pdf skill's HTML->PDF path." >&2
  exit 1
fi

ABS_IN="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"

"$CHROME" \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --print-to-pdf="$OUT" \
  --print-to-pdf-no-header \
  --no-pdf-header-footer \
  "file://$ABS_IN"

echo "Wrote $OUT"

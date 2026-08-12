#!/bin/bash
# ============================================================
# sync-to-second-brain.sh — Sync all documents to iCloud
# ============================================================
# Destination:
#   /Users/dr.faraaz/Library/Mobile Documents/
#     com~apple~CloudDocs/Cleaned and Processed Documents/_second-brain
#
# Usage:   ./scripts/sync-to-second-brain.sh
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DEST="/Users/dr.faraaz/Library/Mobile Documents/com~apple~CloudDocs/Cleaned and Processed Documents/_second-brain/legal-strategy-system"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "============================================"
echo "  Sync to Second Brain (iCloud)"
echo "  $(date)"
echo "============================================"
echo ""

# Check if destination exists
if [ ! -d "$(dirname "$DEST")" ]; then
    echo -e "${RED}ERROR: iCloud path not found.${NC}"
    echo "Expected: $(dirname "$DEST")"
    echo ""
    echo "Make sure:"
    echo "  1. You're running this on your Mac (not a remote server)"
    echo "  2. iCloud Drive is enabled"
    echo "  3. The '_second-brain' folder exists in iCloud"
    exit 1
fi

# Create destination directory
mkdir -p "$DEST"
mkdir -p "$DEST/legal-strategy"
mkdir -p "$DEST/financial-analysis"
mkdir -p "$DEST/timeline"
mkdir -p "$DEST/evidence"
mkdir -p "$DEST/pdfs"

echo "Syncing documents..."
echo ""

# Sync markdown files
for dir in legal-strategy financial-analysis timeline evidence; do
    if [ -d "$PROJECT_DIR/$dir" ]; then
        echo -n "  Syncing $dir/ ... "
        cp -R "$PROJECT_DIR/$dir/"*.md "$DEST/$dir/" 2>/dev/null && \
            echo -e "${GREEN}OK${NC}" || \
            echo -e "${YELLOW}No files${NC}"
    fi
done

# Sync PDFs
if [ -d "$PROJECT_DIR/output" ] && ls "$PROJECT_DIR/output/"*.pdf 1> /dev/null 2>&1; then
    echo -n "  Syncing PDFs ... "
    cp "$PROJECT_DIR/output/"*.pdf "$DEST/pdfs/"
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}  No PDFs found. Run ./scripts/export-pdf.sh first.${NC}"
fi

# Sync README
echo -n "  Syncing README.md ... "
cp "$PROJECT_DIR/README.md" "$DEST/"
echo -e "${GREEN}OK${NC}"

echo ""
echo "============================================"
echo "  Sync Complete"
echo "  Destination: $DEST"
echo "============================================"
echo ""
echo "Your files are now in iCloud and will sync across devices."
echo ""
echo "Next: Follow ./scripts/upload-checklist.md for Drive/Notion/NotebookLM"

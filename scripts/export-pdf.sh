#!/bin/bash
# ============================================================
# export-pdf.sh — Convert all markdown files to PDF
# ============================================================
# Prerequisites: Install pandoc and a LaTeX engine
#   macOS:  brew install pandoc && brew install --cask mactex
#   or:     brew install pandoc && pip install weasyprint
#
# Usage:   ./scripts/export-pdf.sh
# Output:  All PDFs saved to ./output/
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_DIR/output"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "============================================"
echo "  Legal Strategy System — PDF Export"
echo "  $(date)"
echo "============================================"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check for pandoc
if ! command -v pandoc &> /dev/null; then
    echo -e "${RED}ERROR: pandoc is not installed.${NC}"
    echo "Install it with:"
    echo "  macOS:  brew install pandoc"
    echo "  Linux:  sudo apt install pandoc"
    exit 1
fi

# Determine PDF engine
PDF_ENGINE=""
if command -v pdflatex &> /dev/null; then
    PDF_ENGINE="--pdf-engine=pdflatex"
elif command -v weasyprint &> /dev/null; then
    PDF_ENGINE="--pdf-engine=weasyprint"
elif command -v wkhtmltopdf &> /dev/null; then
    PDF_ENGINE="--pdf-engine=wkhtmltopdf"
else
    echo -e "${YELLOW}WARNING: No PDF engine found. Will attempt default.${NC}"
    echo "For best results, install one of:"
    echo "  brew install --cask mactex"
    echo "  pip install weasyprint"
    echo ""
fi

# Export individual documents
SUCCESS=0
FAIL=0

for md_file in $(find "$PROJECT_DIR" -name "*.md" -not -path "*/\.*" -not -path "*/output/*" -not -path "*/scripts/*" | sort); do
    relative_path="${md_file#$PROJECT_DIR/}"
    # Create a clean filename: legal-strategy/00-case-overview.md → legal-strategy_00-case-overview.pdf
    pdf_name=$(echo "$relative_path" | sed 's/\//_/g' | sed 's/\.md$/.pdf/')
    output_file="$OUTPUT_DIR/$pdf_name"

    echo -n "  Converting: $relative_path ... "

    if pandoc "$md_file" -o "$output_file" $PDF_ENGINE \
        -V geometry:margin=1in \
        -V fontsize=11pt \
        --highlight-style=tango \
        2>/dev/null; then
        echo -e "${GREEN}OK${NC}"
        SUCCESS=$((SUCCESS + 1))
    else
        echo -e "${RED}FAILED${NC}"
        FAIL=$((FAIL + 1))
    fi
done

# Create unified combined PDF
echo ""
echo -n "  Creating unified document ... "
COMBINED_MD="$OUTPUT_DIR/_combined_temp.md"
> "$COMBINED_MD"

for md_file in $(find "$PROJECT_DIR" -name "*.md" -not -path "*/\.*" -not -path "*/output/*" -not -path "*/scripts/*" | sort); do
    echo "" >> "$COMBINED_MD"
    echo "---" >> "$COMBINED_MD"
    echo "" >> "$COMBINED_MD"
    cat "$md_file" >> "$COMBINED_MD"
    echo "" >> "$COMBINED_MD"
    echo "\\newpage" >> "$COMBINED_MD"
done

UNIFIED_PDF="$OUTPUT_DIR/UNIFIED_Legal_Strategy_System_${TIMESTAMP}.pdf"
if pandoc "$COMBINED_MD" -o "$UNIFIED_PDF" $PDF_ENGINE \
    -V geometry:margin=1in \
    -V fontsize=11pt \
    --highlight-style=tango \
    --toc \
    -V toc-title:"Table of Contents" \
    2>/dev/null; then
    echo -e "${GREEN}OK${NC}"
    SUCCESS=$((SUCCESS + 1))
else
    echo -e "${RED}FAILED${NC}"
    FAIL=$((FAIL + 1))
fi

rm -f "$COMBINED_MD"

# Summary
echo ""
echo "============================================"
echo "  Export Complete"
echo "  Succeeded: $SUCCESS"
echo "  Failed:    $FAIL"
echo "  Output:    $OUTPUT_DIR/"
echo "============================================"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}All exports succeeded.${NC}"
    echo ""
    echo "Unified PDF: $UNIFIED_PDF"
    echo ""
    echo "Next steps:"
    echo "  1. Run ./scripts/sync-to-second-brain.sh to copy to iCloud"
    echo "  2. Follow ./scripts/upload-checklist.md for Drive/Notion/NotebookLM"
else
    echo -e "${YELLOW}Some exports failed. Check that your PDF engine is installed.${NC}"
fi

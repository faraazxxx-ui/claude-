#!/usr/bin/env python3
"""md -> styled HTML -> PDF (chromium) + DOCX (soffice). Usage: build_docs.py file.md [file2.md ...]"""
import markdown, subprocess, sys, os, shutil

CSS = """
@page { size: letter; margin: 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; color: #1a1d23;
       font-size: 10.5pt; line-height: 1.45; max-width: 100%; margin: 0; }
h1 { font-size: 17pt; border-bottom: 3px solid #8a1f1f; padding-bottom: 6px; margin: 0 0 4px; }
h1 + p em, .banner { color: #8a1f1f; font-weight: 600; }
h2 { font-size: 13pt; color: #21315e; border-bottom: 1px solid #c9d2e4; padding-bottom: 3px;
     margin: 18px 0 8px; page-break-after: avoid; }
h3 { font-size: 11pt; color: #21315e; margin: 12px 0 6px; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 9.2pt; page-break-inside: auto; }
th { background: #21315e; color: #fff; text-align: left; padding: 5px 7px; }
td { border: 1px solid #c9d2e4; padding: 4px 7px; vertical-align: top; }
tr:nth-child(even) td { background: #f4f6fb; }
blockquote { border-left: 3px solid #8a1f1f; margin: 6px 0 6px 4px; padding: 2px 10px;
             color: #40434b; font-style: italic; background: #faf7f7; }
code { background: #eef1f6; padding: 0 3px; border-radius: 3px; font-size: 9pt; }
strong { color: #111; }
hr { border: none; border-top: 1px solid #c9d2e4; margin: 14px 0; }
li { margin: 2px 0; }
"""

def build(md_path):
    base = os.path.splitext(md_path)[0]
    text = open(md_path).read()
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists", "smarty"])
    title = os.path.basename(base).replace("_", " ")
    html = f"<html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"
    html_path = f"{base}.print.html"
    open(html_path, "w").write(html)

    chrome = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
    if not os.path.exists(chrome):
        chrome = shutil.which("chromium") or "/opt/pw-browsers/chromium"
    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                    f"--print-to-pdf={base}.pdf", "--no-pdf-header-footer", html_path],
                   check=True, capture_output=True)
    subprocess.run(["soffice", "--headless", "--convert-to",
                    "docx:MS Word 2007 XML", "--outdir", os.path.dirname(os.path.abspath(md_path)) or ".", html_path],
                   check=True, capture_output=True)
    got = f"{base}.print.docx"
    if os.path.exists(got):
        os.replace(got, f"{base}.docx")
    # verify
    import pypdf
    r = pypdf.PdfReader(f"{base}.pdf")
    txt = "".join((p.extract_text() or "") for p in r.pages[:3])
    assert len(txt) > 200, f"PDF text extraction too small for {base}.pdf"
    print(f"OK {base}.pdf ({len(r.pages)}p) + {base}.docx ({os.path.getsize(base + '.docx')//1024}KB)")

if __name__ == "__main__":
    for f in sys.argv[1:]:
        build(f)

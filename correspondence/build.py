#!/usr/bin/env python3
"""Build the correspondence documents: self-contained HTML + PDF.

Each source in src/ carries three placeholders:
  <!--FONTS-->      -> inline @font-face rules (woff2 as data URIs)
  {{SIGNATURE}}     -> the signature PNG as a data URI
  <!--PDF_DATA-->   -> the rendered PDF, base64, for the page's Download button

Steps per document:
  1. inline fonts + signature            -> scratch/<name>.print.html
  2. Chromium --print-to-pdf             -> scratch/<name>.raw.pdf
  3. PyMuPDF: paint the aged-paper ground under every page, stamp the
     running footer in the bottom margin, set metadata
                                         -> <name>.pdf
  4. inject the PDF back into the HTML   -> <name>.html   (what gets published)
  5. optional page PNGs via PyMuPDF      -> scratch/<name>-p<N>.png

Chromium leaves @page margins unpainted and mis-positions position:fixed in
print, so the paper and the footer are added in step 3 rather than in CSS.

Fonts come from @fontsource on npm (Google Fonts is not reachable from the
build sandbox):  npm pack @fontsource/spectral @fontsource/ibm-plex-mono

usage: build.py --fonts DIR --signature PNG [--scratch DIR] [--chrome PATH] [--pages] [NAME ...]
"""
import argparse
import base64
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = {
    "hf-specialist-letter": {
        "title": "Referral — M F Rahaman",
        "subject": "Heart failure specialist referral: atrial cardiomyopathy with HFpEF, AF/flutter, hypertension, severe OSA",
        "footer": "The Rahman Foundation · Confidential clinical correspondence · M F Rahaman · 5 September 2026",
    },
    "post-visit-summary": {
        "title": "Care Plan — M F Rahaman",
        "subject": "Treatment plan and investigations advised for Mr M F Rahaman",
        "footer": "The Rahman Foundation · Treatment plan · M F Rahaman · 5 September 2026",
    },
}
AUTHOR = "Mohammed Faraaz Rahman, M.D."
FONT_FACES = [
    ("Spectral", 400, "spectral-latin-400-normal.woff2"),
    ("Spectral", 500, "spectral-latin-500-normal.woff2"),
    ("Spectral", 600, "spectral-latin-600-normal.woff2"),
    ("IBM Plex Mono", 400, "ibm-plex-mono-latin-400-normal.woff2"),
    ("IBM Plex Mono", 500, "ibm-plex-mono-latin-500-normal.woff2"),
    ("IBM Plex Mono", 600, "ibm-plex-mono-latin-600-normal.woff2"),
]
DEFAULT_CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

# aged paper: centre / edge, matching --paper-hi / --paper-lo in the CSS
PAPER_HI = (0xFA, 0xF5, 0xEA)
PAPER_LO = (0xF0, 0xE7, 0xD3)
FOOTER_RGB = (0x9A / 255, 0x8F / 255, 0x79 / 255)
MM = 72 / 25.4


def b64(path: pathlib.Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def find_font(fonts_dir: pathlib.Path, fname: str) -> pathlib.Path:
    matches = list(fonts_dir.rglob(fname))
    if not matches:
        sys.exit(f"font file not found under {fonts_dir}: {fname}")
    return matches[0]


def font_css(fonts_dir: pathlib.Path) -> str:
    rules = []
    for family, weight, fname in FONT_FACES:
        rules.append(
            f'@font-face{{font-family:"{family}";font-style:normal;font-weight:{weight};'
            f'font-display:block;src:url(data:font/woff2;base64,{b64(find_font(fonts_dir, fname))}) format("woff2")}}'
        )
    return "<style>\n" + "\n".join(rules) + "\n</style>"


def wrap_document(body_html: str) -> str:
    """Mirror the Artifact host's skeleton so Chromium renders what the viewer will."""
    m = re.search(r"<title>(.*?)</title>", body_html, re.S)
    title = m.group(1).strip() if m else "Document"
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        f"<title>{title}</title>"
        "<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>"
        f"</head><body>{body_html}</body></html>"
    )


def render_pdf(chrome: str, html_path: pathlib.Path, pdf_path: pathlib.Path) -> None:
    cmd = [
        chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
        "--no-pdf-header-footer", "--virtual-time-budget=6000",
        f"--print-to-pdf={pdf_path}", html_path.as_uri(),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if not pdf_path.exists() or pdf_path.stat().st_size < 1000:
        sys.exit(f"chromium did not produce a PDF for {html_path.name}\n{res.stderr[-2000:]}")


def paper_image(scratch: pathlib.Path) -> pathlib.Path:
    """A4 aged-paper ground with a soft radial vignette, as JPEG."""
    out = scratch / "paper-a4.jpg"
    if out.exists():
        return out
    import numpy as np
    from PIL import Image
    w, h = 1191, 1684  # A4 at 144 dpi
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx / w - 0.5) / 0.68) ** 2 + ((yy / h - 0.42) / 0.62) ** 2)
    t = np.clip(r, 0, 1) ** 1.6
    hi = np.array(PAPER_HI, np.float32)
    lo = np.array(PAPER_LO, np.float32)
    img = hi[None, None, :] * (1 - t[..., None]) + lo[None, None, :] * t[..., None]
    Image.fromarray(img.round().astype(np.uint8), "RGB").save(out, quality=88, subsampling=0)
    return out


def mono_ttf(fonts_dir: pathlib.Path, scratch: pathlib.Path) -> pathlib.Path:
    """PyMuPDF embeds TTF/OTF, not woff2 — convert the footer face once."""
    out = scratch / "ibm-plex-mono-400.ttf"
    if not out.exists():
        from fontTools.ttLib import TTFont
        f = TTFont(find_font(fonts_dir, "ibm-plex-mono-latin-400-normal.woff2"))
        f.flavor = None
        f.save(out)
    return out


def finish_pdf(raw: pathlib.Path, final: pathlib.Path, meta: dict, paper: pathlib.Path, ttf: pathlib.Path) -> int:
    import pymupdf
    doc = pymupdf.open(raw)
    font = pymupdf.Font(fontfile=str(ttf))
    size, track = 6.6, 0.17 * 6.6
    # running footer: tracked uppercase, centred 10 mm above the paper's bottom edge
    text = meta["footer"].upper()
    widths = [font.text_length(ch, fontsize=size) for ch in text]
    total = sum(widths) + track * (len(text) - 1)
    xref = 0
    for page in doc:
        # Chromium's content stream leaves its px->pt flip matrix in force; wrap it in q/Q
        # so what we append lands in page coordinates.
        page.clean_contents()
        rect = page.rect
        xref = page.insert_image(rect, filename=str(paper), overlay=False, xref=xref or 0)
        tw = pymupdf.TextWriter(rect, color=FOOTER_RGB)
        x = (rect.width - total) / 2
        y = rect.height - 10 * MM
        for ch, wch in zip(text, widths):
            tw.append((x, y), ch, font=font, fontsize=size)
            x += wch + track
        tw.write_text(page)
    doc.set_metadata({
        "title": meta["title"], "author": AUTHOR, "subject": meta["subject"],
        "creator": "The Rahman Foundation", "producer": "Chromium + PyMuPDF",
    })
    n = doc.page_count
    tmp = final.with_suffix(".tmp.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    os.replace(tmp, final)
    return n


def page_pngs(pdf_path: pathlib.Path, scratch: pathlib.Path, name: str, dpi: int = 110) -> list[str]:
    import pymupdf
    out = []
    with pymupdf.open(pdf_path) as doc:
        for i, page in enumerate(doc, 1):
            p = scratch / f"{name}-p{i}.png"
            page.get_pixmap(dpi=dpi).save(p)
            out.append(str(p))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True, type=pathlib.Path)
    ap.add_argument("--signature", required=True, type=pathlib.Path)
    ap.add_argument("--scratch", type=pathlib.Path, default=ROOT / ".build")
    ap.add_argument("--chrome", default=DEFAULT_CHROME)
    ap.add_argument("--pages", action="store_true", help="also write page PNGs for review")
    ap.add_argument("names", nargs="*", default=list(DOCS))
    args = ap.parse_args()

    args.scratch.mkdir(parents=True, exist_ok=True)
    fonts = font_css(args.fonts)
    signature = "data:image/png;base64," + b64(args.signature)
    paper = paper_image(args.scratch)
    ttf = mono_ttf(args.fonts, args.scratch)

    for name in args.names:
        meta = DOCS[name]
        src = ROOT / "src" / f"{name}.html"
        html = src.read_text(encoding="utf-8")
        for token in ("<!--FONTS-->", "{{SIGNATURE}}", "<!--PDF_DATA-->"):
            if token not in html:
                sys.exit(f"{src.name}: missing placeholder {token}")
        html = html.replace("<!--FONTS-->", fonts).replace("{{SIGNATURE}}", signature)

        print_html = args.scratch / f"{name}.print.html"
        print_html.write_text(wrap_document(html.replace("<!--PDF_DATA-->", "")), encoding="utf-8")

        raw_pdf = args.scratch / f"{name}.raw.pdf"
        render_pdf(args.chrome, print_html, raw_pdf)
        pdf_path = ROOT / f"{name}.pdf"
        pages = finish_pdf(raw_pdf, pdf_path, meta, paper, ttf)

        pdf_tag = f'<script id="pdf-b64" type="text/plain">{b64(pdf_path)}</script>'
        out_html = ROOT / f"{name}.html"
        out_html.write_text(html.replace("<!--PDF_DATA-->", pdf_tag), encoding="utf-8")

        line = f"{name}: {pages} pages, pdf {pdf_path.stat().st_size//1024} KB, html {out_html.stat().st_size//1024} KB"
        if args.pages:
            page_pngs(pdf_path, args.scratch, name)
            line += f" -> {args.scratch}"
        print(line)


if __name__ == "__main__":
    main()

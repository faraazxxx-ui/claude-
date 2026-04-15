#!/usr/bin/env python3
"""
Life Intelligence Engine — Evernote ENEX Exporter
Generates ENEX (Evernote Export) files from assembled knowledge,
one per domain, ready for import into Evernote.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape


def sanitize_xml(text: str) -> str:
    """Escape text for XML/XHTML content."""
    return escape(text).replace("\n", "<br/>")


def content_to_enml(content: str) -> str:
    """Convert plain text/markdown content to ENML (Evernote Markup Language)."""
    lines = content.split("\n")
    enml_parts = []

    for line in lines:
        line = line.strip()
        if not line:
            enml_parts.append("<br/>")
            continue

        # Headings
        if line.startswith("### "):
            enml_parts.append(f"<h3>{escape(line[4:])}</h3>")
        elif line.startswith("## "):
            enml_parts.append(f"<h2>{escape(line[3:])}</h2>")
        elif line.startswith("# "):
            enml_parts.append(f"<h1>{escape(line[2:])}</h1>")
        elif line.startswith("- ") or line.startswith("* "):
            enml_parts.append(f"<div>• {escape(line[2:])}</div>")
        elif line.startswith("```"):
            continue  # Skip code fences
        else:
            enml_parts.append(f"<div>{escape(line)}</div>")

    return "\n".join(enml_parts)


def make_enex_note(title: str, content: str, tags: list,
                   source_url: str = "", created: str = "") -> str:
    """Generate a single ENEX note XML element."""
    now = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    created_dt = created or now

    enml_content = content_to_enml(content)

    tags_xml = "\n".join(f"    <tag>{escape(t)}</tag>" for t in tags)

    return f"""  <note>
    <title>{escape(title)}</title>
    <content><![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>
{enml_content}
</en-note>]]></content>
    <created>{created_dt}</created>
    <updated>{now}</updated>
{tags_xml}
    <note-attributes>
      <source>life-intelligence-engine</source>
      <source-url>{escape(source_url)}</source-url>
    </note-attributes>
  </note>"""


def make_enex_file(notes: list, export_date: str = "") -> str:
    """Wrap notes in ENEX envelope."""
    export_date = export_date or datetime.now().strftime("%Y%m%dT%H%M%SZ")
    notes_xml = "\n".join(notes)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
<en-export export-date="{export_date}" application="Life Intelligence Engine" version="1.0">
{notes_xml}
</en-export>"""


def main():
    parser = argparse.ArgumentParser(description="Export assembled knowledge to Evernote ENEX")
    parser.add_argument("--assembled-dir", required=True, help="Path to assembled knowledge")
    parser.add_argument("--output-dir", required=True, help="Output directory for ENEX files")
    args = parser.parse_args()

    domains_dir = os.path.join(args.assembled_dir, "domains")
    os.makedirs(args.output_dir, exist_ok=True)

    if not os.path.isdir(domains_dir):
        print(f"ERROR: Domains directory not found: {domains_dir}", file=sys.stderr)
        sys.exit(1)

    total_notes = 0

    for domain_slug in sorted(os.listdir(domains_dir)):
        domain_path = os.path.join(domains_dir, domain_slug)
        if not os.path.isdir(domain_path):
            continue

        manifest_path = os.path.join(domain_path, "_manifest.json")
        if not os.path.exists(manifest_path):
            continue

        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        domain_name = manifest.get("domain", domain_slug)
        clusters = manifest.get("clusters", [])

        print(f"Processing domain: {domain_name} ({len(clusters)} clusters)")

        notes = []
        for cluster_info in clusters:
            cluster_file = os.path.join(domain_path, cluster_info.get("file", ""))
            if not os.path.exists(cluster_file):
                continue

            with open(cluster_file, "r") as f:
                cluster = json.load(f)

            # Build note content from cluster nodes
            title = f"{domain_name} — {cluster.get('source_file', 'Unknown')}"
            title = Path(title).stem if "/" in title else title
            title = title[:200]  # Evernote title limit

            content_parts = []
            for node in cluster.get("nodes", []):
                node_content = node.get("content", "")
                if node_content:
                    content_parts.append(node_content)

            content = "\n\n".join(content_parts)

            # Build tags
            tags = [
                f"lie/{domain_slug}",
                f"type/{cluster.get('content_type', 'mixed')}",
                f"importance/{cluster_info.get('importance', 5)}",
            ]

            source_url = f"file://{cluster.get('source_file', '')}"

            note = make_enex_note(title, content, tags, source_url)
            notes.append(note)

        if notes:
            enex_filename = f"{domain_slug.replace('_', '-')}.enex"
            enex_path = os.path.join(args.output_dir, enex_filename)
            enex_content = make_enex_file(notes)

            with open(enex_path, "w", encoding="utf-8") as f:
                f.write(enex_content)

            print(f"  Written: {enex_filename} ({len(notes)} notes)")
            total_notes += len(notes)

    print(f"\nExport complete: {total_notes} notes across {len(os.listdir(args.output_dir))} ENEX files")
    print(f"Output: {args.output_dir}")


if __name__ == "__main__":
    main()

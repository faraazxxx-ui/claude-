#!/usr/bin/env python3
"""
AI Chat Output → Notion Automation Script

Captures AI chat outputs (from Claude, Grok, ChatGPT, Gemini) and
automatically creates structured Notion pages with YAML frontmatter.

Usage:
    python3 ai_to_notion.py --source "claude" --topic "My Topic" --content "Chat output text"
    python3 ai_to_notion.py --file /path/to/exported_chat.md --source "grok"

Environment Variables Required:
    NOTION_API_KEY   - Notion integration token
    NOTION_DB_ID     - Target database ID in Notion

Supported Sources: claude, grok, chatgpt, gemini, claude-code, raycast
"""

import argparse
import json
import os
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)


NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "")
NOTION_DB_ID = os.environ.get("NOTION_DB_ID", "")
NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

VALID_SOURCES = ["claude", "grok", "chatgpt", "gemini", "claude-code", "raycast", "other"]


def create_notion_page(source: str, topic: str, content: str, tags: list = None):
    """Create a new Notion page with YAML-style properties and content."""
    if not NOTION_API_KEY:
        print("ERROR: NOTION_API_KEY environment variable not set.")
        sys.exit(1)
    if not NOTION_DB_ID:
        print("ERROR: NOTION_DB_ID environment variable not set.")
        sys.exit(1)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }

    # Build the page properties (acts as YAML frontmatter equivalent)
    properties = {
        "Name": {"title": [{"text": {"content": f"[{source.upper()}] {topic}"}}]},
        "Source": {"select": {"name": source.lower()}},
        "Date": {"date": {"start": date_str}},
        "Topic": {"rich_text": [{"text": {"content": topic}}]},
        "Timestamp": {"rich_text": [{"text": {"content": f"{date_str}T{time_str}"}}]},
    }

    if tags:
        properties["Tags"] = {
            "multi_select": [{"name": tag} for tag in tags]
        }

    # Build the page content as blocks
    # Split content into chunks of 2000 chars (Notion block limit)
    content_blocks = []
    
    # Add YAML-style header block
    yaml_header = f"""---
source: {source}
topic: {topic}
date: {date_str}
time: {time_str}
tags: {json.dumps(tags or [])}
---"""
    
    content_blocks.append({
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": yaml_header}}],
            "language": "yaml",
        },
    })

    # Add divider
    content_blocks.append({"object": "block", "type": "divider", "divider": {}})

    # Add content in chunks
    for i in range(0, len(content), 2000):
        chunk = content[i : i + 2000]
        content_blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}]
            },
        })

    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": properties,
        "children": content_blocks,
    }

    response = requests.post(NOTION_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        page_id = response.json().get("id", "unknown")
        page_url = response.json().get("url", "")
        print(f"SUCCESS: Created Notion page '{topic}' (ID: {page_id})")
        print(f"URL: {page_url}")
        return page_id
    else:
        print(f"ERROR: Failed to create page. Status: {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Send AI chat outputs to Notion")
    parser.add_argument("--source", required=True, choices=VALID_SOURCES, help="AI platform source")
    parser.add_argument("--topic", default="Untitled Chat", help="Topic/title for the note")
    parser.add_argument("--content", default="", help="Chat content as a string")
    parser.add_argument("--file", default="", help="Path to exported chat file")
    parser.add_argument("--tags", nargs="*", default=[], help="Tags for categorization")

    args = parser.parse_args()

    content = args.content
    if args.file:
        with open(args.file, "r") as f:
            content = f.read()

    if not content:
        print("ERROR: Provide --content or --file with chat output.")
        sys.exit(1)

    create_notion_page(
        source=args.source,
        topic=args.topic,
        content=content,
        tags=args.tags,
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Notion Database Setup Script

Creates a Notion database from a JSON schema definition.

Usage:
    python3 notion_setup.py --page-id <parent-page-id> --schema notion_schema.json

Environment Variables:
    NOTION_API_KEY - Notion integration token
"""

import argparse
import json
import os
import sys

import requests

NOTION_API_URL = "https://api.notion.com/v1/databases"
NOTION_VERSION = "2022-06-28"


def load_schema(path: str) -> dict:
    """Load and return the database schema from a JSON file."""
    with open(path) as f:
        return json.load(f)


def _build_property(definition: dict) -> dict:
    """Convert a schema property definition to Notion API format."""
    prop_type = definition["type"]

    if prop_type == "title":
        return {"title": {}}

    if prop_type in ("select", "multi_select"):
        config = {}
        if "options" in definition:
            config["options"] = [
                {"name": opt["name"], "color": opt["color"]}
                for opt in definition["options"]
            ]
        return {prop_type: config}

    if prop_type == "date":
        return {"date": {}}

    if prop_type == "created_time":
        return {"created_time": {}}

    if prop_type == "last_edited_time":
        return {"last_edited_time": {}}

    if prop_type == "rich_text":
        return {"rich_text": {}}

    if prop_type == "checkbox":
        return {"checkbox": {}}

    return {prop_type: {}}


def build_database_payload(schema: dict, page_id: str) -> dict:
    """Build the Notion API payload for creating a database."""
    properties = {}
    for name, definition in schema["properties"].items():
        properties[name] = _build_property(definition)

    return {
        "parent": {"type": "page_id", "page_id": page_id},
        "title": [{"type": "text", "text": {"content": schema["database_name"]}}],
        "properties": properties,
    }


def create_database(schema: dict, page_id: str, api_key: str) -> dict:
    """Create a Notion database via the API and return the response data."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }
    payload = build_database_payload(schema, page_id)
    response = requests.post(NOTION_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(
            f"Notion API request failed with status {response.status_code}: {response.text}"
        )

    return response.json()


def main():
    parser = argparse.ArgumentParser(description="Create a Notion database from a JSON schema")
    parser.add_argument("--page-id", required=True, help="Parent page ID in Notion")
    parser.add_argument("--schema", default="notion_schema.json", help="Path to schema JSON file")
    args = parser.parse_args()

    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        print("ERROR: NOTION_API_KEY environment variable not set.")
        sys.exit(1)

    schema = load_schema(args.schema)
    result = create_database(schema, page_id=args.page_id, api_key=api_key)

    print(f"Database created: {result.get('url', result.get('id', 'unknown'))}")


if __name__ == "__main__":
    main()

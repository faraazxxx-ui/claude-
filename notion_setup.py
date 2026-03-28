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

SUPPORTED_TYPES = {
    "title", "rich_text", "number", "select", "multi_select", "date",
    "checkbox", "url", "email", "phone_number", "created_time",
    "last_edited_time", "created_by", "last_edited_by",
}


class NotionSetupError(Exception):
    """Raised when database creation fails."""


def load_schema(path: str) -> dict:
    """Load and validate the database schema from a JSON file."""
    with open(path) as f:
        schema = json.load(f)
    if "database_name" not in schema:
        raise ValueError("Schema missing required field: 'database_name'")
    if "properties" not in schema or not schema["properties"]:
        raise ValueError("Schema missing required field: 'properties'")
    return schema


def _build_property(definition: dict) -> dict:
    """Convert a schema property definition to Notion API format."""
    prop_type = definition["type"]
    if prop_type not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported property type: '{prop_type}'")

    if prop_type in ("select", "multi_select") and "options" in definition:
        return {prop_type: {"options": [
            {"name": opt["name"], "color": opt["color"]}
            for opt in definition["options"]
        ]}}

    return {prop_type: {}}


def build_database_payload(schema: dict, page_id: str) -> dict:
    """Build the Notion API payload for creating a database."""
    properties = {
        name: _build_property(defn)
        for name, defn in schema["properties"].items()
    }

    payload = {
        "parent": {"type": "page_id", "page_id": page_id},
        "title": [{"type": "text", "text": {"content": schema["database_name"]}}],
        "properties": properties,
    }

    if schema.get("description"):
        payload["description"] = [
            {"type": "text", "text": {"content": schema["description"]}}
        ]

    return payload


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
        raise NotionSetupError(
            f"Notion API request failed ({response.status_code}): {response.text}"
        )

    return response.json()


def verify_database_matches_schema(db_response: dict, schema: dict) -> None:
    """Verify the created database's properties match the schema.

    Raises NotionSetupError if any property is missing or has a wrong type.
    """
    db_props = db_response.get("properties", {})
    for prop_name, prop_def in schema["properties"].items():
        if prop_name not in db_props:
            raise NotionSetupError(
                f"Property '{prop_name}' missing from created database"
            )
        actual_type = db_props[prop_name].get("type")
        if actual_type != prop_def["type"]:
            raise NotionSetupError(
                f"Property '{prop_name}': expected type '{prop_def['type']}', "
                f"got '{actual_type}'"
            )


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
    verify_database_matches_schema(result, schema)

    print(f"Database created: {result.get('url', result.get('id', 'unknown'))}")


if __name__ == "__main__":
    main()

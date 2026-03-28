"""Create a Notion database from a JSON schema definition."""

import json
import os
import sys

import requests

NOTION_API_URL = "https://api.notion.com/v1/databases"
NOTION_VERSION = "2022-06-28"


def build_database_payload(schema: dict, parent_page_id: str) -> dict:
    """Build the Notion API payload from the schema definition."""
    properties = {}
    for name, prop_def in schema["properties"].items():
        prop_type = prop_def["type"]
        # For the payload, we send everything except the "type" key
        prop_body = {k: v for k, v in prop_def.items() if k != "type"}
        properties[name] = prop_body

    return {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [
            {"type": "text", "text": {"content": schema["database_name"]}}
        ],
        "properties": properties,
    }


def create_notion_database(schema: dict, parent_page_id: str, api_key: str) -> dict:
    """Create a Notion database via the API and return the response JSON."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    payload = build_database_payload(schema, parent_page_id)
    response = requests.post(NOTION_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def main():
    api_key = os.environ.get("NOTION_API_KEY")
    parent_page_id = os.environ.get("NOTION_PARENT_PAGE_ID")

    if not api_key or not parent_page_id:
        print("Error: Set NOTION_API_KEY and NOTION_PARENT_PAGE_ID environment variables.")
        sys.exit(1)

    schema_path = os.path.join(os.path.dirname(__file__), "notion_schema.json")
    with open(schema_path) as f:
        schema = json.load(f)

    result = create_notion_database(schema, parent_page_id, api_key)
    print(f"Database created successfully! ID: {result['id']}")


if __name__ == "__main__":
    main()

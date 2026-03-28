"""Tests for notion_setup.py - Notion database creation from schema."""

import json
from unittest.mock import MagicMock, patch

import pytest

from notion_setup import build_database_payload, create_database, load_schema


@pytest.fixture
def schema():
    with open("notion_schema.json") as f:
        return json.load(f)


@pytest.fixture
def mock_successful_response():
    """Simulates a successful Notion API response for database creation."""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "object": "database",
        "id": "abc123-fake-db-id",
        "title": [{"text": {"content": "Personal Productivity Hub"}}],
        "url": "https://www.notion.so/abc123fakeid",
        "properties": {
            "Name": {"id": "title", "type": "title", "title": {}},
            "Status": {"id": "s1", "type": "select", "select": {"options": [
                {"name": "Not Started", "color": "gray"},
                {"name": "In Progress", "color": "blue"},
                {"name": "Completed", "color": "green"},
                {"name": "Blocked", "color": "red"},
                {"name": "Archived", "color": "default"},
            ]}},
            "Priority": {"id": "p1", "type": "select", "select": {"options": [
                {"name": "P0 - Critical", "color": "red"},
                {"name": "P1 - High", "color": "orange"},
                {"name": "P2 - Medium", "color": "yellow"},
                {"name": "P3 - Low", "color": "gray"},
            ]}},
            "Category": {"id": "c1", "type": "select", "select": {}},
            "Tags": {"id": "t1", "type": "multi_select", "multi_select": {}},
            "Due Date": {"id": "d1", "type": "date", "date": {}},
            "Created": {"id": "cr1", "type": "created_time", "created_time": {}},
            "Last Edited": {"id": "le1", "type": "last_edited_time", "last_edited_time": {}},
            "Notes": {"id": "n1", "type": "rich_text", "rich_text": {}},
            "Energy Level": {"id": "e1", "type": "select", "select": {}},
            "Done": {"id": "dn1", "type": "checkbox", "checkbox": {}},
        },
    }
    return response


class TestLoadSchema:
    def test_loads_valid_schema(self):
        schema = load_schema("notion_schema.json")
        assert schema["database_name"] == "Personal Productivity Hub"
        assert "properties" in schema

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_schema("nonexistent.json")


class TestBuildDatabasePayload:
    def test_payload_has_parent_page(self, schema):
        page_id = "test-page-id-123"
        payload = build_database_payload(schema, page_id)
        assert payload["parent"] == {"type": "page_id", "page_id": page_id}

    def test_payload_has_title(self, schema):
        payload = build_database_payload(schema, "test-page-id")
        title_text = payload["title"][0]["text"]["content"]
        assert title_text == "Personal Productivity Hub"

    def test_payload_has_all_properties(self, schema):
        payload = build_database_payload(schema, "test-page-id")
        props = payload["properties"]
        expected_props = set(schema["properties"].keys())
        assert set(props.keys()) == expected_props

    def test_title_property(self, schema):
        payload = build_database_payload(schema, "test-page-id")
        assert payload["properties"]["Name"] == {"title": {}}

    def test_select_property_with_options(self, schema):
        payload = build_database_payload(schema, "test-page-id")
        status = payload["properties"]["Status"]
        assert status["select"]["options"][0]["name"] == "Not Started"
        assert len(status["select"]["options"]) == 5

    def test_multi_select_property(self, schema):
        payload = build_database_payload(schema, "test-page-id")
        tags = payload["properties"]["Tags"]
        assert "multi_select" in tags
        assert len(tags["multi_select"]["options"]) == 5

    def test_date_property(self, schema):
        payload = build_database_payload(schema, "test-page-id")
        assert payload["properties"]["Due Date"] == {"date": {}}

    def test_created_time_property(self, schema):
        payload = build_database_payload(schema, "test-page-id")
        assert payload["properties"]["Created"] == {"created_time": {}}

    def test_last_edited_time_property(self, schema):
        payload = build_database_payload(schema, "test-page-id")
        assert payload["properties"]["Last Edited"] == {"last_edited_time": {}}

    def test_rich_text_property(self, schema):
        payload = build_database_payload(schema, "test-page-id")
        assert payload["properties"]["Notes"] == {"rich_text": {}}

    def test_checkbox_property(self, schema):
        payload = build_database_payload(schema, "test-page-id")
        assert payload["properties"]["Done"] == {"checkbox": {}}


class TestCreateDatabase:
    @patch("notion_setup.requests.post")
    def test_creates_database_successfully(self, mock_post, schema, mock_successful_response):
        mock_post.return_value = mock_successful_response

        result = create_database(
            schema, page_id="parent-page-id", api_key="fake-api-key"
        )

        assert result["id"] == "abc123-fake-db-id"
        assert result["object"] == "database"

        # Verify the API was called with correct URL and headers
        call_args = mock_post.call_args
        assert call_args[0][0] == "https://api.notion.com/v1/databases"
        headers = call_args[1]["headers"]
        assert headers["Authorization"] == "Bearer fake-api-key"
        assert headers["Notion-Version"] == "2022-06-28"

    @patch("notion_setup.requests.post")
    def test_sends_correct_payload(self, mock_post, schema, mock_successful_response):
        mock_post.return_value = mock_successful_response

        create_database(schema, page_id="parent-page-id", api_key="fake-api-key")

        payload = mock_post.call_args[1]["json"]
        assert payload["parent"]["page_id"] == "parent-page-id"
        assert payload["title"][0]["text"]["content"] == "Personal Productivity Hub"
        assert "Status" in payload["properties"]
        assert "Priority" in payload["properties"]
        assert "Tags" in payload["properties"]
        assert "Done" in payload["properties"]

    @patch("notion_setup.requests.post")
    def test_raises_on_api_error(self, mock_post, schema):
        error_response = MagicMock()
        error_response.status_code = 401
        error_response.text = "Unauthorized"
        error_response.raise_for_status.side_effect = Exception(
            "401 Unauthorized"
        )
        mock_post.return_value = error_response

        with pytest.raises(Exception, match="401|Unauthorized|failed"):
            create_database(
                schema, page_id="parent-page-id", api_key="bad-key"
            )

    @patch("notion_setup.requests.post")
    def test_all_schema_properties_in_api_call(self, mock_post, schema, mock_successful_response):
        """Ensure every property from the schema ends up in the API payload."""
        mock_post.return_value = mock_successful_response

        create_database(schema, page_id="pid", api_key="key")

        payload = mock_post.call_args[1]["json"]
        for prop_name in schema["properties"]:
            assert prop_name in payload["properties"], (
                f"Property '{prop_name}' from schema missing in API payload"
            )

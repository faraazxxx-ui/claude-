"""Tests for notion_setup.py - Notion database creation from schema."""

import json
from unittest.mock import MagicMock, patch

import pytest

from notion_setup import (
    NotionSetupError,
    build_database_payload,
    create_database,
    load_schema,
    verify_database_matches_schema,
)


@pytest.fixture
def schema():
    with open("notion_schema.json") as f:
        return json.load(f)


def _build_mock_response(schema):
    """Build a realistic Notion API response directly from the schema.

    This ensures the mock never drifts from the schema definition.
    """
    properties = {}
    for name, defn in schema["properties"].items():
        prop_type = defn["type"]
        prop = {"id": name[:4], "type": prop_type}
        if prop_type in ("select", "multi_select") and "options" in defn:
            prop[prop_type] = {"options": [
                {"id": f"opt-{i}", "name": opt["name"], "color": opt["color"]}
                for i, opt in enumerate(defn["options"])
            ]}
        else:
            prop[prop_type] = {}
        properties[name] = prop

    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "object": "database",
        "id": "abc123-fake-db-id",
        "title": [{"text": {"content": schema["database_name"]}}],
        "description": [{"text": {"content": schema.get("description", "")}}],
        "url": "https://www.notion.so/abc123fakeid",
        "properties": properties,
    }
    return response


@pytest.fixture
def mock_successful_response(schema):
    return _build_mock_response(schema)


# ---------------------------------------------------------------------------
# load_schema
# ---------------------------------------------------------------------------


class TestLoadSchema:
    def test_loads_valid_schema(self):
        schema = load_schema("notion_schema.json")
        assert schema["database_name"] == "Personal Productivity Hub"
        assert "properties" in schema
        assert len(schema["properties"]) == 11

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_schema("nonexistent.json")

    def test_raises_on_missing_database_name(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({"properties": {"X": {"type": "title"}}}))
        with pytest.raises(ValueError, match="database_name"):
            load_schema(str(bad))

    def test_raises_on_missing_properties(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({"database_name": "Test"}))
        with pytest.raises(ValueError, match="properties"):
            load_schema(str(bad))


# ---------------------------------------------------------------------------
# build_database_payload
# ---------------------------------------------------------------------------


class TestBuildDatabasePayload:
    def test_parent_page(self, schema):
        payload = build_database_payload(schema, "page-123")
        assert payload["parent"] == {"type": "page_id", "page_id": "page-123"}

    def test_title(self, schema):
        payload = build_database_payload(schema, "p")
        assert payload["title"][0]["text"]["content"] == "Personal Productivity Hub"

    def test_description_included(self, schema):
        payload = build_database_payload(schema, "p")
        assert payload["description"][0]["text"]["content"] == schema["description"]

    def test_all_schema_properties_present(self, schema):
        payload = build_database_payload(schema, "p")
        assert set(payload["properties"].keys()) == set(schema["properties"].keys())

    def test_title_property(self, schema):
        payload = build_database_payload(schema, "p")
        assert payload["properties"]["Name"] == {"title": {}}

    def test_select_options_fully_mapped(self, schema):
        """Every select option name AND color must appear in the payload."""
        payload = build_database_payload(schema, "p")
        for prop_name, defn in schema["properties"].items():
            if defn["type"] == "select" and "options" in defn:
                payload_opts = payload["properties"][prop_name]["select"]["options"]
                for expected in defn["options"]:
                    match = [o for o in payload_opts
                             if o["name"] == expected["name"]
                             and o["color"] == expected["color"]]
                    assert match, (
                        f"{prop_name}: option {expected} not found in payload"
                    )

    def test_multi_select_options_fully_mapped(self, schema):
        payload = build_database_payload(schema, "p")
        tags_opts = payload["properties"]["Tags"]["multi_select"]["options"]
        schema_opts = schema["properties"]["Tags"]["options"]
        assert len(tags_opts) == len(schema_opts)
        for expected in schema_opts:
            match = [o for o in tags_opts
                     if o["name"] == expected["name"]
                     and o["color"] == expected["color"]]
            assert match, f"Tag option {expected} not found in payload"

    def test_simple_types(self, schema):
        payload = build_database_payload(schema, "p")
        assert payload["properties"]["Due Date"] == {"date": {}}
        assert payload["properties"]["Created"] == {"created_time": {}}
        assert payload["properties"]["Last Edited"] == {"last_edited_time": {}}
        assert payload["properties"]["Notes"] == {"rich_text": {}}
        assert payload["properties"]["Done"] == {"checkbox": {}}

    def test_rejects_unsupported_type(self):
        bad_schema = {
            "database_name": "Test",
            "properties": {"X": {"type": "invalid_type"}},
        }
        with pytest.raises(ValueError, match="Unsupported property type"):
            build_database_payload(bad_schema, "p")


# ---------------------------------------------------------------------------
# create_database
# ---------------------------------------------------------------------------


class TestCreateDatabase:
    @patch("notion_setup.requests.post")
    def test_returns_database_on_success(self, mock_post, schema, mock_successful_response):
        mock_post.return_value = mock_successful_response
        result = create_database(schema, page_id="pid", api_key="key")
        assert result["object"] == "database"
        assert result["id"] == "abc123-fake-db-id"

    @patch("notion_setup.requests.post")
    def test_calls_correct_endpoint_and_headers(self, mock_post, schema, mock_successful_response):
        mock_post.return_value = mock_successful_response
        create_database(schema, page_id="pid", api_key="my-secret-key")

        args, kwargs = mock_post.call_args
        assert args[0] == "https://api.notion.com/v1/databases"
        assert kwargs["headers"]["Authorization"] == "Bearer my-secret-key"
        assert kwargs["headers"]["Notion-Version"] == "2022-06-28"

    @patch("notion_setup.requests.post")
    def test_payload_matches_schema(self, mock_post, schema, mock_successful_response):
        """The payload sent to the API must contain every schema property."""
        mock_post.return_value = mock_successful_response
        create_database(schema, page_id="pid", api_key="key")

        payload = mock_post.call_args[1]["json"]
        for prop_name, defn in schema["properties"].items():
            assert prop_name in payload["properties"], (
                f"'{prop_name}' missing from API payload"
            )
            prop_type = defn["type"]
            assert prop_type in payload["properties"][prop_name], (
                f"'{prop_name}' should have key '{prop_type}'"
            )

    @patch("notion_setup.requests.post")
    def test_raises_notion_setup_error_on_failure(self, mock_post, schema):
        error_resp = MagicMock()
        error_resp.status_code = 401
        error_resp.text = '{"message":"API token is invalid."}'
        mock_post.return_value = error_resp

        with pytest.raises(NotionSetupError, match="401"):
            create_database(schema, page_id="pid", api_key="bad-key")


# ---------------------------------------------------------------------------
# verify_database_matches_schema (end-to-end correctness check)
# ---------------------------------------------------------------------------


class TestVerifyDatabaseMatchesSchema:
    def test_passes_when_response_matches_schema(self, schema, mock_successful_response):
        db_response = mock_successful_response.json()
        verify_database_matches_schema(db_response, schema)

    def test_fails_on_missing_property(self, schema, mock_successful_response):
        db_response = mock_successful_response.json()
        del db_response["properties"]["Status"]
        with pytest.raises(NotionSetupError, match="Status.*missing"):
            verify_database_matches_schema(db_response, schema)

    def test_fails_on_wrong_type(self, schema, mock_successful_response):
        db_response = mock_successful_response.json()
        db_response["properties"]["Done"]["type"] = "rich_text"
        with pytest.raises(NotionSetupError, match="Done.*expected.*checkbox.*got.*rich_text"):
            verify_database_matches_schema(db_response, schema)

    def test_passes_for_every_property_type(self, schema, mock_successful_response):
        """Confirm verify checks ALL 11 properties, not just a subset."""
        db_response = mock_successful_response.json()
        assert len(db_response["properties"]) == len(schema["properties"])
        verify_database_matches_schema(db_response, schema)

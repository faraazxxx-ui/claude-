import json
import os
from unittest.mock import MagicMock, patch

import pytest

from notion_setup import create_notion_database, build_database_payload

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "notion_schema.json")


@pytest.fixture
def schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


@pytest.fixture
def fake_parent_page_id():
    return "aabbccdd-1234-5678-9999-000000000000"


class TestBuildDatabasePayload:
    """Tests that the API payload is built correctly from the schema."""

    def test_payload_has_parent(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        assert payload["parent"] == {"type": "page_id", "page_id": fake_parent_page_id}

    def test_payload_has_title(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        assert payload["title"] == [
            {"type": "text", "text": {"content": "Personal Productivity"}}
        ]

    def test_payload_contains_all_properties(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        expected_props = set(schema["properties"].keys())
        assert set(payload["properties"].keys()) == expected_props

    def test_title_property(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        assert payload["properties"]["Name"] == {"title": {}}

    def test_select_property_with_options(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        status_prop = payload["properties"]["Status"]
        assert "select" in status_prop
        option_names = [o["name"] for o in status_prop["select"]["options"]]
        assert option_names == ["Not Started", "In Progress", "Done"]

    def test_multi_select_property(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        tags_prop = payload["properties"]["Tags"]
        assert "multi_select" in tags_prop
        option_names = [o["name"] for o in tags_prop["multi_select"]["options"]]
        assert "Work" in option_names
        assert "Personal" in option_names
        assert len(option_names) == 5

    def test_date_property(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        assert payload["properties"]["Due Date"] == {"date": {}}

    def test_checkbox_property(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        assert payload["properties"]["Completed"] == {"checkbox": {}}

    def test_number_property(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        assert payload["properties"]["Effort"] == {"number": {"format": "number"}}

    def test_rich_text_property(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        assert payload["properties"]["Notes"] == {"rich_text": {}}

    def test_url_property(self, schema, fake_parent_page_id):
        payload = build_database_payload(schema, fake_parent_page_id)
        assert payload["properties"]["URL"] == {"url": {}}


class TestCreateNotionDatabase:
    """Tests that the Notion API is called correctly and the response is handled."""

    @patch("notion_setup.requests.post")
    def test_calls_notion_api_with_correct_url(self, mock_post, schema, fake_parent_page_id):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"id": "new-db-id", "title": [{"text": {"content": "Personal Productivity"}}]}),
        )
        create_notion_database(schema, fake_parent_page_id, api_key="fake-key")
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == "https://api.notion.com/v1/databases"

    @patch("notion_setup.requests.post")
    def test_sends_correct_headers(self, mock_post, schema, fake_parent_page_id):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"id": "new-db-id"}),
        )
        create_notion_database(schema, fake_parent_page_id, api_key="fake-key")
        headers = mock_post.call_args[1]["headers"]
        assert headers["Authorization"] == "Bearer fake-key"
        assert headers["Notion-Version"] == "2022-06-28"
        assert headers["Content-Type"] == "application/json"

    @patch("notion_setup.requests.post")
    def test_sends_correct_payload(self, mock_post, schema, fake_parent_page_id):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"id": "new-db-id"}),
        )
        create_notion_database(schema, fake_parent_page_id, api_key="fake-key")
        sent_payload = mock_post.call_args[1]["json"]
        assert sent_payload["parent"]["page_id"] == fake_parent_page_id
        assert "Name" in sent_payload["properties"]

    @patch("notion_setup.requests.post")
    def test_returns_database_id_on_success(self, mock_post, schema, fake_parent_page_id):
        mock_post.return_value = MagicMock(
            status_code=200,
            json=MagicMock(return_value={"id": "new-db-id"}),
        )
        result = create_notion_database(schema, fake_parent_page_id, api_key="fake-key")
        assert result["id"] == "new-db-id"

    @patch("notion_setup.requests.post")
    def test_raises_on_api_error(self, mock_post, schema, fake_parent_page_id):
        mock_post.return_value = MagicMock(
            status_code=400,
            text="Bad Request",
            json=MagicMock(return_value={"message": "Invalid request"}),
        )
        mock_post.return_value.raise_for_status.side_effect = Exception("400 Bad Request")
        with pytest.raises(Exception, match="400 Bad Request"):
            create_notion_database(schema, fake_parent_page_id, api_key="fake-key")

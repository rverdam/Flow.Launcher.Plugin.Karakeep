import pytest

from plugin.karakeep import KarakeepAPI
from plugin.results import query_result, query_results


class DummySettings(dict):
    def get(self, key, default=None):
        if key == "karakeepBaseAddress":
            return "https://karakeep.example"
        return super().get(key, default)


def test_link_result_allows_null_description(monkeypatch):
    monkeypatch.setattr("plugin.results.settings", lambda: DummySettings())
    item = {
        "id": "bookmark-id",
        "content": {
            "type": "link",
            "url": "https://example.com/article",
            "title": "Example Article",
            "description": None,
            "imageUrl": None,
        },
    }

    result = query_result(item).as_dict()

    assert result["Title"] == "Example Article"
    assert result["SubTitle"] == ""
    assert result["JsonRPCAction"]["parameters"][0] == "https://example.com/article"


def test_link_result_uses_url_when_title_is_null(monkeypatch):
    monkeypatch.setattr("plugin.results.settings", lambda: DummySettings())
    item = {
        "id": "bookmark-id",
        "content": {
            "type": "link",
            "url": "https://example.com/no-title",
            "title": None,
            "description": "Tom &amp; Jerry",
            "imageUrl": None,
        },
    }

    result = query_result(item).as_dict()

    assert result["Title"] == "https://example.com/no-title"
    assert result["SubTitle"] == "Tom & Jerry"


def test_query_results_skips_items_without_supported_content():
    class FakeKarakeep:
        def search_bookmarks(self, query):
            assert query == "needle"
            return [
                {"id": "missing-content", "content": None},
                {"id": "asset", "content": {"type": "asset"}},
                {"id": "link", "content": {"type": "link", "url": "https://example.com", "title": "Example", "description": None}},
            ]

    results = [result.as_dict() for result in query_results(FakeKarakeep(), "needle")]

    assert [result["Title"] for result in results] == ["Example"]


class FakeResponse:
    status_code = 200

    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload

    def raise_for_status(self):
        raise AssertionError("raise_for_status should not be called for 200 responses")


def test_search_bookmarks_returns_empty_list_when_response_has_no_bookmarks(monkeypatch):
    api = KarakeepAPI("https://karakeep.example", "secret")
    monkeypatch.setattr("plugin.karakeep.requests.get", lambda *args, **kwargs: FakeResponse({}))

    assert api.search_bookmarks("needle") == []


def test_search_bookmarks_sends_bearer_token_and_query(monkeypatch):
    requests = []

    def fake_get(url, **kwargs):
        requests.append((url, kwargs))
        return FakeResponse({"bookmarks": []})

    api = KarakeepAPI("https://karakeep.example/", "secret")
    monkeypatch.setattr("plugin.karakeep.requests.get", fake_get)

    api.search_bookmarks("needle")

    assert requests == [
        (
            "https://karakeep.example/api/v1/bookmarks/search",
            {
                "headers": {"Authorization": "Bearer secret"},
                "params": {"q": "needle"},
                "timeout": 10,
            },
        )
    ]

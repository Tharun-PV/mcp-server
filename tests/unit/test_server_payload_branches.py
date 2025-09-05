import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with API key."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def complex_list_works_arguments():
    """Complex arguments for list_works testing."""
    return {
        "type": ["issue", "ticket"],
        "cursor": {"next_cursor": "abc", "mode": "after"},
        "applies_to_part": ["part_1"],
        "created_by": ["user_1"],
        "modified_by": ["user_2"],
        "owned_by": ["user_3"],
        "state": ["open"],
        "custom_fields": [{"name": "field", "value": ["val"]}],
        "sla_summary": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "sort_by": ["created_date:asc"],
        "rev_orgs": ["org_1"],
        "subtype": ["bug"],
        "target_close_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "target_start_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "actual_close_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "actual_start_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "created_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "modified_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "sprint": ["sprint_1"]
    }


@pytest.fixture
def complex_list_parts_arguments():
    """Complex arguments for list_parts testing."""
    return {
        "type": "enhancement",
        "cursor": {"next_cursor": "abc", "mode": "after"},
        "owned_by": ["user_1"],
        "parent_part": ["parent_1"],
        "created_by": ["user_2"],
        "modified_by": ["user_3"],
        "sort_by": ["created_date:asc"],
        "accounts": ["acc_1"],
        "target_close_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "target_start_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "actual_close_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "actual_start_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"}
    }


@responses.activate
@pytest.mark.asyncio
async def test_list_works_complex_payload(complex_list_works_arguments):
    """Test list_works with complex payload including all optional fields."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.list",
        json={"works": []},
        status=200
    )
    result = await server.handle_call_tool(name="list_works", arguments=complex_list_works_arguments)
    assert any("Works listed successfully" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_list_parts_complex_payload(complex_list_parts_arguments):
    """Test list_parts with complex payload including all optional fields."""
    responses.add(
        responses.POST,
        "https://api.devrev.ai/parts.list",
        json={"parts": []},
        status=200
    )
    result = await server.handle_call_tool(name="list_parts", arguments=complex_list_parts_arguments)
    assert any("Parts listed successfully" in c.text for c in result)

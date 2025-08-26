import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_list_works_payload_branches(monkeypatch):
    # Covers payload construction for list_works with all optional fields
    class Resp:
        status_code = 200

        def json(self):
            return {"works": []}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    arguments = {
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
    result = await server.handle_call_tool(name="list_works", arguments=arguments)
    assert any("Works listed successfully" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_list_parts_payload_branches(monkeypatch):
    # Covers payload construction for list_parts with all optional fields
    class Resp:
        status_code = 200

        def json(self):
            return {"parts": []}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    arguments = {
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
    result = await server.handle_call_tool(name="list_parts", arguments=arguments)
    assert any("Parts listed successfully" in c.text for c in result)

import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_list_meetings_payload_branches(monkeypatch):
    # Covers payload construction for list_meetings with all optional fields
    class Resp:
        status_code = 200

        def json(self):
            return {"meetings": []}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    arguments = {
        "channel": ["zoom"],
        "created_by": ["user_1"],
        "created_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "cursor": {"next_cursor": "abc", "mode": "after"},
        "ended_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "external_ref": ["ref_1"],
        "limit": 10,
        "members": ["member_1"],
        "modified_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "organizer": ["org_1"],
        "scheduled_date": {"after": "2025-01-01T00:00:00Z", "before": "2025-12-31T00:00:00Z"},
        "sort_by": ["created_date:asc"],
        "state": ["scheduled"]
    }
    result = await server.handle_call_tool(name="list_meetings", arguments=arguments)
    assert any("Meetings listed successfully" in c.text for c in result)

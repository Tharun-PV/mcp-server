import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_update_part_all_fields(monkeypatch):
    # Covers all optional fields for update_part
    class Resp:
        status_code = 200

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    arguments = {
        "id": "part_1",
        "type": "enhancement",
        "name": "name",
        "owned_by": ["user_1"],
        "description": "desc",
        "target_close_date": "2025-12-31T00:00:00Z",
        "target_start_date": "2025-01-01T00:00:00Z",
        "stage": "Ready"
    }
    result = await server.handle_call_tool(name="update_part", arguments=arguments)
    assert any("Part updated successfully" in c.text for c in result)

import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_get_sprints_state_default(monkeypatch):
    # Covers get_sprints with no state provided (should default to 'active')
    class Resp:
        status_code = 200

        def json(self):
            return {"vista_group": ["sprint_1"]}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    arguments = {"ancestor_part_id": "part_1"}
    result = await server.handle_call_tool(name="get_sprints", arguments=arguments)
    assert any("Sprints for 'part_1'" in c.text for c in result)

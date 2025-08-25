import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_get_sprints_error(monkeypatch):
    # Simulate error response for get_sprints
    class Resp:
        status_code = 500
        text = "Internal Error"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="get_sprints", arguments={"ancestor_part_id": "part_1"})
    assert any("Get sprints failed with status 500" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_list_subtypes_error(monkeypatch):
    # Simulate error response for list_subtypes
    class Resp:
        status_code = 404
        text = "Not Found"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="list_subtypes", arguments={"leaf_type": "issue"})
    assert any("List subtypes failed with status 404" in c.text for c in result)

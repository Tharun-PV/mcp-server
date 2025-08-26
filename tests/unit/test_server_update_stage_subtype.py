import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_update_work_stage(monkeypatch):
    # Simulate updating work with stage
    class Resp:
        status_code = 200

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="update_work", arguments={
        "id": "work_1", "type": "issue", "stage": "In Progress"})
    # Should return success message
    assert any("Object updated successfully" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_update_part_stage(monkeypatch):
    # Simulate updating part with stage
    class Resp:
        status_code = 200

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="update_part", arguments={
        "id": "part_1", "type": "enhancement", "stage": "Ready"})
    # Should return success message
    assert any("Part updated successfully" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_update_work_subtype(monkeypatch):
    # Simulate updating work with subtype
    class Resp:
        status_code = 200

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="update_work", arguments={
        "id": "work_1", "type": "issue", "subtype": {"drop": False, "subtype": "bug"}})
    # Should return success message
    assert any("Object updated successfully" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_update_work_subtype_drop(monkeypatch):
    # Simulate updating work with subtype drop
    class Resp:
        status_code = 200

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="update_work", arguments={
        "id": "work_1", "type": "issue", "subtype": {"drop": True}})
    # Should return success message
    assert any("Object updated successfully" in c.text for c in result)

import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_update_work_all_fields(monkeypatch):
    # Covers all optional fields for update_work
    class Resp:
        status_code = 200

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    arguments = {
        "id": "work_1",
        "type": "issue",
        "title": "title",
        "body": "body",
        "modified_by": ["user_1"],
        "owned_by": ["user_2"],
        "applies_to_part": ["part_1"],
        "stage": "In Progress",
        "sprint": "sprint_1",
        "subtype": {"drop": False, "subtype": "bug"}
    }
    result = await server.handle_call_tool(name="update_work", arguments=arguments)
    assert any("Object updated successfully" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_update_work_subtype_drop(monkeypatch):
    # Covers subtype drop branch for update_work
    class Resp:
        status_code = 200

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    arguments = {
        "id": "work_1",
        "type": "issue",
        "subtype": {"drop": True}
    }
    result = await server.handle_call_tool(name="update_work", arguments=arguments)
    assert any("Object updated successfully" in c.text for c in result)

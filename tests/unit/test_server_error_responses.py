import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_get_current_user_error(monkeypatch):
    # Simulate error response for get_current_user
    class Resp:
        status_code = 400
        text = "Unauthorized"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="get_current_user", arguments={})
    assert any("Get current user failed with status 400" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_get_vista_error(monkeypatch):
    # Simulate error response for get_vista
    class Resp:
        status_code = 404
        text = "Not Found"

        def json(self):
            return {}
    monkeypatch.setattr(
        server, "make_internal_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="get_vista", arguments={"id": "vista_1"})
    assert any("get_vista failed with status 404" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_search_error(monkeypatch):
    # Simulate error response for search
    class Resp:
        status_code = 500
        text = "Internal Error"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="search", arguments={"query": "foo", "namespace": "issue"})
    assert any("Search failed with status 500" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_get_work_error(monkeypatch):
    # Simulate error response for get_work
    class Resp:
        status_code = 404
        text = "Not Found"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="get_work", arguments={"id": "work_1"})
    assert any("Get object failed with status 404" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_create_work_error(monkeypatch):
    # Simulate error response for create_work
    class Resp:
        status_code = 400
        text = "Bad Request"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="create_work", arguments={"type": "issue", "title": "t", "applies_to_part": "p"})
    assert any("Create object failed with status 400" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_update_work_error(monkeypatch):
    # Simulate error response for update_work
    class Resp:
        status_code = 400
        text = "Bad Request"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="update_work", arguments={"id": "work_1", "type": "issue"})
    assert any("Update object failed with status 400" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_list_works_error(monkeypatch):
    # Simulate error response for list_works
    class Resp:
        status_code = 500
        text = "Internal Error"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="list_works", arguments={"type": ["issue"]})
    assert any("List works failed with status 500" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_get_part_error(monkeypatch):
    # Simulate error response for get_part
    class Resp:
        status_code = 404
        text = "Not Found"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="get_part", arguments={"id": "part_1"})
    assert any("Get part failed with status 404" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_create_part_error(monkeypatch):
    # Simulate error response for create_part
    class Resp:
        status_code = 400
        text = "Bad Request"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="create_part", arguments={"type": "enhancement", "name": "n", "owned_by": ["u"], "parent_part": ["p"]})
    assert any("Create part failed with status 400" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_update_part_error(monkeypatch):
    # Simulate error response for update_part
    class Resp:
        status_code = 400
        text = "Bad Request"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="update_part", arguments={"id": "part_1", "type": "enhancement"})
    assert any("Update part failed with status 400" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_list_parts_error(monkeypatch):
    # Simulate error response for list_parts
    class Resp:
        status_code = 500
        text = "Internal Error"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="list_parts", arguments={"type": "enhancement"})
    assert any("List parts failed with status 500" in c.text for c in result)

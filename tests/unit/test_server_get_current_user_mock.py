import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_get_current_user_mock(monkeypatch):
    # Mock the DevRev API response for get_current_user
    class MockResponse:
        status_code = 200
        text = '{"user": "mocked_user"}'

        def json(self):
            return {"user": "mocked_user"}
    monkeypatch.setattr(server, "make_devrev_request",
                        lambda *a, **kw: MockResponse())
    result = await server.handle_call_tool(name="get_current_user", arguments={})
    assert any("mocked_user" in c.text for c in result)

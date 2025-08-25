import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_get_work_success():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.get",
        json={"work": {"id": "work_1", "title": "Test Work"}},
        status=200
    )
    result = await server.handle_call_tool(
        name="get_work",
        arguments={"id": "work_1"}
    )
    assert any("Object information for 'work_1'" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_get_work_error():
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.get",
        json={"error": "Not found"},
        status=404
    )
    result = await server.handle_call_tool(
        name="get_work",
        arguments={"id": "work_1"}
    )
    assert any("Get object failed with status 404" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_get_work_missing_args():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="get_work", arguments=None)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_get_work_missing_id():
    with pytest.raises(ValueError, match="Missing arguments"):
        await server.handle_call_tool(name="get_work", arguments={})

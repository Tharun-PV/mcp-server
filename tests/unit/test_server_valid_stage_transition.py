import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_valid_stage_transition_success(monkeypatch):
    # Mock make_devrev_request to simulate all API calls
    def mock_make_devrev_request(endpoint, payload):
        if endpoint == "works.get":
            return type("Resp", (), {
                "status_code": 200,
                "json": lambda self: {"work": {"stage": {"stage": {"id": "stage_1"}}, "type": "issue", "subtype": "subtype_1"}},
                "text": '{"work": {"stage": {"stage": {"id": "stage_1"}}, "type": "issue", "subtype": "subtype_1"}}'
            })()
        elif endpoint == "schemas.aggregated.get":
            return type("Resp", (), {
                "status_code": 200,
                "json": lambda self: {"schema": {"stage_diagram_id": {"id": "diagram_1"}}},
                "text": '{"schema": {"stage_diagram_id": {"id": "diagram_1"}}}'
            })()
        elif endpoint == "stage-diagrams.get":
            return type("Resp", (), {
                "status_code": 200,
                "json": lambda self: {"stage_diagram": {"stages": [{"stage": {"id": "stage_1"}, "transitions": ["to_stage_2"]}]}},
                "text": '{"stage_diagram": {"stages": [{"stage": {"id": "stage_1"}, "transitions": ["to_stage_2"]}]}}'
            })()
        return type("Resp", (), {
            "status_code": 404,
            "json": lambda self: {},
            "text": ""
        })()
    monkeypatch.setattr(server, "make_devrev_request",
                        mock_make_devrev_request)
    result = await server.handle_call_tool(
        name="valid_stage_transition",
        arguments={"type": "issue", "id": "work_1"}
    )
    assert any("Valid Transitions for 'work_1'" in c.text for c in result)


@responses.activate
@pytest.mark.asyncio
async def test_handle_call_tool_valid_stage_transition_error(monkeypatch):
    def mock_make_devrev_request(endpoint, payload):
        return type("Resp", (), {
            "status_code": 404,
            "json": lambda self: {},
            "text": "Not Found"
        })()
    monkeypatch.setattr(server, "make_devrev_request",
                        mock_make_devrev_request)
    result = await server.handle_call_tool(
        name="valid_stage_transition",
        arguments={"type": "issue", "id": "work_1"}
    )
    assert any("Get work item failed with status 404" in c.text for c in result)

import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_list_meetings_error(monkeypatch):
    # Simulate error response for list_meetings
    class Resp:
        status_code = 500
        text = "Internal Error"

        def json(self):
            return {}
    monkeypatch.setattr(server, "make_devrev_request", lambda *a, **kw: Resp())
    result = await server.handle_call_tool(name="list_meetings", arguments={})
    assert any("List meetings failed with status 500" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_valid_stage_transition_schema_error(monkeypatch):
    # Simulate error response for schemas.aggregated.get
    def mock_make_devrev_request(endpoint, payload):
        if endpoint == "works.get":
            class Resp:
                status_code = 200

                def json(self):
                    return {"work": {"stage": {"stage": {"id": "stage_1"}}, "type": "issue", "subtype": "subtype_1"}}
            return Resp()
        elif endpoint == "schemas.aggregated.get":
            class Resp:
                status_code = 500
                text = "Schema Error"

                def json(self):
                    return {}
            return Resp()
        return None
    monkeypatch.setattr(server, "make_devrev_request",
                        mock_make_devrev_request)
    result = await server.handle_call_tool(name="valid_stage_transition", arguments={"type": "issue", "id": "work_1"})
    assert any("Get schema failed with status 500" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_valid_stage_transition_stage_diagram_error(monkeypatch):
    # Simulate error response for stage-diagrams.get
    def mock_make_devrev_request(endpoint, payload):
        if endpoint == "works.get":
            class Resp:
                status_code = 200

                def json(self):
                    return {"work": {"stage": {"stage": {"id": "stage_1"}}, "type": "issue", "subtype": "subtype_1"}}
            return Resp()
        elif endpoint == "schemas.aggregated.get":
            class Resp:
                status_code = 200

                def json(self):
                    return {"schema": {"stage_diagram_id": {"id": "diagram_1"}}}
            return Resp()
        elif endpoint == "stage-diagrams.get":
            class Resp:
                status_code = 500
                text = "Stage Diagram Error"

                def json(self):
                    return {}
            return Resp()
        return None
    monkeypatch.setattr(server, "make_devrev_request",
                        mock_make_devrev_request)
    result = await server.handle_call_tool(name="valid_stage_transition", arguments={"type": "issue", "id": "work_1"})
    assert any(
        "Get stage diagram for Get stage transitions failed with status 500" in c.text for c in result)


@pytest.mark.asyncio
async def test_handle_call_tool_valid_stage_transition_no_transitions(monkeypatch):
    # Simulate no valid transitions found
    def mock_make_devrev_request(endpoint, payload):
        if endpoint == "works.get":
            class Resp:
                status_code = 200

                def json(self):
                    return {"work": {"stage": {"stage": {"id": "stage_1"}}, "type": "issue", "subtype": "subtype_1"}}
            return Resp()
        elif endpoint == "schemas.aggregated.get":
            class Resp:
                status_code = 200

                def json(self):
                    return {"schema": {"stage_diagram_id": {"id": "diagram_1"}}}
            return Resp()
        elif endpoint == "stage-diagrams.get":
            class Resp:
                status_code = 200

                def json(self):
                    return {"stage_diagram": {"stages": [{"stage": {"id": "other_stage"}, "transitions": ["to_stage_2"]}]}}
            return Resp()
        return None
    monkeypatch.setattr(server, "make_devrev_request",
                        mock_make_devrev_request)
    result = await server.handle_call_tool(name="valid_stage_transition", arguments={"type": "issue", "id": "work_1"})
    assert any("No valid transitions found for 'work_1'" in c.text for c in result)

import pytest
import responses
from devrev_mcp import server


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    """Set up test environment with required environment variables."""
    monkeypatch.setenv("DEVREV_API_KEY", "test-api-key")


@pytest.fixture
def valid_update_arguments():
    """Provide valid arguments for updating work with all fields."""
    return {
        "id": "work_123",
        "type": "issue",
        "title": "Updated Title",
        "body": "Updated body content",
        "modified_by": ["user_1"],
        "owned_by": ["user_2"],
        "applies_to_part": ["part_1"],
        "stage": "In Progress",
        "sprint": "sprint_1",
        "subtype": {"drop": False, "subtype": "bug"}
    }


@pytest.fixture
def subtype_drop_arguments():
    """Provide arguments for dropping subtype."""
    return {
        "id": "work_123",
        "type": "issue",
        "subtype": {"drop": True}
    }


@responses.activate
@pytest.mark.asyncio
async def test_update_work_all_fields(valid_update_arguments):
    """Test updating work with all optional fields."""
    expected_response = {
        "work": {
            "id": "work_123",
            "title": "Updated Title",
            "type": "issue",
            "stage": "In Progress"
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="update_work",
        arguments=valid_update_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Object updated successfully" in result[0].text


@responses.activate
@pytest.mark.asyncio
async def test_update_work_subtype_drop(subtype_drop_arguments):
    """Test updating work with subtype drop."""
    expected_response = {
        "work": {
            "id": "work_123",
            "type": "issue",
            "subtype": None
        }
    }
    
    responses.add(
        responses.POST,
        "https://api.devrev.ai/works.update",
        json=expected_response,
        status=200
    )

    result = await server.handle_call_tool(
        name="update_work",
        arguments=subtype_drop_arguments
    )

    assert len(result) == 1
    assert result[0].type == "text"
    assert "Object updated successfully" in result[0].text

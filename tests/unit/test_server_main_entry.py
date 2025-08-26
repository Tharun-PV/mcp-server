import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_handle_call_tool_main(monkeypatch):
    # Covers the main async entry point
    class DummyStream:
        async def __aenter__(self):
            return (self, self)

        async def __aexit__(self, exc_type, exc, tb):
            pass

    async def dummy_run(*args, **kwargs):
        return None
    monkeypatch.setattr(server.mcp.server.stdio,
                        "stdio_server", lambda: DummyStream())
    monkeypatch.setattr(server.server, "run", dummy_run)
    await server.main()

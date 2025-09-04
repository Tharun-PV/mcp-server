import pytest
from devrev_mcp import server


@pytest.mark.asyncio
async def test_server_main_entry(monkeypatch):
    """Test the main async entry point."""
    # Mock the stdio server and run function
    class DummyStream:
        async def __aenter__(self):
            return (self, self)

        async def __aexit__(self, exc_type, exc, tb):
            pass

    async def dummy_run(*args, **kwargs):
        return None
    
    monkeypatch.setattr(server.mcp.server.stdio, "stdio_server", lambda: DummyStream())
    monkeypatch.setattr(server.server, "run", dummy_run)
    
    # Should not raise any exceptions
    await server.main()

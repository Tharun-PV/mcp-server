
import subprocess
import sys
import os
import json
import time
from devrev_mcp import utils


def dummy_response(*args, **kwargs):
    class Dummy:
        status_code = 200

        def json(self):
            return {"user": "mocked_user"}
        text = '{"user": "mocked_user"}'
    return Dummy()


def test_mcp_server_protocol(monkeypatch):
    # Patch the utils functions before starting the server
    monkeypatch.setattr(utils, "make_devrev_request", dummy_response)
    monkeypatch.setattr(utils, "make_internal_devrev_request", dummy_response)

    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    proc = subprocess.Popen(
        [sys.executable, "-m", "src.devrev_mcp.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True
    )

    time.sleep(1)

    # Send initialize request
    init_request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "0.4.2",
            "capabilities": {"toolSupport": True},
            "clientInfo": {"name": "integration-test", "version": "1.0"}
        },
        "id": 1
    }
    proc.stdin.write(json.dumps(init_request) + "\n")
    proc.stdin.flush()
    print("Sent initialize request.")
    init_response = proc.stdout.readline()
    print("Initialize response:", init_response)

    # Send tools/call request
    tool_request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_current_user",
            "arguments": {}
        },
        "id": 2
    }
    proc.stdin.write(json.dumps(tool_request) + "\n")
    proc.stdin.flush()
    print("Sent tools/call request.")
    tool_response = proc.stdout.readline()
    print("Tool response:", tool_response)

    proc.terminate()

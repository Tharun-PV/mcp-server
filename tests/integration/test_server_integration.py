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


def test_server_get_current_user_integration(monkeypatch):
    # Patch DevRev API calls
    monkeypatch.setattr(utils, "make_devrev_request", dummy_response)
    monkeypatch.setattr(utils, "make_internal_devrev_request", dummy_response)

    import threading

    proc = subprocess.Popen(
        [sys.executable, "-m", "devrev_mcp.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "DEVREV_API_KEY": "dummy_key", "MCP_TEST_MODE": "1"},
        text=True
    )

    # Ensure the subprocess is killed if it hangs
    import threading

    def kill_proc_after_timeout(p, timeout=10):
        def target():
            try:
                p.wait(timeout=timeout)
            except Exception:
                p.kill()
        t = threading.Thread(target=target)
        t.daemon = True
        t.start()
    kill_proc_after_timeout(proc, timeout=15)

    time.sleep(1)
    print("Server started, sending initialize request...")

    # Send initialize request first
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
    print("Initialize request sent.")
    _ = proc.stdout.readline()

    # Send tools/call request
    tool_request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "get_current_user", "arguments": {}},
        "id": 2
    }
    proc.stdin.write(json.dumps(tool_request) + "\n")
    # Read and print all lines until we get a response to initialize
    for i in range(5):
        line = proc.stdout.readline()
        print(f"[DEBUG] Line {i} after initialize: {line.strip()}")
        if line.strip():
            break
    print("tools/call request sent.")

    output = None

    def read_output():
        nonlocal output
        output = proc.stdout.readline()

    thread = threading.Thread(target=read_output)
    thread.start()
    thread.join(timeout=5)
    if thread.is_alive():
        print("Timeout: No response from server after 5 seconds.")
        # Read and print all lines until we get a response to tools/call
        for i in range(10):
            line = proc.stdout.readline()
            print(f"[DEBUG] Line {i} after tools/call: {line.strip()}")
            if line.strip():
                output = line
                break
    print("Raw output:", output)
    stderr_output = proc.stderr.read()
    print("Stderr output:", stderr_output)
    try:
        response = json.loads(output)
    except Exception as e:
        print(f"JSON decode error: {e}")
        assert False, f"Server did not return valid JSON. Raw output: {output} Stderr: {stderr_output}"

    # Check response structure
    assert "result" in response or "error" in response

    proc.terminate()

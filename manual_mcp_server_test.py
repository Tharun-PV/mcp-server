import subprocess
import sys
import os
import json


def run_manual_mcp_server_test():
    proc = subprocess.Popen(
        [sys.executable, "-m", "devrev_mcp.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "DEVREV_API_KEY": "dummy_key"},
        text=True
    )

    print("Server started. Type JSON-RPC requests below. Type 'exit' to quit.")
    try:
        while True:
            user_input = input("Request> ")
            if user_input.strip().lower() == "exit":
                break
            proc.stdin.write(user_input + "\n")
            # proc.stdin.flush()
            print("Waiting for server response...")
            response = proc.stdout.readline()
            print("Response:", response)
    finally:
        proc.terminate()
        print("Server process terminated.")


if __name__ == "__main__":
    run_manual_mcp_server_test()

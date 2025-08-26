"""
Copyright (c) 2025 DevRev, Inc.
SPDX-License-Identifier: MIT

This module provides utility functions for making authenticated requests to the DevRev API.
"""

import os
import requests
from typing import Any, Dict


def make_devrev_request(endpoint: str, payload: Dict[str, Any]) -> requests.Response:
    """
    Make an authenticated request to the DevRev API.

    Args:
        endpoint: The API endpoint path (e.g., "works.get" or "search.hybrid")
        payload: The JSON payload to send

    Returns:
        requests.Response object

    Raises:
        ValueError: If DEVREV_API_KEY environment variable is not set
    """
    # If MCP_TEST_MODE is set, return a dummy response for integration tests
    if os.environ.get("MCP_TEST_MODE") == "1":
        class DummyResponse:
            """
            A dummy response class that can be used to simulate various response scenarios.
            Different response types can be simulated by setting environment variables:
            - RESPONSE_TYPE=empty: Simulates an empty response body
            - RESPONSE_TYPE=malformed: Simulates a malformed JSON response
            - Any other value: Returns normal mocked response
            """
            status_code = 200

            @property
            def text(self):
                """Return response text based on RESPONSE_TYPE environment variable"""
                response_type = os.environ.get("RESPONSE_TYPE", "normal")
                if response_type == "empty":
                    return ""
                elif response_type == "malformed":
                    return "not a json"
                else:
                    return '{"user": "mocked_user", "result": "ok"}'

            def json(self):
                """Parse JSON from text property or raise JSONDecodeError for malformed/empty responses"""
                import json
                return json.loads(self.text)

        return DummyResponse()

    api_key = os.environ.get("DEVREV_API_KEY")
    if not api_key:
        raise ValueError("DEVREV_API_KEY environment variable is not set")

    headers = {
        "Authorization": f"{api_key}",
        "Content-Type": "application/json",
    }
    return requests.post(
        f"https://api.devrev.ai/{endpoint}",
        headers=headers,
        json=payload
    )


def make_internal_devrev_request(endpoint: str, payload: Dict[str, Any]) -> requests.Response:
    """
    Make an authenticated request to the DevRev API.

    Args:
        endpoint: The API endpoint path (e.g., "works.get" or "search.hybrid")
        payload: The JSON payload to send

    Returns:
        requests.Response object

    Raises:
        ValueError: If DEVREV_API_KEY environment variable is not set
    """
    # If MCP_TEST_MODE is set, return a dummy response for integration tests
    if os.environ.get("MCP_TEST_MODE") == "1":
        class DummyResponse:
            """
            A dummy response class for internal API requests
            """
            status_code = 200

            @property
            def text(self):
                """Return response text based on RESPONSE_TYPE environment variable"""
                response_type = os.environ.get("RESPONSE_TYPE", "normal")
                if response_type == "empty":
                    return ""
                elif response_type == "malformed":
                    return "not a json"
                else:
                    return '{"user": "mocked_user", "result": "internal_ok"}'

            def json(self):
                """Parse JSON from text property or raise JSONDecodeError for malformed/empty responses"""
                import json
                return json.loads(self.text)

        return DummyResponse()

    api_key = os.environ.get("DEVREV_API_KEY")
    if not api_key:
        raise ValueError("DEVREV_API_KEY environment variable is not set")

    headers = {
        "Authorization": f"{api_key}",
        "Content-Type": "application/json",
    }
    return requests.post(
        f"https://api.devrev.ai/internal/{endpoint}",
        headers=headers,
        json=payload
    )

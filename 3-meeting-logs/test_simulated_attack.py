import pytest
from datetime import datetime
import pytz
from simulated_attack import generate_test_strings, check_logs


@pytest.fixture(scope="module")
def test_data():
    """
    Fixture to generate test strings once for all tests
    """
    stage_strings, prod_strings = generate_test_strings(
        5
    )  # Generate 5 strings for each environment
    results = check_logs(stage_strings, prod_strings)
    return {
        "stage_strings": stage_strings,
        "prod_strings": prod_strings,
        "results": results,
    }


def test_initial_requests_return_200(test_data):
    """
    Test that initial HTTP requests to both stage and prod return 200,
    confirming successful URL generation and initial access.
    """
    results = test_data["results"]

    # Check stage responses
    for response in results["stage_responses"]:
        assert response["status_code"] == 200, (
            f"Stage URL {response['url']} returned {response['status_code']} "
            "instead of 200 - URL generation may have failed"
        )

    # Check prod responses
    for response in results["prod_responses"]:
        assert response["status_code"] == 200, (
            f"Prod URL {response['url']} returned {response['status_code']} "
            "instead of 200 - URL generation may have failed"
        )


def test_requests_logged_with_302_redirect(test_data):
    """
    Test that all requests appear in OpenSearch logs with 302 status code,
    confirming proper redirect behavior after initial access.
    """
    results = test_data["results"]

    # Verify we have logs to check
    assert results["opensearch_logs"], "No logs found in OpenSearch"

    # Get all request paths from the initial requests
    all_request_paths = [
        response["url"].split("/")[-1] for response in results["stage_responses"]
    ] + [response["url"].split("/")[-1] for response in results["prod_responses"]]

    # Check each log entry corresponds to our requests and has 302 status
    found_paths = []
    for log in results["opensearch_logs"]:
        request_path = log["request_path"].split("/")[-1]
        if request_path in all_request_paths:
            found_paths.append(request_path)

    # Verify all our requests were found in logs
    missing_paths = set(all_request_paths) - set(found_paths)
    assert not missing_paths, f"Some requests were not found in OpenSearch logs with 302 status: {missing_paths}"


def test_logs_appear_in_opensearch(test_data):
    """
    Test that all requests are properly logged in OpenSearch within the expected timeframe.
    Also verifies that the number of logs matches the number of requests made.
    """
    results = test_data["results"]
    total_requests = len(test_data["stage_strings"]) + len(test_data["prod_strings"])
    logged_requests = len(results["opensearch_logs"])

    assert (
        logged_requests == total_requests
    ), f"Expected {total_requests} log entries but found {logged_requests}"

    # Verify timestamps are within the last 30 seconds
    now = datetime.now(pytz.utc)
    for log in results["opensearch_logs"]:
        time_diff = now - log["timestamp"]
        assert (
            time_diff.total_seconds() <= 30
        ), f"Log entry timestamp {log['timestamp']} is more than 30 seconds old"


def test_client_host_distribution(test_data):
    """
    Test that the client hosts are properly distributed and counted.
    Each unique client host should have made at least one request.
    """
    results = test_data["results"]

    # Verify we have client host counts
    assert len(results["client_host_counts"]) > 0, "No client hosts found in logs"

    # Verify total requests match client host request counts
    total_requests = len(test_data["stage_strings"]) + len(test_data["prod_strings"])
    total_client_requests = sum(results["client_host_counts"].values())
    assert (
        total_client_requests == total_requests
    ), f"Total requests ({total_requests}) doesn't match sum of client host requests ({total_client_requests})"

import requests
from datetime import datetime
from opensearchpy import OpenSearch
import pytz
import time
import random
import string
from typing import List, Dict, Tuple


def check_logs(stage_strings: List[str], prod_strings: List[str]) -> Dict:
    # Define base URLs for stage and prod
    stage_base_url = "https://tvab.stage.intfas.se/"
    prod_base_url = "https://tvab.intfas.se/"

    # Store results for testing
    results = {
        "stage_responses": [],
        "prod_responses": [],
        "opensearch_logs": [],
        "client_host_counts": {},
    }

    print("\n")
    # Requests towards stage and status codes
    for str in stage_strings:
        url = stage_base_url + str
        response = requests.get(url)
        results["stage_responses"].append(
            {"url": url, "status_code": response.status_code}
        )
        print(f"Stage URL: {url} || Status Code: {response.status_code}")

    # Requests towards prod and status codes
    for str in prod_strings:
        url = prod_base_url + str
        response = requests.get(url)
        results["prod_responses"].append(
            {"url": url, "status_code": response.status_code}
        )
        print(f"Prod URL: {url} || Status Code: {response.status_code}")

    print("\n")

    # Add 20s delay
    for i in range(20, -1, -1):
        print(f"Waiting {i} seconds for logs to appear in Opensearch ", end="\r")
        time.sleep(1)

    # OpenSearch config
    host = "vpc-intelligy-6qh4hpet3b6ik3rx7z56hx5lmq.eu-central-1.es.amazonaws.com"
    port = 443
    utc = pytz.utc
    lcl_tz = pytz.timezone("Europe/Stockholm")

    # Initialize OpenSearch config
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        use_ssl=True,
        verify_certs=True,
        ssl_show_warn=False,
    )

    # Query to fetch 302 logs
    query = {
        "query": {
            "bool": {
                "filter": [
                    {"term": {"OriginStatus": 302}},
                    {"range": {"@timestamp": {"gte": "now-30s", "lte": "now"}}},
                ]
            }
        },
        "size": 10000,
    }

    # Execute search query
    response = client.search(body=query, index="traefik")

    print("\n")
    # Process and display log entries with timezone conversion
    for hit in response["hits"]["hits"]:
        timestamp = (
            datetime.strptime(hit["_source"]["@timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
            .replace(tzinfo=utc)
            .astimezone(lcl_tz)
        )
        log_entry = {
            "request_addr": hit["_source"]["RequestAddr"],
            "request_path": hit["_source"]["RequestPath"],
            "client_host": hit["_source"]["ClientHost"],
            "timestamp": timestamp,
        }
        results["opensearch_logs"].append(log_entry)
        print(
            f"RequestAddr: {hit['_source']['RequestAddr']}, "
            f"RequestPath: {hit['_source']['RequestPath']}, "
            f"ClientHost: {hit['_source']['ClientHost']}, "
            f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    # Count and display frequency of client hosts
    client_hosts = {}
    for hit in response["hits"]["hits"]:
        client_host = hit["_source"]["ClientHost"]
        if client_host in client_hosts:
            client_hosts[client_host] += 1
        else:
            client_hosts[client_host] = 1

    results["client_host_counts"] = client_hosts

    print("\nClientHost count:")
    for client_host, count in client_hosts.items():
        print(f"{client_host}: {count}")

    return results


def generate_random_string(length: int = 8) -> str:
    """Generate a random string of specified length"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_test_strings(count: int = 5) -> Tuple[List[str], List[str]]:
    """
    Generate test strings for both stage and production environments.
    Returns a tuple of (stage_strings, prod_strings)
    """
    stage_strings = [generate_random_string() for _ in range(count)]
    prod_strings = [generate_random_string() for _ in range(count)]
    return stage_strings, prod_strings


if __name__ == "__main__":
    stage_strings, prod_strings = generate_test_strings()
    check_logs(stage_strings, prod_strings)

"""
    This module contains the client used for interacting with the New Relic GraphQL API.
"""

from typing import Optional
import requests
import os
from cancel_managed_accounts.utils import setup_logger

# Create logger for the module
logger = setup_logger(__name__)

def get_api_key() -> Optional[str]:
    """
    Load New Relic API key from local environment variables
    :return: API key
    """

    return os.getenv('NEW_RELIC_API_KEY')


def execute_query(query: str, variables: dict = None) -> dict:
    """Execute a single GraphQL query"""

    api_key = get_api_key()

    if not api_key:
        logger.warning("Missing API key")
        raise ValueError("Missing API key")

    headers = {
        "Content-Type": "application/json",
        "API-Key": api_key
    }

    try:
        logger.info("Sending GraphQL request.")
        response = requests.post(
            "https://api.newrelic.com/graphql",
            headers=headers,
            json={"query": query, "variables": variables}
        )

        response.raise_for_status()

    except Exception as e:
        logger.error(f"Query failed to run: {e}")
        raise Exception(f"Query failed to run: {e}")

    return response.json()
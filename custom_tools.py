import http.client
import json
import logging
import os
import sys
import urllib.error
import urllib.request

import boto3
from strands import tool

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


class CustomTools:
    """A collection of tools for interacting with AWS services and performing operations."""

    def __init__(self):
        # Basic logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger = logger

        secrets = self.get_secret("PersonalizedRecommendationAgent")
        if not secrets:
            self.logger.fatal(
                "Failed to retrieve secrets. Please check your AWS Secrets Manager configuration."
            )
            sys.exit(1)
        if secrets:
            self.serper_api_key = secrets.get("serper_api_key")
            self.tavily_api_key = secrets.get("tavily_api_key")

    @tool(
        name="google_search",
        description="Perform targeted Google searches using the Serper API.",
    )
    def google_search(self, search_query: str, target_website: str = "") -> str:
        """
        This tool performs a Google search using the Serper API.
        Specializes in fast, structured Google SERP data retrieval at a lower cost compared to traditional search APIs, making it ideal for LLMs and agents that require quick access to search results.

        Args:
            search_query (str): The query to search for.
            target_website (str, optional): If provided, restricts the search to this website.
        Returns:
            str: The JSON response from the Serper API containing search results.
        """
        if self.serper_api_key is None:
            raise ValueError(
                "serper_api_key is not set. Please set the environment variable."
            )
        if not search_query:
            raise ValueError("Search query cannot be empty.")

        self.logger.info(f"Performing Google search with query: {search_query}")

        if target_website:
            search_query += f" site:{target_website}"

        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": search_query})
        headers = {"X-API-KEY": self.serper_api_key, "Content-Type": "application/json"}

        try:
            conn.request("POST", "/search", payload, headers)
            response = conn.getresponse()
            response_data = response.read().decode("utf-8")
            return response_data
        except http.client.HTTPException as e:
            self.logger.error(
                f"Failed to retrieve search results from Serper API, error: {e}"
            )

        return ""

    @tool(
        name="tavily_ai_search",
        description="Perform curated, content-rich searches using the Tavily AI Search API.",
    )
    def tavily_ai_search(self, search_query: str, target_website: str = "") -> str:
        """
        This tool performs a search using the Tavily AI Search API.
        Optimized for AI agents and LLMs, offering curated, content-rich search results ideal for research and generative AI tasks.

        Args:
            search_query (str): The query to search for.
            target_website (str, optional): If provided, restricts the search to this website.
        Returns:
            str: The JSON response from the Tavily AI Search API containing search results.
        """
        if self.tavily_api_key is None:
            raise ValueError(
                "tavily_api_key is not set. Please set the environment variable."
            )
        if not search_query:
            raise ValueError("Search query cannot be empty.")

        self.logger.info(f"Performing Tavily AI search with query: {search_query}")

        base_url = "https://api.tavily.com/search"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        payload = {
            "api_key": self.tavily_api_key,
            "query": search_query,
            "search_depth": "advanced",
            "include_images": False,
            "include_answer": False,
            "include_raw_content": False,
            "max_results": 3,
            "include_domains": [target_website] if target_website else [],
            "exclude_domains": [],
        }

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(base_url, data=data, headers=headers)

        try:
            response = urllib.request.urlopen(request)
            response_data = response.read().decode("utf-8")
            return response_data
        except urllib.error.HTTPError as e:
            self.logger.error(
                f"Failed to retrieve search results from Tavily AI Search, error: {e.code}"
            )

        return ""

    def get_secret(self, secret_name) -> dict:
        region_name = AWS_REGION  # Adjust if your secret is in another region

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
            secret = get_secret_value_response["SecretString"]
            # Parse the string as JSON to access individual keys
            secret_dict = json.loads(secret)
            return secret_dict
        except Exception as e:
            print(f"Error retrieving secret: {e}")
            return None

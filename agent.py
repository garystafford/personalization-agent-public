import logging
import os
import sys

from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.models import BedrockModel
from strands_tools import current_time

from custom_tools import CustomTools

# Load environment variables
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.2"))

# Basic logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

# Initialize custom tools
custom_tools = CustomTools()


def create_agent() -> Agent:
    # Create an Amazon Bedrock model instance
    # Assumes you have handled your AWS credentials and configuration

    model = BedrockModel(
        model_id=MODEL_ID,
        region_name=AWS_REGION,
        temperature=MODEL_TEMPERATURE,
        streaming=False,
        cache_prompt="default",
        cache_tools="default",
        include_tool_result_status=True,
    )
    logger.info(f"Model initialized: {model.config}")
    # Create a conversation manager
    conversation_manager = SlidingWindowConversationManager(
        window_size=20,
    )

    # Define a system prompt for the agent
    main_system_prompt = """Get the current date and time before making recommendations. Any dates before this are in the past, and any dates after this are in the future. When the user asks for the 'latest', 'most recent', 'today's', etc. don't assume your knowledge is up to date; confirm the current date and time.

You are a helpful assistant. 
Try to use the google_search first for general queries, and use tavily_ai_search for more specific or content-rich queries. The google_search tool is best for finding the latest information on trending topics, while the tavily_ai_search tool is best for retrieving curated content and detailed information on specific subjects. 
Important, always show your work, the tools you used, and the commands you executed."""

    # Create an agent with these tools
    search_agent = Agent(
        system_prompt=main_system_prompt,
        model=model,
        tools=[
            current_time,
            custom_tools.google_search,
            custom_tools.tavily_ai_search,
        ],
        conversation_manager=conversation_manager,
    )
    return search_agent

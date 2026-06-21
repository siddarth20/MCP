import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv(
    "API_KEY"
)

PLANNER_MODEL = os.getenv(
    "PLANNER_MODEL",
    "gemini-2.5-flash"
)

GENERATOR_MODEL = os.getenv(
    "GENERATOR_MODEL",
    "gemini-2.5-flash"
)

TARGET_URL = os.getenv(
    "TARGET_URL"
)

PLAYWRIGHT_MCP_URL = os.getenv(
    "PLAYWRIGHT_MCP_URL",
    "http://localhost:8931/mcp"
)
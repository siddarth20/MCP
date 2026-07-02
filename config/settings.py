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

#
# Running Playwright MCP Server
#
# Start manually:
#
# npx @playwright/mcp@latest --port 8931
#
# Then this client will connect to the running server.
#

PLAYWRIGHT_MCP_URL = os.getenv(
    "PLAYWRIGHT_MCP_URL",
    "http://localhost:8931/mcp"
)

#
# Number of retries if the MCP session is terminated.
#

MCP_MAX_RETRIES = int(
    os.getenv(
        "MCP_MAX_RETRIES",
        "1"
    )
)

#
# Timeout (seconds) before considering an MCP request failed.
#

MCP_REQUEST_TIMEOUT = int(
    os.getenv(
        "MCP_REQUEST_TIMEOUT",
        "60"
    )
)
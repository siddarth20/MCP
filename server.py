import asyncio

from agent.mcp_client import MCPClient
from agent.mcp_orchestrator import run_mcp_agent

from llm.generator import generate_framework
from generation.framework_writer import write_framework

async def main():

    gherkin = """
    Scenario: Login

        Given user opens login page

        When user enters valid credentials

        Then login succeeds
    """

    mcp_client = MCPClient()

    await mcp_client.connect()

    try:

        context = await run_mcp_agent(
            gherkin=gherkin,
            session=mcp_client.session
        )

        framework = generate_framework(
            gherkin,
            context
        )

        write_framework(
            framework
        )

    finally:

        await mcp_client.disconnect()


if __name__ == "__main__":

    asyncio.run(
        main()
    )
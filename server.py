import asyncio

from agent.mcp_client import MCPClient

from agent.mcp_orchestrator import MCPOrchestrator

from llm.generator import FrameworkGenerator

from generation.framework_writer import FrameworkWriter


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

        orchestrator = MCPOrchestrator(
            mcp_client
        )

        page_model = await orchestrator.execute(
            gherkin
        )

        generator = FrameworkGenerator()

        framework = generator.generate(

            gherkin,

            page_model

        )

        writer = FrameworkWriter()

        writer.write(

            framework

        )

        print()

        print("=" * 80)

        print("Robot Framework project generated successfully.")

        print("=" * 80)

    finally:

        await mcp_client.disconnect()


if __name__ == "__main__":

    asyncio.run(
        main()
    )
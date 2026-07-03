import asyncio
import traceback  # Added to properly diagnose the orchestration crash

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

    # Establish connection and spin up background keep-alive safety threads
    await mcp_client.connect()

    try:
        # The crash is occurring inside this function call during Iteration 2
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

    except Exception as e:
        print("\n" + "="*50)
        print("[CRITICAL ERROR] Orchestration loop broke during execution:")
        print("="*50)
        # Fixed: Prints the entire stack trace so you can find the exact breaking line
        traceback.print_exc() 
        print("="*50 + "\n")
    
    finally:
        print('[MCP] Initiating graceful lifecycle shutdown...')
        # Fixed: Re-enabled. Closing the exit stack prevents the unhandled asyncio task errors
        await mcp_client.disconnect()


if __name__ == "__main__":
    asyncio.run(
        main()
    )
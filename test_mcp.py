import asyncio

from agent.mcp_client import MCPClient


async def main():

    client = MCPClient()

    await client.connect()

    print("Navigate")

    await client.call_tool(
        "browser_navigate",
        {
            "url": "https://the-internet.herokuapp.com/login"
        }
    )

    print("Waiting 20 seconds...")

    await asyncio.sleep(20)

    print("Snapshot")

    await client.call_tool(
        "browser_snapshot",
        {}
    )

    print("Success")

    await client.disconnect()


asyncio.run(main())
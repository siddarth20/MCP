from mcp import ClientSession

from mcp.client.stdio import (
    stdio_client,
    StdioServerParameters
)


class MCPClient:

    def __init__(self):

        self.session = None

        self.transport = None

    async def connect(self):

        params = (
            StdioServerParameters(
                command=r"C:\Program Files\nodejs\npx.cmd",
                args=[
                    "@playwright/mcp@latest"
                ]
            )
        )

        self.transport = (
            stdio_client(
                params
            )
        )

        (
            read_stream,
            write_stream
        ) = await self.transport.__aenter__()

        self.session = (
            ClientSession(
                read_stream,
                write_stream
            )
        )

        await self.session.__aenter__()

        await self.session.initialize()

        print(
            "\nConnected to Playwright MCP"
        )

        tools = await self.session.list_tools()

        print(
            f"\nLoaded {len(tools.tools)} tools"
        )

        return self.session

    async def disconnect(self):

        if self.session:

            await self.session.__aexit__(
                None,
                None,
                None
            )

        if self.transport:

            await self.transport.__aexit__(
                None,
                None,
                None
            )
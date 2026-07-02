import copy

from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from config.settings import (
    PLAYWRIGHT_MCP_URL
)


class MCPClient:

    def __init__(self):

        self.exit_stack = None

        self.session = None

        self.native_tools = []

        self.tools = []

        self.connected = False

    async def connect(self):

        if self.connected:

            return

        print()
        print("=" * 80)
        print("CONNECTING TO PLAYWRIGHT MCP")
        print("=" * 80)

        self.exit_stack = AsyncExitStack()

        (
            read_stream,
            write_stream,
            _
        ) = await self.exit_stack.enter_async_context(

            streamablehttp_client(

                PLAYWRIGHT_MCP_URL

            )

        )

        self.session = await self.exit_stack.enter_async_context(

            ClientSession(

                read_stream,

                write_stream

            )

        )

        await self.session.initialize()

        await self.discover_tools()

        self.connected = True

        print()
        print("Connected.")

    async def reconnect(self):

        print()
        print("=" * 80)
        print("RECONNECTING MCP SESSION")
        print("=" * 80)

        try:

            if self.exit_stack:

                await self.exit_stack.aclose()

        except Exception:

            pass

        self.connected = False

        self.session = None

        self.exit_stack = None

        await self.connect()

    async def discover_tools(self):

        response = await self.session.list_tools()

        self.native_tools = response.tools

        self.tools = []

        for tool in self.native_tools:

            schema = copy.deepcopy(

                tool.inputSchema

            )

            schema.setdefault(

                "additionalProperties",

                False

            )

            self.tools.append(

                {

                    "type": "function",

                    "function": {

                        "name": tool.name,

                        "description": tool.description or "",

                        "parameters": schema

                    }

                }

            )

    async def call_tool(
            self,
            tool_name,
            tool_args):

        if not self.connected:

            await self.connect()

        try:

            return await self.session.call_tool(

                tool_name,

                tool_args

            )

        except Exception as ex:

            #
            # Retry only when the session has died
            #

            if "Session terminated" not in str(ex):

                raise

            print()
            print("=" * 80)
            print("SESSION TERMINATED")
            print("Attempting reconnect...")
            print("=" * 80)

            await self.reconnect()

            print()
            print("Retrying tool...")
            print(tool_name)

            return await self.session.call_tool(

                tool_name,

                tool_args

            )

    def get_openai_tools(self):

        return self.tools

    def get_mcp_tools(self):

        return self.native_tools

    async def disconnect(self):

        if self.exit_stack:

            await self.exit_stack.aclose()

        self.connected = False

        self.session = None

        self.exit_stack = None
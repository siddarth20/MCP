import json

from agent.enterprise_tools.browser_get_page_info import (
    BrowserGetPageInfo
)

from agent.enterprise_tools.browser_get_framework import (
    BrowserGetFramework
)

from agent.enterprise_tools.browser_get_inputs import (
    BrowserGetInputs
)

from agent.enterprise_tools.browser_get_buttons import (
    BrowserGetButtons
)

from agent.enterprise_tools.browser_get_forms import (
    BrowserGetForms
)


class ToolExecutor:

    def __init__(
            self,
            mcp_client):

        self.mcp_client = mcp_client

        self.enterprise_tools = {

            "browser_get_page_info":
                BrowserGetPageInfo(),

            "browser_get_framework":
                BrowserGetFramework(),

            "browser_get_inputs":
                BrowserGetInputs(),

            "browser_get_buttons":
                BrowserGetButtons(),

            "browser_get_forms":
                BrowserGetForms()

        }

    async def execute(
            self,
            tool_name,
            tool_args):

        print()
        print("=" * 80)
        print(f"TOOL : {tool_name}")
        print("=" * 80)

        print(

            json.dumps(

                tool_args,

                indent=4

            )

        )

        #
        # Enterprise Tool
        #

        if tool_name in self.enterprise_tools:

            print()

            print(
                "Executing Enterprise Tool..."
            )

            return await self.enterprise_tools[
                tool_name
            ].execute(

                self.mcp_client,

                tool_args

            )

        #
        # Native MCP Tool
        #

        print()

        print(
            "Executing Native MCP Tool..."
        )

        try:

            result = await self.mcp_client.call_tool(

                tool_name,

                tool_args

            )

        except Exception as ex:

            print()

            print("=" * 80)

            print("TOOL FAILED")

            print("=" * 80)

            print(tool_name)

            print(ex)

            raise

        if not result.content:

            return {}

        text = result.content[0].text

        try:

            return json.loads(

                text

            )

        except Exception:

            return {

                "raw": text

            }

    def get_available_tools(self):

        tools = list(

            self.mcp_client.get_openai_tools()

        )

        for tool in self.enterprise_tools.values():

            tools.append(

                {

                    "type": "function",

                    "function": {

                        "name":
                            tool.name,

                        "description":
                            tool.description,

                        "parameters":
                            tool.parameters

                    }

                }

            )

        return tools
import json
import time

from config.settings import TARGET_URL

from agent.system_prompt import SYSTEM_PROMPT

from agent.tool_executor import ToolExecutor

from llm.tool_planner import ToolPlanner

from models.page_model import PageModel

from models.page_model_mapper import PageModelMapper


class MCPOrchestrator:

    def __init__(
            self,
            mcp_client):

        self.mcp_client = mcp_client

        self.tool_executor = ToolExecutor(

            mcp_client

        )

        self.page_model = PageModel()

        self.planner = ToolPlanner(

            self.tool_executor

        )

    async def execute(
            self,
            gherkin):

        #
        # Ensure MCP connection
        #

        await self.mcp_client.connect()

        self.planner.initialize(

            SYSTEM_PROMPT,

            gherkin

        )

        iteration = 1

        while True:

            print()

            print("=" * 100)

            print(
                f"ITERATION {iteration}"
            )

            print("=" * 100)

            #
            # Ask planner
            #

            planner_start = time.perf_counter()

            message = self.planner.ask()

            planner_time = (

                time.perf_counter()

                - planner_start

            )

            print()

            print(

                f"Planner completed in "

                f"{planner_time:.2f}s"

            )

            #
            # Planner output
            #

            if message.content:

                print()

                print("=" * 80)

                print("MODEL CONTENT")

                print("=" * 80)

                print(

                    message.content

                )

            if message.tool_calls:

                print()

                print("=" * 80)

                print("TOOLS")

                print("=" * 80)

                for tc in message.tool_calls:

                    print()

                    print(

                        tc.function.name

                    )

                    print(

                        tc.function.arguments

                    )

            #
            # Finished
            #

            if (

                message.content

                and

                "GENERATE_FRAMEWORK"

                in message.content

            ):

                print()

                print("=" * 80)

                print(

                    "Framework generation requested."

                )

                print("=" * 80)

                return self.page_model

            #
            # Safety
            #

            if not message.tool_calls:

                raise RuntimeError(

                    "Planner returned no tool calls."

                )

            #
            # Execute tools
            #

            for tool_call in message.tool_calls:

                tool_name = (

                    tool_call.function.name

                )

                tool_args = {}

                if tool_call.function.arguments:

                    tool_args = json.loads(

                        tool_call.function.arguments

                    )

                #
                # Never trust LLM URL
                #

                if tool_name == "browser_navigate":

                    tool_args = {

                        "url": TARGET_URL

                    }

                result = await self.tool_executor.execute(

                    tool_name,

                    tool_args

                )

                PageModelMapper.update(

                    self.page_model,

                    tool_name,

                    result

                )

                self.planner.add_tool_result(

                    tool_call,

                    result

                )

            iteration += 1
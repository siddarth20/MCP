import asyncio
import json

from discovery.context_builder import build_context

from llm.tool_planner import decide_next_action

from agent.system_prompt import SYSTEM_PROMPT

from config.settings import TARGET_URL


class MCPMemory:

    def __init__(self):

        self.context = {}

        self.tool_history = []

        self.execution_history = []

        self.snapshot_counter = 0

    def add(
            self,
            tool_name,
            result):

        if tool_name == "browser_snapshot":

            self.snapshot_counter += 1

            self.context[
                f"browser_snapshot_{self.snapshot_counter}"
            ] = result

        else:

            self.context[
                tool_name
            ] = result

        self.tool_history.append(
            tool_name
        )

        self.execution_history.append(
            {
                "tool": tool_name,
                "result": result
            }
        )

        self.context[
            "tool_history"
        ] = list(
            self.tool_history
        )

        self.context[
            "execution_history"
        ] = list(
            self.execution_history
        )

    def get_context(self):

        return self.context


async def execute_tool(
        session,
        tool_name,
        tool_args):

    try:

        print(
            f"\nCALLING TOOL: {tool_name}"
        )

        print(
            f"ARGS: {tool_args}"
        )

        result = await session.call_tool(
            tool_name,
            tool_args
        )

        if not result.content:

            return {
                "success": False,
                "error": "No content returned"
            }

        text = (
            result.content[0]
            .text
        )

        try:

            return json.loads(
                text
            )

        except Exception:

            return {
                "raw": text
            }

    except Exception as ex:

        return {
            "success": False,
            "error": str(ex)
        }


async def run_mcp_agent(
        gherkin,
        session):

    memory = MCPMemory()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"""
TARGET_URL

{TARGET_URL}

GHERKIN

{gherkin}
"""
        }
    ]

    iteration = 0

    max_iterations = 30

    while True:

        iteration += 1

        print(
            f"\n==== ITERATION {iteration} ===="
        )

        if iteration > max_iterations:

            raise RuntimeError(
                "Agent exceeded maximum iterations"
            )

        message = (
            decide_next_action(
                messages
            )
        )

        print(
            "\n==== MODEL RESPONSE ===="
        )

        print(
            message
        )

        if (
            message.content
            and
            "GENERATE_FRAMEWORK"
            in message.content
        ):

            print(
                "\nAgent requested framework generation"
            )

            break

        if not message.tool_calls:

            raise RuntimeError(
                f"No tool calls returned:\n{message}"
            )

        for tool_call in message.tool_calls:

            tool_name = (
                tool_call.function.name
            )

            tool_args = json.loads(
                tool_call.function.arguments
            )

            #
            # Force configured URL
            #
            if tool_name == "browser_navigate":

                tool_args = {
                    "url": TARGET_URL
                }

            print(
                f"\nExecuting tool: {tool_name}"
            )

            print(
                json.dumps(
                    tool_args,
                    indent=2
                )
            )

            tool_result = (
                await execute_tool(
                    session,
                    tool_name,
                    tool_args
                )
            )

            #
            # Give browser time to stabilize
            #
            if tool_name == "browser_navigate":

                await asyncio.sleep(2)

            #
            # Detect dead session early
            #
            if (
                isinstance(
                    tool_result,
                    dict
                )
                and
                "Session terminated"
                in str(tool_result)
            ):

                raise RuntimeError(
                    "Playwright MCP session terminated"
                )

            memory.add(
                tool_name,
                tool_result
            )

            print(
                f"\nStored {tool_name}"
            )

            print(
                json.dumps(
                    tool_result,
                    indent=2
                )[:2000]
            )

            messages.append(
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": json.dumps(
                                    tool_args
                                )
                            }
                        }
                    ]
                }
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        tool_result
                    )[:10000]
                }
            )

    context = build_context(
        memory
    )

    return context
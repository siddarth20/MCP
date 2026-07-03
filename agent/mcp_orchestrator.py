import asyncio
import json

from discovery.context_builder import build_context
from llm.tool_planner import decide_next_action
from agent.system_prompt import SYSTEM_PROMPT
from agent.optimized_dom import build_optimized_dom_script
from config.settings import TARGET_URL


class MCPMemory:

    def __init__(self):
        self.context = {}
        self.tool_history = []
        self.execution_history = []
        self.snapshot_counter = 0

    def add(self, tool_name, result):
        if tool_name == "browser_snapshot":
            self.snapshot_counter += 1
            self.context[f"browser_snapshot_{self.snapshot_counter}"] = result
        else:
            self.context[tool_name] = result

        self.tool_history.append(tool_name)
        self.execution_history.append({
            "tool": tool_name,
            "result": result
        })

        self.context["tool_history"] = list(self.tool_history)
        self.context["execution_history"] = list(self.execution_history)

    def get_context(self):
        return self.context


async def execute_tool(session, tool_name, tool_args):
    try:
        print(f"\nCALLING TOOL: {tool_name}")
        print(f"ARGS: {tool_args}")

        #
        # browser_get_optimized_dom isn't a native Playwright MCP tool.
        # Enforce strict overrides here to prevent the model from requesting 
        # massive, deep DOM structures that trigger buffer failures.
        #
        if tool_name == "browser_get_optimized_dom":
            # Strict safety bounds override model generation parameters
            tool_args["max_depth"] = 4    
            tool_args["max_nodes"] = 35   
            tool_args["include_hidden"] = False

            raw_script = build_optimized_dom_script(tool_args)

            # Minify and flatten stringified JSON layout within the browser context
            wrapped_function = f"""
            (() => {{
                try {{
                    const res = ({raw_script})();
                    const jsonStr = JSON.stringify(res);
                    return jsonStr.replace(/\\r?\\n|\\r/g, ' ').trim();
                }} catch(e) {{
                    return JSON.stringify({{ "success": false, "error": e.message }});
                }}
            }})()
            """

            result = await session.call_tool(
                "browser_evaluate",
                {
                    "function": wrapped_function
                }
            )

        else:
            result = await session.call_tool(
                tool_name,
                tool_args
            )

        if not result.content:
            return {
                "success": False,
                "error": "No content returned"
            }

        # Safely extract text across variant SDK content array definitions
        if hasattr(result.content, 'text'):
            text = result.content.text
        elif isinstance(result.content, list) and len(result.content) > 0:
            text = getattr(result.content[0], 'text', str(result.content[0]))
        else:
            text = str(result.content)

        try:
            # Handle cases where the MCP server wraps outputs in markdown wrappers
            if isinstance(text, str) and ("###" in text or "```" in text):
                cleaned = text.replace("### Result", "")
                cleaned = cleaned.replace("```json", "")
                cleaned = cleaned.replace("```", "")
                cleaned = cleaned.strip()
                return json.loads(cleaned)

            return json.loads(text)

        except Exception:
            return {
                "raw": text
            }

    except Exception as ex:
        # If the server closed the transport channel, pass it as a drop flag
        if "terminated" in str(ex).lower() or "404" in str(ex):
            return {"success": False, "error": "Session terminated"}
        return {
            "success": False,
            "error": str(ex)
        }


async def run_mcp_agent(gherkin, session):
    memory = MCPMemory()

    # CRITICAL FIX: Forces the LLM to skip long explanations.
    # This prevents the Playwright server from timing out while waiting for a response.
    tightly_bounded_prompt = SYSTEM_PROMPT + "\n\n" + (
        "CRITICAL OPERATIONAL CONSTRAINT:\n"
        "Your thinking/reasoning response must be extremely concise (under 2 sentences).\n"
        "Do not list out upcoming steps or elaborate on plans. Output the tool call immediately."
    )

    messages = [
        {
            "role": "system",
            "content": tightly_bounded_prompt
        },
        {
            "role": "user",
            "content": f"TARGET_URL\n\n{TARGET_URL}\n\nGHERKIN\n\n{gherkin}"
        }
    ]

    iteration = 0
    max_iterations = 30

    while True:
        iteration += 1
        print(f"\n==== ITERATION {iteration} ====")

        if iteration > max_iterations:
            raise RuntimeError("Agent exceeded maximum iterations")

        message = decide_next_action(messages)
        print("\n==== MODEL RESPONSE ====")
        print(message)

        if message.content and "GENERATE_FRAMEWORK" in message.content:
            print("\nAgent requested framework generation")
            break

        if not message.tool_calls:
            raise RuntimeError(f"No tool calls returned:\n{message}")

        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            # Force configured target URL mapping
            if tool_name == "browser_navigate":
                tool_args = {
                    "url": TARGET_URL
                }

            print(f"\nExecuting tool: {tool_name}")
            print(json.dumps(tool_args, indent=2))

            tool_result = await execute_tool(
                session,
                tool_name,
                tool_args
            )

            # Give browser animations time to stabilize
            if tool_name == "browser_navigate":
                await asyncio.sleep(2)

            # Detect dead network drops early
            if isinstance(tool_result, dict) and tool_result.get("error") == "Session terminated":
                raise RuntimeError("Playwright MCP session terminated")

            memory.add(tool_name, tool_result)
            print(f"\nStored {tool_name}")
            print(json.dumps(tool_result, indent=2)[:2000])

            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": json.dumps(tool_args)
                        }
                    }
                ]
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)[:10000]
            })

    context = build_context(memory)
    return context

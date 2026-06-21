from llm.client import client

from config.settings import (
    PLANNER_MODEL
)

from agent.playwright_tools import (
    TOOLS
)


def decide_next_action(
        messages):

    response = (
        client.chat.completions.create(
            model=PLANNER_MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )
    )

    return (
        response
        .choices[0]
        .message
    )
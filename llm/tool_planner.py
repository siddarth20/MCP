import json

from llm.client import client

from config.settings import PLANNER_MODEL


class ToolPlanner:

    def __init__(
            self,
            tool_executor):

        self.tool_executor = tool_executor

        self.messages = []

    def initialize(
            self,
            system_prompt,
            gherkin):

        self.messages = [

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": gherkin
            }

        ]

    def ask(self):

        response = client.chat.completions.create(

            model=PLANNER_MODEL,

            messages=self.messages,

            tools=self.tool_executor.get_available_tools(),

            tool_choice="auto",

            temperature=0

        )

        message = response.choices[0].message

        print("\n")
        print("=" * 80)
        print("LLM RESPONSE")
        print("=" * 80)
        print(response.model_dump_json(indent=2))

        #
        # Store the EXACT assistant message returned
        # by the model.
        #
        self.messages.append(

            message.model_dump(
                exclude_none=True
            )

        )

        return message

    def add_tool_result(

            self,

            tool_call,

            result):

        #
        # DO NOT reconstruct the assistant message.
        # It is already present in self.messages.
        #

        self.messages.append(

            {

                "role": "tool",

                "tool_call_id":
                    tool_call.id,

                "content":
                    json.dumps(
                        result,
                        ensure_ascii=False
                    )

            }

        )

        print()
        print("=" * 80)
        print("MESSAGE HISTORY")
        print("=" * 80)

        for index, message in enumerate(self.messages):

            print(
                f"{index + 1}. {message['role']}"
            )

    def dump_messages(self):

        print()

        print("=" * 80)

        print("CURRENT CONVERSATION")

        print("=" * 80)

        for message in self.messages:

            print()

            print(message["role"])

            print("-" * 40)

            print(

                json.dumps(

                    message,

                    indent=2,

                    ensure_ascii=False

                )

            )
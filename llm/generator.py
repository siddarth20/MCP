import json
import re
from dataclasses import asdict

from llm.client import client

from config.settings import (
    GENERATOR_MODEL
)


class FrameworkGenerator:

    def __init__(self):
        pass

    def generate(
            self,
            gherkin,
            page_model):

        page = asdict(page_model)

        prompt = f"""
You are a senior Robot Framework automation architect.

Generate a complete enterprise Robot Framework project.

Requirements

- Use Page Object Model.
- Use reusable keywords.
- Use reusable resource files.
- Use variables.
- Prefer id locator.
- Then name.
- Then data-testid.
- Then aria-label.
- Then role.
- Use xpath only as a last resort.
- Do not duplicate locators.
- Generate only valid Robot Framework files.

Gherkin Scenario

{gherkin}

Current Page Model (JSON)

{json.dumps(page, indent=2)}

Return ONLY valid JSON.

The JSON schema MUST be exactly:

{{
    "tests": [
        {{
            "name": "",
            "content": ""
        }}
    ],
    "pages": [
        {{
            "name": "",
            "content": ""
        }}
    ],
    "resources": [
        {{
            "name": "",
            "content": ""
        }}
    ],
    "variables": [
        {{
            "name": "",
            "content": ""
        }}
    ],
    "keywords": [
        {{
            "name": "",
            "content": ""
        }}
    ]
}}

Do not wrap the JSON inside markdown.

Do not explain anything.

Return only JSON.
"""

        response = client.chat.completions.create(

            model=GENERATOR_MODEL,

            temperature=0,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        text = response.choices[0].message.content.strip()

        #
        # Direct JSON
        #

        try:

            return json.loads(text)

        except Exception:

            pass

        #
        # Remove markdown if present
        #

        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
            flags=re.MULTILINE
        )

        text = re.sub(
            r"```$",
            "",
            text,
            flags=re.MULTILINE
        ).strip()

        #
        # Try JSON again
        #

        try:

            return json.loads(text)

        except Exception:

            pass

        #
        # Extract first JSON object
        #

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:

            try:

                return json.loads(
                    text[start:end + 1]
                )

            except Exception:

                pass

        raise RuntimeError(
            "Generator did not return valid JSON.\n\n"
            + text
        )
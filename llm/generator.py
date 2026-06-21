import json

from llm.client import (
    client
)

from config.settings import (
    GENERATOR_MODEL
)

from llm.generator_prompt import GENERATOR_PROMPT


def generate_framework(gherkin, context):


  prompt = f"""


  {GENERATOR_PROMPT}

  Gherkin:

  {gherkin}

  Context:

  {json.dumps(
  context,
  indent=2
  )}
  """

  response = (
      client.chat.completions.create(
          model=GENERATOR_MODEL,
          messages=[
              {
                  "role": "user",
                  "content": prompt
              }
          ],
          temperature=0.1
      )
  )

  response_text = (
      response
      .choices[0]
      .message
      .content
      .strip()
  )

  # Remove markdown fences if Groq returns them

  if response_text.startswith(
          "```json"
  ):

      response_text = (
          response_text.replace(
              "```json",
              "",
              1
          )
      )

  if response_text.startswith(
          "```"
  ):

      response_text = (
          response_text.replace(
              "```",
              "",
              1
          )
      )

  if response_text.endswith(
          "```"
  ):

      response_text = (
          response_text[:-3]
      )

  response_text = (
      response_text.strip()
  )

  print(
      "\n==== GROQ RESPONSE ====\n"
  )

  print(
      response_text
  )

  print(
      "\n=======================\n"
  )

  return response_text

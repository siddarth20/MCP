from openai import OpenAI

from config.settings import (
    API_KEY
)

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)
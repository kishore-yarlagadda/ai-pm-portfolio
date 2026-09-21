"""Optional Groq/OpenAI-compatible language-generation client."""

import os

try:
    from dotenv import find_dotenv, load_dotenv
except ImportError:
    find_dotenv = load_dotenv = None


if load_dotenv is not None:
    load_dotenv(find_dotenv())


class LLMClient:
    """Generate customer-facing wording when a live Groq key is configured.

    Routing, state, calculations, and compliance review remain outside this
    client. Callers own deterministic fallback behavior.
    """

    def __init__(self, model_name: str = "openai/gpt-oss-120b"):
        self.model_name = model_name
        self.api_key = os.getenv("GROQ_API_KEY")

    @property
    def is_live_available(self) -> bool:
        return bool(self.api_key)

    def generate_response(self, system_prompt: str, user_message: str) -> str:
        """Return a live language draft or raise so the caller can fail safe."""
        if not self.api_key:
            raise RuntimeError("Live LLM generation is not configured")

        from openai import OpenAI

        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=self.api_key,
        )
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Live LLM generation returned an empty draft")
        return content.strip()

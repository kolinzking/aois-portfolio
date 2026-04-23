from __future__ import annotations

import os

from anthropic import Anthropic


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=256,
        temperature=0,
        system="You are an SRE assistant that explains infrastructure logs clearly.",
        messages=[
            {
                "role": "user",
                "content": "Analyze this log: pod OOMKilled exit code 137",
            }
        ],
    )

    for block in response.content:
        if getattr(block, "type", None) == "text":
            print(block.text)


if __name__ == "__main__":
    main()

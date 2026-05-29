import discord
from typing import List, Dict

from anthropic import Anthropic

class Claude:
    def __init__(self, api_key: str = None):
        self.client = Anthropic(
            # This is the default and can be omitted
            api_key=api_key,
        )

    def response_from_conversation(self, conversation: List[Dict[str, str]]):
        # Read prompt from prompt.txt
        prompt = open("prompt.txt", "r").read()

        return self.client.messages.create(
            max_tokens=1024,
            messages=conversation,
            model="claude-haiku-4-5",
            system=prompt
        )


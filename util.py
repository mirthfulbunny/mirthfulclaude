from typing import List, Dict

import discord


async def conversation_from_ctx(ctx: discord.Context, bot: discord.Client) -> List[Dict[str, str]]:
    last_messages = await ctx.channel.history(limit=20).flatten()
    last_messages_list = list(last_messages)
    last_messages_list.reverse()
    conversation = [{
        "role": "user" if msg.author != bot.user else "assistant",
        "content": "\"{}\" said: {}".format(msg.author.name, msg.clean_content)
    } for msg in last_messages_list
    ]

    return conversation
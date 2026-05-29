import discord
from anthropic import Anthropic
import os # default module

from discord import TextChannel, ForumChannel
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="respond", description="Respond to the last message that was sent")
async def respond(ctx: discord.ApplicationContext):
    # Get the last 20 messages that were sent
    channel = ctx.channel
    if isinstance(channel, TextChannel):
        last_messages = await ctx.channel.history(limit=20).flatten()
        last_messages_list = list(last_messages)
        last_messages_list.reverse()
        conversation = [ {
                "role": "user" if msg.author != bot.user else "assistant",
                "content": "\"{}\" said: {}".format(msg.author.name, msg.clean_content)
            } for msg in last_messages_list
        ]

        response = client.messages.create(
            max_tokens=1024,
            messages=conversation,
            model="claude-haiku-4-5",
            system="""You are Claude, participating as one member of a multi-person Discord chat.

Conversation format:
- Each incoming message is prefixed with the speaker's name, like:  "alice" said: hello there
- These names identify different humans in the channel. They are NOT you.
- Your own past replies appear without that prefix — those are you.

How to participate:
- Write a fresh message that adds to the conversation. Do NOT complete or continue the last speaker's sentence.
- Do not prefix your reply with your own name or with "Claude said:". Just write the message.
- Keep replies short and conversational — usually 1–3 sentences, like a person typing in chat. Long paragraphs only when someone clearly asked for depth.
- If the last message wasn't directed at you and you have nothing to add, it's fine to say so briefly (e.g. "no strong opinion here") rather than forcing a reply.
- Match the tone of the channel. Don't lecture, don't over-explain, don't end every message with a follow-up question.
- Refer to people by name when it helps clarity ("agreeing with alice — ...")."""
        )

        last_messages_str = "\n".join("{} said: {}".format(msg.author.name, msg.clean_content[:200] + "...") for msg in last_messages_list)
        print(last_messages_str)
        print(response, response.content)

        reply_text = "".join(block.text for block in response.content if block.type == "text")

        # Respond with response, sending one message for every 2,000 characters
        for i in range(0, len(reply_text), 2000):
            chunk = reply_text[i:i+2000]
            if i == 0:
                await ctx.respond(chunk)
            else:
                await ctx.followup.send(chunk)
    else:
        await ctx.respond("This command can only be used in a text channel. This is a " + str(type(channel)))




bot.run(os.getenv('TOKEN')) # run the bot with the token
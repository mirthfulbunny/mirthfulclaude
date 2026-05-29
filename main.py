import discord
import os

from discord import TextChannel, ForumChannel
from dotenv import load_dotenv

from claude import Claude
import util

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

claude = Claude(api_key=os.getenv("CLAUDE_API_KEY"))

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="respond", description="Respond to the last message that was sent")
async def respond(ctx: discord.ApplicationContext):
    # Get the last 20 messages that were sent
    channel = ctx.channel
    if isinstance(channel, TextChannel):
        conversation = await util.conversation_from_ctx(ctx, bot)
        response = claude.response_from_conversation(conversation)

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
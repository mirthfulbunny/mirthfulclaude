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
    channel = ctx.channel
    if not isinstance(channel, TextChannel):
        await ctx.respond("This command can only be used in a text channel. This is a " + str(type(channel)))
        return

    await ctx.defer()

    try:
        conversation = await util.conversation_from_ctx(ctx, bot)

        # Debug log the conversation
        print(conversation)

        response = claude.response_from_conversation(conversation)
        print(response)

        reply_text = "".join(block.text for block in response.content if block.type == "text")

        for i in range(0, len(reply_text), 2000):
            await ctx.followup.send(reply_text[i:i+2000])
    except Exception as e:
        await ctx.followup.send("An error occured while generating a response.")
        raise e


bot.run(os.getenv('TOKEN')) # run the bot with the token
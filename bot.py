import asyncio
import discord
import os
import random
from dotenv import load_dotenv

# Have to set intents so bot can see users in voice channels
intents = discord.Intents.default()
intents.members = True

bot = discord.Client(intents=intents)

# Load environment variables from .env file
load_dotenv()

@bot.event
async def on_ready():
    print("Connected & Logged in. I solemnly swear that I am up to no good!")

@bot.event
async def on_voice_state_update(member, before, after):

    if before.channel == None and after.channel != None:

        await asyncio.sleep(1)
        voice_client: discord.VoiceClient = await after.channel.connect()

        async def mute_and_disconnect() -> None:
            await member.edit(mute=True)
            print("User {} muted in channel. Mischief managed!".format(member))
            await voice_client.disconnect()

        async def deafen_and_disconnect() -> None:
            await member.edit(deafen=True)
            print("User {} deafened in channel. Mischief managed!".format(member))
            await voice_client.disconnect()

        async def kick_and_disconnect() -> None:
            await member.edit(voice_channel=None)
            print("User {} removed from channel. Mischief managed!".format(member))
            await voice_client.disconnect()
        
        async def kick_from_guild_and_disconnect() -> None:
            await member.kick()

        async def ban_from_guild_and_disconnect() -> None:
            await member.ban()

        def after_play(e):
            # We have to hook into asyncio here as voice_client.play
            # runs the Callable it's given without await'ing it
            # Basically this just calls `kick_and_disconnect`
            asyncio.run_coroutine_threadsafe(
                kick_and_disconnect(), bot.loop)

        f = random.choice([mute_and_disconnect,deafen_and_disconnect])    
        voice_client.play(discord.FFmpegPCMAudio("khande_kiri.mp3"), after=after_play)
        #await f()
        return

@bot.event
async def on_message(message):

    if message.author != bot.user:
        await message.delete()
        await message.channel.send("I deleted your message "+ message.author.mention + ". \**Evil Laugh*\*")


# Run the bot with token read from env variable
bot.run(os.environ.get("ANNOYING_BOT_TOKEN"))

"""Various fun commands that aren't harmful in any way."""
from discord.ext import commands
import utilities as util
import asyncio
import discord
import random

class miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def historyfetch(self, ctx):
        """Fetches the message history of the guild. Does not record bot messages."""
        excounter = 0
        
        with open("./cogs-experimental/data.txt", "w") as datafile:
            for channel in ctx.guild.text_channels:
                async for message in channel.history(limit=None):
                    if not message.author.bot: 
                        try: datafile.write(message.content + "\n")
                        except Exception: excounter += 1
                
                print(channel.name + " has been recorded.")
        await ctx.send("All channels recorded to data.txt.")

    @commands.command()
    async def nigga(self, ctx, user: discord.Member):
        """big n-word energy"""
        voiceclass = self.bot.get_cog("voice")
        lastchannel = ctx.author.voice.channel
        ctx.author.voice.channel = random.choice(ctx.guild.voice_channels)
        
        await voiceclass.join(ctx)
        guildvoice = ctx.guild.voice_client
        await user.edit(voice_channel=ctx.author.voice.channel)
        await voiceclass.play(ctx, "./ffmpeg/music/reallynigga.mp3")
        
        await asyncio.sleep(2)
        await user.edit(voice_channel=lastchannel)
        await guildvoice.disconnect()

    @commands.command()
    async def echotoall(self, ctx, *, message):
        """Echos `message` to all channels that aren't forbidden."""
        communists = util.fetchbannedchannels(ctx)
        for channels in ctx.guild.text_channels:
            if not channels.id in communists:
                try: await channels.send(message)
                except Exception: pass
                else: await asyncio.sleep(1)

def setup(bot): bot.add_cog(miscellaneous(bot))                
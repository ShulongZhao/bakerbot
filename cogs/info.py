import discord.ext.commands as commands
import discord
from discord.ext.commands.core import command
import model
import time

class Information(commands.Cog):
    def __init__(self, bot: model.YunYutility):
        self.colours = bot.utils.Colours
        self.icons = bot.utils.Icons
        self.embeds = bot.utils.Embeds
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")
    
    @commands.command()
    async def invite(self, ctx: commands.Context):
        """ Bot invite link """
        await ctx.send("Invite me to your server! https://discord.com/api/oauth2/authorize?client_id=674200699260895233&permissions=8&scope=bot")
    
    @commands.command()
    async def source(self, ctx: commands.Context):
        """ Check out the source code! """
        await ctx.send(f"**{ctx.bot.user}** is written by <@369059807946080257>, check out the code at \nhttps://github.com/ShulongZhao/yunyutility")
    
    @commands.command()
    async def info(self, ctx):
        """ About the bot """

        embedColour = discord.Embed.Empty
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)}", inline=True)
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]), inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)
        

def setup(bot: model.YunYutility) -> None:
    cog = Information(bot)
    bot.add_cog(cog)
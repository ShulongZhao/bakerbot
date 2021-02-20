from libs.utilities import Embeds, Colours, Icons, Choices
from libs.wikipedia import Wikipedia
from libs.models import Bakerbot
from discord.ext import commands

import discord

class Internet(commands.Cog):
    """Bakerbot's portal to the World Wide Web!"""
    def __init__(self, bot: Bakerbot) -> None:
        self.bot = bot

    @commands.group(invoke_without_subcommand=True)
    async def wiki(self, ctx: commands.Context) -> None:
        """The parent command for all things Wikipedia related."""
        if ctx.invoked_subcommand is None:
            # Since there was no subcommand, inform the user about the group and its subcommands.
            desc = ("Welcome to the Wikipedia command group! This cog provides commands for interacting "
                    "with the APIs provided by Wikipedia. Search to your heart's content.\n"
                    "See `$help internet` for available subcommands.")

            embed = discord.Embed(description=desc, colour=Colours.regular, timestamp=Embeds.now())
            embed.set_footer(text="Powered by the Wikipedia API.", icon_url=Icons.wikipedia)
            await ctx.send(embed=embed)

    @wiki.command()
    async def read(self, ctx: commands.Context, *, query: str) -> None:
        """Read a Wikipedia article."""
        async with ctx.typing():
            if (response := await Wikipedia.search(query)) is None:
                fail = Embeds.status(success=False, desc="Wikipedia couldn't find anything.")
                return await ctx.send(embed=fail)

            # Get the article corresponding to the first page ID.
            response = await Wikipedia.article(response[0].pageid)

        # Render the page in an embed and send it off.
        embed = discord.Embed(colour=Colours.regular, timestamp=Embeds.now())
        embed.set_footer(text="Powered by the Wikipedia API.", icon_url=Icons.wikipedia)
        embed.set_thumbnail(url=response.thumbnail if response.thumbnail else discord.Embed.Empty)
        embed.title = f"Wikipedia: {response.title}"
        embed.description = response.extract

        await ctx.send(embed=embed)

    @wiki.command()
    async def search(self, ctx: commands.Context, *, query: str) -> None:
        """Search for a Wikipedia article."""
        async with ctx.typing():
            if (response := await Wikipedia.search(query)) is None:
                fail = Embeds.status(success=False, desc="Wikipedia couldn't find anything.")
                return await ctx.send(embed=fail)

        embed = discord.Embed(description="", colour=Colours.regular, timestamp=Embeds.now())
        embed.set_footer(text="Powered by the Wikipedia API.", icon_url=Icons.wikipedia)

        for index, result in enumerate(response, 1):
            embed.description += f"**{index}**. [{result.title}]({result.link})\n"

        # Get a integer selection using Choice.prompt().
        if (choice := await Choices.prompt(ctx=ctx, embed=embed, n=5, author_only=True)) is None:
            return

        # Display the selected page.
        async with ctx.typing():
            response = await Wikipedia.article(response[choice].pageid)
            embed = discord.Embed(description=response.extract, colour=Colours.regular, timestamp=Embeds.now())
            embed.set_footer(text="Powered by the Wikipedia API.", icon_url=Icons.wikipedia)
            embed.set_thumbnail(url=response.thumbnail if response.thumbnail else discord.Embed.Empty)
            embed.title = f"Wikipedia: {response.title}"
            await ctx.send(embed=embed)

def setup(bot): bot.add_cog(Internet(bot))

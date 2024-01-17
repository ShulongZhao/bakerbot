import discord.app_commands as application
import discord.ext.commands as commands

import discord
import asyncio
import bot
import colours

class YunYun(commands.Cog):
    def __init__(self, bot: bot.Bot):
        self.bot = bot

    @application.command(description="Generate a Discord Embed.")
    @application.describe(title="The title of the Embed.")
    async def embed(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(thinking=True)
        package = discord.Embed(title)
        await interaction.followup.send(package)
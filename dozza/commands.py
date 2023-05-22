from dozza import backend

import discord.app_commands as application
import discord.ext.commands as commands

import discord
import logging
import aiohttp
import asyncio

class Dozza(commands.Cog):
    def __init__(self, bot: commands.Bot, logger: logging.Logger, session: aiohttp.ClientSession):
        self.logger = logger
        self.bot = bot

        self.session = session

    @application.command(description="Get a fucking joke.")
    async def joke(self, interaction: discord.Interaction):
        joke = await backend.funny(self.session)
        await interaction.response.send_message(joke.quip)

        if joke.followup is not None:
            await asyncio.sleep(3.0)
            await interaction.edit_original_response(content=f"{joke.quip}\n{joke.followup}")
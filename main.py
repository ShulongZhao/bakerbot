import discord
import pathlib
import model

if __name__ == "__main__":
    # Setup Discord API intents.
    intents = discord.Intents.default()
    intents.presences = False
    intents.typing = False
    intents.members = True

    # Setup the bot's activity.
    ver = discord.version_info
    name = "StarCraft II"
    activity = discord.Game(name=name)

    # Instantiate the bot with the required arguments.
    bot = model.YunYutility(command_prefix="^",
                           case_insensitive=True,
                           intents=intents,
                           activity=activity)

    # Load extensions from the cogs folder.
    for path in pathlib.Path("cogs").glob("*.py"):
        try:
            bot.load_extension(f"cogs.{path.stem}")
        except:
            pass

    bot.run()

import discord.ext.commands as commands
import model
import discord 
import requests
import json

class Genshin(commands.Cog):
    """Genshin Impact Stuff."""
    def __init__(self, bot: model.YunYutility):
        self.colours = bot.utils.Colours
        self.icons = bot.utils.Icons
        self.embeds = bot.utils.Embeds
        self.bot = bot
        
        API = 'https://api.genshin.dev/{}'

        char = API.format("characters/{}")
        art = API.format("artifacts/{}")
        wp = API.format("weapons/{}")
        imgc = 'https://rerollcdn.com/GENSHIN/Characters/{}.png'
        imga = 'https://rerollcdn.com/GENSHIN/Gear/{}.png'
        imgw = 'https://rerollcdn.com/GENSHIN/Weapon/NEW/{}.png'

        charlist = requests.get('https://api.genshin.dev/characters').text
        cl = json.loads(charlist)
        artlist = requests.get('https://api.genshin.dev/artifacts').text
        al = json.loads(artlist)
        wplist = requests.get('https://api.genshin.dev/weapons').text
        wl = json.loads(wplist)
    
    @commands.command()
    async def character(self, ctx, *, arg = None):
        """Searches Genshin Character"""
        async def character(ctx, *, arg=None):  
            if arg == None:
                embeded = discord.Embed(title="Character List")
                for i in cl:
                    response = requests.get(char.format(i)).text
                    data = json.loads(response)
                    embeded.add_field(name=i.title().replace("-", " "), value="{} Star | {}".format(data['rarity'],data['vision']), inline=True)
                await ctx.send(embed=embeded)

            elif arg != None:
                arg = arg.replace(" ", "-").lower()
                if arg in cl:
                    response = requests.get(char.format(arg)).text
                    data = json.loads(response)
                    embeded = discord.Embed(title=data['name'.replace("-", "")],description=data['description'])
                    if arg == "traveler-geo":
                        embeded.set_thumbnail(url='https://rerollcdn.com/GENSHIN/Characters/Traveler%20(Geo).png')
                    elif arg == "traveler-anemo":
                        embeded.set_thumbnail(url='https://rerollcdn.com/GENSHIN/Characters/Traveler%20(Anemo).png') 
                    else:
                        embeded.set_thumbnail(url=imgc.format(data['name']))
                        embeded.add_field(name="Vision", value=data['vision'], inline=True)
                        embeded.add_field(name="Weapon", value=data['weapon'], inline=True)
                    rrt = int(data['rarity'])
                    strg = "".join([" :star: ".format(x, x*2) for x in range(rrt)])
                    embeded.add_field(name="Rarity", value=strg, inline=True)
                    for skillTalents in data['skillTalents']:
                        embeded.add_field(name="{} : {}".format(skillTalents['unlock'], skillTalents['name']), value=skillTalents['description'].replace("\n\n", "\n"), inline=False)
                    for passiveTalents in data['passiveTalents']:
                        embeded.add_field(name="Passive Skill: {} \n({})".format(passiveTalents['name'], passiveTalents['unlock']), value=passiveTalents['description'].replace("\n\n", "\n"), inline=True)

                    await ctx.send(embed=embeded)
                else:
                    await ctx.send("{} not Found!".format(arg).title().replace("-", " "))

def setup(bot: model.YunYutility) -> None:
    cog = Genshin(bot)
    bot.add_cog(cog)
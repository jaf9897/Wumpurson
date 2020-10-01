import requests
import discord
from discord.ext import commands


class NasaPic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def apod(self, ctx):
        nasa_api = 'fPvgYFC86oLsL16zhiYNxORnA6EDhX35doNbQI4P'

        req = requests.get('https://api.nasa.gov/planetary/apod?api_key={0}'.format(nasa_api))
        if req.status_code == 200:
            print('Grabbed photo successfully')
            description = req.json()

            embed = discord.Embed(title="NASA Picture of the Day",
                                  description=description['explanation'],
                                  color=discord.Color.dark_grey()
                                  )
            # multiple images in the dictionary, but this gives the higher resolution one
            embed.set_image(url=description['hdurl'])

            await ctx.send(embed=embed)

        else:
            print("Photo was not able to be grabbed")


def setup(bot):
    bot.add_cog(NasaPic(bot))

import discord
from discord.ext import commands
import requests


class SpaceStation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def iss(self, ctx):
        gmaps_API = 'AIzaSyB_z3gerJFcy_TId8h9NJJEed94yem9RUM'
        # base url to access the gmaps static API
        gmaps_URL = 'https://maps.googleapis.com/maps/api/staticmap?center='
        req = requests.get("http://api.open-notify.org/iss-now.json")
        size = '640x640'

        if req.status_code == 200:
            print("Success")
            iss_pos = req.json()
            latitude_longitude = '{0},{1}'.format(iss_pos["iss_position"]["latitude"], iss_pos["iss_position"]["longitude"])

            # this abomination is to build the url that will give us the image for the lat long of the ISS
            map_url = '{0}{1}&zoom=6&size={2}&markers=color:red|{1}&key={3}'.format(gmaps_URL, latitude_longitude, size, gmaps_API)
            embed = discord.Embed(title="International Space Station Location",
                                  description=latitude_longitude,
                                  color=discord.Color.dark_grey()
                                  )
            embed.set_image(url=map_url)
            await ctx.send(embed=embed)

        elif req.status_code == 400:
            print("Not found")
            await ctx.send("Error reaching ISS location")


def setup(bot):
    bot.add_cog(SpaceStation(bot))

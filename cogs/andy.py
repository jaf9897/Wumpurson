import discord
import random
from discord.ext import commands

bot = commands.Bot(command_prefix='~')


class Andy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Commands
    @commands.command()
    async def chef(self, ctx):
        embed = discord.Embed(title='My chef 👩‍🍳', color=discord.Color.dark_grey())
        embed.set_image(url='https://iili.io/dSuQdQ.jpg')
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def commie(self, ctx):
        embed = discord.Embed(title='Мой бой', description='Сегодня мы пьем как короли, товарищ"',
                              color=discord.Color.dark_grey())
        embed.set_image(url='https://iili.io/dSuPqb.jpg')
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def love(self, ctx):
        embed = discord.Embed(title='My love, Lenahan ❤',
                              description="He's the kindest bro you will meet, and you should be grateful you met him",
                              color=discord.Color.dark_grey())
        embed.set_image(url='https://iili.io/d82ucJ.jpg')
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def forget(self, ctx):
        embed = discord.Embed(title="Let's not forget the true king💕",
                              description="Everyone take a minute and think about what he has done for you",
                              color=discord.Color.dark_grey())
        embed.set_image(url='https://iili.io/d8FFIV.jpg')
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def happy(self, ctx):
        embed = discord.Embed(title="The greatest smile in the land",
                              color=discord.Color.dark_grey())
        embed.set_image(url='https://iili.io/d8flef.jpg')
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def hostage(self, ctx):
        embed = discord.Embed(title="Please help... Wumpus got me",
                              color=discord.Color.dark_grey())
        embed.set_image(url='https://iili.io/drIS5l.jpg')
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def naked(self, ctx):
        embed = discord.Embed(title="Saucy photo with the bois 🍆",
                              color=discord.Color.dark_grey())
        embed.set_image(url='https://iili.io/d8fusI.jpg')
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def sexy(self, ctx):
        embed = discord.Embed(title="You can't stay mad at this face. Soon it will be mine",
                              color=discord.Color.dark_grey())
        embed.set_image(url='https://iili.io/d8350u.jpg')
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def updog(self, ctx):
        embed = discord.Embed(title="You got some up dog on your shoe",
                              color=discord.Color.dark_grey())
        embed.set_image(url='https://iili.io/dPC4DP.jpg')
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Andy(bot))

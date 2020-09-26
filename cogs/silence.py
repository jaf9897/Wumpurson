import asyncio
from datetime import datetime
import discord
import random
from pymongo import MongoClient
from discord.ext import commands

bot = commands.Bot(command_prefix='~')


async def is_silenced(message):
    return message.author == Silencer.silenced_user


async def is_nick(ctx):
    return ctx.author.id == 241842243441262593


class Silencer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    silenced_user = None
    silence_start = datetime(1970, 1, 1)
    silence_period = 0

    first_silence = False

    # Events
    @commands.Cog.listener('on_message')
    async def message_silencer(self, message):
        if message.author == self.bot.user or Silencer.silenced_user is None:
            return

        if (datetime.now() - Silencer.silence_start).total_seconds() > Silencer.silence_period:
            Silencer.silenced_user = None
            Silencer.silence_start = datetime(1970, 1, 1)
            Silencer.silence_period = 0

        await message.channel.purge(limit=3, check=is_silenced, after=Silencer.silence_start)

        if Silencer.first_silence and is_silenced(message):
            messages = [await message.channel.send(file=discord.File('top.png')),
                        await message.channel.send(message.content),
                        await message.channel.send(file=discord.File('bottom.png')),
                        await message.channel.send("You're coming with me.")]
            await asyncio.sleep(3)
            for m in messages:
                await m.delete()
            Silencer.first_silence = False

    @commands.Cog.listener('on_voice_state_update')
    async def channel_silencer(self, member, before, after):
        if (member == Silencer.silenced_user
                and before.channel is None
                and after.channel is not None
                and (datetime.now() - Silencer.silence_start).total_seconds() < Silencer.silence_period):
            await member.move_to(None)

    @commands.command()
    @commands.check(is_nick)
    async def silence(self, ctx, username, silence_time: int):
        try:
            if len(ctx.message.mentions) != 1:
                await ctx.send("Usage: ~silence <@user> <minutes to silence user>")
                return
            if Silencer.silenced_user is not None:
                await ctx.send("Only one soul can be silenced at a time.")
                return

            Silencer.silenced_user = ctx.message.mentions[0]
            Silencer.silence_start = datetime.now()
            Silencer.silence_period = silence_time * 60
            Silencer.first_silence = True

            await ctx.send("For {0} minutes, {1} shall be silenced.".format(silence_time, username))

        except ValueError:
            print("Usage: ~silence <@user> <minutes to silence user>")

    @silence.error
    async def silenceHandler(self, ctx, error):
        await ctx.send("Usage: ~silence <@user> <minutes to silence user>")


    @commands.command()
    async def unsilence(self, ctx):
        if Silencer.silenced_user is None:
            await ctx.send("No users are currently silenced")
            return

        pfp = Silencer.silenced_user.avatar_url
        Silencer.silenced_user = None
        Silencer.silence_start = datetime(1970, 1, 1)
        Silencer.silence_period = 0

        messages = []
        messages.append(await ctx.send(file=discord.File('drop.gif'))),
        await ctx.send(pfp)
        messages.append(await ctx.send("Return to the mortal realm."))
        await asyncio.sleep(2)
        for m in messages:
            await m.delete()


"""
async def grab(ctx, message):
    pfp = await message.author.avatar_url.read()
    await bot.user.edit(avatar=pfp)
    await bot.user.edit(username=ctx.author.name)
    await ctx.send(file=discord.File('top.png'))
    await ctx.send(message)
    await ctx.send(file=discord.File('bottom.png'))
    await ctx.send("You're coming with me.")
    await asyncio.sleep(3)
    await message.channel.purge(limit=10, check=is_me)
    with open('wump.jpg', 'rb') as f:
        fdata = f.read()
        await bot.user.edit(avatar=fdata)
    await bot.user.edit(username="wump2")
    print("fixed")"""


def setup(bot):
    bot.add_cog(Silencer(bot))

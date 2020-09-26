import discord
from discord.ext import commands
import random
import asyncio
import requests
import os
from bs4 import BeautifulSoup

# 746860942746452048 server id
TOKEN = 'NTUwNTAyNjgwNTM2MDIzMDQx.D1jiQQ.Y9f_MmsbsZcP8cdSVEaw18CFPyo'

blakes = open("blake.txt", "r")
proverbs = blakes.read().split('^')
blakes.close()

member_join = open("memberjoin.txt", "r")
member_join_phrases = member_join.read().split(',')
member_join.close()

bot = commands.Bot(command_prefix='~')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def commands(ctx):
    embed = discord.Embed(title='List of Commands',
                          description='Use "~" as the prefix',
                          color=discord.Color.dark_grey())
    embed.add_field(name='Andy Lenahan commands',
                    value='chef\n commie\n love\n forget\n happy\n nake\n sexy\n updog',
                    inline=False)
    embed.add_field(name='General Commands',
                    value='clear',
                    inline=False)
    await ctx.channel.send(embed=embed)


@bot.command()
async def person(ctx):
    await ctx.send("Generating image...")
    site = "https://thispersondoesnotexist.com/"
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]

    for url in urls:
        with open('image.jpg', 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)
    try:
        await ctx.send("This person does not exist:")
        await ctx.send(file=discord.File('image.jpg'))
    except ValueError:
        await ctx.send("Image file error.")


# Sends a random William Blake poem
@bot.command()
async def blake(ctx):
    print("blake invoked")
    msg = random.choice(proverbs)
    await ctx.send(msg)
    await asyncio.sleep(2)
    await ctx.send("So it is written.")


# Plays 3 songs at the same time really loud
@bot.command()
async def friends(ctx):
    try:
        channel = ctx.author.voice.channel
        await ctx.send("Initiating conflict resolution program.")
        await ctx.send("Use !resolved to terminate conflict resolution.")
        player = await channel.connect()
        player.play(discord.FFmpegPCMAudio("friends.mp3"), after=lambda: print('done'))
        while player.is_playing():
            await asyncio.sleep(1)  # Will leave when the entire song is finished
        player.stop()
        await player.disconnect()
    except AttributeError:
        await ctx.send("Must be in a voice channel to resolve conflicts.")


@bot.command()
async def resolved(ctx):
    if bot.voice_clients:
        for x in bot.voice_clients:
            await x.disconnect()
        await ctx.send("Conflict successfully resolved.")
    else:
        await ctx.send("No conflict resolution currently active.")


"""
React to emoji being added to a message
This won't do anything because that emoji doesn't exist here but all we'd have to do is change the "20" to whatever
emoji we'd want
"""


@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    emoji = reaction.emoji
    author = reaction.message.author
    if isinstance(emoji, discord.Emoji):
        name = emoji.name
    elif isinstance(emoji, str):
        name = emoji
    else:
        raise ValueError("Unknown emoji of type:", type(emoji))

    if author == bot.user and name == "20":
        await channel.send("There is nothing more small brained than small braining a machine, you coward.")


@bot.event
async def on_member_join(member):
    phrase = random.choice(member_join_phrases)
    channel = bot.get_channel(746860942746452051)
    await channel.send(phrase.format(member=member.mention))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)

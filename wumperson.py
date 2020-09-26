import discord
from discord.ext import commands
import random
import asyncio
import requests
import os
from bs4 import BeautifulSoup

# 746860942746452048 server id
TOKEN = 'NzU5MTgzMDgzMTE5MDUwNzg0.X25yVw.DHFx8AgWWqXc0Qg-Hc0o1YoCXz4'

blakes = open("blake.txt", "r")
proverbs = blakes.read().split('^')
blakes.close()

member_join = open("memberjoin.txt", "r")
member_join_phrases = member_join.read().split(',')
member_join.close()

bot = commands.Bot(command_prefix='~')
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('mindgames'))
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title='✅ Successfully deleted ' + str(amount) + ' messages')
    await ctx.channel.send(embed=embed)
    print(str(amount) + ' messages were deleted')


# @bot.command()
# async def kick(ctx, member : discord.Member, *, reason=None):
#     await member.kick(reason=reason)
#
# @bot.command()
# async def ban(ctx, member : discord.Member, *, reason=None):
#     await member.ban(reason=reason)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title='List of Commands',
                          description='Use "~" as the prefix',
                          color=discord.Color.dark_grey())
    embed.add_field(name='Andy Lenahan commands',
                    value='chef\n commie\n love\n forget\n happy\n nake\n sexy\n updog',
                    inline=False)
    embed.add_field(name='clear',
                    value='Deletes a given amount of messages from the channel the command was sent from.\n'
                          'Specify number of messages after the ~clear, 5 by default.',
                    inline=False)
    embed.add_field(name='silence',
                    value='Prevents a user from speaking in text and voice for the given amount of minutes.\n'
                          'Usage: ~silence <@user> <minutes to silence user>',
                    inline=False)
    embed.add_field(name='piggybank',
                    value='Shows the total money in the swear jar, as well as the top 3 contributors.',
                    inline=False)
    embed.add_field(name='mypiggybank',
                    value='Shows you how much you\'ve contributed to the swear jar',
                    inline=False)
    embed.add_field(name='blake',
                    value='Sends a random poem written by English poet William Blake (1757-1827).',
                    inline=False)
    embed.add_field(name='person',
                    value='Retrieves a person that does not exist (face generated by AI).',
                    inline=False)
    embed.add_field(name='friends',
                    value='Deploys emergency conflict resolution procedure. You must be in a voice channel for proper execution.\n'
                          '(Plays three songs about friendship simultaneously.)\n'
                          'Stop with ~resolved.',
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
    print(bot.user)
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
        await ctx.send("Use ~resolved to terminate conflict resolution.")
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

    embed = discord.Embed(title='List of Commands',
                          description=f'{member.mention}, use "~" as the prefix',
                          color=discord.Color.dark_grey())
    embed.add_field(name='Andy Lenahan commands',
                    value='chef\n commie\n love\n forget\n happy\n nake\n sexy\n updog',
                    inline=False)
    embed.add_field(name='General Commands',
                    value='clear\nsilence\npiggybank\nmypiggyank',
                    inline=False)
    await channel.send(embed=embed)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)

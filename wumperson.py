import discord
from discord.ext import commands
import random
import asyncio


TOKEN = 'NTUwNTAyNjgwNTM2MDIzMDQx.D1jiQQ.Y9f_MmsbsZcP8cdSVEaw18CFPyo'
blakes = open("blake.txt", "r")
proverbs = blakes.read().split('^')
blakes.close()
member_join = open("memberjoin.txt", "r")
member_join_phrases = member_join.read().split(',')

mentions = dict()
bot = commands.Bot(command_prefix='!')
client = discord.Client()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print(random.choice(member_join_phrases))

#Sends a random William Blake poem
@bot.command()
async def person(ctx):
    print("person invoked")
    msg = random.choice(proverbs)
    await ctx.send(msg)
    await asyncio.sleep(2)
    await ctx.send("So it is written.")

#Plays 3 songs at the same time really loud
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
    try:
        for x in bot.voice_clients:
            return await x.disconnect()
        ctx.send("Conflict successfully resolved.")
    except:
        ctx.send("No conflict resolution currently active.")

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
    channel = bot.get_channel(746860942746452051)
    await channel.send(random.choice(member_join_phrases))

bot.run(TOKEN)
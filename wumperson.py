import discord
from discord.ext import commands
import random
import asyncio
import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

# 746860942746452048 server id

# Connection URL for MongoDB
mango_url = "mongodb+srv://dentifrag:pBn6ixQcgHEgeOYS@wumperson-swearing-poin.jgmys.mongodb.net/test"
cluster = MongoClient(mango_url)
db = cluster["swearingPoints"]
collection = db["Points for Swearing"]

TOKEN = 'NTUwNTAyNjgwNTM2MDIzMDQx.D1jiQQ.Y9f_MmsbsZcP8cdSVEaw18CFPyo'

blakes = open("blake.txt", "r")
proverbs = blakes.read().split('^')
blakes.close()

member_join = open("memberjoin.txt", "r")
member_join_phrases = member_join.read().split(',')
member_join.close()

swears_file = open('swears.txt', 'r')
swears = swears_file.read().split(',')

ricardo_gifs_file = open('Ricardo gifs.txt', 'r')
ricardo_gifs = ricardo_gifs_file.read().split(',')

mentions = dict()
bot = commands.Bot(command_prefix='~')
client = discord.Client()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


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


@bot.command()
async def tip(ctx):
    user = ctx.author.name
    embed = discord.Embed(title="Thanks for the tip 🍆",
                          description='Your tip will be added',
                          color=discord.Color.dark_grey())
    embed.set_image(url=random.choice(ricardo_gifs))
    await ctx.send(embed=embed)
    # after sending the embed, bot is either sending updated points,
    # or is creating a new member if they haven't tipped before
    my_query = {"_id": ctx.author.id}
    if (collection.count_documents(my_query) == 0):
        post = {"_id": ctx.author.id, "tips": 1}
        collection.insert_one(post)
        print('User was added to database')
    else:
        user = collection.find(my_query)
        for result in user:
            score = result["score"]
        score += 1
        collection.update_one({"_id": ctx.author.id}), {"$set": {"score": score}}
        print("Value was updated")


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


@bot.listen('on_message')
async def swearing(message):
    # ignoring messages from the bot, or else it causes ifinite ricardo
    if message.author == bot.user:
        return

    if any(bad_words in message.content.strip().lower() for bad_words in swears):
        embed = discord.Embed(title="Swearing isn't permitted, shit head",
                              description=f"""{message.author.mention}, use '~tip' to leave a tip""",
                              color=discord.Color.dark_grey())
        embed.set_image(url='https://iili.io/d8fGX2.jpg')
        await message.channel.send(embed=embed)


bot.run(TOKEN)

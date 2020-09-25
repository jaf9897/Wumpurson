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
swears_file.close()

ricardo_gifs_file = open('Ricardo gifs.txt', 'r')
ricardo_gifs = ricardo_gifs_file.read().split(',')

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
async def piggybank(ctx):
    leaderboard_order = []
    users_in_descending_order = []
    scores_in_descending_order = []
    # this grabs the the collection from mongodb
    # and sorts them from highest to lowest
    for i in collection.find().sort('tips', -1):
        leaderboard_order.append(i)
    #TODO add these usernames and tips to an embed to display users rank
    for users in leaderboard_order:
        users_in_descending_order.append(users['_id'])
        scores_in_descending_order.append(users['tips'])
    print(users_in_descending_order)
    print(scores_in_descending_order)

    # embed = discord.Embed(title="You guys have some dirty mouths 👄",
    #                       color=discord.Color.dark_grey())
    # embed.set_thumbnail(url='https://i.ibb.co/ngsbzkf/988532.jpg')
    # embed.add_field(name="Most Tips in the Swear Jar", value=leaderboard_order, inline=True)
    # await ctx.channel.send(embed=embed)


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
    # ignoring messages from the bot, or else it causes infinite ricardo
    if message.author == bot.user:
        return

    if any(bad_words in message.content.strip().lower() for bad_words in swears):
        embed = discord.Embed(title="Swearing isn't permitted, shit head",
                              description=f"""{message.author.mention}, your tip will be added to the swear jar""",
                              color=discord.Color.dark_grey())
        embed.set_image(url=random.choice(ricardo_gifs))
        await message.channel.send(embed=embed)

        my_query = {"_id": message.author.name}
        if collection.count_documents(my_query) == 0:
            post = {"_id": message.author.name, "tips": 1}
            collection.insert_one(post)
            print('User was added to database')
        else:
            user = collection.find(my_query)
            for result in user:
                score = result["tips"]
            score += 1
            collection.update_one({"_id": message.author.name}, {"$set": {"tips": score}})
            print("Value was updated")


bot.run(TOKEN)

import discord
import random
from pymongo import MongoClient
from discord.ext import commands

mango_url = "mongodb+srv://dentifrag:pBn6ixQcgHEgeOYS@wumperson-swearing-poin.jgmys.mongodb.net/test"
cluster = MongoClient(mango_url)
db = cluster["swearingPoints"]
collection = db["Points for Swearing"]

swears_file = open('swears.txt', 'r')
swears = swears_file.read().split(',')
swears_file.close()

ricardo_gifs_file = open('Ricardo gifs.txt', 'r')
ricardo_gifs = ricardo_gifs_file.read().split(',')
ricardo_gifs_file.close()

bot = commands.Bot(command_prefix='~')


class Swearing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener('on_message')
    async def swearing(self, message):
        # ignoring messages from the bot, or else it causes infinite ricardo
        if message.author == bot.user:
            return

        if any(bad_words in message.content.lower().split() for bad_words in swears):
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
                    tips = result["tips"]
                tips += 1
                collection.update_one({"_id": message.author.name}, {"$set": {"tips": tips}})
                print("Value was updated")

    # Commands
    @commands.command()
    async def piggybank(self, ctx):
        leaderboard_order = []
        users_order = []
        tips_order = []
        total_tips = 0
        # this grabs the the collection from mongodb
        # and sorts them from highest to lowest
        for i in collection.find().sort('tips', -1):
            leaderboard_order.append(i)
        for users in leaderboard_order:
            users_order.append(users['_id'])
            tips_order.append(users['tips'])
            total_tips += users['tips']

        embed = discord.Embed(title="You guys have some dirty mouths 👄", color=discord.Color.dark_grey())
        embed.set_thumbnail(url='https://i.ibb.co/ngsbzkf/988532.jpg')
        embed.add_field(name="Total Money in the Piggy Bank", value='$' + str(total_tips), inline=True)
        embed.add_field(name="Most Tips in the Swear Jar", value="I'll spend it on a new thong", inline=False)
        # put users and scores in via index because they'll be in order from greatest to least from being sorted
        embed.add_field(name="First place 🏆",
                        value=users_order[0] + ': $' + str(tips_order[0]), inline=False)
        embed.add_field(name="Second place",
                        value=users_order[1] + ': $' + str(tips_order[1]), inline=False)
        embed.add_field(name="Third place", value=users_order[2] + ': $' + str(tips_order[2]),
                        inline=False)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def mypiggybank(self, ctx):
        """
        there is no name function to get the username by itself using 'ctx'
        so this is splitting the whole username (e.g. username#1234)
        at the '#' symbol
        """
        author = str(ctx.message.author).split('#')[0]
        leaderboard_order = []
        users = []
        tips = []
        # finding and sorting users from DB by tips
        for i in collection.find().sort('tips', -1):
            leaderboard_order.append(i)
            # spliting user names and tips into separate lists
        for i in leaderboard_order:
            users.append(i['_id'])
            tips.append(i['tips'])
        if author in users:
            author_index = users.index(author)
            # adding one to get the rank of the user since counting starts at 0
            author_rank = users.index(author) + 1
            authors_tip = tips[author_index]

            embed = discord.Embed(title="Your rank is:",
                                  description='#' + str(author_rank) + ' out of ' + str(len(users)),
                                  color=discord.Color.dark_grey())
            embed.add_field(name='Your tips:', value='$' + str(authors_tip), inline=False)
            embed.set_image(url='https://i.ibb.co/3fdqg5Q/zmvotbbjgj031.jpg')
            embed.set_footer(text='Thanks for all your tips 😉')
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Doesn't seem like you've tipped the tip jar before",
                                  description=f"""{ctx.message.author.mention}, start working that mouth of yours 👄""",
                                  color=discord.Color.dark_grey())
            embed.set_image(url='https://i.ibb.co/hFf6Pp0/D-Kp-Tj-ZXs-AAd-G1n.jpg')
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Swearing(bot))

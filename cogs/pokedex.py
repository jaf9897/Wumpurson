import discord
from discord.ext import commands
import pypokedex


class Pokedex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pokedex(self, ctx, pokemon):
        try:
            pokemon = pypokedex.get(name=pokemon)
            base_abilities = []
            base_stats = []
            pokemon_types = []
            sprite = pokemon.sprites

            for abilities in pokemon.abilities:
                base_abilities.append(abilities.name)
            for stats in pokemon.base_stats:
                # all values are initially grabbed as ints
                base_stats.append(str(stats))
            for types in pokemon.types:
                pokemon_types.append(types)

            embed = discord.Embed(title="Who's that pokemon?", description="It's {0}, bitch".format(pokemon.name.capitalize()),
                                  color=discord.Color.dark_grey())
            embed.set_thumbnail(url=sprite.front["default"])
            embed.add_field(name="Abilities:", value=', '.join(base_abilities), inline=False)
            embed.add_field(name="Height:", value=str(pokemon.height) + 'ft', inline=False)
            embed.add_field(name="Weight:", value=str(pokemon.weight) + 'lb(s)', inline=False)

            embed.add_field(name="HP:", value=base_stats[0], inline=True, )
            embed.add_field(name="Atk:", value=base_stats[1], inline=True, )
            embed.add_field(name="Def:", value=base_stats[2], inline=True, )
            embed.add_field(name="Sp Atk:", value=base_stats[3], inline=True, )
            embed.add_field(name="Sp Def:", value=base_stats[4], inline=True, )
            embed.add_field(name="Speed:", value=base_stats[5], inline=True, )

            embed.add_field(name="Type(s): ", value=','.join(pokemon_types), inline=False)

            await ctx.send(embed=embed)
        except:
            await ctx.send("That pokemon doesn't exist")


def setup(bot):
    bot.add_cog(Pokedex(bot))

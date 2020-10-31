from discord.ext import commands
import random as rd


class Random(commands.Cog):
    @commands.command(brief='Get a random number in a range.')
    async def random(self, ctx, _min: int, _max: int):
        await ctx.send('Your number is %d' % (rd.randint(_min, _max)))

    @commands.command(brief='Show the name of a random user.', aliases=['randomuser'])
    async def random_user(self, ctx: commands.Context):
        member = rd.choice(ctx.guild.members)
        await ctx.send(member.name)

    @random.error
    async def random_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Invalid input.')

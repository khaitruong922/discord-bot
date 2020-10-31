from discord.ext import commands


class Greeting(commands.Cog):
    @commands.command(brief='Make bot say hello :D')
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command(brief='Make bot say goodbye :D')
    async def bye(self, ctx: commands.Context):
        await ctx.send(f'Goodbye {ctx.author.name}!')

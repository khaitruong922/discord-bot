from discord.ext import commands


class Task(commands.Cog):
    @commands.command(brief='Clear a number of messages in a channel.')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount=1):
        await ctx.channel.purge(limit=amount)

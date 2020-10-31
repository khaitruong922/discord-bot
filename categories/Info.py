from discord.ext import commands
from datetime import datetime

REPO_URL = 'https://github.com/khaitruong922/discord-bot'
TIME_FORMAT = '%d/%m/%Y %H:%M:%S'


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Show current latency.')
    async def ping(self, ctx: commands.Context):
        await ctx.trigger_typing()
        await ctx.send(str(int(self.bot.latency * 1000)) + ' ms')

    @commands.command(brief='Show current time.')
    async def now(self, ctx: commands.Context):
        await ctx.send(datetime.now().strftime(TIME_FORMAT))

    @commands.command(brief='Show bot info.')
    async def info(self, ctx: commands.Context):
        await ctx.send(
            f'Source code: {REPO_URL}')

    @commands.command(brief='Display current channel and server.')
    async def here(self, ctx: commands.Context):
        await ctx.send(f'{ctx.guild}\n/{ctx.channel}')

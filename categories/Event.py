from discord.ext import commands
import discord
import random as rd


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_ids = {
            'welcome': 770950580373946390,
            'bot-command': 751355121455071233,
        }

    @commands.Cog.listener()
    async def on_ready(self):
        game = ['League of Legends', 'League of Runeterra', 'VALORANT', 'Apex Legends', 'Among Us']
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(rd.choice(game)))
        # await bot.get_channel(channel_ids.get('bot-command')).send("I'm online.")
        print('Bot is ready.')

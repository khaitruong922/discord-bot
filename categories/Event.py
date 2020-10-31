from discord.ext import commands
import discord
import random as rd

CHANNEL_IDS = {
    'welcome': 770950580373946390,
    'bot-command': 751355121455071233,
}


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        game = ['League of Legends', 'League of Runeterra', 'VALORANT', 'Apex Legends', 'Among Us']
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(rd.choice(game)))
        # await self.bot.get_channel(CHANNEL_IDS.get('bot-command')).send("I'm online.")
        print('Bot is ready.')

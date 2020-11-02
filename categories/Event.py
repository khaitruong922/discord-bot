from discord.ext import commands
import discord
import random as rd
import json

CHANNEL_IDS = {
    'welcome': 770950580373946390,
    'bot-command': 751355121455071233,
}
BAD_WORDS_FILE = 'data/bad_words.json'


def get_bad_words():
    with open(BAD_WORDS_FILE) as file:
        return json.load(file)


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        game = ['League of Legends', 'League of Runeterra', 'VALORANT', 'Apex Legends', 'Among Us']
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(rd.choice(game)))
        # await self.bot.get_channel(CHANNEL_IDS.get('bot-command')).send("I'm online.")
        print('Bot is ready.')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        content = message.content.lower()
        channel = message.channel
        bad_words = get_bad_words()
        name = message.author.name
        bad = any(word in bad_words for word in content.split())
        if 'bot ngu' in content:
            await channel.send(f'Dám chửi t à {name}?')
            return
        if not bad:
            return
        await channel.send(f'Không nói bậy nha bạn {name} !!')

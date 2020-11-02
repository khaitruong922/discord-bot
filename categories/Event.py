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
        content = message.content
        bad_words = get_bad_words()
        bad = any(word in bad_words for word in content.split())
        if not bad:
            return
        channel = message.channel
        name = message.author.name
        await channel.send(f'Không nói bậy nha bạn {name} !!')

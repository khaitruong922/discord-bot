from discord.ext import commands
import discord
import random as rd
from utils.JSONFileIO import JSONFileIO

CHANNEL_IDS = {
    'welcome': 770950580373946390,
    'bot-command': 751355121455071233,
}
AUTO_REPLY_CHANNELS = [
    751355121455071233,
]

BOT_OFFEND_WORDS = ['bot ngu', 'bot oc cho', 'dm bot', 'đm bot', 'bot óc chó']
blacklist_file = JSONFileIO('data/blacklist.json')


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
        if channel.id in AUTO_REPLY_CHANNELS:
            ctx = await self.bot.get_context(message)
            chat_cog = self.bot.get_cog('Chat')
            if chat_cog is not None:
                await chat_cog.chat(ctx, content, no_default_reply=True)
        bad_words = blacklist_file.get()
        name = message.author.name
        offend_bot = any(word in content for word in BOT_OFFEND_WORDS)
        if offend_bot:
            await channel.send(f'Dám chửi t à {name}?')
            return
        bad = any(word in bad_words for word in content.split())
        if bad:
            await channel.send(f'Không nói bậy nha bạn {name} !!')
            return

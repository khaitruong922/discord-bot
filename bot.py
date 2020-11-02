import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

from categories.Chat import Chat
from categories.TicTacToe import TicTacToe
from categories.GitHub import GitHub
from categories.LOL import LOL
from categories.Random import Random
from categories.Event import Event
from categories.Greeting import Greeting
from categories.Info import Info
from categories.Task import Task

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents)

COGS = [
    Event(bot),
    Chat(),
    Greeting(),
    Random(),
    Info(bot),
    # LOL(),
    # GitHub(),
    # TicTacToe(),
    Task(),
]

for cog in COGS:
    bot.add_cog(cog)

bot.run(TOKEN)

import discord
import requests
import random as rd
import os
from Board import Board
from File import File
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix='.')
TEXT_FILENAME = 'log.txt'
TEXT_FILE = File(TEXT_FILENAME)
board = Board()


@client.event
async def on_ready():
    game = ['League of Legends', 'League of Runeterra', 'VALORANT', 'Apex Legends', 'Among Us']
    await client.change_presence(status=discord.Status.online, activity=discord.Game(rd.choice(game)))
    print('Bot is ready.')


@client.event
async def on_member_join(member):
    print('%s has joined the gang.' % (member))


@client.event
async def on_member_remove(member):
    print('%s has left the gang.' % (member))


@client.command()
async def ping(ctx):
    await ctx.send(str(int(client.latency * 1000)) + ' ms')


@client.command()
async def now(ctx):
    await ctx.send(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


@client.command()
async def info(ctx):
    await ctx.send('I am a bot.')


@client.command()
async def random(ctx, min, max):
    await ctx.send('Your number is %d' % (rd.randint(int(min), int(max))))


@random.error
async def random_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Invalid input.')


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


def fetch_champion_data(name):
    try:
        res = requests.get(f'http://ddragon.leagueoflegends.com/cdn/10.21.1/data/en_US/champion/{name}.json')
        res.raise_for_status()
        return res.json().get('data').get(name)
    except:
        return None


def get_champion_name(args):
    name = ' '.join(args).title()
    name = ''.join(name.split())
    return name


@client.command()
async def lore(ctx, *args):
    name = get_champion_name(args)
    data = fetch_champion_data(name)
    if not data:
        await ctx.send('No data found.')
        return
    lore = data.get('lore')
    await ctx.send(lore)


@client.command()
async def skill(ctx, *args):
    name = get_champion_name(args[:-1])
    key = args[-1].upper()
    # print(name, key)

    data = fetch_champion_data(name)
    if not data:
        await ctx.send('No data found.')
        return
    if key == 'P':
        passive = data.get('passive')
        passive_name = passive.get('name')
        desc = passive.get('description')
        content = f'{key}: {passive_name}\n{desc}'
        await ctx.send(content)
        return
    key_to_index = {'Q': 0, 'W': 1, 'E': 2, 'R': 3}
    index = key_to_index[key]

    spells = data.get('spells')
    spell = spells[index]
    spell_name = spell.get('name')
    desc = spell.get('description')
    content = f'{key}: {spell_name}\n{desc}'
    await ctx.send(content)


@client.command()
async def skin(ctx, *args):
    name = get_champion_name(args)
    data = fetch_champion_data(name)
    if not data:
        await ctx.send('No data found.')
        return
    skins = data.get('skins')
    content = ', '.join([skin.get('name') for skin in skins][1:])
    await ctx.send(content)


@client.command(aliases=['tip'])
async def tips(ctx, *args):
    name = get_champion_name(args)
    data = fetch_champion_data(name)
    if not data:
        await ctx.send('No data found.')
        return
    ally_tips = data.get('allytips')
    counter_tips = data.get('enemytips')
    ally_content = '\n'.join(f'{i + 1}. {ally_tip}' for i, ally_tip in enumerate(ally_tips))
    counter_content = '\n'.join(f'{i + 1}. {counter_tip}' for i, counter_tip in enumerate(counter_tips))
    content = f'- Ally tips:\n{ally_content}\n- Counter tips:\n{counter_content}'
    await ctx.send(content)


@client.command(aliases=['write'])
async def log(ctx, *args):
    message = ' '.join(args)
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    username = ctx.message.author.name
    content = f'[{time}] {username}: {message} \n'
    TEXT_FILE.append(content)

    await ctx.send(content)


@client.command()
async def github(ctx, username):
    await ctx.send(f'https://github.com/{username}')


@client.command()
async def repo(ctx, username, repo):
    await ctx.send(f'https://github.com/{username}/{repo}')


@client.command(aliases=['view', 'viewlog'])
async def view_log(ctx, latest=10):
    content = TEXT_FILE.get_latest_lines(latest)
    embed = discord.Embed(
        title=f'Log history ({latest} latest) ',
        description=content,
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


@client.command(aliases=['clearlog'])
async def clear_log(ctx, latest=1):
    content = TEXT_FILE.get_lines_until_latest(latest)
    TEXT_FILE.write(content)
    await ctx.send(f"Clear {latest} line(s).")


def get_guide_embed():
    return discord.Embed(
        title=f'Discord Tic Tac Toe',
        description=board.get_guide(),
        color=discord.Color.blue()
    )


def get_board_embed():
    return discord.Embed(
        description=board.get_board_data(),
        color=discord.Color.red()
    )


def get_turn_embed():
    return discord.Embed(
        description=board.get_next_turn_message(),
        color=discord.Color.purple()
    )


def get_win_message_embed():
    tie = board.get_win_message() == board.TIE
    title = "Tie" if tie else "Victory"
    description = "" if tie else board.get_win_message()
    color = discord.Color.gold() if tie else discord.Color.green()
    return discord.Embed(
        title=title,
        description=description,
        color=color
    )


@client.command(aliases=['ttt'])
async def tictactoe(ctx):
    board.reset_board()
    await ctx.send(embed=get_guide_embed())
    await ctx.send(embed=get_board_embed())
    await ctx.send(embed=get_turn_embed())


@client.command(aliases=['m', 'place'])
async def move(ctx, *args):
    message = ' '.join(*args)
    status = board.get_move_status(message)

    if status != board.SUCCESS_MESSAGE:
        await ctx.send(status)
        return

    move = int(message)
    board.place(move)

    await ctx.send(embed=get_board_embed())

    # Print out message and reset game if there is a winner or tie.
    if board.get_win_message():
        await ctx.send(embed=get_win_message_embed())
        board.reset_board()
        return
    # If not, other player will play.
    board.switch_player()
    await ctx.send(embed=get_turn_embed())


client.run(TOKEN)

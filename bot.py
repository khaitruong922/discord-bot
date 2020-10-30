import discord
import requests
import random as rd
import os
import json
from Board import Board
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MODEL_FILENAME = 'chat.json'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents)
REPO_URL = 'https://github.com/khaitruong922/discord-bot'
TIME_FORMAT = '%d/%m/%Y %H:%M:%S'
board = Board()
channel_ids = {
    'welcome': 770950580373946390,
    'bot-command': 751355121455071233,
}


@bot.event
async def on_ready():
    game = ['League of Legends', 'League of Runeterra', 'VALORANT', 'Apex Legends', 'Among Us']
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(rd.choice(game)))
    # await bot.get_channel(channel_ids.get('bot-command')).send("I'm online.")
    print('Bot is ready.')


@bot.event
async def on_guild_join(member):
    await bot.get_channel(channel_ids.get('welcome')).send(f"{member} has joined the server.")


@bot.event
async def on_guild_remove(member):
    await bot.get_channel(channel_ids.get('welcome')).send(f"{member} has left the server.")


@bot.command(brief='Show current latency.')
async def ping(ctx: commands.Context):
    await ctx.trigger_typing()
    await ctx.send(str(int(bot.latency * 1000)) + ' ms')


@bot.command(brief='Show current time.')
async def now(ctx: commands.Context):
    await ctx.send(datetime.now().strftime(TIME_FORMAT))


@bot.command(brief='Make bot say hello :D')
async def hello(ctx: commands.Context):
    await ctx.send(f'Hello {ctx.author.name}!')


def format_question(question):
    return ''.join(c for c in question if c.isalnum()).lower()


def format_answer(answer):
    return answer.strip()


@bot.command(brief='Train bot.')
async def train(ctx: commands.Context, *args):
    questions_content, answers_content = ' '.join(args).split("|")
    questions = list(map(format_question, questions_content.split('&')))
    answers = list(map(format_answer, answers_content.split('&')))
    with open(MODEL_FILENAME) as file:
        data = json.load(file)
        for question in questions:
            file_answers = data.get(question, [])
            for answer in answers:
                if answer not in file_answers:
                    file_answers.append(answer)
            data[question] = file_answers
        with open(MODEL_FILENAME, 'w') as w_file:
            json_text = json.dumps(data, indent=4)
            w_file.write(json_text)
    await ctx.send(f':thumbsup:')


@bot.command(aliases=['ask', 'c'], brief='Ask bot.')
async def chat(ctx: commands.Context, *args):
    question = ''.join(args)
    question_key = format_question(question)
    with open(MODEL_FILENAME) as file:
        data = json.load(file)
        answers = data.get(question_key, [])
        if not answers:
            answers = data.get('ngoaitamhieubiet', [])
            if not answers:
                answers = ["Em không biết câu này. Dạy em với [name] ơi :yum:"]
        answer = rd.choice(answers)
        answer = parse_answer(answer, ctx)
        await ctx.send(answer)


def parse_answer(answer, ctx: commands.Context):
    if "[" not in answer:
        return answer
    markdown_dict = {
        "[name]": ctx.author.name,
        "[random-name]": rd.choice(ctx.guild.members).name
    }
    for markdown, str_to_replace in markdown_dict.items():
        answer = answer.replace(markdown, str_to_replace)
    return answer


@bot.command(brief='Make bot say goodbye :D')
async def bye(ctx: commands.Context):
    await ctx.send(f'Goodbye {ctx.author.name}!')


@bot.command(brief='Show bot info.')
async def info(ctx: commands.Context):
    await ctx.send(
        f'Source code: {REPO_URL}\nLast updated: {datetime.fromtimestamp(os.path.getmtime(__file__)).strftime(TIME_FORMAT)}')


@bot.command(brief='Get a random number in a range.')
async def random(ctx, _min: int, _max: int):
    await ctx.send('Your number is %d' % (rd.randint(_min, _max)))


@random.error
async def random_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('Invalid input.')


@bot.command(brief='Display current channel and server.')
async def here(ctx: commands.Context):
    await ctx.send(f'Server: {ctx.guild}\nChannel: {ctx.channel}')


@bot.command(brief='Clear a number of messages in a channel')
@commands.has_permissions(manage_messages=True)
async def clear(ctx: commands.Context, amount=1):
    await ctx.channel.purge(limit=amount)


def fetch_champion_data(name):
    try:
        res = requests.get(f'http://ddragon.leagueoflegends.com/cdn/10.21.1/data/en_US/champion/{name}.json')
        res.raise_for_status()
        return res.json().get('data').get(name)
    except requests.exceptions.HTTPError:
        return None


def fetch_github_user(username):
    try:
        res = requests.get(f'https://api.github.com/users/{username}')
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError:
        return None


def fetch_github_repo(username, repo_name):
    try:
        res = requests.get(f'https://api.github.com/repos/{username}/{repo_name}')
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError:
        return None


def get_champion_name(args):
    name = ' '.join(args).title()
    name = ''.join(name.split())
    return name


@bot.command(brief='Show the lore of a LoL champion')
async def lore(ctx: commands.Context, *args):
    name = get_champion_name(args)
    data = fetch_champion_data(name)
    if not data:
        await ctx.send('No data found.')
        return
    name = data.get('name')
    title = data.get('title')
    lore_content = data.get('lore')
    content = f'{name} - {title}\n{lore_content}'
    await ctx.send(content)


@bot.command(brief='Show an ability description of a LoL champion', aliases=['ability'])
async def skill(ctx: commands.Context, *args):
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
    cooldown = spell.get('cooldown')
    cooldown = '/'.join(map(str, cooldown))
    cost = spell.get('cost')
    cost = '/'.join(map(str, cost))
    desc = spell.get('description')
    content = f'{key}: {spell_name}\nCooldown: {cooldown}\nCost: {cost}\n{desc}'
    await ctx.send(content)


@bot.command(brief='List all skins of a LoL champion.')
async def skin(ctx: commands.Context, *args):
    name = get_champion_name(args)
    data = fetch_champion_data(name)
    if not data:
        await ctx.send('No data found.')
        return
    skins = data.get('skins')
    content = ', '.join([skin.get('name') for skin in skins][1:])
    await ctx.send(content)


@bot.command(aliases=['tip'], brief='List all tips related to a LoL champion.')
async def tips(ctx: commands.Context, *args):
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


@bot.command(brief='Show the name of a random user.', aliases=['randomuser'])
async def random_user(ctx: commands.Context):
    member = rd.choice(ctx.guild.members)
    await ctx.send(member.name)


@bot.command(brief='Show the info of a GitHub user.')
async def github(ctx: commands.Context, username):
    user = fetch_github_user(username)
    if not user:
        await ctx.send(f'User {username} is not found.')
        return
    title = f'{username}'
    url = f'https://github.com/{username}'
    followers = user.get("followers")
    following = user.get("following")
    public_repos = user.get("public_repos")
    avatar_url = user.get("avatar_url")
    desc = f'Followers: {followers}\nFollowings: {following}\nPublic repos: {public_repos}'
    embed = discord.Embed(
        title=title,
        url=url,
        description=desc,
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=avatar_url)
    await ctx.send(embed=embed)


@bot.command(brief='Show the info of a GitHub repo.')
async def repo(ctx: commands.Context, username, repo_name):
    repo = fetch_github_repo(username, repo_name)
    if not repo:
        await ctx.send(f'Repository {username}/{repo_name} is not found.')
        return
    url = f'https://github.com/{username}/{repo_name}'
    title = repo.get('full_name')
    stars = repo.get('stargazers_count')
    watchers = repo.get('watchers_count')
    language = repo.get('language')
    desc = f'Stars: {stars}\nWatchers: {watchers}\nLanguage: {language}'
    avatar_url = repo.get("owner").get("avatar_url")
    embed = discord.Embed(
        title=title,
        url=url,
        description=desc,
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=avatar_url)
    await ctx.send(embed=embed)


@bot.command(aliases=['ttt'], brief='Show TicTacToe rules.')
async def tictactoe(ctx: commands.Context):
    board.reset_board()
    await ctx.send(embed=board.get_guide_embed())
    await ctx.send(embed=board.get_board_embed())
    await ctx.send(embed=board.get_turn_embed())


@bot.command(aliases=['m'], brief='Make a move in TicTacToe board.', description='Valid inputs: 1-9')
async def move(ctx: commands.Context, *args):
    message = ' '.join(*args)
    status = board.get_move_status(message)

    if status != board.SUCCESS_MESSAGE:
        await ctx.send(status)
        return

    move = int(message)
    board.place(move)

    await ctx.send(embed=board.get_board_embed())

    # Print out message and reset game if there is a winner or tie.
    if board.get_win_message():
        await ctx.send(embed=board.get_win_message_embed())
        board.reset_board()
        return
    # If not, other player will play.
    board.switch_player()
    await ctx.send(embed=board.get_turn_embed())


bot.run(TOKEN)

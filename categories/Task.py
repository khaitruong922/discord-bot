from discord.ext import commands
import json

BAD_WORDS_FILE = 'data/bad_words.json'


class Task(commands.Cog):
    @commands.command(brief='Clear a number of messages in a channel.')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount=1):
        await ctx.channel.purge(limit=amount)

    @commands.command(brief='Add restricted word.')
    async def ban(self, ctx: commands.Context, word):
        bad_words = get_bad_words()
        if word in bad_words:
            await ctx.send(f'Từ {word} đã có trong danh sách đen rồi.')
            return
        bad_words.append(word)
        write_bad_words(bad_words)
        await ctx.send(f'Từ {word} mới vô danh sách đen. Chúc bạn xài từ cẩn thận.')

    @ban.error
    async def ban_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Muốn ban hay không nói một lời.')


def get_bad_words():
    with open(BAD_WORDS_FILE) as file:
        return json.load(file)


def write_bad_words(data):
    with open(BAD_WORDS_FILE, 'w') as file:
        json_text = json.dumps(data, indent=2)
        file.write(json_text)

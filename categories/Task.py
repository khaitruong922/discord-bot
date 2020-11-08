from discord.ext import commands
from utils.JSONFileIO import JSONFileIO

blacklist_file = JSONFileIO('data/blacklist.json')


class Task(commands.Cog):
    @commands.command(brief='Clear a number of messages in a channel.')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount=1):
        await ctx.channel.purge(limit=amount)

    @commands.command(brief='Add restricted word.')
    @commands.has_permissions(manage_messages=True)
    async def ban(self, ctx: commands.Context, word):
        bad_words = blacklist_file.get()
        if word in bad_words:
            await ctx.send(f'Từ {word} đã có trong danh sách đen rồi.')
            return
        bad_words.append(word.lower())
        blacklist_file.write(bad_words)
        await ctx.send(f'Từ {word} mới vô danh sách đen. Chúc bạn xài từ cẩn thận.')

    @commands.command(brief='Remove restricted word.')
    @commands.has_permissions(manage_messages=True)
    async def rmban(self, ctx: commands.Context, word):
        bad_words = blacklist_file.get()
        bad_words.remove(word.lower())
        blacklist_file.write(bad_words)
        await ctx.send(f'Từ {word} đã bị xoá khỏi danh sách đen. Chúc bạn xài từ cẩn thận.')

    @ban.error
    async def ban_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Muốn ban hay không nói một lời.')

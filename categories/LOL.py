from discord.ext import commands
import requests


class LOL(commands.Cog):
    @commands.command(brief='Show the lore of a champion')
    async def lore(self, ctx: commands.Context, *args):
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

    @commands.command(brief='Show an ability of a champion.', aliases=['ability'])
    async def skill(self, ctx: commands.Context, *args):
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

    @commands.command(brief='List all skins of a champion.')
    async def skin(self, ctx: commands.Context, *args):
        name = get_champion_name(args)
        data = fetch_champion_data(name)
        if not data:
            await ctx.send('No data found.')
            return
        skins = data.get('skins')
        content = ', '.join([skin.get('name') for skin in skins][1:])
        await ctx.send(content)

    @commands.command(aliases=['tip'], brief='List all tips related to a champion.')
    async def tips(self, ctx: commands.Context, *args):
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


def fetch_champion_data(name):
    try:
        res = requests.get(f'http://ddragon.leagueoflegends.com/cdn/10.21.1/data/en_US/champion/{name}.json')
        res.raise_for_status()
        return res.json().get('data').get(name)
    except requests.exceptions.HTTPError:
        return None


def get_champion_name(args):
    name = ' '.join(args).title()
    name = ''.join(name.split())
    return name

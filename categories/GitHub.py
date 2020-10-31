from discord.ext import commands
import discord
import requests


class GitHub(commands.Cog):

    @commands.command(brief='Show the info of a GitHub user.')
    async def github(self, ctx: commands.Context, username):
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

    @commands.command(brief='Show the info of a GitHub repo.')
    async def repo(self, ctx: commands.Context, username, repo_name):
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

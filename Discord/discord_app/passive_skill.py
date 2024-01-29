import discord
from discord.ext import commands
import requests
from discord_app.core.Embed import EmbedMultiplePage


class PassiveSkill(commands.Cog):
    def __init__(self, bot, url):
        self.bot = bot
        self.url = url

    @commands.command(name='passive_skill')
    async def passive_skill(self, ctx, name):
        x = requests.get(f'{self.url}/passive_skills/name/{name.lower()}')
        if x.status_code != 200:
            await ctx.send(f'Error {x.status_code}')
            return
        data = x.json()
        embed = discord.Embed(title='Passive Skill', description=data['name'].capitalize(), color=0x00ff00,
                              url=f'{self.url}/passive_skill/name/{name.lower()}')
        embed.add_field(name='ID', value=data['id'], inline=False)
        embed.add_field(name='Description', value=data['description'], inline=False)
        embed.add_field(name='Level', value=data['level'], inline=False)
        send = EmbedMultiplePage(ctx, [embed])
        await send.start()

    @commands.command(name='passive_skills')
    async def passive_skills(self, ctx):
        x = requests.get(f'{self.url}/passive_skills')
        if x.status_code != 200:
            await ctx.send(f'Error {x.status_code}')
            return
        data = x.json()
        pages = []

        for i in data:
            embed = discord.Embed(title='Passive Skills', description=i['name'].capitalize(), color=0x00ff00,
                                  url=f'{self.url}/passive_skills')
            embed.add_field(name='ID', value=i['id'], inline=False)
            embed.add_field(name='Description', value=i['description'], inline=False)
            embed.add_field(name='Level', value=i['level'], inline=False)
            pages.append(embed)
        send = EmbedMultiplePage(ctx, pages)
        await send.start()





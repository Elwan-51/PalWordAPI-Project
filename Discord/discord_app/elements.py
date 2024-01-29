import discord
from discord.ext import commands
import requests
from discord_app.core.Embed import EmbedMultiplePage


class Elements(commands.Cog):
    def __init__(self, bot, url):
        self.bot = bot
        self.url = url

    @commands.command(name='elements')
    async def elements(self, ctx):
        files_path = []
        pages = []
        x = requests.get(f'{self.url}/elements')
        if x.status_code != 200:
            await ctx.send(f'Error {x.status_code}')
            return
        data = x.json()
        for element in data:
            embed, file_path = self.elements_embed(element, url=f'{self.url}/elements')
            pages.append(embed)
            files_path.append(file_path)
        send = EmbedMultiplePage(ctx, pages, files_path=files_path)
        await send.start()

    @commands.command(name='element')
    async def element(self, ctx, name):
        x = requests.get(f'{self.url}/elements/type/{name.lower()}')
        if x.status_code != 200:
            await ctx.send(f'Error {x.status_code}')
            return
        data = x.json()
        embed, file_path = self.elements_embed(data, url=f'{self.url}/elements/name/{name.lower()}')
        send = EmbedMultiplePage(ctx, [embed], files_path=[file_path])
        await send.start()

    @staticmethod
    def elements_embed(data, url=None):
        embed = discord.Embed(title='Elements', color=0x00ff00, url=url)
        files_path = {'element_img': f"{data['img_path']}"}
        embed.set_thumbnail(url="attachment://element_img.png")
        embed.add_field(name='Type', value=data['name'].capitalize(), inline=False)
        embed.add_field(name='ID', value=data['id'], inline=False)
        return embed, files_path


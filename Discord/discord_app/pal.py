import discord
from discord.ext import commands
import requests
import os
from enum import Enum
from discord_app.core.Embed import EmbedMultiplePage


class WorkAbility(Enum):
    kindling = "<:kindling:1201158397274365992>"
    planting = "<:planting:1201158466857861130>"
    handwork = "<:handwork:1201158087193661530>"
    lumbering = "<:lumbering:1201158414433259594>"
    medicine_production = "<:medicine_production:1201158431269191790>"
    transporting = "<:transporting:1201158482519408651>"
    watering = "<:watering:1201158500873678868>"
    generating_electricity = "<:generating_electric:1201158375552077834>"
    mining = "<:mining:1201158447215943840>"
    cooling = "<:cooling:1201158319948177429>"
    farming = "<:farming:1201158336209489920>"


class Pal(commands.Cog):
    def __init__(self, bot, url):
        self.bot = bot
        self.url = url

    @commands.command(name='pal')
    async def pal(self, ctx, *name: str):
        pal_name = ' '.join(name)
        url = f'{self.url}/pals/name/{pal_name.lower().replace(" ", "%20")}'
        x = requests.get(url)
        if x.status_code != 200:
            await ctx.send(f'Error {x.status_code}')
            return
        data = x.json()
        await self.pal_embed(ctx, data, url)

    @commands.command(name='pal_id')
    async def pal_id(self, ctx, pal_id: str):
        url = f'{self.url}/pals/id/{str(pal_id):0>3}'
        print(url)
        x = requests.get(url)
        if x.status_code != 200:
            await ctx.send(f'Error {x.status_code}')
            return
        data = x.json()
        await self.pal_embed(ctx, data, url)

    async def pal_embed(self, ctx, data, url=None):
        pages = []
        files_path = []
        embed = discord.Embed(title='Pal', description=data['name'].capitalize(), color=0x00ff00,
                              url=url)
        emojies = "**Element** : "
        for element in data['element']:
            emoji = discord.utils.get(self.bot.emojis, name=str(element['name']).lower())
            emojies += f"{emoji} "
        img_path = {"pal_img": "", "day_habitat_img": "", "night_habitat_img": ""}
        for i in img_path.keys():

            img_path[i] = data[i] if os.path.exists(data[i]) else "./img/unknown.png"

        files_path.append({'pal_img': img_path['pal_img']})
        embed.set_thumbnail(url="attachment://pal_img.png")
        embed.add_field(name="Information",
                        value=f"**Name** : {str(data['name']).capitalize()} - **ID** : {data['id']}\n" +
                              emojies + f"\n**Food** : {data['food']} ", inline=True)
        embed.add_field(name="Partner skill", value=f"{data['partner_skill']}", inline=False)
        work_ability = ""
        for value in WorkAbility: work_ability += f"{value.value}: {data[value.name]}\n"
        embed.add_field(name="Work Ability", value=work_ability, inline=False)
        embed.add_field(name="Farming Loot", value=f"{data['farming_loot']}", inline=False) if data['farming_loot'] else None
        pages.append(embed)

        embed = discord.Embed(title='Pal', description=data['name'].capitalize(), color=0x00ff00,
                              url=url)
        embed.add_field(name="Information",
                        value=f"**Name** : {str(data['name']).capitalize()} - **ID** : {data['id']}\n" +
                              emojies + f"\n**Food** : {data['food']} ", inline=True)
        embed.add_field(name="Day Habitat", value="", inline=False)
        files_path.append({'day_habitat_img': img_path['day_habitat_img'], 'pal_img': img_path['pal_img']})
        embed.set_thumbnail(url="attachment://pal_img.png")
        embed.set_image(url="attachment://day_habitat_img.png")
        pages.append(embed)
        embed = discord.Embed(title='Pal', description=data['name'].capitalize(), color=0x00ff00,
                              url=url)
        embed.add_field(name="Information",
                        value=f"**Name** : {str(data['name']).capitalize()} - **ID** : {data['id']}\n" +
                              emojies + f"\n**Food** : {data['food']} ", inline=True)
        embed.add_field(name="Night Habitat", value="", inline=False)
        files_path.append({'night_habitat_img': img_path['night_habitat_img'], 'pal_img': img_path['pal_img']})
        embed.set_thumbnail(url="attachment://pal_img.png")
        embed.set_image(url="attachment://night_habitat_img.png")
        pages.append(embed)
        send = EmbedMultiplePage(ctx, pages, files_path)
        await send.start()



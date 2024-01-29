import discord
from discord.ext import commands
import requests
from discord_app.core.Embed import EmbedMultiplePage

class CheckEmbed(EmbedMultiplePage):
    def __init__(self, ctx, pages, url, user_id,files_path=None):
        super().__init__(ctx, pages, files_path=files_path)
        self.reaction_emojis_dict = {
                'left': '◀️',
                'validate': '✅',
                'right': '▶️',
            }
        self.url = url
        self.reaction_emojis = list(self.reaction_emojis_dict.values())
        self.user_id = user_id

    async def action(self, reaction):
        if reaction.emoji == self.reaction_emojis_dict['left']:
            self.current_page -= 1
        elif reaction.emoji == self.reaction_emojis_dict['right']:
            self.current_page += 1
        elif reaction.emoji == self.reaction_emojis_dict['validate']:
            data = {'pal_id': self.message.embeds[0].fields[1].value.split(' ')[-1], 'user_id': self.user_id, 'is_complete': True}
            x = requests.put(f'{self.url}/pal_complete_users', json=data)
            if x.status_code == 200:
                self.embeds.pop(self.current_page)
                self.files_path.pop(self.current_page)
        await self.message.delete()
        self.create_files() if self.files_path else []
        self.message = await self.ctx.send(embed=self.embeds[self.current_page], files=self.files if self.files else [])
        await self.add_reaction()


class Paldex(commands.Cog):
    def __init__(self, bot, url):
        self.bot = bot
        self.url = url

    @commands.command(name='completed_paldexv2')
    async def completed_paldex(self, ctx, list=False):
        x = requests.get(f'{self.url}/users/username/{ctx.author.id}')
        if x.status_code != 200:
            await ctx.channel.send(f"Vous n'êtes pas enregistré, faite `/register` pour vous enregistrer")
            return
        user_id = x.json()['id']
        x = requests.get(f'{self.url}/pal_complete_users/user_id/{user_id}/is_not_complete')
        if x.status_code != 200:
            await ctx.channel.send(f"Vous avez complété votre paldex")
            return
        data = x.json()
        if list:
            pal_list = ""
            for pal in data:
                pal_list += f"{pal['pal']['name'].capitalize()} - {pal['pal']['id']}\n"
            await ctx.channel.send(pal_list)
        else:
            pages = []
            files_path = []
            for pal in data:
                embed, file_path = self.paldex_embed(pal)
                pages.append(embed)
                files_path.append(file_path)
            send = CheckEmbed(ctx, pages, self.url, user_id,files_path=files_path)
            await send.start()


    @staticmethod
    def paldex_embed(data, url=None):
        embed = discord.Embed(title='Paldex', color=0x00ff00, url=url)
        files_path = {'pal_img': f"{data['pal']['pal_img']}"}
        embed.set_thumbnail(url="attachment://pal_img.png")
        embed.add_field(name='Name', value=data['pal']['name'].capitalize(), inline=False)
        embed.add_field(name='ID', value=data['pal']['id'], inline=False)
        return embed, files_path





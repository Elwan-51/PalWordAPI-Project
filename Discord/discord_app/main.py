import asyncio

import discord
from discord.ext import tasks, commands
import requests
import logging
import os



# Bot configuration
intents = discord.Intents.default()
intents.message_content = True


# Bot definition
bot = commands.Bot(command_prefix=os.getenv('PREFIX', '/'), intents=intents)

URL = os.getenv('URL_API', 'https://palworld-api.asylium.app/api/v1')

# Bot starting event


@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')
    # Initialised planed task

# Command section

@bot.command()
async def elements(ctx):
    x = requests.get(f'{URL}/elements/')
    data = x.json()
    for element_data in data:
        embed = discord.Embed(title="Element", color=0x00ff00, url="https://palworld-api.asylium.app")
        files = [discord.File(element_data['img_path'], filename=element_data['img_path'].split('/')[-1])]
        embed.set_thumbnail(url='attachment://' + element_data['img_path'].split('/')[-1])
        embed.add_field(name="Type", value=str(element_data['name']).capitalize(), inline=True)
        embed.add_field(name="ID", value=element_data['id'], inline=True)
        await ctx.channel.send(files=files, embed=embed)


@bot.command()
async def element_info(ctx, command_element):
    # Command that return the last luminosity in the channel requesting the meteo
    x = requests.get(f'{URL}/elements/type/{str(command_element).lower()}')
    if x.status_code != 200:
        await ctx.channel.send(f'Le type {str(command_element).capitalize()} n\'existe pas')
        return
    data = x.json()
    embed = discord.Embed(title="Element", color=0x00ff00, url=f"{URL}/elements/type/"+f"{str(command_element).lower()}")

    if os.path.isfile(data['img_path']):
        files.append(discord.File(data['img_path'], filename=data['img_path'].split('/')[-1]))
        embed.set_thumbnail(url='attachment://' + data['img_path'].split('/')[-1])
    else:
        files.append(discord.File('./img/unknown.png', filename='./img/unknown.png'.split('/')[-1]))
        embed.set_thumbnail(url='attachment://' + './img/unknown.png'.split('/')[-1])
    embed.add_field(name="Type", value=str(data['name']).capitalize(), inline=True)
    embed.add_field(name="ID", value=data['id'], inline=True)
    await ctx.channel.send(files=files, embed=embed)

files= []

@bot.command(name="pal",description="Commande qui retourne les information sur un pal")
async def pal(ctx, command_pal, cmd=""):
    if cmd:
        url = f'{URL}/pals/name/{str(command_pal).lower()}%20{str(cmd).lower()}'
        x = requests.get(url)
    else :
        url = f'{URL}/pals/name/{str(command_pal).lower()}'
        x = requests.get(url)
    if x.status_code != 200:
        await ctx.channel.send(f'Le pal {str(command_pal).capitalize()} n\'existe pas')
        return
    data = x.json()
    pages = []
    embed = discord.Embed(title=f"Pal - {str(data['name']).capitalize()}", color=0x00ff00, url=url)
    emojies = "**Element** : "
    for element in data['element']:
        emoji = discord.utils.get(bot.emojis, name=str(element['name']).lower())
        emojies += f"{emoji} "
    img_path = {"pal_img": "", "day_habitat_img": "", "night_habitat_img": ""}

    if os.path.isfile(data['pal_img']):
        img_path['pal_img'] = data['pal_img']
    else:
        img_path['pal_img'] = './img/unknown.png'
    embed.set_thumbnail(url='attachment://' + img_path['pal_img'].split('/')[-1])

    embed.add_field(name="Information", value=f"**Name** : {str(data['name']).capitalize()} - **ID** : {data['id']}\n"+
                                              emojies + f"\n**Food** : {data['food']} ", inline=True)
    embed.add_field(name="Partner skill", value=f"{data['partner_skill']}", inline=False)
    embed.add_field(name="Work ability", value=f"<:kindling:1201158397274365992> : {data['kindling']}\n"
                                               f"<:planting:1201158466857861130> : {data['planting']}\n"
                                               f"<:handwork:1201158087193661530> : {data['handwork']}\n"
                                               f"<:lumbering:1201158414433259594> : {data['lumbering']}\n"
                                               f"<:medicine_production:1201158431269191790> : {data['medicine_production']}\n"
                                               f"<:transporting:1201158482519408651> : {data['transporting']}\n"
                                               f"<:watering:1201158500873678868> : {data['watering']}\n"
                                               f"<:generating_electric:1201158375552077834> : {data['generating_electricity']}\n"
                                               f"<:mining:1201158447215943840> : {data['mining']}\n"
                                               f"<:cooling:1201158319948177429> : {data['cooling']}\n"
                                               f"<:farming:1201158336209489920> : {data['farming']}\n", inline=False)
    if data['farming_loot'] is not None:
        embed.add_field(name="Farming loot", value=str(data['farming_loot']).capitalize(), inline=False)
    pages.append(embed)
    embed_day = discord.Embed(title=f"Pal - {str(data['name']).capitalize()}", color=0x00ff00, url=url)

    embed_day.add_field(name="Information", value=f"**Name** : {str(data['name']).capitalize()} - **ID** : {data['id']}\n"+
                                              emojies)
    if os.path.isfile(data['day_habitat_img']):
        img_path['day_habitat_img'] = data['day_habitat_img']
    else:
        img_path['day_habitat_img'] = './img/unknown.png'
    embed_day.add_field(name="Day habitat", value=f"", inline=False)
    embed_day.set_image(url='attachment://' + img_path['day_habitat_img'].split('/')[-1])
    embed_day.set_thumbnail(url='attachment://' + data['pal_img'].split('/')[-1])

    pages.append(embed_day)
    embed_night = discord.Embed(title=f"Pal - {str(data['name']).capitalize()}", color=0x00ff00, url=url)
    embed_night.set_thumbnail(url='attachment://' + data['pal_img'].split('/')[-1])
    embed_night.add_field(name="Information", value=f"**Name** : {str(data['name']).capitalize()} - **ID** : {data['id']}\n"+
                                              emojies)
    embed_night.add_field(name="Night habitat", value=f"", inline=False)
    if os.path.isfile(data['night_habitat_img']):
        img_path['night_habitat_img'] = data['night_habitat_img']
    else:
        img_path['night_habitat_img'] = './img/unknown.png'
    embed_night.set_image(url='attachment://' + img_path['night_habitat_img'].split('/')[-1])
    pages.append(embed_night)
    files_path = []
    for img in img_path:
        files_path.append(img_path[img])


    page = 0
    left = "◀️"
    right = "▶️"

    msg = await ctx.channel.send(embed=pages[page], files=[discord.File(files_path[page], filename=files_path[page].split('/')[-1])])
    await msg.add_reaction(left)
    await msg.add_reaction(right)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [left, right]

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=20, check=check)
            if str(reaction.emoji) == left:
                page = page - 1
                if page < 0:
                    page = len(pages) - 1
            elif str(reaction.emoji) == right:
                page = page + 1
                if page > len(pages) - 1:
                    page = 0
            await msg.delete()

            msg = await ctx.channel.send(embed=pages[page],  files=[discord.File(files_path[page], filename=files_path[page].split('/')[-1]), discord.File(files_path[0], filename=files_path[0].split('/')[-1])])
            await msg.add_reaction(left)
            await msg.add_reaction(right)
        except asyncio.TimeoutError:
            break
@bot.command()
async def pal_me(ctx):
    x = requests.get(f'{URL}/users/username/{ctx.author.id}')
    if x.status_code == 200:
        await ctx.channel.send(f"Vous êtes enregistré")
    else:
        await ctx.channel.send(f"Vous n'êtes pas enregistré, faite `/register` pour vous enregistrer")
@bot.command()
async def register(ctx):
    #print({"id": ctx.author.id, "username": ctx.author.name})
    x = requests.post(f'{URL}/users', json={"username": str(ctx.author.id)})
    if x.status_code == 201:
        await ctx.channel.send(f'Enregistrement de {ctx.author.name} en cours')
        user_id = x.json()['id']
        pal_list = requests.get(f'{URL}/pals')
        data = pal_list.json()

        async def register_completed_pal(pal, user_id):
            new_complete = requests.post(f'{URL}/pal_complete_users', json={"pal_id": pal['id'], "user_id": user_id, "is_complete": False})
            if new_complete.status_code != 201:
                await ctx.channel.send(f"Une erreur est survenue lors de l'enregistrement de vos pal")
                x = requests.delete(f'{URL}/users/{user_id}')
                return

        for pal in data:
            await register_completed_pal(pal, user_id)
        await ctx.channel.send(f"Vous avez été enregistré avec succès")
    else:
        await ctx.channel.send(f"Une erreur est survenue lors de l'enregistrement de votre compte")


@bot.command()
async def completed_paldex(ctx, list=False):
    files_path = []
    x = requests.get(f'{URL}/users/username/{ctx.author.id}')
    if x.status_code == 200:
        user_id = x.json()['id']
        x = requests.get(f'{URL}/pal_complete_users/user_id/{user_id}/is_not_complete')
        if x.status_code == 200:
            if list:
                pal_list = ""
                for pal in x.json():
                    pal_list += f"{pal['pal']['name']}\n"

                await ctx.channel.send(f"Voici la liste de vos pal a completer :\n{pal_list}")
            else:
                pages = []
                for pal in x.json():
                    embed = discord.Embed(title="Pal complete", color=0x00ff00,
                                          url=f"{URL}/pal_complete_users/user_id/{user_id}/is_not_complete")
                    if os.path.isfile(pal['pal']['pal_img']):
                        files_path.append(pal['pal']['pal_img'])
                        embed.set_thumbnail(url='attachment://' + pal['pal']['pal_img'].split('/')[-1])
                    else:
                        files_path.append('./img/unknown.png')
                        embed.set_thumbnail(url='attachment://' + './img/unknown.png'.split('/')[-1])
                    embed.add_field(name=f"{pal['pal']['name'].capitalize()}", value=f"ID : {pal['pal']['id']}", inline=True)
                    pages.append(embed)
                page = 0
                left = "◀️"
                right = "▶️"
                validate = "✅"

                msg = await ctx.channel.send(embed=pages[page], files=[discord.File(files_path[page], filename=files_path[page].split('/')[-1])])
                await msg.add_reaction(left)
                await msg.add_reaction(right)
                await msg.add_reaction(validate)

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in [left, right, validate]

                while True:
                    try:
                        reaction, user = await bot.wait_for("reaction_add", timeout=30, check=check)
                        if str(reaction.emoji) == left:
                            page = page - 1
                            if page < 0:
                                page = len(pages) - 1
                        elif str(reaction.emoji) == right:
                            page = page + 1
                            if page > len(pages) - 1:
                                page = 0
                        elif str(reaction.emoji) == validate:
                            msg_data = msg.embeds[0].fields[0].value.split(' ')[-1]
                            x = requests.put(f'{URL}/pal_complete_users/', json={"pal_id": msg_data, 'user_id': user_id,"is_complete": True})
                            if x.status_code == 200:
                                pages.pop(page)
                        await msg.delete()

                        msg = await ctx.channel.send(embed=pages[page], files=[discord.File(files_path[page], filename=files_path[page].split('/')[-1])])
                        await msg.add_reaction(left)
                        await msg.add_reaction(right)
                        await msg.add_reaction(validate)
                    except asyncio.TimeoutError:
                        break
    else:
        await ctx.channel.send(f"Vous n'êtes pas enregistré")

@bot.command()
async def pal_help(ctx):
    pages = []
    embed = discord.Embed(title="Pal help", color=0x00ff00, url="https://palworld-api.asylium.app")
    embed.add_field(name="Commande", value="/pal <name>", inline=True)
    embed.add_field(name="Description", value="Commande qui retourne les information sur un pal", inline=True)
    pages.append(embed)
    embed = discord.Embed(title="Pal help", color=0x00ff00, url="https://palworld-api.asylium.app")
    embed.add_field(name="Commande", value="/elements", inline=True)
    embed.add_field(name="Description", value="Commande qui retourne les information sur les elements", inline=True)
    pages.append(embed)
    embed = discord.Embed(title="Pal help", color=0x00ff00, url="https://palworld-api.asylium.app")
    embed.add_field(name="Commande", value="/element_info <name>", inline=True)
    embed.add_field(name="Description", value="Commande qui retourne les information sur un element", inline=True)
    pages.append(embed)
    embed = discord.Embed(title="Pal help", color=0x00ff00, url="https://palworld-api.asylium.app")
    embed.add_field(name="Commande", value="/register", inline=True)
    embed.add_field(name="Description", value="Commande qui enregistre un utilisateur", inline=True)
    pages.append(embed)
    embed = discord.Embed(title="Pal help", color=0x00ff00, url="https://palworld-api.asylium.app")
    embed.add_field(name="Commande", value="/completed_paldex", inline=True)
    embed.add_field(name="Description", value="Commande qui retourne les pal que vous avez complété", inline=True)
    pages.append(embed)
    embed = discord.Embed(title="Pal help", color=0x00ff00, url="https://palworld-api.asylium.app")
    embed.add_field(name="Commande", value="/completed_paldex list", inline=True)
    embed.add_field(name="Description", value="Commande qui retourne les pal que vous avez complété sous forme de liste", inline=True)
    pages.append(embed)
    embed = discord.Embed(title="Pal help", color=0x00ff00, url="https://palworld-api.asylium.app")
    embed.add_field(name="Commande", value="/reset_account", inline=True)
    embed.add_field(name="Description", value="Commande qui supprime votre compte", inline=True)
    pages.append(embed)


    page = 0
    left = "◀️"
    right = "▶️"

    msg = await ctx.channel.send(embed=pages[page])
    await msg.add_reaction(left)
    await msg.add_reaction(right)

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in [left, right]

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=120, check=check)
            if str(reaction.emoji) == left:
                page = page - 1
                if page < 0:
                    page = len(pages) - 1
            elif str(reaction.emoji) == right:
                page = page + 1
                if page > len(pages) - 1:
                    page = 0
            await msg.delete()

            msg = await ctx.channel.send(embed=pages[page])
            await msg.add_reaction(left)
            await msg.add_reaction(right)
        except asyncio.TimeoutError:
            break


@bot.command()
async def reset_account(ctx):
    x = requests.get(f'{URL}/users/username/{ctx.author.id}')
    print(x.status_code)
    if x.status_code == 200:
        x = requests.delete(f'{URL}/users/id/{x.json()["id"]}')
        print(x.status_code)
        if x.status_code == 200:
            await ctx.channel.send(f"Votre compte a été supprimé avec succès")
    else:
        await ctx.channel.send(f"Une erreur est survenue lors de la suppression de votre compte")


# Bot startup
bot.run(os.getenv('TOKEN', 'API'))

import asyncio

import discord
from discord.ext import tasks, commands
import requests
import logging
import os
from discord_app.passive_skill import PassiveSkill
from discord_app.pal import Pal
from discord_app.elements import Elements
from discord_app.user import User
from discord_app.paldex import Paldex
from discord_app.core.Embed import EmbedMultiplePage



# Bot configuration
intents = discord.Intents.default()
intents.message_content = True

logging.basicConfig(level=logging.INFO)


# Bot definition
bot = commands.Bot(command_prefix=os.getenv('PREFIX', '/'), intents=intents)

URL = os.getenv('URL_API', 'https://palworld-api.asylium.app/api/v1')

# Bot starting event


@bot.event
async def on_ready():
    logging.info(f'We have logged in as {bot.user}')
    await bot.add_cog(PassiveSkill(bot, URL))
    logging.info(f'Passive skill cog loaded')
    await bot.add_cog(Pal(bot, URL))
    logging.info(f'Pal cog loaded')
    await bot.add_cog(Elements(bot, URL))
    logging.info(f'Elements cog loaded')
    await bot.add_cog(User(bot, URL))
    logging.info(f'User cog loaded')
    await bot.add_cog(Paldex(bot, URL))
    logging.info(f'Paldex cog loaded')

    # Initialised planed task

# Command section

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

    send = EmbedMultiplePage(ctx, pages)
    await send.start()


# Bot startup
bot.run(os.getenv('TOKEN', 'API'))

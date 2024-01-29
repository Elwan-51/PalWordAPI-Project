from discord.ext import commands
import requests


class User(commands.Cog):
    def __init__(self, bot, url):
        self.bot = bot
        self.url = url

    @commands.command(name='pal_me')
    async def pal_me(self, ctx):
        x = requests.get(f'{self.url}/users/username/{ctx.author.id}')
        if x.status_code == 200:
            await ctx.channel.send(f"Vous êtes enregistré")
        else:
            await ctx.channel.send(f"Vous n'êtes pas enregistré, faite `/register` pour vous enregistrer")

    @commands.command(name='register')
    async def register(self, ctx):
        x = requests.post(f'{self.url}/users', json={"username": str(ctx.author.id)})
        if x.status_code == 201:
            await ctx.channel.send(f'Enregistrement de {ctx.author.name} en cours')
            user_id = x.json()['id']
            pal_list = requests.get(f'{self.url}/pals')
            data = pal_list.json()

            async def register_completed_pal(pal, user_id):
                new_complete = requests.post(f'{self.url}/pal_complete_users', json={"pal_id": pal['id'], "user_id": user_id, "is_complete": False})
                if new_complete.status_code != 201:
                    await ctx.channel.send(f"Une erreur est survenue lors de l'enregistrement de vos pal")
                    x = requests.delete(f'{self.url}/users/{user_id}')
                    return

            for pal in data:
                await register_completed_pal(pal, user_id)
            await ctx.channel.send(f"Vous avez été enregistré avec succès")
        else:
            await ctx.channel.send(f"Une erreur est survenue lors de l'enregistrement de votre compte")

    @commands.command(name='reset_account')
    async def reset_account(self, ctx):
        x = requests.get(f'{self.url}/users/username/{ctx.author.id}')
        if x.status_code == 200:
            x = requests.delete(f'{self.url}/users/id/{x.json()["id"]}')
            if x.status_code == 200:
                await ctx.channel.send(f"Votre compte a été supprimé avec succès")
        else:
            await ctx.channel.send(f"Une erreur est survenue lors de la suppression de votre compte")
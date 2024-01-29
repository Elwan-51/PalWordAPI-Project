import asyncio
import discord

class EmbedMultiplePage:
    def __init__(self, ctx, embeds: list, files_path: list[dict] | None = None, timeout: int = 60):
        self.reaction_emojis_dict = {
                'left': '◀️',
                'right': '▶️',
            }
        self.ctx = ctx
        self.embeds = embeds
        self.files = []
        self.files_path = files_path
        self.timeout = timeout
        self.current_page = 0
        self.message = None
        self.reaction_emojis = list(self.reaction_emojis_dict.values())

    def check(self, reaction, user):
        return user == self.ctx.author and reaction.message.id == self.message.id and reaction.emoji in self.reaction_emojis

    async def start(self):
        self.create_files() if self.files_path else []

        if len(self.embeds) == 1:
            self.current_page = 0
            self.message = await self.ctx.send(embed=self.embeds[self.current_page], files=self.files)
            return
        if len(self.embeds) == 0:
            return

        self.message = await self.ctx.send(embed=self.embeds[self.current_page], files=self.files)
        await self.add_reaction()
        await self.wait_for_reaction()

    async def wait_for_reaction(self):
        while True:
            try:
                reaction, user = await self.ctx.bot.wait_for('reaction_add', timeout=self.timeout, check=self.check)
            except asyncio.TimeoutError:
                await self.message.clear_reactions()
                return
            else:
                await self.action(reaction)

    async def action(self, reaction):
        if reaction.emoji == self.reaction_emojis_dict['left']:
            self.current_page -= 1
        elif reaction.emoji == self.reaction_emojis_dict['right']:
            self.current_page += 1
        self.current_page %= len(self.embeds)
        await self.message.delete()
        self.create_files() if self.files_path else []
        self.message = await self.ctx.send(embed=self.embeds[self.current_page], files=self.files if self.files else [])
        await self.add_reaction()

    async def add_reaction(self):
        for emoji in self.reaction_emojis:
            await self.message.add_reaction(emoji)

    def create_files(self):
        self.files = []
        for i in self.files_path[self.current_page].keys():
            self.files.append(discord.File(self.files_path[self.current_page][i], filename=i+".png"))



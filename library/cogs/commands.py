import discord
from os import name
from random import choice, randint
from discord import Embed, Member, DMChannel
from discord.ext.commands import Cog, BucketType
from discord.ext.commands.errors import BadArgument
from discord.ext.commands import command
class Comm(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello','Hi','Hey'))} {ctx.author.mention}!")

    @command(name="dm_friend", aliases=["dmfriend"])
    async def friend_dm(self, ctx, user: discord.Member, *, args):
        if args != None:
            try:
                await user.send(args)
                await ctx.send(f'Dm sent to {user.name}')
            except:
                await ctx.send("No permission to send DM")

    @command(name="ask", aliases=["askbot"])
    async def ask_bot(self, message):
        dm = await message.author.create_dm()
        await dm.send("Ask me something about GSR:")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Ready up -")

def setup(bot):
    bot.add_cog(Comm(bot))

# Adicionar  um cooldown para um command
# @cooldown(1, 60, BucketType.user)

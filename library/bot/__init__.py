import discord
from asyncio import sleep
from datetime import datetime
from inspect import Arguments
from logging import error
from discord.errors import HTTPException, Forbidden
from discord import Intents, Embed, File, DMChannel
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import command, Cog, Context
from discord.ext.commands import when_mentioned_or, command, has_permissions
from pathlib import Path
from discord.ext.commands import Context
from discord.ext.commands.errors import (BadArgument, CommandNotFound, CommandOnCooldown, MissingRequiredArgument)
from discord.utils import get

from ..db import db
from glob import glob

PREFIX = "!"
COGS = [path.split("\\")[-1][:-3] for path in glob("./library/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

def get_prefix(bot, message):
    prefix = db.field(
        "SELECT Prefix FROM guild WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(PREFIX)(bot, message)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=PREFIX,
            intents=Intents.all(),
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"library.cogs.{cog}")
            print(f"{cog}.py cog loaded")

        print("setup complete")

    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guild (GuildID) VALUES (?)", 
                     ((guild.id,) for guild in self.guilds))

        db.multiexec("INSERT OR IGNORE INTO register (UserID) VALUES (?)",
                     ((member.id,) for member in self.guild.members if not member.bot))
        
        to_remove = []
        stored_members = db.column("SELECT UserID FROM register")
        for id_ in stored_members:
            if not self.guild.get_member(id_):
                to_remove.appedn(id_)

        db.multiexec("DELETE FROM register WHERE UserID = ?",
                     ((id_)for id_ in to_remove))

        db.commit()

    def run(self):
        print(" running setup...")
        self.setup()

        with open("./library/bot/token", 'r', encoding='utf-8') as f:
            self.token = f.read()

        print(" running bot...")
        super().run(self.token, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await ctx.send("I am not ready to receive commands. Please wait a few seconds!")

    @command(name="prefix")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("The prefix can not be more than 5 characteres in length.")

        else:
            db.execute(
                "Update guild SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
            await ctx.send(f"Prefix set to {new}.")

    async def on_connect(self):
        print("Bot online")

    async def on_disconnect(self):
        print("Bot offline")
        await self.stdout.send("Diva offline!")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.stdout.send("An error ocurred.")
        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")
        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"That command is on cooldown. Try again in {exc.retry_after:,.2f} seconds.")
        elif isinstance(exc.original, HTTPException):
            await ctx.send("Unable to send message.")
        elif isinstance(exc.original, Forbidden):
            await ctx.send("Do not have permission to do that.")
        else:
            raise exc.original

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(906958110642569296)
            self.stdout = self.get_channel(918294847427837973)
            
            self.update_db()

            await self.stdout.send("Diva online!")
            self.ready = True
            print("Diva is getting ready...")
        else:
            print("Diva reconnected")


bot = Bot()

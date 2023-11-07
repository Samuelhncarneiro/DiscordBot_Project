import discord
import asyncio
from discord import Forbidden
from discord_ui import Button
from discord.ext.commands import Cog, command
from ..db import db

class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    """@command(name="register")
    @Cog.listener()
    async def register(ctx, member, option: str=None):
        if option is None:
            await ctx.send("Please register: !register (username) (student or professor)")
        else:
            student = discord.utils.get(ctx.guild.roles, id=1014199096698998824)
            professor = discord.utils.get(ctx.guild.roles, id=1014198831564464219)
            if option.lower() == "student":
                await member.add_roles(student)
                await ctx.send("You have been registered as a student!")
            elif option.lower() == "professor":
                await member.add_roles(professor)
                await ctx.send("You have been registered as a professor!")"""
     
    @Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(928702084453384271)

        def check(m: discord.Message):
            return m == "student" or m=="professor" 

        await asyncio.sleep(5)
        await channel.send(f"Welcome **{member.guild.name}** {member.mention}!")
        await channel.send("Are you a professor or a student? Please register on the server")

        msg = await self.bot.wait_for('message', timeout=30)
        attempt = msg.content

        st = discord.utils.get(self.bot.guild.roles, id=1014199096698998824)
        pr = discord.utils.get(self.bot.guild.roles, id=1014198831564464219)

        if attempt == "student" or attempt == "Student" :
            await member.add_roles(st)
            await channel.send("You have been registered as a student!")
        elif attempt == "professor" or attempt == "Professor":
            await member.add_roles(pr)
            await channel.send("You have been registered as a professor!")
        else:
            await channel.send("Please insert one of this roles: student / professor!")

        db.execute("INSERT INTO register (UserID) VALUES (?)", member.id)

    @Cog.listener()
    async def on_member_remove(self, member):
        """db.execute("DELETE FROM register WHERE UserID = ?", member.id)"""
        await self.bot.get_channel(928702084453384271).send(f"Bye {member.display_name}!")

def setup(bot):
    bot.add_cog(Welcome(bot))

from datetime import datetime
from discord import Embed
from datetime import datetime
from discord.ext.commands import Cog, command

class Log(Cog):
    def __init__(self,bot):
        self.bot=bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.log_channel = self.bot.get_channel(928759648234917928)
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_user_update(self,before,after):
        if before.name != after.name:
            embed= Embed(title="Username changes",
                        description="Member Update",
                        colour=after.colour,
                        timestamp=datetime.utcnow())

            fields =[("Before", before.name, False),
                    ("After",after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)
        
        if before.discriminator != after.discriminator:
            embed= Embed(title="Discriminator Update",
                        colour=after.colour,
                        timestamp=datetime.utcnow())

            fields =[("Before", before.discriminator, False),
                    ("After", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        if before.avatar_url != after.avatar_url:
            embed= Embed(title="Avatar Changes",
                        description="New image update",
                        colour=after.colour,
                        timestamp=datetime.utcnow())

            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url= after.avatar_url)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed= Embed(title="Nickname changes",
                        description="Member Update",
                        colour=after.colour,
                        timestamp=datetime.utcnow())

            fields =[("Before", before.display_name, False),
                    ("After",after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)
        
        elif before.roles != after.roles:
            embed= Embed(title="Role changes",
                        description="Member Update",
                        colour=after.colour,
                        timestamp=datetime.utcnow())

            fields =[("Before",", ".join([r.mention for r in before.roles]), False),
                    ("After",", ".join([r.mention for r in after.roles]), False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            if before.content != after.content:
                embed= Embed(title="Message Update",
                            description="Message has been changed",
                            colour=after.author.colour,
                            timestamp=datetime.utcnow())

                fields =[("Before",before.content, False),
                        ("After",after.content, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = Embed(title="Message deletion",
						  description=f"Action by {message.author.display_name}.",
						  colour=message.author.colour,
						  timestamp=datetime.utcnow())
                          
            fields = [("Content", message.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            
            await self.log_channel.send(embed=embed)
            
def setup(bot):
    bot.add_cog(Log(bot))
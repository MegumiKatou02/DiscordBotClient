import discord
from discord import app_commands
from discord.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def avatar_and_avt(interaction: discord.Interaction, member: discord.Member = None, ephemeral: bool = False):
        if member is None:
            member = interaction.user
        
        avatar_url = member.display_avatar.url 

        embed = discord.Embed(
            title=f"Avatar của {member.display_name}",
            description="",
            color=discord.Color.blue()
        )
        embed.set_image(url=avatar_url)

        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

    #avatar
    @app_commands.command(name="avatar", description="Hiển thị avatar của một thành viên")
    async def avatar_command(self, interaction: discord.Interaction, member: discord.Member = None):
        await self.avatar_and_avt(interaction, member)

    #avt
    @app_commands.command(name="avt", description="Hiển thị avatar của một thành viên")
    async def avt_command(self, interaction: discord.Interaction, member: discord.Member = None):
        await self.avatar_and_avt(interaction, member)

async def setup(bot):
    await bot.add_cog(Avatar(bot))
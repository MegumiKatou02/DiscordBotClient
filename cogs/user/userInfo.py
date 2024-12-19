import discord
from discord.ext import commands
from discord import app_commands

class UserInfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="userinfo", description="Hiển thị thông tin người dùng")
    @app_commands.describe(user="Chọn người dùng cần xem thông tin")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user

        nickname = user.nick if user.nick else user.name

        nickname = nickname.replace("_", "\\_")
        name = user.name.replace("_", "\\_")

        user_info = (
            f"**Name:** {name}\n"
            f"**Nickname:** {nickname}\n"
            f"**ID:** {user.id}\n\n"
            f"**Joined server:** \n`{user.joined_at.strftime('%d/%m/%Y %H:%M:%S')}`\n\n"
            f"**Joined Discord:** \n`{user.created_at.strftime('%d/%m/%Y %H:%M:%S')}`"
        )

        embed = discord.Embed(
            title="Thông tin người dùng",
            description=user_info,
            color=discord.Color(0xFFFFFF)
        )
        embed.set_thumbnail(url=user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfoCog(bot))

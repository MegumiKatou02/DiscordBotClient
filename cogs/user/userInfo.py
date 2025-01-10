import discord
from discord.ext import commands
from discord import app_commands
import datetime
from cogs.user.avatar import Avatar

class AvatarButton(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__()
        self.user: discord.Member = user

    @discord.ui.button(label="Xem Avatar", style=discord.ButtonStyle.primary)
    async def view_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await Avatar.avatar_and_avt(interaction, self.user, ephemeral=True)

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

        user_joined = int(user.joined_at.timestamp())
        user_created = int(user.created_at.timestamp())

        user_info = (
            f"**User Info**\n"
            f"ID: {user.id}\n"
            f"Tên người dùng: {name}\n"
            f"Nickname: {nickname}\n\n"
            f"**Ngày tham gia server**\n<t:{user_joined}> (<t:{user_joined}:R>)\n\n"
            f"**Ngày tham gia Discord**\n<t:{user_created}> (<t:{user_created}:R>)\n\n"
        )

        embed = discord.Embed(
            description=user_info,
            color=discord.Color(0xFFFFFF),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=f"@{user}", icon_url=user.display_avatar.url)
        embed.set_thumbnail(url=user.display_avatar.url)

        view = AvatarButton(user)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(UserInfoCog(bot))

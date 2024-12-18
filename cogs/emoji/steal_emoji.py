import discord
from discord import app_commands
from discord.ext import commands
import aiohttp  


class StealEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="steal_emoji", description="Lấy emoji từ server khác và thêm vào server hiện tại")
    async def steal_emoji(self, interaction: discord.Interaction, emoji: str, name: str = None):
        if not interaction.user.guild_permissions.manage_emojis:
            await interaction.response.send_message("Bạn không có quyền quản lý emoji trong server này", ephemeral=True)
            return

        guild = interaction.guild
        if not guild.me.guild_permissions.manage_emojis:
            await interaction.response.send_message("Bot không có quyền quản lý emoji trong server này", ephemeral=True)
            return

        if emoji.startswith("<") and emoji.endswith(">"):
            parts = emoji.strip("<>").split(":")
            if len(parts) == 3:
                emoji_id = parts[2]
                is_animated = emoji.startswith("<a")
                file_extension = "gif" if is_animated else "png"
                emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{file_extension}"

                if name is None:
                    name = parts[1]  

                async with aiohttp.ClientSession() as session:
                    async with session.get(emoji_url) as response:
                        if response.status == 200:
                            emoji_data = await response.read()
                            try:
                                new_emoji = await guild.create_custom_emoji(name=name, image=emoji_data)
                                await interaction.response.send_message(
                                    f"Đã thêm emoji thành công: {new_emoji} với tên `{name}`!"
                                )
                            except discord.HTTPException as e:
                                await interaction.response.send_message(f"Lỗi khi thêm emoji: {str(e)}", ephemeral=True)
                            return

        await interaction.response.send_message("Emoji không hợp lệ hoặc không thể xử lý", ephemeral=True)


async def setup(bot):
    await bot.add_cog(StealEmoji(bot))
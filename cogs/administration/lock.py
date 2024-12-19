import discord
from discord.ext import commands
from discord import app_commands

class LockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="lock", description="khoá kênh")
    async def lock_channel(self, interaction: discord.Interaction):
        channel = interaction.channel
        
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("Bạn không có quyền khóa kênh này.", ephemeral=True)
            return
        
        await channel.set_permissions(interaction.guild.default_role, send_messages=False)
        
        await interaction.response.send_message(f"Đã khoá kênh `{channel.name}` ✅")

async def setup(bot):
    await bot.add_cog(LockCog(bot))
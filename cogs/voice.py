import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class AutoVoiceChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trigger_channel_id = None  
        self.default_channel_name = "{member}'s Channel"  

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not self.trigger_channel_id:
            return

        if after.channel and after.channel.id == self.trigger_channel_id:
            guild = member.guild

            new_channel = await guild.create_voice_channel(
                name=self.default_channel_name.format(member=member.name),
                category=after.channel.category,
                user_limit=self.default_user_limit,
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(connect=True),  
                    # member: discord.PermissionOverwrite(connect=True), 
                },
                reason=f"Kênh được tạo tự động cho {member.name}"
            )

            await member.move_to(new_channel)

            await self.auto_delete_channel(new_channel)

    async def auto_delete_channel(self, channel):
        while True:
            await asyncio.sleep(5)
            if len(channel.members) == 0:
                await channel.delete(reason="Tự động xóa kênh vì không còn ai sử dụng.")
                break

    @app_commands.command(name="set_voice", description="Đặt kênh voice đặc biệt để tạo kênh tự động.")
    async def set_voice(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        self.trigger_channel_id = channel.id
        await interaction.response.send_message(
            f"Kênh voice `{channel.name}` đã được đặt làm kênh đặc biệt.", ephemeral=True
        )

    @app_commands.command(name="get_voice", description="Xem kênh voice đặc biệt hiện tại.")
    async def get_voice(self, interaction: discord.Interaction):
        if self.trigger_channel_id:
            guild = interaction.guild
            channel = guild.get_channel(self.trigger_channel_id)
            if channel:
                await interaction.response.send_message(
                    f"Kênh voice đặc biệt hiện tại là: `{channel.name}`", ephemeral=True
                )
                return

        await interaction.response.send_message(
            "Chưa có kênh voice đặc biệt nào được đặt.", ephemeral=True
        )

    @app_commands.command(name="channel_rename", description="Đổi tên kênh voice bạn đang tham gia")
    @app_commands.describe(new_name="Tên mới của kênh")
    async def rename_channel(self, interaction: discord.Interaction, new_name: str):
        channel = interaction.user.voice.channel if interaction.user.voice else None
        
        if channel is None:
            await interaction.response.send_message("Bạn không ở trong kênh voice nào.", ephemeral=True)
            return

        if not interaction.user.guild_permissions.administrator:
            perms = channel.permissions_for(interaction.user)
            if not perms.manage_channels:
                await interaction.response.send_message("Bạn không có quyền thay đổi giới hạn người tham gia trong kênh voice này.", ephemeral=True)
                return

        try:
            await channel.edit(name=new_name)
            await interaction.response.send_message(f"Tên kênh đã được đổi thành: {new_name}")
        except Exception as e:
            await interaction.response.send_message(f"Đã xảy ra lỗi: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AutoVoiceChannel(bot))
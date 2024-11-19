import time
import discord
from discord import app_commands
from discord.ext import commands

import config

class SendDev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_last_sent = {} 

    @app_commands.command(description="Gửi tin nhắn đến nhà phát triển")
    async def send_dev(self, interaction: discord.Interaction, message: str):
        user_id = interaction.user.id
        current_time = time.time()

        if user_id in self.user_last_sent:
            last_sent_time = self.user_last_sent[user_id]
            if current_time - last_sent_time < 600:
                remaining_time = 600 - (current_time - last_sent_time)
                await interaction.response.send_message(
                    f"Bạn phải đợi {int(remaining_time)} giây nữa mới có thể gửi tin nhắn tiếp theo.",
                    ephemeral=True
                )
                return

        dev_user = await self.bot.fetch_user(config.USER_ID)  
        try:
            guild_name = interaction.guild.name if interaction.guild else "DM"
            content = f"Tin nhắn từ **{interaction.user.name}** từ server **{guild_name}**:\n{message}"

            await dev_user.send(content)
            self.user_last_sent[user_id] = current_time
            
            await interaction.response.send_message("Đã gửi tin nhắn tới nhà phát triển!", ephemeral=True)
        except discord.Forbidden:
            
            await interaction.response.send_message("Không thể gửi tin nhắn cho nhà phát triển. Hãy đảm bảo tôi có quyền gửi tin nhắn DM cho bạn.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SendDev(bot))

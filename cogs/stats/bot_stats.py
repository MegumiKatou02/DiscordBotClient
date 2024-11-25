from datetime import timedelta
import time
from discord import app_commands
import discord
from discord.ext import commands

import config
import setup_bot

class BotStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @app_commands.command(name="bot_stats", description="Thông tin về bot")
    async def info(self, interaction: discord.Interaction):
        bot = interaction.client

        bot_name = bot.user.name
        bot_avatar = bot.user.avatar.url
        guild_count = len(bot.guilds)
        member_count = sum(len(guild.members) for guild in bot.guilds)
        channel_count = sum(len(guild.text_channels) + len(guild.voice_channels) for guild in bot.guilds)

        uptime_seconds = time.time() - self.start_time
        bot_uptime = str(timedelta(seconds=uptime_seconds))

        bot_owner_id = config.USER_ID
        bot_owner = await interaction.guild.fetch_member(bot_owner_id)
        bot_owner_name = bot_owner.name if bot_owner else "Không tìm thấy"

        version_bot = setup_bot.VERSION

        embed = discord.Embed(title=f"Thông tin bot: {bot_name}", color=0xff0033)
        embed.set_thumbnail(url=bot_avatar)
        embed.add_field(name="Phiên bản", value=version_bot, inline=False)
        embed.add_field(name="Số lượng server", value=guild_count, inline=False)
        embed.add_field(name="Số lượng thành viên", value=member_count, inline=False)
        embed.add_field(name="Số lượng kênh", value=channel_count, inline=False)
        embed.add_field(name="Thời gian hoạt động", value=str(bot_uptime), inline=False)
        embed.add_field(name="Chủ sở hữu bot", value=bot_owner_name, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BotStats(bot))
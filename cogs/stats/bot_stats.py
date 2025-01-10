from datetime import datetime
import time
from discord import app_commands
import discord
from discord.ext import commands

import config
from utils.json_handle import JsonHandler

class BotStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.data = JsonHandler("template/bot.json", "load")

    @app_commands.command(name="bot_stats", description="Thông tin về bot")
    async def info(self, interaction: discord.Interaction):
        bot = interaction.client

        bot_name = bot.user.name
        bot_avatar = bot.user.avatar.url
        guild_count = len(bot.guilds)
        member_count = sum(len(guild.members) for guild in bot.guilds)
        channel_count = sum(len(guild.text_channels) + len(guild.voice_channels) for guild in bot.guilds)

        uptime_seconds = time.time() - self.start_time
        uptime_datetime: datetime = datetime.fromtimestamp(time.time() - uptime_seconds)
        formatted_uptime = f"<t:{int(uptime_datetime.timestamp())}>"
        discord_timestamp_relative = f"<t:{int(self.start_time)}:R>"
        combined_uptime = f"{formatted_uptime} ({discord_timestamp_relative})"

        bot_owner_id = config.USER_ID
        bot_owner = await interaction.guild.fetch_member(bot_owner_id)
        bot_owner_name = bot_owner.name if bot_owner else "Yukiookii"

        version_bot = self.data["version"]

        embed = discord.Embed(title=f"Thông tin bot: {bot_name}", color=0xFFFFFF)
        embed.set_thumbnail(url=bot_avatar)
        embed.add_field(name="Phiên bản", value=version_bot, inline=False)
        embed.add_field(name="Số lượng server", value=guild_count, inline=False)
        embed.add_field(name="Số lượng thành viên", value=member_count, inline=True)
        embed.add_field(name="Số lượng kênh", value=channel_count, inline=True)
        embed.add_field(name="Thời gian hoạt động", value=combined_uptime, inline=False)
        embed.add_field(name="Chủ sở hữu bot", value=bot_owner_name, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BotStats(bot))
from discord import app_commands
import discord
from discord.ext import commands

class ServerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="server_stats", description="Xem thống kê thành viên trong server")
    async def server_stats(self, interaction: discord.Interaction):
        guild = interaction.guild
        if not guild:
            await interaction.response.send_message("Không thể lấy thông tin từ server này", ephemeral=True)
            return

        total_members = guild.member_count
        
        members = [member for member in guild.members if not member.bot]
        bots = [member for member in guild.members if member.bot]
        
        total_users = len(members) 
        total_bots = len(bots)   
        
        online_members = len([member for member in guild.members if member.status != discord.Status.offline])

        embed = discord.Embed(
            title=f"Thống Kê Server: {guild.name}",
            color=0xFFFFFF
        )
        embed.add_field(name="Tổng số thành viên", value=total_members, inline=False)
        embed.add_field(name="Số thành viên (người)", value=total_users, inline=True)
        embed.add_field(name="Số bot", value=total_bots, inline=True)
        embed.add_field(name="Thành viên đang online", value=online_members, inline=False)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerStats(bot))
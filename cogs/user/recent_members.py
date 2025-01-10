import discord
from discord.ext import commands
from discord import app_commands

class RecentMembers(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="recent_members", description="Danh sách các thành viên đã tham gia gần đây")
    async def recent_members(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Bạn không có quyền sử dụng lệnh này", ephemeral=True)
            return

        guild = interaction.guild

        sorted_members = sorted(guild.members, key=lambda member: member.joined_at, reverse=True)

        recent_members = sorted_members[:10]

        if not recent_members:
            await interaction.response.send_message("Không có thành viên nào trong server", ephemeral=True)
            return

        member_info = []
        for member in recent_members:
            join_date = f"<t:{int(member.joined_at.timestamp())}>"
            join_long = f"<t:{int(member.joined_at.timestamp())}:R>"
            member_info.append(f"**{member.name}**  - {join_date} ({join_long})")

        embed = discord.Embed(
            title="Các thành viên tham gia gần đây",
            description="\n".join(member_info),
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(RecentMembers(bot))
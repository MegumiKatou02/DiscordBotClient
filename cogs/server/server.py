import discord
from discord.ext import commands
from discord import app_commands

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description = "Hiển thị thông tin máy chủ") #
    async def server(self, interaction: discord.Interaction):
        guild = interaction.guild

        embed = discord.Embed(title=f"Thông tin về server {guild.name}", color=discord.Color.blue())

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        else:
            embed.add_field(name="Icon Server", value='Không có icon', inline=False)
        embed.add_field(name="Tên Server", value=guild.name, inline=False)
        embed.add_field(name="ID Server", value=guild.id, inline=False)
        embed.add_field(name="Ngày tạo", value=guild.created_at.strftime('%d-%m-%Y %H:%M:%S'), inline=False)
        embed.add_field(name="Số Thành Viên", value=guild.member_count, inline=False)
        embed.add_field(name="Số Kênh", value=len(guild.channels), inline=False)

        owner = guild.owner
        embed.add_field(name="Server Owner", value=owner.mention, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Server(bot))
import discord
import requests
from discord.ext import commands
from discord import app_commands

class AnimeImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_anime_image(self, anime_name: str):
        url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
        response = requests.get(url)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            anime_image = data["data"][0]["images"]["jpg"]["image_url"]
            return anime_image
        return None
    
    @app_commands.command(name="anime", description="Tìm kiếm hình ảnh anime theo tên")
    async def anime_command(self, interaction: discord.Interaction, anime_name: str):
        image_url = self.get_anime_image(anime_name)

        if image_url:
            embed = discord.Embed(
                title=f"Hình ảnh anime: {anime_name}",
                color=discord.Color.blue()
            )
            embed.set_image(url=image_url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Không tìm thấy hình ảnh anime với tên này", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AnimeImage(bot))
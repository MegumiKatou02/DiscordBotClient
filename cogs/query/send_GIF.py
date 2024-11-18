import random
import discord
import requests
from discord.ext import commands
from discord import app_commands

import config

GIPHY_API_KEY = config.GIPHY_API_KEY
GIPHY_URL = "https://api.giphy.com/v1/gifs/search"

class SendGIF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_gif(self, style: str):
        query = style + ' anime'
        params = {
            'q': query,
            'api_key': GIPHY_API_KEY,
            'limit': 10
        }
        response = requests.get(GIPHY_URL, params=params)
        data = response.json()

        if data['data']:
            return random.choice(data['data'])['images']['original']['url']
        else:
            return None

    @app_commands.command(name="hug", description="Lệnh ôm ai đó và gửi GIF")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug_command(self, interaction: discord.Interaction, user: discord.Member):
        """Lệnh ôm ai đó và gửi GIF"""
        gif_url = await self.fetch_gif("hug")
        if gif_url:
            embed = discord.Embed(
                title=f"{interaction.user} hugs {user.name}",
                description=f"Here's a GIF of a hug for {user.mention}!",
                color=discord.Color.blue()
            )
            embed.set_image(url=gif_url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{interaction.user} hugs {user.name}, nhưng không tìm thấy GIF :(")

    @hug_command.error
    async def hug_command_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            await interaction.response.send_message(f"Bạn phải đợi {round(error.retry_after, 1)} giây trước khi sử dụng lại lệnh này.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SendGIF(bot))
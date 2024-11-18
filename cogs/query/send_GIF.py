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
    async def hug_command(self, interaction: discord.Interaction, user: discord.Member):
        """Lệnh ôm ai đó và gửi GIF"""
        gif_url = await self.fetch_gif("hug")
        if gif_url:
            await interaction.response.send_message(f"{interaction.user} hugs {user.mention}!\n{gif_url}")
        else:
            await interaction.response.send_message(f"{interaction.user} hugs {user.mention}, nhưng không tìm thấy GIF :(")

async def setup(bot):
    await bot.add_cog(SendGIF(bot))
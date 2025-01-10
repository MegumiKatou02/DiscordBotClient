import random
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
from enum import Enum
import config

GIPHY_API_KEY = config.GIPHY_API_KEY
GIPHY_URL = "https://api.giphy.com/v1/gifs/search"

class Action(Enum):
    KISS = 'kiss',
    HUG = 'hug'

class SendGIF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def get_pharse(self, source: str, style: str, target: str):
        hug = [
            f"{target} receives a big, warm hug from {source}!",
            f"{target} is enveloped in a cozy hug by {source}.",
            f"{target} gets a sweet hug from {source}.",
            f"{target} is hugged tightly by {source}.",
            f"A warm embrace for {target} from {source}!"
        ]
        kiss = [
            f"{target} receives a loving kiss from {source}!",
            f"{target} gets a sweet kiss from {source}.",
            f"A kiss on the cheek for {target} from {source}.",
            f"{target} is kissed by {source}.",
            f"{target} gets a gentle kiss from {source}!"
        ]

        if style == "hug":
            return random.choice(hug)
        elif style == "kiss":
            return random.choice(kiss)
        return ""

    async def fetch_gif(self, style: str, interaction: discord.Interaction, user: discord.Member):
        query = style + ' anime'
        params = {
            'q': query,
            'api_key': GIPHY_API_KEY,
            'limit': 10
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(GIPHY_URL, params=params) as response:
                data = await response.json()

                if data['data']:
                    gif_url = random.choice(data['data'])['images']['original']['url']
                    title_random = self.get_pharse(interaction.user, style, user.name)

                    embed = discord.Embed(
                        title=title_random,
                        description=f"Here's a GIF of a {style} for {user.mention}!",
                        color=discord.Color.blue()
                    )
                    embed.set_image(url=gif_url)
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message(f"{interaction.user} {style} {user.name}, nhưng không tìm thấy GIF :(")

    @app_commands.command(name="hug", description="Lệnh ôm ai đó và gửi GIF")
    async def hug_command(self, interaction: discord.Interaction, user: discord.Member):
        if user == interaction.user:
            responses = [
                f"Hugging yourself... 🤗 Somebody, come give you a hug!",
                f"Giving yourself a big, warm hug! Don't be sad~ 💖",
                f"Hugging yourself... Do you need a hug from someone special? <(\")",
                f"Wrapping yourself up in a cozy blanket for a self-hug~ ☁️💞",
                f"Snuggling a pillow tightly! Everything's gonna be okay~ 💕"
            ]
            await interaction.response.send_message(random.choice(responses))
        else:
            await self.fetch_gif(Action.HUG.value, interaction, user)

    @app_commands.command(name="kiss", description="Lệnh kiss ai đó và gửi GIF")
    async def kiss(self, interaction: discord.Interaction, user: discord.Member):
        if user == interaction.user:
            responses = [
            f"Kisses themselves... 😘 Loving yourself is amazing!",
            f"Gives themselves a cheek kiss~ UwU 💕",
            f"Blows a kiss to themselves! 💋✨",
            f"Smooches themselves! Someone should come and claim this kiss~ 💞",
            f"Rewards themselves with a cute kiss! You're awesome! <(\")"
        ]
            await interaction.response.send_message(random.choice(responses))
        else:
            await self.fetch_gif(Action.KISS.value, interaction, user)

async def setup(bot):
    await bot.add_cog(SendGIF(bot))
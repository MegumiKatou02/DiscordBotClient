import discord
import requests

def get_anime_image(anime_name: str):
    url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
    response = requests.get(url)
    data = response.json()

    if "data" in data and len(data["data"]) > 0:
        anime_image = data["data"][0]["images"]["jpg"]["image_url"]
        return anime_image
    return None

async def anime_command(interaction: discord.Interaction, anime_name: str):
    image_url = get_anime_image(anime_name)

    if image_url:
        embed = discord.Embed(
            title=f"Hình ảnh anime: {anime_name}",
            color=discord.Color.blue()
        )
        embed.set_image(url=image_url)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Không tìm thấy hình ảnh anime với tên này", ephemeral=True)
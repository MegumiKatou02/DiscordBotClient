import discord
from discord import app_commands
from discord.ext import commands


class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="emoji_image", description="Hiển thị hình ảnh của emoji")
    async def emoji_command(self, interaction: discord.Interaction, emoji: str):
        custom_emoji = None

        if emoji.startswith("<") and emoji.endswith(">"):
            emoji_id = emoji.split(":")[-1][:-1]
            custom_emoji = discord.utils.get(self.bot.emojis, id=int(emoji_id))

        if custom_emoji:
            embed = discord.Embed(
                # title=f"Hình ảnh của emoji: {emoji}",
                title=f"Emoji:",
                color=discord.Color.blue()
            )
            embed.set_image(url=custom_emoji.url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Không hợp lệ: hãy chắc rằng bạn nhập emoji trong server và đúng định dạng (ᓀ ᓀ)", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Emoji(bot))
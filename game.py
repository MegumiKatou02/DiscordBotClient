import random
import discord
from discord.ext import commands

async def roll(interaction: discord.Interaction, min_value: int = 0, max_value: int = 1000):
    if min_value > max_value:
        await interaction.response.send_message('Số nhỏ hơn phải đứng trước số lớn hơn.', ephemeral = True)
        return

    result = random.randint(min_value, max_value)
    await interaction.response.send_message(f'Kết quả: {result}')
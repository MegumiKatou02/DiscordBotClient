import random
import discord
from discord.ext import commands
from discord import app_commands

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def roll(self, interaction: discord.Interaction, min_value: int = 0, max_value: int = 1000):
        if min_value > max_value:
            await interaction.response.send_message('Nhập sai thứ tự', ephemeral = True)
            return
        
        if max_value > 100000:
            await interaction.response.send_message('Yêu cầu nhập số nhỏ hơn 100000', ephemeral = True)
            return

        result = random.randint(min_value, max_value)
        await interaction.response.send_message(f'Kết quả: {result}')

    @app_commands.command(name = 'roll', description="Random số")
    async def roll_command(self, interaction: discord.Interaction, min_value: int = 0, max_value: int = 1000):
        await self.roll(interaction, min_value, max_value)

async def setup(bot):
    await bot.add_cog(Roll(bot))
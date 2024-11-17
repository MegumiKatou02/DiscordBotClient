import random
from discord.ext import commands

async def roll(ctx, min_value: int = 0, max_value: int = 1000):
    if min_value > max_value:
        await ctx.send('Số nhỏ hơn phải đứng trước số lớn hơn.')
        return

    result = random.randint(min_value, max_value)
    await ctx.send(f'Kết quả: {result}')
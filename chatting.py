import re
from discord.ext import commands

async def on_message(message, bot):
    greetings = ['chào', 'hello', 'hi', 'yo']

    if any(re.fullmatch(r'\b' + greeting + r'\b', message.content.lower()) for greeting in greetings) and not message.author.bot:
        await message.channel.send(f"Chào bạn, {message.author.name} :3")

    await bot.process_commands(message)
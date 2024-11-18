import asyncio
import re
from discord.ext import commands

async def on_message(message, bot):
    greetings = ['chào', 'hello', 'hi', 'yo']

    if any(re.fullmatch(r'\b' + greeting + r'\b', message.content.lower()) for greeting in greetings) and not message.author.bot:
        await message.channel.send(f"Chào bạn, {message.author.name} :3")

    if not message.author.bot and message.content.lower().startswith('chinh bel bel nga sap duong'):
        await message.channel.send('Co m nga ay')

    if bot.user.mentioned_in(message) and not message.author.bot:
        hello_message = await message.channel.send("Nhấn `/help` để biết thêm thông tin !")

        await asyncio.sleep(5)
        
        await hello_message.delete()

    await bot.process_commands(message)
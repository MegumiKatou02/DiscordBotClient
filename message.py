import asyncio
import random
import re

greetings = ['chào', 'hello', 'hi', 'yo']

async def on_message_event(message, bot):
    responses = [
        f"Chào bạn, {message.author.name} :3",
        f"Hi {message.author.name}, chúc bạn một ngày tốt lành! 🌞",
        f"Xin chào, {message.author.name}, bạn có khỏe không? 😊",
        f"Chào bạn {message.author.name}, mình rất vui được gặp bạn! 😄",
        f"Hey {message.author.name}, có gì vui không? 🤗"
    ]
    
    if any(re.fullmatch(r'\b' + greeting + r'\b', message.content.lower()) for greeting in greetings) and not message.author.bot:
        response = random.choice(responses) 
        await message.channel.send(response)

    # if not message.author.bot and message.content.lower().startswith('chinh bel bel nga sap duong'):
    #     await message.channel.send('Co m nga ay')

    if not message.author.bot and re.search(r'\bbel bel nga sap duong\b$', message.content.lower()):
        await message.channel.send('Co m nga ay')

    if not message.author.bot and re.search(r'\bchinh bel\b$', message.content.lower()):
        await message.channel.send('Co m bel ay')

    if not message.author.bot and re.search(r'\bching bel\b$', message.content.lower()):
        await message.channel.send('Co m bel ay')

    if bot.user.mentioned_in(message) and not message.author.bot:
        hello_message = await message.channel.send("Nhấn `/help` để biết thêm thông tin !")

        await asyncio.sleep(3)
        
        await hello_message.delete()

    await bot.process_commands(message)
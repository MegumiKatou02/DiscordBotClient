import asyncio
import random
import re
import discord
from discord.ext import commands
from fuzzywuzzy import fuzz
from itertools import permutations
import requests
import config

greetings = ['chào', 'hello', 'hi', 'yo']

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_similar(self, input_text, target_text, threshold=70):
        return fuzz.ratio(input_text.lower(), target_text.lower()) >= threshold

    def generate_permutations(self, phrase):

        words = phrase.split()
        perms = [" ".join(p) for p in permutations(words)]
        return perms

    def is_variant_of_chinh_bel(self, input_text):
        base_phrases = [
            "chinh bel", "chinh beo", "chinh béo", "chinh bai veo", "chinh bái vẻo",
            "chinh bel@L", "chinh be<@!707188474012500028>", "chinh be<@!1111129182110486598>",
            "<@!604949724788817920> beo"
        ]
        
        target_texts = []
        for phrase in base_phrases:
            target_texts.extend(self.generate_permutations(phrase))
        
        special_cases = ["chb", "chinhb", "chinh b"]
        target_texts.extend(special_cases)
        
        for target_text in target_texts:
            if fuzz.ratio(input_text.lower(), target_text.lower()) >= 70:
                return True

        pattern = re.compile(
            r'\b(?:chinh|ching|chInh|chIng|chink|chin)\s+(?:bel|beo|béo|beI|bai veo|bái vẻo|bai|vẻo)\b', 
            re.IGNORECASE
        )
        return bool(pattern.search(input_text))

    async def ocr_space(self, url, overlay=False, api_key=config.ORC_SPACE, language='eng'):

        payload = {
            'url': url,
            'isOverlayRequired': overlay,
            'apikey': api_key,
            'language': language,
        }
        response = requests.post(
            'https://api.ocr.space/parse/image',
            data=payload,
        )
        result = response.json()
        if result['IsErroredOnProcessing']:
            print(f"Lỗi từ OCR.space: {result['ErrorMessage']}")
            return None
        return result['ParsedResults'][0]['ParsedText']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                    extracted_text = await self.ocr_space(attachment.url)
                    # print(extracted_text)
                    if extracted_text:
                        # await message.channel.send(f"Văn bản trích xuất từ hình ảnh:\n```{extracted_text}```")
                        if self.is_variant_of_chinh_bel(extracted_text.lower()):
                            await message.channel.send("Co m beo ay")
                    else:
                        # await message.channel.send("Không thể trích xuất văn bản từ hình ảnh.")
                        print("Không thể trích xuất văn bản từ hình ảnh.")
                    break

        responses = [
            f"Chào bạn, {message.author.name} :3",
            f"Hi {message.author.name}, chúc bạn một ngày tốt lành! 🌞",
            f"Xin chào, {message.author.name}, bạn có khỏe không? 😊",
            f"Chào bạn {message.author.name}, mình rất vui được gặp bạn! 😄",
            f"Hey {message.author.name}, có gì vui không? 🤗"
        ]

        if any(re.fullmatch(r'\b' + greeting + r'\b', message.content.lower()) for greeting in greetings):
            response = random.choice(responses)
            await message.channel.send(response)

        if self.is_similar(message.content.lower(), "Chinh bel bel nga sap duong"):
            await message.channel.send('Co m nga ay')

        if self.is_variant_of_chinh_bel(message.content.lower()):
            await message.channel.send('Co m bel ay')

        if message.content.lower() == "o o":
            emojis = ["🐔", "⁉️"]  
            try:
                for emoji in emojis:
                    if emoji:
                        await message.add_reaction(emoji)
            except discord.HTTPException as e:
                print(f"Không thể thêm reaction: {e}")

        if re.search(r'\b(?:an co|ăn cỏ)\b$', message.content.lower()):
            emoji = random.choice(["🐂", "🐄"])
            try:
                await message.add_reaction(emoji)
            except discord.HTTPException as e:
                print(f"Không thể thêm reaction: {e}")

        if self.bot.user.mentioned_in(message):
            hello_message = await message.channel.send("Nhấn `/help` để biết thêm thông tin !")
            await asyncio.sleep(3)
            await hello_message.delete()

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(OnMessage(bot))
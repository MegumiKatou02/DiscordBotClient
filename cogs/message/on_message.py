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

MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '/': ' ', '': ''
}

def decode_morse(morse_code):
    words = morse_code.strip().split(' / ')
    decoded_message = []
    for word in words:
        letters = word.split(' ')
        decoded_word = []
        for letter in letters:
            decoded_word.append(MORSE_CODE_DICT.get(letter, ''))
        decoded_message.append(''.join(decoded_word))
    return ' '.join(decoded_message)

def decode_binary(binary_str):
    binary_values = binary_str.split()
    text = ''
    for binary in binary_values:
        decimal = int(binary, 2)
        text += chr(decimal)
    return text

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
        if all(char in ['-', '.', ' ', '/'] for char in input_text):
            decoded_text = decode_morse(input_text)
            if decoded_text:
                input_text = decoded_text.lower()

        if all(char in ['0', '1', ' '] for char in input_text):
            decoded_text = decode_binary(input_text)
            if decoded_text:
                input_text = decoded_text.lower()

        if len(input_text.split()) < 2:
            return False

        base_phrases = [
            # "chinh bel", "chinh beo", "chinh béo", "chinh bai veo", "chinh bái vẻo",
            # "chinh bel@L", "chinh be<@!707188474012500028>", "chinh be<@!1111129182110486598>",
            "<a:BK_Letter_C:983550902801678377> <a:BK_Letter_H:983550904957542460><a:BK_Letter_I:983550898150178837>  <a:BK_Letter_N:983550920203845642> <a:BK_Letter_G:983550879737204766><a:BK_Letter_B:983550875245117480><a:BK_Letter_E:983550918186373150><a:BK_Letter_L:983550893486137384>",
            # "<@!604949724788817920> beo",
        ]
        
        target_texts = []
        for phrase in base_phrases:
            target_texts.extend(self.generate_permutations(phrase))
        
        # special_cases = ["chb", "chinhb", "chinh b"]
        # target_texts.extend(special_cases)
        
        for target_text in target_texts:
            if fuzz.ratio(input_text.lower(), target_text.lower()) >= 70:
                # print("fuzz")
                return True

        pattern = re.compile(
            r'\b(?:chinh|ching|chInh|chIng|chink|chin|cking|ckink|ck3nk|<@!604949724788817920>|ckinh)\s+(?:bel|beo|béo|beI|bai veo|bái vẻo|bai|vẻo)\b', 
            re.IGNORECASE
        )
        # if pattern.search(input_text):
        #     print("regex")

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
        
        # print(message.content)

        if message.attachments:
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                    extracted_text = await self.ocr_space(attachment.url)
                    if extracted_text:
                        if self.is_variant_of_chinh_bel(extracted_text.lower()):
                            await message.channel.send("Co m bel ay")
                    else:
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

        # if self.is_variant_of_chinh_bel(message.content.lower()) and message.author.id != 604949724788817920:
        #     await message.channel.send('Co m bel ay')

        if self.is_variant_of_chinh_bel(message.content.lower()) and message.author.id != config.USER_ID:
            await message.channel.send('Co m bel ay')

        if message.content.lower().startswith("o o") or re.search(r'\bo o\b', message.content.lower()):
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
            await asyncio.sleep(2.6)
            await hello_message.delete()

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(OnMessage(bot))
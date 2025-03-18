import discord
from discord import app_commands
from discord.ext import commands
import json
import aiohttp

class NoiTu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_started = False
        self.last_word = "" 
        self.channel = None 
        self.last_player = None
        self.used_words = set()
        self.word_cache = {}  
        self.scores = {}

    # is_valid, is_stuck
    async def is_valid_word(self, word):
        if word in self.word_cache:
            return self.word_cache[word], False

        url = f"https://vietnamese-dictionary-api.vercel.app/api/search?word={word}&next=true"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
            
                        is_valid = data.get("valid", False)

                        nextSuggest = data.get("next")

                        if nextSuggest and len(nextSuggest) == 1:
                            nextSplit = nextSuggest[0].split()
                            if len(nextSplit) > 1 and nextSplit[0] == nextSplit[1]:
                                return is_valid, True

                        is_stuck: bool = not nextSuggest

                        self.word_cache[word] = is_valid 

                        return is_valid, is_stuck
                    else:
                        print(f"Lỗi khi gọi API: {response.status}")
                        return False, False
        except Exception as e:
            print(f"Lỗi khi kết nối đến API: {e}")
            return False, False
        # return word.lower() in self.valid_words

    @app_commands.command(name="noitu", description="Quản lý trò chơi nối từ")
    @app_commands.describe(action="Hành động", channel="Kênh để bắt đầu trò chơi")
    @app_commands.choices(
        action=[
            app_commands.Choice(name="Bắt đầu", value="start"),
            app_commands.Choice(name="Kết thúc", value="end"),
        ]
    )
    async def noitu(self, interaction: discord.Interaction, action: app_commands.Choice[str], channel: discord.TextChannel = None):
        if action.value == "start":
            if self.game_started:
                await interaction.response.send_message("Trò chơi đã bắt đầu rồi!", ephemeral=True)
                return

            if channel is None:
                await interaction.response.send_message("Vui lòng chọn kênh để bắt đầu trò chơi!", ephemeral=True)
                return

            self.game_started = True
            self.last_word = ""
            self.channel = channel
            self.last_player = None
            self.used_words = set()
            self.used_words.add(self.last_word)

            await interaction.response.send_message(f"Trò chơi đã được nâng cấp từ điển kể từ ngày 14/03/2025. Nếu bạn nghĩ có một số từ bị thiếu hoặc sai sót xin đừng chửi Ching :sob:, chửi tôi đây này (toi chinh la Nerine).\n\nTrò chơi nối từ đã bắt đầu trong kênh {channel.mention}! Hãy bắt đầu với từ đầu tiên hợp lệ")

        elif action.value == "end":
            if not self.game_started:
                await interaction.response.send_message("Trò chơi chưa bắt đầu!", ephemeral=True)
                return

            self.game_started = False
            self.last_word = ''
            self.channel = None
            self.last_player = None
            self.used_words = set()
            self.scores = {}

            await interaction.response.send_message("Kết thúc trò chơi!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.game_started or message.channel != self.channel or message.author.bot:
            return

        if message.author == self.last_player:
            await message.add_reaction("❌")
            await message.reply("Không được nối liên tiếp", delete_after=5)
            return

        word = message.content.lower().strip()

        if word in self.used_words:
            await message.add_reaction("❌")
            await message.reply(f"Từ **{word}** đã được sử dụng trước đó!", delete_after=5)
            return
        
        is_valid, is_stuck = await self.is_valid_word(word)

        if not is_valid:
            await message.add_reaction("❌")
            await message.reply(f"Từ **{word}** không có trong từ điển", delete_after=5)
            return

        ### Còn lại đều là valid :v

        new_words = word.split()
        last_words = self.last_word.split()
        if  (self.last_word != '') and (new_words[0] != last_words[-1]):
            await message.add_reaction("❌")
            await message.reply(f"Từ **{word}** không hợp lệ. Từ tiếp theo phải bắt đầu bằng chữ **'{last_words[-1]}'**!", delete_after=5)
            return

        self.last_word = word
        self.last_player = message.author
        self.used_words.add(word)

        self.scores[message.author.global_name] = self.scores.get(message.author.global_name, 0) + 1
        await message.add_reaction("✅")

        if is_stuck:
            self.scores[message.author.global_name] = self.scores.get(message.author.global_name, 0) - 2
            await message.channel.send(f"{message.author.global_name} bị trừ 2đ vì nối từ đến giới hạn :penguin:")

            score_text = "\n".join(f"{user}: {score} điểm" for user, score in self.scores.items())
            await message.channel.send(f"Trò chơi kết thúc vì không có từ nào hợp lệ nữa\n\n**Bảng xếp hạng:**\n{score_text}")

            self.scores = {}
            self.game_started = False
            return

        await message.reply(f"Từ **{word}** hợp lệ. Tiếp tục", delete_after=5)

async def setup(bot):
    await bot.add_cog(NoiTu(bot))
import discord
from discord import app_commands
from discord.ext import commands
import json

class NoiTu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_started = False
        self.last_word = "" 
        self.channel = None 
        self.last_player = None
        self.used_words = set()

        with open("cogs/game/vietnamese_words.json", "r", encoding="utf-8") as f:
            self.valid_words = set(item["text"].lower() for item in json.load(f))

    def is_valid_word(self, word):
        return word.lower() in self.valid_words

    @app_commands.command(name="noitu", description="Quản lý trò chơi nối từ")
    @app_commands.describe(action="Hành động (start/end)", channel="Kênh để bắt đầu trò chơi")
    async def noitu(self, interaction: discord.Interaction, action: str, channel: discord.TextChannel = None):
        if action == "start":
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

            await interaction.response.send_message(f"Trò chơi nối từ đã bắt đầu trong kênh {channel.mention}! Hãy bắt đầu với từ đầu tiên hợp lệ")

        elif action == "end":
            if not self.game_started:
                await interaction.response.send_message("Trò chơi chưa bắt đầu!", ephemeral=True)
                return

            self.game_started = False
            self.last_word = ''
            self.channel = None
            self.last_player = None
            self.used_words = set()

            await interaction.response.send_message("Kết thúc trò chơi!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.game_started or message.channel != self.channel or message.author.bot:
            return

        if message.author == self.last_player:
            await message.add_reaction("❌")
            await message.reply("Không được nối liền kề!", delete_after=5)
            return

        word = message.content.lower().strip()

        if word in self.used_words:
            await message.add_reaction("❌")
            await message.reply(f"Từ **{word}** đã được sử dụng trước đó!", delete_after=5)
            return

        if not self.is_valid_word(word):
            await message.add_reaction("❌")
            await message.reply(f"Từ **{word}** không có trong từ điển", delete_after=5)
            return

        new_words = word.split()
        last_words = self.last_word.split()
        if  (self.last_word != '') and (new_words[0] != last_words[-1]):
            await message.add_reaction("❌")
            await message.reply(f"Từ **{word}** không hợp lệ. Từ tiếp theo phải bắt đầu bằng chữ **'{last_words[-1]}'**!", delete_after=5)
            return

        self.last_word = word
        self.last_player = message.author
        self.used_words.add(word)

        await message.add_reaction("✅")
        await message.reply(f"Từ **{word}** hợp lệ. Tiếp tục", delete_after=5)

async def setup(bot):
    await bot.add_cog(NoiTu(bot))
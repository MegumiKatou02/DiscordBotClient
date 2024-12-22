import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from datetime import datetime, timedelta
import re
import sympy as sp

class Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #goodbye
    @app_commands.command(name="goodbye", description="Goodbye")
    async def goodbye(self, interaction: discord.Interaction):
        await interaction.response.send_message("Cook gium cai <(\")")

    #say
    @app_commands.command(name="say", description="Nói thông qua bot")
    async def say(self, interaction: discord.Interaction, *, message: str):
        await interaction.response.send_message("Đang xử lý...", ephemeral=True)
        await interaction.channel.purge(limit=1, check=lambda msg: msg.author == interaction.user)
        await interaction.channel.send(message)

    #choose
    @app_commands.command(name="choose", description = "Random 1 trong nhiều lựa chọn")
    async def choose(self, interaction: discord.Interaction, choice1: str, choice2: str, choice3: str = None, 
                    choice4: str = None, choice5: str = None, choice6: str = None, choice7: str = None,
                    choice8: str = None, choice9: str = None, choice10: str = None):
        choice_list = [choice1, choice2, choice3, choice4, choice5, choice6, choice7, choice8, choice9, choice10]
        
        choice_list = [choice.strip() for choice in choice_list if choice]
        
        if not choice_list:
            await interaction.response.send_message("Please provide some options to choose from!", ephemeral=True)
            return
        
        chosen_option = random.choice(choice_list)
        
        await interaction.response.send_message(f"I choose: {chosen_option}")

    #find member
    @app_commands.command(name= "find_member", description="Tạo ra chủ đề và tìm người chiến thắng")
    async def find_member(self, interaction: discord.Interaction, topic: str,
                        member1: discord.Member,
                        member2: discord.Member = None, 
                        member3: discord.Member = None,
                        member4: discord.Member = None,
                        member5: discord.Member = None,
                        member6: discord.Member = None,
                        member7: discord.Member = None,
                        member8: discord.Member = None,
                        member9: discord.Member = None,
                        member10: discord.Member = None):
        members = [member for member in [member1, member2, member3, member4, member5,
                                        member6, member7, member8, member9, member10] if member]

        if not members:
            await interaction.response.send_message("Please provide some options to choose from!", ephemeral=True)
            return
        
        chosen_member = random.choice(members)

        await interaction.response.send_message(f'**{topic}**: {chosen_member.mention}')

    #reminder
    @app_commands.command(description="Đặt nhắc nhở")
    async def reminder(self, interaction: discord.Interaction, time: str, *, message: str):
        try:
            reminder_time = datetime.strptime(time, "%H:%M")
            
            now = datetime.now()
            wait_time = (reminder_time - now).total_seconds()

            if wait_time < 0:
                reminder_time += timedelta(days=1)
                wait_time = (reminder_time - now).total_seconds()

            await interaction.response.send_message(f"Nhắc nhở của bạn đã được đặt vào lúc {reminder_time.strftime('%H:%M')}! Tôi sẽ nhắc bạn: **{message}**", ephemeral=True)

            await asyncio.sleep(wait_time)

            await interaction.user.send(f"**Nhắc nhở bạn đã đặt**: {message}")
        
        except ValueError:
            await interaction.response.send_message("Vui lòng nhập thời gian đúng định dạng HH:MM (vd: 02:24)", ephemeral=True)

    #math
    @app_commands.command(name="math", description="Tính toán biểu thức toán học")
    async def math_command(self, interaction: discord.Interaction, expression: str):
        try:
            expression = expression.replace("^", "**")
            expression = expression.replace("e", "E")
            expression = re.sub(r'(\d+)!', r'factorial(\1)', expression)

            result = sp.sympify(expression)
            answer = result.evalf()
            form_answer = str(answer).rstrip('0').rstrip('.') if '.' in str(answer) else str(answer)

            await interaction.response.send_message(f"Kết quả: {form_answer}")
        except (sp.SympifyError, ValueError, ZeroDivisionError) as e:
            await interaction.response.send_message(f"Lỗi cú pháp hoặc toán học trong biểu thức: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Extension(bot))
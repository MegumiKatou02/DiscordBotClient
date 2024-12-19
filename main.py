import asyncio
from datetime import datetime, timedelta
import random
import re
import discord
from discord.ext import commands
import sympy as sp
import psutil

import Anime
from message import on_message_event
import config
import game
import help_list
import Weather
from pypresence import Presence

import setup_bot

CLIENT_ID = setup_bot.CLIENT_ID

intents = discord.Intents.default()  
intents.message_content = True 
intents.members = True
intents.guilds = True
intents.presences = True

clients = commands.Bot(command_prefix='>>', intents=intents)

@clients.event
async def on_ready():
    print("ready !!!")
    print("----------")

    game = discord.Game("Khu Wibu")
   
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="Khu Wibu",
        details="Playing in the Misty Woods",
        assets={
            'large_image': 'catlove',
            'large_text': 'Playing in the Misty Woods',
            'small_image': 'https://i.pinimg.com/736x/3f/8d/86/3f8d868caa3b401449d4ca027b738031.jpg',
            'small_text': 'Example User'
        }
    )
    await clients.change_presence(activity=activity)

    # load corgs
    await load_cogs()

    await clients.tree.sync() 

    print("----------")

    print('Servers bot đã tham gia:')
    for guild in clients.guilds:
        print(f' - {guild.name} (ID: {guild.id})')

    for guild in clients.guilds:
        owner = guild.owner
        if owner:
            try:
                embed = discord.Embed(
                    title=f"📢 Thông báo từ {guild.name}",
                    description=(
                        f"**Tiếng Việt:**\n"
                        f"Chào bạn **{owner.name}** từ **{guild.name}**, cảm ơn bạn đã mời bot của chúng tôi vào server của bạn.\n"
                        f"Liệu bạn có thể cho chúng tôi biết server của bạn dùng ngôn ngữ gì không?\n"
                        f"Chúng tôi sẽ thiết lập ngôn ngữ cho bot của mình dựa trên ngôn ngữ mà server của bạn sử dụng.\n"
                        f"Nếu được xin hãy dùng lệnh `/send_dev`. Hãy gửi theo cú pháp `/send_dev [ngôn ngữ] [tên server của bạn]`.\n\n"
                        f"**English:**\n"
                        f"Hello **{owner.name}** from **{guild.name}**, thank you for inviting our bot to your server.\n"
                        f"Could you please let us know what language your server primarily uses?\n"
                        f"We will configure the bot's language based on your server's preferred language.\n"
                        f"If possible, please use the command `/send_dev`. Send it in the format: `/send_dev [language] [your server's name]`."
                    ),
                    color=discord.Color.blue()
                )
                embed.set_footer(text="Cảm ơn bạn đã sử dụng bot của chúng tôi! | Thank you for using our bot!")

                await owner.send(embed=embed)
            except discord.Forbidden:
                print(f"Không thể nhắn tin cho owner của server: {guild.name} (ID: {guild.id}) do họ đã tắt tin nhắn trực tiếp.")
    print("Đã gửi tin nhắn cho tất cả chủ sở hữu server.")


#load file cogs
async def load_cogs():
    await clients.load_extension("cogs.query.send_GIF")

    await clients.load_extension("cogs.user.userInfo")

    await clients.load_extension("cogs.emoji.emoji_image")
    await clients.load_extension("cogs.emoji.steal_emoji")

    await clients.load_extension("cogs.notification")
    await clients.load_extension("cogs.voice")
    
    await clients.load_extension("cogs.stats.server_stats")
    await clients.load_extension("cogs.stats.bot_stats")

    await clients.load_extension("cogs.administration.event")
    await clients.load_extension("cogs.administration.notification")
    await clients.load_extension("cogs.administration.lock")

    await clients.load_extension("cogs.delete_mess")
    await clients.load_extension("cogs.avatar")
    await clients.load_extension("cogs.send_dev")
    await clients.load_extension("cogs.event_server")
    
#goodbye
@clients.tree.command()
async def goodbye(interaction: discord.Interaction):
    await interaction.response.send_message("Cook gium cai <(\")")

#say
@clients.tree.command(description="Nói thông qua bot")
async def say(interaction: discord.Interaction, *, message: str):
    await interaction.response.send_message("Đang xử lý...", ephemeral=True)
    await interaction.channel.purge(limit=1, check=lambda msg: msg.author == interaction.user)
    await interaction.channel.send(message)

#roll
@clients.tree.command(name = 'roll', description="Random số")
async def roll_command(interaction: discord.Interaction, min_value: int = 0, max_value: int = 1000):
    await game.roll(interaction, min_value, max_value)

#check prefix //
@clients.event
async def on_message(message):
    await on_message_event(message, clients)

#server
@clients.tree.command(description = "Hiển thị thông tin máy chủ") #
async def server(interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(title=f"Thông tin về server {guild.name}", color=discord.Color.blue())

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    else:
        embed.add_field(name="Icon Server", value='Không có icon', inline=False)
    embed.add_field(name="Tên Server", value=guild.name, inline=False)
    embed.add_field(name="ID Server", value=guild.id, inline=False)
    embed.add_field(name="Ngày tạo", value=guild.created_at.strftime('%d-%m-%Y %H:%M:%S'), inline=False)
    embed.add_field(name="Số Thành Viên", value=guild.member_count, inline=False)
    embed.add_field(name="Số Kênh", value=len(guild.channels), inline=False)

    owner = guild.owner
    embed.add_field(name="Server Owner", value=owner.mention, inline=False)

    await interaction.response.send_message(embed=embed)

#help
@clients.tree.command(description="Help and show commands")
async def help(interaction: discord.Interaction):
    await help_list.send_help_message(interaction)

#run
@clients.command()
async def run(ctx):
    await ctx.send("Khu Wibu bot discord is running")

#choose
@clients.tree.command(name="choose", description = "Random 1 trong nhiều lựa chọn")
async def choose(interaction: discord.Interaction, choice1: str, choice2: str, choice3: str = None, 
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
@clients.tree.command(name= "find_member", description="Tạo ra chủ đề và tìm người chiến thắng")
async def find_member(interaction: discord.Interaction, topic: str,
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
@clients.tree.command(description="Đặt nhắc nhở")
async def reminder(interaction: discord.Interaction, time: str, *, message: str):
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

#recent members
@clients.tree.command(description="Danh sách các thành viên đã tham gia gần đây")
async def recent_members(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Bạn không có quyền sử dụng lệnh này", ephemeral=True)
        return

    guild = interaction.guild

    sorted_members = sorted(guild.members, key=lambda member: member.joined_at, reverse=True)

    recent_members = sorted_members[:10]

    if not recent_members:
        await interaction.response.send_message("Không có thành viên nào trong server", ephemeral=True)
        return

    member_info = []
    for member in recent_members:
        join_date = member.joined_at.strftime('%d-%m-%Y %H:%M:%S')
        member_info.append(f"**{member.name}**  -  Tham gia vào: {join_date}")

    embed = discord.Embed(
        title="Các thành viên tham gia gần đây",
        description="\n".join(member_info),
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)

#weather
@clients.tree.command(description="Kiểm tra thời tiết tại một thành phố")
async def weather(interaction: discord.Interaction, city_name: str):
    await Weather.weather_command(interaction, city_name)

#anime
@clients.tree.command(name="anime", description="Tìm kiếm hình ảnh anime theo tên")
async def anime(interaction: discord.Interaction, name: str):
    await Anime.anime_command(interaction, name)

#math
@clients.tree.command(name="math", description="Tính toán biểu thức toán học")
async def math_command(interaction: discord.Interaction, expression: str):
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

@clients.tree.command()
async def log_memory_usage(interaction: discord.Interaction):
    process = psutil.Process()
    mem_info = process.memory_info()
    await interaction.response.send_message(f"RSS: {mem_info.rss / 1024 / 1024:.2f} MB")

clients.run(config.TOKEN)
import discord
from discord.ext import commands
from tabulate import tabulate

import chatting
import config
import game

intents = discord.Intents.default()  
intents.message_content = True 
intents.members = True

clients = commands.Bot(command_prefix='>>', intents=intents)

@clients.event
async def on_ready():
    print("ready !!!")
    print("----------")
    game = discord.Game("Khu Wibu")
    await clients.change_presence(activity=game)

    # Hoặc, bạn có thể sử dụng các trạng thái khác
    # streaming = discord.Streaming(name="Chơi game trên Twitch", url="https://www.twitch.tv/yourchannel")
    # await clients.change_presence(activity=streaming)

    print("----------")

@clients.command()
async def hello(ctx):
    await ctx.send("Hello, I am bot")

@clients.command()
async def goodbye(ctx):
    await ctx.send("Cook gium cai <(\")")

@clients.event
async def member_join(member):
    channel = clients.get_channel(1210656611270533222)
    if channel:
        print("nice.")
        await channel.send(f"Welcome, {member.name}!")
    else:
        print("Channel not found or invalid channel ID.")

@clients.command()
async def list_members(ctx):
    guild = ctx.guild
    members = '\n'.join([member.name for member in guild.members])
    await ctx.send(f"Members:\n{members}")

@clients.command()
async def say(ctx, *, message: str):
    await ctx.message.delete()
    
    await ctx.send(message)

@clients.command(name = 'roll')
async def roll_command(ctx, min_value: int = 0, max_value: int = 1000):
    await game.roll(ctx, min_value, max_value)

@clients.event
async def on_message(message):
    await chatting.on_message(message, clients) 

    # await clients.process_commands(message)

@clients.command()
async def server_info(ctx):
    # Lấy thông tin về server (guild)
    guild = ctx.guild

    # Tạo embed để hiển thị thông tin server
    embed = discord.Embed(title=f"Thông tin về server {guild.name}", color=discord.Color.blue())

    # Thêm các trường thông tin vào embed
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    else:
        embed.add_field(name="Icon Server", value='Không có icon', inline=False)
    embed.add_field(name="Tên Server", value=guild.name, inline=False)
    embed.add_field(name="ID Server", value=guild.id, inline=False)
    embed.add_field(name="Ngày tạo", value=guild.created_at.strftime('%d-%m-%Y %H:%M:%S'), inline=False)
    embed.add_field(name="Số Thành Viên", value=guild.member_count, inline=False)
    embed.add_field(name="Số Kênh", value=len(guild.channels), inline=False)

    # Gửi Embed vào channel
    await ctx.send(embed=embed)

clients.run(config.TOKEN)
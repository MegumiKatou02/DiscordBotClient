import random
import discord
from discord.ext import commands
from tabulate import tabulate
from discord.ui import Select, View

import chatting
import config
import game
import help_list

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

    await clients.tree.sync() 

    print("----------")

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

@clients.command()
async def helpkwb(ctx):
    await help_list.send_help_message(ctx)

@clients.tree.command(description="Hiển thị avatar của một thành viên")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    if not member:
        member = interaction.user  
    
    avatar_url = member.display_avatar.url 

    embed = discord.Embed(
        title=f"Avatar của {member.display_name}",
        description="",
        color=discord.Color.blue()
    )
    embed.set_image(url=avatar_url)

    await interaction.response.send_message(embed=embed)
    
@clients.tree.command(description="Hiển thị avatar của một thành viên")
async def avt(interaction: discord.Interaction, member: discord.Member = None):
    if not member:
        member = interaction.user  
    
    avatar_url = member.display_avatar.url 

    embed = discord.Embed(
        title=f"Avatar của {member.display_name}",
        description="",
        color=discord.Color.blue()
    )
    embed.set_image(url=avatar_url)

    await interaction.response.send_message(embed=embed)

@clients.command()
async def run(ctx):
    await ctx.send("Khu Wibu bot discord is running")

@clients.tree.command(name="choose", description = "Random 1 trong nhiều lựa chọn")
async def choose(interaction: discord.Interaction, choice1: str, choice2: str, choice3: str = None, 
                 choice4: str = None, choice5: str = None, choice6: str = None, choice7: str = None,
                 choice8: str = None, choice9: str = None, choice10: str = None):
    choice_list = [choice1, choice2, choice3, choice4, choice5, choice6, choice7, choice8, choice9, choice10]
    
    choice_list = [choice.strip() for choice in choice_list if choice]
    
    if not choice_list:
        await interaction.response.send_message("Please provide some options to choose from!")
        return
    
    chosen_option = random.choice(choice_list)
    
    await interaction.response.send_message(f"I choose: {chosen_option}")

clients.run(config.TOKEN)
import discord
from discord.ext import commands

import config
import game

intents = discord.Intents.default()  
intents.message_content = True 
intents.members = True

clients = commands.Bot(command_prefix='!', intents=intents)

@clients.event
async def on_ready():
    print("ready !!!")
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

clients.run(config.TOKEN)
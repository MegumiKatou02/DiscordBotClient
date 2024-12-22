import asyncio
from datetime import datetime, timedelta
import random
import re
import discord
from discord.ext import commands
import sympy as sp
import psutil

from message import on_message_event
import config
from pypresence import Presence

import setup_bot
import individual
import json
import template

CLIENT_ID = setup_bot.CLIENT_ID

intents = discord.Intents.default()  
intents.message_content = True 
intents.members = True
intents.guilds = True
intents.presences = True

clients = commands.Bot(command_prefix='>>', intents=intents)

config_bot = "template/bot.json"

@clients.event
async def on_ready():
    print("ready !!!")
    print("----------")

    with open("template/bot.json", "r", encoding="utf-8") as f:
        config_bot = json.load(f)
    state = config_bot["state"]
    
    # game = discord.Game("Khu Wibu")
   
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name= state,
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


#load file cogs
async def load_cogs():
    await clients.load_extension("cogs.extension.extension")

    await clients.load_extension("cogs.help.help_list")

    await clients.load_extension("cogs.query.send_GIF")
    await clients.load_extension("cogs.query.anime_image")
    await clients.load_extension("cogs.query.weather")

    await clients.load_extension("cogs.server.server")

    await clients.load_extension("cogs.user.userInfo")
    await clients.load_extension("cogs.user.recent_members")

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

    await clients.load_extension("cogs.game.roll")

    await clients.load_extension("cogs.message.on_message")

#run
@clients.command()
async def run(ctx):
    await ctx.send("Khu Wibu bot discord is running")

@clients.tree.command()
async def log_memory_usage(interaction: discord.Interaction):
    process = psutil.Process()
    mem_info = process.memory_info()
    await interaction.response.send_message(f"RSS: {mem_info.rss / 1024 / 1024:.2f} MB")

clients.run(config.TOKEN_TEST_BOT) # **/ignore
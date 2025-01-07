#*
#           Copyright belongs to Yukiookii and Haiku team 2024   
#
#           Contribute: https://github.com/MegumiKatou02/DiscordBotClient.git
#
#           Email contact: ledinhchinh.dev@gmail.com  
# 
#
#*#

import discord
from discord.ext import commands
import psutil
import config
import setup_bot
from Util.json_handle import JsonHandler

CLIENT_ID = setup_bot.CLIENT_ID

intents = discord.Intents.default()  
intents.message_content = True 
intents.members = True
intents.guilds = True
intents.presences = True

clients = commands.Bot(command_prefix='>>', intents=intents)

data = JsonHandler("template/bot.json", "load")

is_ready = False

@clients.event
async def on_ready():
    global is_ready
    if not is_ready:
        is_ready = True
        print("ready !!!")
        print("----------")

        state = data["state"]
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name=state
        )
        await clients.change_presence(activity=activity)

        await load_cogs()

        try:
            await clients.tree.sync()
            print("Slash commands synced ngon :3!")
        except Exception as e:
            print(f"Failed to sync slash commands :< : {e}")

        print("----------")
        print('Servers bot đã tham gia:')
        for guild in clients.guilds:
            print(f' - {guild.name} (ID: {guild.id})')


#load file cogs
async def load_cogs():
    cogs = [
        "cogs.administration.delete_mess",
        "cogs.administration.event",
        "cogs.administration.lock",
        "cogs.administration.notification",
        "cogs.administration.voice",

        "cogs.emoji.emoji_image",
        "cogs.emoji.steal_emoji",

        "cogs.event.event_server",

        "cogs.extension.extension",
        "cogs.extension.notification",
        "cogs.extension.send_dev",

        "cogs.game.roll",
        "cogs.game.word_association",

        "cogs.help.help_list",

        "cogs.message.on_message",

        "cogs.query.anime_image",
        "cogs.query.send_GIF",
        "cogs.query.weather",

        "cogs.server.server",

        "cogs.stats.bot_stats",
        "cogs.stats.server_stats",
        
        "cogs.user.avatar",
        "cogs.user.recent_members",
        "cogs.user.userInfo"
    ]
    
    for cog in cogs:
        try:
            await clients.load_extension(cog)
        except Exception as e:
            print(f"Failed to load {cog}: {e}")
    

@clients.event
async def on_guild_join(guild: discord.Guild):
    print("--------------------")
    print(f"Bot đã được thêm vào server: {guild.name} (ID: {guild.id})")
    print(f"Chủ server: {guild.owner} (ID: {guild.owner_id})")
    print(f"Số lượng thành viên: {guild.member_count}")
    print("--------------------")

#run
@clients.command()
async def run(ctx):
    if not ctx.message.author.bot:
        await ctx.send("{} bot discord is running".format(data["name"]))

@clients.tree.command(description="log memory usage")
async def log_memory_usage(interaction: discord.Interaction):
    process = psutil.Process()
    mem_info = process.memory_info()
    await interaction.response.send_message(f"RSS: {mem_info.rss / 1024 / 1024:.2f} MB")

clients.run(config.TOKEN_TEST_BOT) # **/ignore
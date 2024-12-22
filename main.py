import discord
from discord.ext import commands
import psutil
import config
import setup_bot
from Util.jsonLoad import JsonLoad

CLIENT_ID = setup_bot.CLIENT_ID

intents = discord.Intents.default()  
intents.message_content = True 
intents.members = True
intents.guilds = True
intents.presences = True

clients = commands.Bot(command_prefix='>>', intents=intents)

data = JsonLoad("template/bot.json")

@clients.event
async def on_ready():
    print("ready !!!")
    print("----------")

    state = data["state"]
    
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name= state
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
    await clients.load_extension("cogs.administration.delete_mess")
    await clients.load_extension("cogs.administration.event")
    await clients.load_extension("cogs.administration.lock")
    await clients.load_extension("cogs.administration.notification")
    await clients.load_extension("cogs.administration.voice")

    await clients.load_extension("cogs.emoji.emoji_image")
    await clients.load_extension("cogs.emoji.steal_emoji")

    await clients.load_extension("cogs.event.event_server")

    await clients.load_extension("cogs.extension.extension")
    await clients.load_extension("cogs.extension.notification")
    await clients.load_extension("cogs.extension.send_dev")

    await clients.load_extension("cogs.game.roll")

    await clients.load_extension("cogs.help.help_list")

    await clients.load_extension("cogs.message.on_message")

    await clients.load_extension("cogs.query.anime_image")
    await clients.load_extension("cogs.query.send_GIF")
    await clients.load_extension("cogs.query.weather")

    await clients.load_extension("cogs.server.server")

    await clients.load_extension("cogs.stats.bot_stats")
    await clients.load_extension("cogs.stats.server_stats")

    await clients.load_extension("cogs.user.avatar")
    await clients.load_extension("cogs.user.recent_members")
    await clients.load_extension("cogs.user.userInfo")
    
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
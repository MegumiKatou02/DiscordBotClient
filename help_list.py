import discord
from discord.ext import commands

async def send_help_message(ctx):
    message = """
    **`prefix: >>`**
    **goodbye**
    **list_members**
    **say**
    **roll**
    **server_info**
    **helpkwb**
    **avatar (hoặc avt)**
    """
    embed = discord.Embed(
        title="Commands bot Khu Wibu",
        description="tính đến thời điểm hiện tại",
        color=discord.Color.blue() 
    )
    
    embed.set_thumbnail(url=ctx.bot.user.avatar.url)

    embed.add_field(name="", value= message, inline=False)
    await ctx.author.send(embed = embed)
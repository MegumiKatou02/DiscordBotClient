from discord.ext import commands

async def send_help_message(ctx):
    message = """
    --- Lệnh bot Khu Wibu --
        (tính đến hiện tại)
    >>goodbye
    >>list_members
    >>say
    >>roll
    >>server_info
    >>helpkwb
    """
    await ctx.author.send(message)
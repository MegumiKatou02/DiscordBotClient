import discord
from discord.ext import commands

async def send_help_message(interaction: discord.Interaction):
    message = """
    **/goodbye**
    **/say**
    **/roll**
    **/server**
    **/help**
    **/avatar /avt**
    **/choose**
    **/find_member**
    **/reminder**
    **/recent_members (permissions administrator)**
    **/weather**
    **/anime**
    **/math**
    **/event**
    **/events_list (permissions administrator)**
    Nếu có vấn đề hoặc bot có lỗi xin liên hệ bằng **/send_dev**
    """
    embed = discord.Embed(
        title="Commands bot Khu Wibu",
        description="tính đến thời điểm hiện tại",
        color=discord.Color.green() 
    )
    
    embed.set_thumbnail(url=interaction.client.user.avatar.url)

    embed.add_field(name="", value= message, inline=False)
    
    try:
        await interaction.user.send(embed=embed)
        await interaction.response.send_message("Hãy kiểm tra DM của bạn ! 📩", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("Không thể gửi tin nhắn riêng. Hãy kiểm tra cài đặt DM của bạn.", ephemeral=True)
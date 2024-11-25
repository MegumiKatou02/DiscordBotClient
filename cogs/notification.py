import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from datetime import datetime
import config

class NotificationServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = "database/notifications.db"
        self.init_database()
        self.allowed_user_id = config.USER_ID

    def init_database(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                creator_id INTEGER,
                creator_name TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

    def get_notifications(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT message, creator_name, timestamp FROM notifications")
        notifications = cursor.fetchall()
        conn.close()
        return notifications
    
    @app_commands.command(name="notification", description="Kiểm tra thông báo.")
    async def check_notifications(self, interaction: discord.Interaction):
        notifications = self.get_notifications()

        for msg in notifications:
            lines = msg[0]

            lines = lines.replace("\\n", "\n")
            
            description = f"{lines}\nNgười tạo: {msg[1]}\nThời gian: {msg[2]}\n"

        if notifications:
            embed = discord.Embed(
                title="Danh sách thông báo",
                description=description,
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("Không có thông báo nào.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(NotificationServer(bot))
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from datetime import datetime
import config

class Notification(commands.Cog):
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

    def save_notification(self, message, creator_id, creator_name):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notifications (message, creator_id, creator_name, timestamp)
            VALUES (?, ?, ?, ?)
        """, (message, creator_id, creator_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()

    def delete_all_notifications(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notifications")
        conn.commit()
        conn.close()

    def delete_notifications_range(self, start, end):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM notifications
            WHERE notification_id BETWEEN ? AND ?
        """, (start, end))
        conn.commit()
        conn.close()

    @app_commands.command(name="make_notification", description="Kiểm tra thông báo")
    async def make_notification(self, interaction: discord.Interaction, message: str):
        if interaction.user.id != self.allowed_user_id:
            await interaction.response.send_message("Chỉ nhà phát triển mới dùng được lệnh này", ephemeral=True)
            return

        self.save_notification(message, interaction.user.id, interaction.user.name)
        await interaction.response.send_message(f"Thông báo đã được tạo: {message}", ephemeral=True)

    @app_commands.command(name="clear_notifications", description="Xóa thông báo hoặc một khoảng thông báo.")
    async def clear_notifications(self, interaction: discord.Interaction, start: int = None, end: int = None):
        if interaction.user.id != self.allowed_user_id:
            await interaction.response.send_message("Chỉ nhà phát triển mới dùng được lệnh này", ephemeral=True)
            return

        if start is None and end is None:
            self.delete_all_notifications()
            await interaction.response.send_message("Tất cả thông báo đã được xóa!", ephemeral=True)
        elif start is not None and end is not None:
            if start > end:
                await interaction.response.send_message("Tham số không hợp lệ! `start` phải nhỏ hơn hoặc bằng `end`.", ephemeral=True)
                return

            self.delete_notifications_range(start, end)
            await interaction.response.send_message(f"Đã xóa thông báo từ {start} đến {end}!", ephemeral=True)
        else:
            await interaction.response.send_message("Vui lòng cung cấp cả `start` và `end` hoặc không cung cấp tham số nào để xóa tất cả.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Notification(bot))
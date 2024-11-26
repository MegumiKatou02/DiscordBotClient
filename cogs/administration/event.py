import discord
import sqlite3
from discord import app_commands
from discord.ext import commands

import config

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = "database/events.db"
        self.init_database()
        self.allowed_user_id = config.USER_ID

    def init_database(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                server_id TEXT,
                event_code TEXT,
                name TEXT,
                topic TEXT,
                end_time TEXT,
                creator_id INTEGER,
                creator_name TEXT,
                PRIMARY KEY (server_id, event_code)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                server_id TEXT,
                event_code TEXT,
                user_id INTEGER,
                user_name TEXT,
                PRIMARY KEY (server_id, event_code, user_id)
            )
        """)
        conn.commit()
        conn.close()

    def get_event_count_per_server(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT server_id, COUNT(*) 
            FROM events 
            GROUP BY server_id
        """)
        results = cursor.fetchall()
        conn.close()
        return results


    @app_commands.command(name="event_counts", description="Hiển thị số lượng sự kiện trong từng server")
    async def event_counts(self, interaction: discord.Interaction):
        if interaction.user.id != self.allowed_user_id:
            await interaction.response.send_message("Chỉ nhà phát triển mới dùng được lệnh này", ephemeral=True)
            return

        results = self.get_event_count_per_server()

        if not results:
            await interaction.response.send_message("Hiện không có sự kiện nào trên các server.", ephemeral=True)
            return

        event_summary = []
        for server_id, count in results:
            server = self.bot.get_guild(int(server_id))
            server_name = server.name if server else "Không xác định"
            event_summary.append(f"**Server**: {server_name} (ID: {server_id})\n**Số sự kiện**: {count}")

        embed = discord.Embed(
            title="Số lượng sự kiện trong từng server",
            description="\n\n".join(event_summary),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Event(bot))
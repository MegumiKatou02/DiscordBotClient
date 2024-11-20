import discord
import sqlite3
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View
from datetime import datetime, timedelta
import re

class EventServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_file = "database/events.db"
        self.init_database()
        self.check_events_end.start()

    def init_database(self):
        """Khởi tạo cơ sở dữ liệu SQLite."""
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

    def save_event(self, server_id, event_code, name, topic, end_time, creator_id, creator_name):
        """Lưu sự kiện vào cơ sở dữ liệu."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO events (server_id, event_code, name, topic, end_time, creator_id, creator_name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (server_id, event_code, name, topic, end_time.strftime("%Y-%m-%d %H:%M:%S"), creator_id, creator_name))
        conn.commit()
        conn.close()

    def delete_event(self, server_id, event_code):
        """Xóa sự kiện khỏi cơ sở dữ liệu."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE server_id = ? AND event_code = ?", (server_id, event_code))
        cursor.execute("DELETE FROM participants WHERE server_id = ? AND event_code = ?", (server_id, event_code))
        conn.commit()
        conn.close()

    def add_participant(self, server_id, event_code, user_id, user_name):
        """Thêm người tham gia vào sự kiện."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO participants (server_id, event_code, user_id, user_name)
            VALUES (?, ?, ?, ?)
        """, (server_id, event_code, user_id, user_name))
        conn.commit()
        conn.close()

    def remove_participant(self, server_id, event_code, user_id):
        """Xóa người tham gia khỏi sự kiện."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM participants
            WHERE server_id = ? AND event_code = ? AND user_id = ?
        """, (server_id, event_code, user_id))
        conn.commit()
        conn.close()

    def get_events(self, server_id):
        """Lấy danh sách sự kiện từ cơ sở dữ liệu."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE server_id = ?", (server_id,))
        events = cursor.fetchall()
        conn.close()
        return events
    
    @tasks.loop(minutes=1)
    async def check_events_end(self):
        """Kiểm tra và xóa các sự kiện đã kết thúc."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT server_id, event_code, end_time FROM events")
        events = cursor.fetchall()
        current_time = datetime.now()

        for server_id, event_code, end_time in events:
            end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            if current_time >= end_time_obj:
                self.delete_event(server_id, event_code)
                print(f"Sự kiện {event_code} đã kết thúc và đã bị xóa.")
        conn.close()

    def parse_duration(self, duration: str):
        """Chuyển đổi chuỗi như '3d2h' thành đối tượng timedelta."""
        days, hours, minutes = 0, 0, 0

        days_match = re.search(r'(\d+)d', duration)
        if days_match:
            days = int(days_match.group(1))

        hours_match = re.search(r'(\d+)h', duration)
        if hours_match:
            hours = int(hours_match.group(1))

        minutes_match = re.search(r'(\d+)m', duration)
        if minutes_match:
            minutes = int(minutes_match.group(1))

        return timedelta(days=days, hours=hours, minutes=minutes)

    @app_commands.command(name="event", description="Tạo sự kiện với mã sự kiện, tên, chủ đề và thời gian kết thúc")
    async def event(self, interaction: discord.Interaction, event_code: str, name: str, topic: str, duration: str):
        """Tạo một sự kiện mới với mã sự kiện, tên, chủ đề và thời gian kết thúc."""
        topic = topic.replace("\\n", "\n")
        try:
            duration_obj = self.parse_duration(duration)
        except ValueError:
            await interaction.response.send_message("Định dạng thời gian không hợp lệ!", ephemeral=True)
            return

        if duration_obj < timedelta(minutes=1):
            await interaction.response.send_message("Thời gian kết thúc phải lớn hơn 1 phút!", ephemeral=True)
            return

        end_time_obj = datetime.now() + duration_obj
        server_id = str(interaction.guild.id)

        existing_events = self.get_events(server_id)
        if any(event[1] == event_code for event in existing_events):
            await interaction.response.send_message(f"Mã sự kiện '{event_code}' đã tồn tại!", ephemeral=True)
            return

        self.save_event(server_id, event_code, name, topic, end_time_obj, interaction.user.id, interaction.user.name)

        join_button = Button(label="Tham gia", style=discord.ButtonStyle.green)
        leave_button = Button(label="Huỷ tham gia", style=discord.ButtonStyle.red)

        async def join_callback(interaction: discord.Interaction):
            server_id = str(interaction.guild.id)
            user_id = interaction.user.id
            user_name = interaction.user.name

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM participants
                WHERE server_id = ? AND event_code = ? AND user_id = ?
            """, (server_id, event_code, user_id))
            already_participated = cursor.fetchone()[0] > 0
            conn.close() ##

            if already_participated:
                await interaction.response.send_message("Bạn đã tham gia sự kiện này trước đó!", ephemeral=True)
                return

            self.add_participant(server_id, event_code, user_id, user_name)
            await interaction.response.send_message(f"Bạn đã tham gia sự kiện: {name}!", ephemeral=True)

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM participants
                WHERE server_id = ? AND event_code = ?
            """, (server_id, event_code))
            participant_count = cursor.fetchone()[0]
            conn.close()

            embed = discord.Embed(
                title=f"Sự kiện: {name}",
                description=(
                    f"**Người tạo**: {user_name}\n"
                    f"**Chủ đề**: \n  {topic}\n"
                    f"**Thời gian kết thúc**: {end_time_obj.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"**Số người tham gia: {participant_count}**"
                ),
                color=discord.Color.blue()
            )
            await interaction.message.edit(embed=embed)
       
        async def leave_callback(interaction: discord.Interaction):
            if self.check_end_event(datetime.now()):
                await interaction.response.send_message("Sự kiện này đã kết thúc, bạn không thể tham gia nữa.", ephemeral=True)
                return

            server_id = str(interaction.guild.id)
            user_id = interaction.user.id
            user_name = interaction.user.name

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM participants
                WHERE server_id = ? AND event_code = ? AND user_id = ?
            """, (server_id, event_code, user_id))
            is_participant = cursor.fetchone()[0] > 0
            conn.close()

            if not is_participant:
                await interaction.response.send_message("Bạn chưa tham gia sự kiện này, không thể huỷ tham gia!", ephemeral=True)
                return

            self.remove_participant(server_id, event_code, user_id)
            await interaction.response.send_message(f"Bạn đã huỷ tham gia sự kiện: {name}!", ephemeral=True)

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM participants
                WHERE server_id = ? AND event_code = ?
            """, (server_id, event_code))
            participant_count = cursor.fetchone()[0]
            conn.close()

            embed = discord.Embed(
                title=f"Sự kiện: {name}",
                description=(
                    f"**Người tạo**: {user_name}\n"
                    f"**Chủ đề**: \n  {topic}\n"
                    f"**Thời gian kết thúc**: {end_time_obj.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    f"**Số người tham gia: {participant_count}**"
                ),
                color=discord.Color.blue()
            )
            await interaction.message.edit(embed=embed)

        join_button.callback = join_callback
        leave_button.callback = leave_callback

        view = View()
        view.add_item(join_button)
        view.add_item(leave_button)

        embed = discord.Embed(
            title=f"Sự kiện: {name}",
            description=(
                f"**Người tạo**: {interaction.user.name}\n"
                f"**Chủ đề**: \n  {topic}\n"
                f"**Thời gian kết thúc**: {end_time_obj.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"**Số người tham gia: 0**"
            ),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="events_list", description="Liệt kê danh sách sự kiện có trong Server")
    async def events_in_server(self, interaction: discord.Interaction):
        server_id = str(interaction.guild.id)

        events = self.get_events(server_id)

        if not events:
            await interaction.response.send_message("Không có sự kiện nào trong server này.", ephemeral=True)
            return

        event_list = []
        for event in events:
            event_code, name, end_time, creator_name = event[1], event[2], event[4], event[6]
            end_time_obj = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            event_list.append(f"**Mã sự kiện**: {event_code}\n"
                            f"**Tên sự kiện**: {name}\n"
                            f"**Thời gian kết thúc**: {end_time_obj.strftime('%Y-%m-%d %H:%M:%S')}\n"
                            f"**Người tạo**: {creator_name}\n")

        
        embed = discord.Embed(
            title="Danh sách sự kiện",
            description="\n".join(event_list),
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed)
            
async def setup(bot):
    await bot.add_cog(EventServer(bot))
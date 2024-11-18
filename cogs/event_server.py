import discord
import json
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View
import os
from datetime import datetime, timedelta
import re

class EventServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events_data_file = "data/events_data.json"
        self.load_events_data()
        self.check_events_end.start() 

    def load_events_data(self):
        """Tải dữ liệu sự kiện từ tệp JSON."""
        if os.path.exists(self.events_data_file) and os.path.getsize(self.events_data_file) > 0:
            try:
                with open(self.events_data_file, "r") as file:
                    self.events_data = json.load(file)

                    for server_id, events in self.events_data.items():
                        for event_info in events.values():
                            event_info["end_time"] = datetime.strptime(event_info["end_time"], "%Y-%m-%d %H:%M:%S")
            except json.JSONDecodeError:
                print("Tệp JSON không hợp lệ. Sử dụng dữ liệu mặc định.")
                self.events_data = {} 
        else:
            self.events_data = {} 

    def save_events_data(self):
        """Lưu dữ liệu sự kiện vào tệp JSON."""
        os.makedirs(os.path.dirname(self.events_data_file), exist_ok=True)

        with open(self.events_data_file, "w") as file:
            events_data = {}
            for server_id, events in self.events_data.items():
                events_data[server_id] = {}
                for event_code, event_info in events.items():
                    events_data[server_id][event_code] = {
                        "name": event_info["name"],
                        "topic": event_info["topic"],
                        "end_time": event_info["end_time"].strftime("%Y-%m-%d %H:%M:%S") if "end_time" in event_info else None,
                        "creator_id": event_info["creator_id"],
                        "creator_name": event_info["creator_name"],
                        "participants": [{"id": participant["id"], "name": participant["name"]} for participant in event_info["participants"]]
                    }
            json.dump(events_data, file, indent=4)

    @tasks.loop(minutes=1)
    async def check_events_end(self):
        """Kiểm tra và xóa các sự kiện đã kết thúc."""
        current_time = datetime.now()

        for server_id, events in list(self.events_data.items()):
            for event_code, event_info in list(events.items()):
                if "end_time" in event_info:
                    end_time = event_info["end_time"]
                    if current_time >= end_time:
                        del self.events_data[server_id][event_code] 
                        self.save_events_data() 
                        print(f"Sự kiện {event_code} đã kết thúc và đã bị xóa.")

    def parse_duration(self, duration: str):
        """Chuyển đổi chuỗi như '3d2h' thành đối tượng timedelta."""
        days, hours, minutes = 0, 0, 0

        # Tìm các đơn vị ngày, giờ và phút trong chuỗi
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

#event
    @app_commands.command(name="event", description="Tạo sự kiện với mã sự kiện, tên, chủ đề và thời gian kết thúc")
    @app_commands.describe(
        event_code="Mã sự kiện duy nhất (không trùng lặp).",
        name="Tên sự kiện của bạn.",
        topic="Chủ đề mô tả sự kiện (có thể xuống dòng bằng \\n).",
        duration="Thời gian kết thúc sự kiện, ví dụ: 3d2h"
    )
    async def event(self, interaction: discord.Interaction, event_code: str, name: str, topic: str, duration: str):
        """Tạo một sự kiện mới với mã sự kiện, tên, chủ đề và thời gian kết thúc."""

        topic = topic.replace("\\n", "\n")

        try:
            duration_obj = self.parse_duration(duration)
            
        except ValueError:
            await interaction.response.send_message("Định dạng thời gian kết thúc không hợp lệ. Vui lòng nhập theo định dạng 'XdYhZm' (ví dụ: 3d2h1m).", ephemeral=True)
            return

        one_minute = timedelta(minutes=1) 
        if(duration_obj < one_minute):
            await interaction.response.send_message("Thời gian kết thúc phải lớn hơn 1 phút", ephemeral=True)
            return

        end_time_obj = datetime.now() + duration_obj

        server_id = interaction.guild.id

        if server_id not in self.events_data:
            self.events_data[server_id] = {}

        if event_code in self.events_data[server_id]:
            await interaction.response.send_message(f"Sự kiện với mã '{event_code}' đã tồn tại trong server này.", ephemeral=True)
            return

        creator_id = interaction.user.id
        creator_name = interaction.user.name

        self.events_data[server_id][event_code] = {
            "name": name,
            "topic": topic,
            "end_time": end_time_obj,
            "creator_id": creator_id,
            "creator_name": creator_name,
            "participants": []
        }

        self.save_events_data()  
        join_button = Button(label="Tham gia", style=discord.ButtonStyle.green)
        leave_button = Button(label="Huỷ tham gia", style=discord.ButtonStyle.red)

        async def join_callback(interaction: discord.Interaction):
            if interaction.user.id not in [p["id"] for p in self.events_data[server_id][event_code]["participants"]]:
                self.events_data[server_id][event_code]["participants"].append({"id": interaction.user.id, "name": interaction.user.name})
                self.save_events_data() 
                await interaction.response.send_message(f"Bạn đã tham gia sự kiện: {name}!", ephemeral=True)
            else:
                await interaction.response.send_message("Bạn đã tham gia sự kiện này rồi!", ephemeral=True)

            embed = discord.Embed(
                title=f"Sự kiện: {name}",
                description=f"**Chủ đề**: {topic}\n**Thời gian kết thúc**: {end_time_obj.strftime('%Y-%m-%d %H:%M:%S')}\n**Người tạo**: {creator_name}\n\n**Số người tham gia: {len(self.events_data[server_id][event_code]['participants'])}**",
                color=discord.Color.blue()
            )
            await interaction.message.edit(embed=embed) 

        async def leave_callback(interaction: discord.Interaction):
            participants = self.events_data[server_id][event_code]["participants"]
            participant_to_remove = next((p for p in participants if p["id"] == interaction.user.id), None)
            if participant_to_remove:
                self.events_data[server_id][event_code]["participants"].remove(participant_to_remove)
                self.save_events_data()  
                await interaction.response.send_message(f"Bạn đã huỷ tham gia sự kiện: {name}!", ephemeral=True)
            else:
                await interaction.response.send_message("Bạn chưa tham gia sự kiện này!", ephemeral=True)

            embed = discord.Embed(
                title=f"Sự kiện: {name}",
                description=f"**Người tạo**: {creator_name}\n**Chủ đề**: \n  {topic}\n**Thời gian kết thúc**: {end_time_obj.strftime('%Y-%m-%d %H:%M:%S')}\n\n**Số người tham gia: {len(self.events_data[server_id][event_code]['participants'])}**",
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
            description=f"**Người tạo**: {creator_name}\n**Chủ đề**: \n  {topic}\n**Thời gian kết thúc**: {end_time_obj.strftime('%Y-%m-%d %H:%M:%S')}\n\n**Số người tham gia: 0**",
            color=discord.Color.blue()
        )

        await interaction.response.send_message(embed=embed, view=view)

#events list
    @app_commands.command(name="events_list", description="Liệt kê mã sự kiện, tên sự kiện và người tạo sự kiện trong server hiện tại.")
    async def events_in_server(self, interaction: discord.Interaction):
        server_id = str(interaction.guild.id)  

        try:
            with open('data/events_data.json', 'r', encoding='utf-8') as file:
                events_data = json.load(file)
        except FileNotFoundError:
            await interaction.response.send_message("Không tìm thấy dữ liệu sự kiện.", ephemeral=True)
            return

        if server_id not in events_data:
            await interaction.response.send_message("Không có sự kiện nào trong server này.", ephemeral=True)
            return

        server_events = events_data[server_id]

        embed = discord.Embed(title="Sự kiện trong server", color=discord.Color.blue())
        for event_code, event_info in server_events.items():
            embed.add_field(
                name=f"Mã sự kiện: {event_code} - Tên sự kiện: {event_info['name']}",
                value=f"Người tạo: {event_info['creator_name']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(EventServer(bot))

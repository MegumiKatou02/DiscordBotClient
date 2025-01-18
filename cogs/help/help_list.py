import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List

class HelpList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands_categories: Dict[str, List[Dict[str, str]]] = {
            "🎮 Giải Trí": [
                {"name": "goodbye", "desc": "Tạm biệt một ai đó"},
                {"name": "say", "desc": "Để bot nói hộ bạn"},
                {"name": "roll", "desc": "Random số ngẫu nhiên"},
                {"name": "choose", "desc": "Giúp bạn chọn lựa ngẫu nhiên"},
                {"name": "anime", "desc": "Tìm kiếm thông tin anime"}
            ],
            "🛠️ Tiện Ích": [
                {"name": "avatar", "desc": "Xem avatar người dùng"},
                {"name": "server", "desc": "Xem thông tin server"},
                {"name": "find_member", "desc": "Tìm kiếm thành viên"},
                {"name": "reminder", "desc": "Đặt nhắc nhở"},
                {"name": "weather", "desc": "Xem thông tin thời tiết"},
                {"name": "math", "desc": "Giải toán đơn giản"},
                {"name": "remove_bg", "desc": "Xóa background ảnh"}
            ],
            "📊 Thống Kê": [
                {"name": "server_stats", "desc": "Thống kê về server"},
                {"name": "bot_stats", "desc": "Thống kê về bot"},
                {"name": "userinfo", "desc": "Thông tin người dùng"}
            ],
            "⚡ Admin Tools": [
                {"name": "recent_members", "desc": "Xem thành viên mới (Admin)"},
                {"name": "events_list", "desc": "Quản lý sự kiện (Admin)"},
                {"name": "set_voice", "desc": "Cài đặt voice (Admin)"},
                {"name": "get_voice", "desc": "Xem cài đặt voice (Admin)"},
                {"name": "steal_emoji", "desc": "Thêm emoji vào server (Admin)"},
                {"name": "lock", "desc": "Khóa channel (Admin)"}
            ],
            "🔧 Quản Lý": [
                {"name": "channel_rename", "desc": "Đổi tên channel"},
                {"name": "delete_messenger", "desc": "Xóa tin nhắn"},
                {"name": "emoji_image", "desc": "Chuyển emoji thành ảnh"}
            ]
        }

    def create_help_embeds(self) -> List[discord.Embed]:
        embeds = []
        
        main_embed = discord.Embed(
            title="🤖 Hệ Thống Trợ Giúp - Khu Wibu Bot",
            description="Sử dụng `/help` để xem danh sách lệnh.\nMọi lệnh đều sử dụng prefix `/`",
            color=discord.Color.blue()
        )
        main_embed.add_field(
            name="📝 Thông Tin Quan Trọng",
            value="• Gặp vấn đề? Sử dụng `/send_dev`\n• Cập nhật mới? Xem `/notification`",
            inline=False
        )
        embeds.append(main_embed)

        for category, commands in self.commands_categories.items():
            embed = discord.Embed(
                title=f"{category}",
                color=discord.Color.blue()
            )
            
            for cmd in commands:
                embed.add_field(
                    name=f"/{cmd['name']}", 
                    value=cmd['desc'],
                    inline=True
                )
            
            embed.set_footer(text="💡 Mẹo: Dùng / để xem mô tả chi tiết của từng lệnh")
            embeds.append(embed)

        return embeds

    @app_commands.command(name="help", description="Xem danh sách lệnh và hướng dẫn sử dụng")
    async def help(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        embeds = self.create_help_embeds()
        
        try:
            dm_sent = False
            try:
                for embed in embeds:
                    await interaction.user.send(embed=embed)
                dm_sent = True
            except discord.Forbidden:
                dm_sent = False
            
            if dm_sent:
                await interaction.followup.send(
                    "📨 Đã gửi hướng dẫn vào tin nhắn riêng của bạn!",
                    ephemeral=True
                )
            else:
                message = await interaction.followup.send(
                    embeds=embeds[:1],
                    ephemeral=True
                )
                
                for embed in embeds[1:]:
                    await interaction.followup.send(
                        embed=embed,
                        ephemeral=True
                    )
                
        except Exception as e:
            await interaction.followup.send(
                f"❌ Có lỗi xảy ra: {str(e)}",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(HelpList(bot))
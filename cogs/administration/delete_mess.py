import discord
from discord.ext import commands

class DeleteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="delete_messenger", description="Xóa tin nhắn trong kênh")
    @discord.app_commands.describe(amount="Số lượng tin nhắn cần xóa", user="Tên người dùng (tuỳ chọn)")
    async def delete(self, interaction: discord.Interaction, amount: int, user: discord.Member = None):
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("Bạn không có quyền xóa tin nhắn.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        deleted_count = 0
        messages_to_delete_bulk = []
        messages_to_delete_single = []

        async for message in interaction.channel.history(limit=500):
            if user is None or message.author == user:
                if (discord.utils.utcnow() - message.created_at).days < 14:
                    messages_to_delete_bulk.append(message)
                else:
                    messages_to_delete_single.append(message)

                deleted_count += 1
                if deleted_count >= amount:
                    break

        if messages_to_delete_bulk:
            for i in range(0, len(messages_to_delete_bulk), 100):
                batch = messages_to_delete_bulk[i:i + 100]
                await interaction.channel.delete_messages(batch)

        for msg in messages_to_delete_single:
            await msg.delete()

        if deleted_count > 0:
            await interaction.followup.send(f"Đã xóa {deleted_count} tin nhắn", ephemeral=True)
        else:
            await interaction.followup.send("Không tìm thấy tin nhắn nào để xóa", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DeleteCog(bot))
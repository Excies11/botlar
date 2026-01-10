import discord
from discord.ext import commands
from datetime import datetime

LOG_CHANNEL_ID = 1409914069317718017  # mllog kanalı

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ================= READY =================
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Streaming(
                name="SSD Discord 🤍",
                url="https://twitch.tv/ssd"
            )
        )
        print("🎵 MUSIC BOT READY")

    def get_log_channel(self, guild):
        return guild.get_channel(LOG_CHANNEL_ID)

    # ================= MESSAGE DELETE =================
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        channel = self.get_log_channel(message.guild)
        if not channel:
            return

        embed = discord.Embed(
            title="🗑️ Mesaj Silindi",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Kullanıcı", value=message.author.mention)
        embed.add_field(name="Kanal", value=message.channel.mention)
        embed.add_field(name="İçerik", value=message.content[:1000], inline=False)

        await channel.send(embed=embed)

    # ================= MESSAGE EDIT =================
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return

        channel = self.get_log_channel(before.guild)
        if not channel:
            return

        embed = discord.Embed(
            title="✏️ Mesaj Düzenlendi",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Kullanıcı", value=before.author.mention)
        embed.add_field(name="Önce", value=before.content[:500], inline=False)
        embed.add_field(name="Sonra", value=after.content[:500], inline=False)

        await channel.send(embed=embed)

    # ================= MEMBER JOIN =================
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.get_log_channel(member.guild)
        if not channel:
            return

        embed = discord.Embed(
            title="➕ Kullanıcı Katıldı",
            description=f"{member.mention} sunucuya girdi",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        await channel.send(embed=embed)

    # ================= MEMBER LEAVE =================
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.get_log_channel(member.guild)
        if not channel:
            return

        embed = discord.Embed(
            title="➖ Kullanıcı Ayrıldı",
            description=f"{member} sunucudan çıktı",
            color=discord.Color.dark_gray(),
            timestamp=datetime.utcnow()
        )

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))

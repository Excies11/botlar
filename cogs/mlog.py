import discord
from discord.ext import commands

LOG_CHANNEL_ID = 1409914069317718017  # mllog kanalı


class MLog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("🟣 MLOG BOT READY")

    # ===== MEMBER JOIN =====
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.get_channel(LOG_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title="➕ Sunucuya Katıldı",
            color=discord.Color.green()
        )
        embed.add_field(name="Kullanıcı", value=member.mention, inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)

        await channel.send(embed=embed)

    # ===== MEMBER LEAVE =====
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = member.guild.get_channel(LOG_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title="➖ Sunucudan Ayrıldı",
            color=discord.Color.red()
        )
        embed.add_field(name="Kullanıcı", value=str(member), inline=False)
        embed.add_field(name="ID", value=member.id, inline=False)

        await channel.send(embed=embed)

    # ===== MESSAGE DELETE =====
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if not message.guild or message.author.bot:
            return

        channel = message.guild.get_channel(LOG_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title="🗑️ Mesaj Silindi",
            color=discord.Color.red()
        )
        embed.add_field(name="Kullanıcı", value=message.author.mention, inline=False)
        embed.add_field(name="Kanal", value=message.channel.mention, inline=False)
        embed.add_field(
            name="Mesaj",
            value=message.content[:1000] if message.content else "*Boş / embed*",
            inline=False
        )

        await channel.send(embed=embed)

    # ===== MESSAGE EDIT =====
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot or before.content == after.content:
            return

        channel = before.guild.get_channel(LOG_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title="✏️ Mesaj Düzenlendi",
            color=discord.Color.orange()
        )
        embed.add_field(name="Kullanıcı", value=before.author.mention, inline=False)
        embed.add_field(name="Eski", value=before.content[:500], inline=False)
        embed.add_field(name="Yeni", value=after.content[:500], inline=False)

        await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(MLog(bot))

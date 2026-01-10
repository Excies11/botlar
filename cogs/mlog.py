import discord
from discord.ext import commands

LOG_CHANNEL_ID = 1409914069317718017  # mllog kanalı


class MLog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ===== BOT READY =====
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="Server Logs"
            )
        )
        print("📜 MLOG COG YÜKLENDİ")

    # ===== MESSAGE DELETE LOG =====
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

    # ===== MESSAGE EDIT LOG =====
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


# ===== EXTENSION SETUP (ZORUNLU) =====
async def setup(bot: commands.Bot):
    await bot.add_cog(MLog(bot))

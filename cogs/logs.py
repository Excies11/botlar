import discord
from discord.ext import commands
from datetime import datetime

LOG_CHANNEL_ID = 1409915479438393425  # sadece bu cog kullanır

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="🟢 Sunucuya Katıldı",
            description=f"{member.mention} sunucuya katıldı.",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(
            name="👤 Kullanıcı",
            value=f"{member} (`{member.id}`)",
            inline=False
        )
        embed.set_footer(text="Giriş Logu")

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="🔴 Sunucudan Ayrıldı",
            description=f"**{member}** sunucudan ayrıldı.",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(
            name="👤 Kullanıcı ID",
            value=str(member.id),
            inline=False
        )
        embed.set_footer(text="Çıkış Logu")

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))

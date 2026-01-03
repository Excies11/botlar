import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta, datetime
import time
import re

BAD_WORDS = ["amk", "aq", "orospu", "sik"]  # düzenle
LINK_REGEX = re.compile(r"(https?://|www\.)")

SPAM_LIMIT = 6
SPAM_TIME = 5
user_message_times = {}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ================= AUTOMOD =================
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower()

        # Küfür filtresi
        if any(w in content for w in BAD_WORDS):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} ❌ küfür yasak",
                delete_after=5
            )
            return

        # Link engelleme
        if LINK_REGEX.search(content):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} 🔗 link yasak",
                delete_after=5
            )
            return

        # Spam koruma
        now = time.time()
        times = user_message_times.get(message.author.id, [])
        times = [t for t in times if now - t < SPAM_TIME]
        times.append(now)
        user_message_times[message.author.id] = times

        if len(times) >= SPAM_LIMIT:
            try:
                await message.author.timeout(
                    timedelta(minutes=5),
                    reason="Spam"
                )
                await message.channel.send(
                    f"{message.author.mention} 🔇 spam nedeniyle susturuldu",
                    delete_after=5
                )
            except:
                pass

        await self.bot.process_commands(message)

    # ================= ! KOMUTLAR =================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 {amount} mesaj silindi", delete_after=5)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member} atıldı | {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member} banlandı | {reason}")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int):
        await member.timeout(timedelta(minutes=minutes))
        await ctx.send(f"🔇 {member} {minutes} dk susturuldu")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 {member} susturması kaldırıldı")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! `{round(self.bot.latency*1000)}ms`")

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title="👤 Kullanıcı Bilgisi",
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="İsim", value=member, inline=True)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Hesap Açılış", value=member.created_at.strftime("%d.%m.%Y"))
        await ctx.send(embed=embed)

    # ================= / SLASH KOMUTLAR =================
    @app_commands.command(name="ban", description="Kullanıcıyı banla")
    @app_commands.checks.has_permissions(ban_members=True)
    async def slash_ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Sebep yok"):
        await member.ban(reason=reason)
        await interaction.response.send_message(
            f"🔨 {member} banlandı | {reason}",
            ephemeral=True
        )

    @app_commands.command(name="kick", description="Kullanıcıyı at")
    @app_commands.checks.has_permissions(kick_members=True)
    async def slash_kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Sebep yok"):
        await member.kick(reason=reason)
        await interaction.response.send_message(
            f"👢 {member} atıldı | {reason}",
            ephemeral=True
        )

    @app_commands.command(name="clear", description="Mesaj sil")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def slash_clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(
            f"🧹 {amount} mesaj silindi",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Moderation(bot))

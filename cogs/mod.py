import discord
from discord.ext import commands
from datetime import timedelta
import time

BAD_WORDS = ["amk", "aq", "orospu", "sik"]
LINKS = ["http://", "https://", "discord.gg"]
user_messages = {}


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ===== BOT READY =====
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.streaming,
                name="SSD Discord 🤍"
            )
        )
        print("🛡️ MOD COG YÜKLENDİ")

    # ===== HELP =====
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="🛡️ Moderasyon Komutları",
            color=discord.Color.blurple()
        )
        embed.add_field(name="!ban / !unban", value="Kullanıcıyı banla / kaldır", inline=False)
        embed.add_field(name="!kick", value="Kullanıcıyı at", inline=False)
        embed.add_field(name="!mute / !unmute", value="Sustur / aç", inline=False)
        embed.add_field(name="!warn / !warnings", value="Uyarı sistemi", inline=False)
        embed.add_field(name="!clear", value="Mesaj sil", inline=False)
        embed.add_field(name="!slowmode", value="Yavaş mod", inline=False)
        embed.add_field(name="!lock / !unlock", value="Kanal kilitle", inline=False)
        embed.set_footer(text="SSD Moderasyon Bot")
        await ctx.send(embed=embed)

    # ===== BAN =====
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} banlandı | {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"♻️ {user} banı kaldırıldı")

    # ===== KICK =====
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} atıldı | {reason}")

    # ===== CLEAR =====
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 {amount} mesaj silindi", delete_after=3)

    # ===== MUTE =====
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int):
        await member.timeout(discord.utils.utcnow() + timedelta(minutes=minutes))
        await ctx.send(f"🔇 {member.mention} {minutes} dk susturuldu")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} susturması kaldırıldı")

    # ===== WARN =====
    warnings = {}

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        self.warnings.setdefault(member.id, []).append(reason)
        await ctx.send(f"⚠️ {member.mention} uyarıldı | {reason}")

    @commands.command()
    async def warnings(self, ctx, member: discord.Member):
        warns = self.warnings.get(member.id, [])
        if not warns:
            await ctx.send("Uyarı yok")
            return

        embed = discord.Embed(title=f"{member} Uyarıları", color=discord.Color.orange())
        for i, w in enumerate(warns, 1):
            embed.add_field(name=f"{i}. Uyarı", value=w, inline=False)
        await ctx.send(embed=embed)

    # ===== LOCK =====
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Kanal kilitlendi")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Kanal açıldı")

    # ===== SLOWMODE =====
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"🐢 Slowmode {seconds} saniye")

    # ===== AUTOMOD =====
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        content = message.content.lower()

        if any(word in content for word in BAD_WORDS):
            await message.delete()
            await message.channel.send(
                f"🚫 {message.author.mention} yasaklı kelime!",
                delete_after=3
            )

        if any(link in content for link in LINKS):
            await message.delete()
            await message.channel.send(
                f"🔗 {message.author.mention} link yasak!",
                delete_after=3
            )

        now = time.time()
        user_messages.setdefault(message.author.id, []).append(now)
        user_messages[message.author.id] = [
            t for t in user_messages[message.author.id] if now - t < 5
        ]

        if len(user_messages[message.author.id]) > 6:
            await message.author.timeout(
                discord.utils.utcnow() + timedelta(minutes=1)
            )
            await message.channel.send(
                f"⛔ {message.author.mention} spam yaptı!",
                delete_after=3
            )

        await self.bot.process_commands(message)


# ===== EXTENSION SETUP =====
async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))

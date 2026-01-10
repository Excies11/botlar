import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ===== BOT READY =====
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Moderation"
            )
        )
        print("🛡️ MOD COG YÜKLENDİ")

    # ===== KICK =====
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} atıldı | **{reason}**")

    # ===== BAN =====
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} banlandı | **{reason}**")

    # ===== CLEAR =====
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 {amount} mesaj silindi", delete_after=3)

    # ===== MUTE (TIMEOUT) =====
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int):
        await member.timeout(
            discord.utils.utcnow() + discord.timedelta(minutes=minutes)
        )
        await ctx.send(f"🔇 {member.mention} {minutes} dk susturuldu")

    # ===== UNMUTE =====
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} susturması kaldırıldı")


# ===== EXTENSION SETUP (ŞART) =====
async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))

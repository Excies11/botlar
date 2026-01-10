import discord
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ================= READY =================
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="SSD Moderation"
            )
        )
        print("🛡️ MOD COG YÜKLENDİ")

    # ================= HELP =================
    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(
            title="🛡️ SSD Moderation",
            description="Moderasyon Komutları",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="👢 !kick <üye> [sebep]",
            value="Kullanıcıyı sunucudan atar",
            inline=False
        )
        embed.add_field(
            name="🔨 !ban <üye> [sebep]",
            value="Kullanıcıyı banlar",
            inline=False
        )
        embed.add_field(
            name="🧹 !clear <sayı>",
            value="Mesaj siler",
            inline=False
        )
        embed.add_field(
            name="🔇 !mute <üye> <dk>",
            value="Susturur (timeout)",
            inline=False
        )
        embed.add_field(
            name="🔊 !unmute <üye>",
            value="Susturmayı kaldırır",
            inline=False
        )
        embed.add_field(
            name="⏱️ !slowmode <sn>",
            value="Yavaş modu ayarlar",
            inline=False
        )
        embed.set_footer(text="SSD Moderation Bot")

        await ctx.send(embed=embed)

    # ================= KICK =================
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} atıldı | **{reason}**")

    # ================= BAN =================
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} banlandı | **{reason}**")

    # ================= CLEAR =================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 {amount} mesaj silindi", delete_after=3)

    # ================= MUTE =================
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int):
        await member.timeout(
            discord.utils.utcnow() + timedelta(minutes=minutes)
        )
        await ctx.send(f"🔇 {member.mention} {minutes} dk susturuldu")

    # ================= UNMUTE =================
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 {member.mention} susturması kaldırıldı")

    # ================= SLOWMODE =================
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"⏱️ Slowmode: **{seconds} saniye**")


# ================= SETUP =================
async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))

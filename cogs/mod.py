import discord
from discord.ext import commands
from datetime import timedelta

AUTO_MOD_WORDS = ["küfür1", "küfür2", "amk", "aq"]

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ================= HELP =================
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="🛡️ Moderasyon Komutları",
            description="Yetkili komutları aşağıda listelenmiştir",
            color=discord.Color.blurple()
        )
        embed.add_field(name="!ban", value="Kullanıcıyı banlar", inline=False)
        embed.add_field(name="!kick", value="Kullanıcıyı atar", inline=False)
        embed.add_field(name="!timeout", value="Geçici susturma", inline=False)
        embed.add_field(name="!untimeout", value="Susturmayı kaldırır", inline=False)
        embed.add_field(name="!clear", value="Mesaj siler", inline=False)
        embed.add_field(name="!slowmode", value="Yavaş mod", inline=False)
        embed.add_field(name="!lock / !unlock", value="Kanal kilitle", inline=False)
        embed.add_field(name="!warn", value="Uyarı verir", inline=False)
        embed.set_footer(text="Gelişmiş Mod Bot")
        await ctx.send(embed=embed)

    # ================= BAN =================
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member} banlandı | {reason}")

    # ================= KICK =================
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member} atıldı | {reason}")

    # ================= TIMEOUT =================
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason="Sebep yok"):
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        await ctx.send(f"🔇 {member} {minutes} dk susturuldu")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 {member} susturması kaldırıldı")

    # ================= CLEAR =================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 {amount} mesaj silindi", delete_after=3)

    # ================= SLOWMODE =================
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"🐢 Slowmode: {seconds} saniye")

    # ================= LOCK =================
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

    # ================= WARN =================
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await ctx.send(f"⚠️ {member.mention} uyarıldı | {reason}")

    # ================= AUTOMOD =================
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if any(word in message.content.lower() for word in AUTO_MOD_WORDS):
            await message.delete()
            await message.channel.send(
                f"🚫 {message.author.mention} yasaklı kelime!",
                delete_after=3
            )

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Mod(bot))

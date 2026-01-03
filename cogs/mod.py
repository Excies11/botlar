import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, BadArgument
from datetime import timedelta

AUTO_MOD_WORDS = ["küfür1", "küfür2", "amk", "aq"]

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ================= HELP =================
    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🛡️ Moderasyon Komutları",
            description="Yetkili komutları aşağıda listelenmiştir",
            color=discord.Color.blurple()
        )
        embed.add_field(name="!ban", value="Kullanıcıyı banlar\n`!ban @user sebep`", inline=False)
        embed.add_field(name="!kick", value="Kullanıcıyı atar\n`!kick @user sebep`", inline=False)
        embed.add_field(name="!mute", value="Kullanıcıyı susturur\n`!mute @user dakika`", inline=False)
        embed.add_field(name="!unmute", value="Susturmayı kaldırır\n`!unmute @user`", inline=False)
        embed.add_field(name="!clear", value="Mesaj siler\n`!clear 10`", inline=False)
        embed.add_field(name="!slowmode", value="Yavaş mod\n`!slowmode 5`", inline=False)
        embed.add_field(name="!lock / !unlock", value="Kanal kilit aç/kapat", inline=False)
        embed.add_field(name="!warn", value="Uyarı verir\n`!warn @user sebep`", inline=False)
        embed.set_footer(text="Gelişmiş Moderasyon Bot")
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

    # ================= MUTE / UNMUTE =================
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

    # ================= LOCK / UNLOCK =================
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
        if message.author.bot or message.guild is None:
            return

        content = message.content.lower()
        if any(word in content for word in AUTO_MOD_WORDS):
            try:
                await message.delete()
            except discord.Forbidden:
                return
            await message.channel.send(
                f"🚨 **GUARD:** {message.author.mention} yasaklı kelime kullandı!",
                delete_after=3
            )
            return  # komutları bozmamak için burada dur

        # Komutları işle
        await self.bot.process_commands(message)

    # ================= ERROR HANDLER =================
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        elif isinstance(error, MissingPermissions):
            await ctx.send("❌ Bu komutu kullanmak için yetkin yok!")
        elif isinstance(error, BadArgument):
            await ctx.send("❌ Hatalı argüman! Örnek kullanım:\n`!warn @user sebep`")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Eksik argüman! Doğru kullanım:\n`{ctx.command} {ctx.command.signature}`")
        else:
            await ctx.send(f"❌ Bir hata oluştu: {str(error)}")

# ================= SETUP =================
async def setup(bot):
    await bot.add_cog(Mod(bot))

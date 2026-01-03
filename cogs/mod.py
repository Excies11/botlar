import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, BadArgument
from datetime import timedelta

AUTO_MOD_WORDS = ["küfür1", "küfür2", "amk", "aq"]

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await ctx.send(f"⚠️ {member.mention} uyarıldı | {reason}")

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
            return

# ================= SETUP =================
async def setup(bot):  # 🔥 BOT parametresi eklendi
    await bot.add_cog(Mod(bot))

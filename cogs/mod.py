import discord
from discord.ext import commands

class Mod(commands.Cog):
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

    # ===== ÖRNEK MOD KOMUTLARI =====

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} kicklendi | {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} banlandı | {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🧹 {amount} mesaj silindi")
        await msg.delete(delay=3)


# ===== EXTENSION SETUP (ŞART) =====
async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot))

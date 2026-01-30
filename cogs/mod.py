from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member, *, reason="Yok"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member} atıldı | {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member, *, reason="Yok"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member} banlandı | {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 {amount} mesaj silindi", delete_after=3)

async def setup(bot):
    await bot.add_cog(Moderation(bot))

from discord.ext import commands
import discord

ATERNOS_PANEL = "https://aternos.org/server/"
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Streaming(
                name="SSD Discord 🤍",
                url="https://twitch.tv/ssd"
            )
        )
        print("🎵 MUSIC BOT READY")
class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx):
        await ctx.send(
            "🟡 **Sunucu durumu bot üzerinden alınamıyor**\n"
            "📌 Aternos API olmadığı için manuel kontrol gerekli."
        )

    @commands.command()
    async def server(self, ctx):
        await ctx.send(
            "🚀 Sunucuyu başlatmak için Aternos paneline git:\n"
            f"{ATERNOS_PANEL}"
        )

async def setup(bot):
    await bot.add_cog(Minecraft(bot))

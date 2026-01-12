from discord.ext import commands
from aternos import Client
import os

ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")
ATERNOS_SERVER = os.getenv("ATERNOS_SERVER")

class Minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = Client()
        self.server = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("⛏️ MINECRAFT BOT READY (COOKIE MODE)")
        await self.login_with_cookie()

    async def login_with_cookie(self):
        self.client.session.cookies.set(
            "ATERNOS_SESSION",
            ATERNOS_SESSION,
            domain=".aternos.org"
        )

        self.client.connect()
        self.server = self.client.account.servers[ATERNOS_SERVER]

    @commands.command()
    async def server(self, ctx):
        await ctx.send("⏳ Sunucu kontrol ediliyor...")

        if self.server.status == "online":
            return await ctx.send("✅ Sunucu zaten **AÇIK**")

        if self.server.status == "loading":
            return await ctx.send("⏳ Sunucu **ZATEN BAŞLATILIYOR**")

        self.server.start()
        await ctx.send("🚀 Sunucu **SIRAYA ALINDI / BAŞLATILDI**")

    @commands.command()
    async def status(self, ctx):
        await ctx.send(f"🧠 Durum: **{self.server.status.upper()}**")

async def setup(bot: commands.Bot):
    await bot.add_cog(Minecraft(bot))

from discord.ext import commands
from aternos import Client
import os
import asyncio

ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")
ATERNOS_SERVER = int(os.getenv("ATERNOS_SERVER"))

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Client()
        self.server = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("⛏️ Minecraft sistemi bağlanıyor...")
        await asyncio.to_thread(self.login)

    def login(self):
        self.client.session.cookies.set(
            "ATERNOS_SESSION",
            ATERNOS_SESSION,
            domain=".aternos.org"
        )
        self.client.connect()
        self.server = self.client.account.servers[ATERNOS_SERVER]
        print(f"✅ Aternos bağlı: {self.server.name}")

    # ================= STATUS =================
    @commands.command()
    async def status(self, ctx):
        await asyncio.to_thread(self.server.fetch)

        durum = {
            "online": "🟢 AÇIK",
            "offline": "🔴 KAPALI",
            "loading": "🟡 BAŞLATILIYOR",
            "starting": "🟡 BAŞLATILIYOR",
            "stopping": "🟠 DURDURULUYOR"
        }.get(self.server.status, self.server.status)

        await ctx.send(
            f"⛏️ **Minecraft Sunucusu**\n"
            f"📡 **{self.server.name}**\n"
            f"📊 Durum: **{durum}**"
        )

    # ================= START =================
    @commands.command()
    async def server(self, ctx):
        await asyncio.to_thread(self.server.fetch)

        if self.server.status == "online":
            return await ctx.send("✅ Sunucu zaten **AÇIK**")

        if self.server.status in ("loading", "starting"):
            return await ctx.send("⏳ Sunucu zaten **BAŞLATILIYOR**")

        await asyncio.to_thread(self.server.start)
        await ctx.send("🚀 Sunucu **SIRAYA ALINDI / BAŞLATILIYOR**")

async def setup(bot):
    await bot.add_cog(Minecraft(bot))

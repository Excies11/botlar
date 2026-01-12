from discord.ext import commands
from aternos import Client
import os
import asyncio

ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")
ATERNOS_SERVER = int(os.getenv("ATERNOS_SERVER"))  # INDEX (0,1,2...)

class Minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = Client()
        self.server = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("⛏️ MINECRAFT BOT READY")
        await self.login_with_cookie()

    async def login_with_cookie(self):
        self.client.session.cookies.set(
            "ATERNOS_SESSION",
            ATERNOS_SESSION,
            domain=".aternos.org"
        )

        # Aternos sync → blocking, o yüzden thread
        await asyncio.to_thread(self.client.connect)

        self.server = self.client.account.servers[ATERNOS_SERVER]
        print(f"🎮 Sunucu bağlandı: {self.server.name}")

    # ================= START =================
    @commands.command(name="server")
    async def server_start(self, ctx):
        await ctx.send("⏳ Sunucu kontrol ediliyor...")

        await asyncio.to_thread(self.server.fetch)

        if self.server.status == "online":
            return await ctx.send("✅ Sunucu zaten **AÇIK**")

        if self.server.status in ("loading", "starting"):
            return await ctx.send("⏳ Sunucu **ZATEN BAŞLATILIYOR**")

        await asyncio.to_thread(self.server.start)
        await ctx.send("🚀 Sunucu **SIRAYA ALINDI / BAŞLATILDI**")

    # ================= STATUS =================
    @commands.command(name="status")
    async def server_status(self, ctx):
        await asyncio.to_thread(self.server.fetch)

        durum_map = {
            "online": "🟢 AÇIK",
            "offline": "🔴 KAPALI",
            "loading": "🟡 BAŞLATILIYOR",
            "starting": "🟡 BAŞLATILIYOR",
            "stopping": "🟠 DURDURULUYOR"
        }

        durum = durum_map.get(self.server.status, self.server.status.upper())

        await ctx.send(
            f"⛏️ **Minecraft Sunucu Durumu**\n"
            f"📡 Sunucu: **{self.server.name}**\n"
            f"📊 Durum: **{durum}**"
        )

# ================= SETUP =================
async def setup(bot: commands.Bot):
    await bot.add_cog(Minecraft(bot))

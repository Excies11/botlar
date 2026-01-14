from discord.ext import commands
import requests
import os

ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")

STATUS_URL = "https://aternos.org/panel/ajax/status.php"
START_URL = "https://aternos.org/panel/ajax/start.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
}

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.cookies.set(
            "ATERNOS_SESSION",
            ATERNOS_SESSION,
            domain=".aternos.org"
        )

    def get_status(self):
        r = self.session.get(STATUS_URL)
        data = r.json()

        status = data.get("status", "unknown")
        queue = data.get("queue")

        return status, queue

    def start_server(self):
        self.session.post(START_URL)

    @commands.command()
    async def status(self, ctx):
        status, queue = self.get_status()

        status_map = {
            "online": "🟢 **AÇIK**",
            "offline": "🔴 **KAPALI**",
            "loading": "🟡 **BAŞLATILIYOR**",
            "queue": "🟠 **SIRADA**"
        }

        msg = f"⛏️ Sunucu Durumu: {status_map.get(status, status)}"
        if queue:
            msg += f"\n📥 Sıra: **{queue}**"

        await ctx.send(msg)

    @commands.command()
    async def server(self, ctx):
        status, _ = self.get_status()

        if status == "online":
            return await ctx.send("✅ Sunucu zaten **AÇIK**")

        if status in ("loading", "queue"):
            return await ctx.send("⏳ Sunucu zaten **başlatılıyor / sırada**")

        self.start_server()
        await ctx.send("🚀 Sunucu **SIRAYA ALINDI / BAŞLATILDI**")

async def setup(bot):
    await bot.add_cog(Minecraft(bot))

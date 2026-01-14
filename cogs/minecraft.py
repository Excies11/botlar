from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import os

ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")
ATERNOS_SERVER = os.getenv("ATERNOS_SERVER")  # STRING KALACAK

BASE_URL = "https://aternos.org"
HEADERS = {"User-Agent": "Mozilla/5.0"}

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
        r = self.session.get(f"{BASE_URL}/server/{ATERNOS_SERVER}")
        soup = BeautifulSoup(r.text, "html.parser")

        status = soup.select_one("#statuslabel")
        queue = soup.select_one("#queue")

        return (
            status.text.strip() if status else "Bilinmiyor",
            queue.text.strip() if queue else None
        )

    def start_server(self):
        self.session.post(f"{BASE_URL}/panel/ajax/start.php")

    @commands.command()
    async def status(self, ctx):
        status, queue = self.get_status()

        msg = f"⛏️ **Sunucu Durumu:** `{status}`"
        if queue:
            msg += f"\n📥 **Sıra:** {queue}"

        await ctx.send(msg)

    @commands.command()
    async def server(self, ctx):
        status, _ = self.get_status()

        if "Online" in status:
            return await ctx.send("✅ Sunucu zaten **AÇIK**")

        self.start_server()
        await ctx.send("🚀 Sunucu **SIRAYA ALINDI / BAŞLATILIYOR**")

async def setup(bot):
    await bot.add_cog(Minecraft(bot))

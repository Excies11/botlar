import os
import discord
from discord.ext import commands
from aternos import Client

ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")
ATERNOS_SERVER = os.getenv("ATERNOS_SERVER")  # STRING olacak

class Minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.client = Client()
        self.server = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("⛏️ Minecraft COG hazır")
        await self.login()

    async def login(self):
        if not ATERNOS_SESSION or not ATERNOS_SERVER:
            print("❌ ATERNOS ENV eksik")
            return

        # Cookie ile giriş
        self.client.session.cookies.set(
            "ATERNOS_SESSION",
            ATERNOS_SESSION,
            domain=".aternos.org"
        )

        self.client.connect()

        # SERVER ID STRING
        self.server = self.client.account.servers[ATERNOS_SERVER]
        print("✅ Aternos sunucu bağlandı")

    @commands.command()
    async def status(self, ctx):
        if not self.server:
            return await ctx.send("❌ Sunucuya bağlanılamadı")

        await ctx.send(f"🧠 Sunucu durumu: **{self.server.status.upper()}**")

    @commands.command()
    async def server(self, ctx):
        if not self.server:
            return await ctx.send("❌ Sunucuya bağlanılamadı")

        if self.server.status == "online":
            return await ctx.send("✅ Sunucu zaten **AÇIK**")

        if self.server.status == "loading":
            return await ctx.send("⏳ Sunucu zaten **başlatılıyor**")

        self.server.start()
        await ctx.send("🚀 Sunucu **BAŞLATILDI / SIRAYA ALINDI**")

    # TEST KOMUTU
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("🏓 pong")

async def setup(bot: commands.Bot):
    print("🧩 Minecraft COG yüklendi")
    await bot.add_cog(Minecraft(bot))

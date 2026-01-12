import discord
from discord.ext import commands
import requests
import os

class Aternos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = requests.Session()
        self.session.cookies.set(
            "ATERNOS_SESSION",
            os.getenv("ATERNOS_SESSION"),
            domain=".aternos.org"
        )

    @commands.command()
    async def server(self, ctx):
        await ctx.send("⏳ Sunucu sıraya alınıyor...")

        server_id = os.getenv("ATERNOS_SERVER")

        url = f"https://aternos.org/panel/ajax/start.php"

        r = self.session.post(url, data={
            "server": server_id
        })

        if r.status_code == 200:
            await ctx.send("✅ Sunucu **başlatma kuyruğuna alındı**")
        else:
            await ctx.send("❌ Sunucu başlatılamadı")


async def setup(bot):
    await bot.add_cog(Aternos(bot))

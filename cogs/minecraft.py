from discord.ext import commands
from playwright.async_api import async_playwright
import os

ATERNOS_SESSION = os.getenv("ATERNOS_SESSION")

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def server(self, ctx):
        await ctx.send("⏳ Aternos açılıyor...")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()

            # COOKIE EKLE
            await context.add_cookies([{
                "name": "ATERNOS_SESSION",
                "value": ATERNOS_SESSION,
                "domain": ".aternos.org",
                "path": "/"
            }])

            page = await context.new_page()
            await page.goto("https://aternos.org/servers/")

            # SERVER START BUTONU
            await page.wait_for_selector("button.start", timeout=20000)
            await page.click("button.start")

            await browser.close()

        await ctx.send("🚀 Sunucu **BAŞLATILDI / SIRAYA ALINDI**")

async def setup(bot):
    await bot.add_cog(Minecraft(bot))

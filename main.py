import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # ileride komutlar için

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

# COG YÜKLEME
initial_extensions = [
    "cogs.logs",
]

async def load_cogs():
    for ext in initial_extensions:
        try:
            await bot.load_extension(ext)
            print(f"{ext} yüklendi")
        except Exception as e:
            print(f"{ext} yüklenemedi: {e}")

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("TOKEN bulunamadı! Railway Variables kontrol et.")

async def main():
    await load_cogs()
    await bot.start(TOKEN)

import asyncio
asyncio.run(main())

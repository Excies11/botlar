import os
import asyncio
import discord
from discord.ext import commands

# ===== INTENTS =====
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# ===== LOG BOT =====
log_bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@log_bot.event
async def on_ready():
    print(f"🟢 LOG BOT AKTİF: {log_bot.user}")

# ===== MOD BOT =====
mod_bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@mod_bot.event
async def on_ready():
    print(f"🔵 MOD BOT AKTİF: {mod_bot.user}")

# ===== START FUNCTIONS =====
async def start_log_bot():
    token = os.getenv("LOG_TOKEN")
    if not token:
        raise ValueError("LOG_TOKEN bulunamadı")
    await log_bot.load_extension("cogs.logs")
    await log_bot.start(token)

async def start_mod_bot():
    token = os.getenv("MOD_TOKEN")
    if not token:
        raise ValueError("MOD_TOKEN bulunamadı")
    await mod_bot.load_extension("cogs.mod")
    await mod_bot.start(token)

# ===== MAIN =====
async def main():
    await asyncio.gather(
        start_log_bot(),
        start_mod_bot()
    )

asyncio.run(main())

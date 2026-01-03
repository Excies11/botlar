import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# ===== LOG BOT =====
log_bot = commands.Bot(command_prefix="!", intents=intents)

@log_bot.event
async def on_ready():
    print(f"LOG BOT aktif: {log_bot.user}")

async def start_log_bot():
    await log_bot.load_extension("cogs.logs")
    await log_bot.start(os.getenv("LOG_TOKEN"))


# ===== MOD BOT =====
mod_bot = commands.Bot(command_prefix="!", intents=intents)

@mod_bot.event
async def on_ready():
    print(f"MOD BOT aktif: {mod_bot.user}")

async def start_mod_bot():
    await mod_bot.load_extension("cogs.mod")
    await mod_bot.start(os.getenv("MOD_TOKEN"))


# ===== MAIN =====
async def main():
    await asyncio.gather(
        start_log_bot(),
        start_mod_bot()
    )

asyncio.run(main())

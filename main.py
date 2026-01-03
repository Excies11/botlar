import os
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# ===== LOG BOT =====
log_bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@log_bot.event
async def on_ready():
    print(f"🟢 LOG BOT AKTİF: {log_bot.user}")

async def start_log_bot():
    await log_bot.load_extension("cogs.logs")
    await log_bot.start(os.getenv("LOG_TOKEN"))


# ===== MOD BOT =====
mod_bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None   # 🔥 BU SATIR HATAYI ÇÖZER
)

@mod_bot.event
async def on_ready():
    print(f"🔵 MOD BOT AKTİF: {mod_bot.user}")

async def start_mod_bot():
    await mod_bot.load_extension("cogs.mod")
    await mod_bot.start(os.getenv("MOD_TOKEN"))


async def main():
    await asyncio.gather(
        start_log_bot(),
        start_mod_bot()
    )

asyncio.run(main())

import os
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()

async def start_bot(bot, token, name, extension):
    if not token:
        print(f"❌ {name} TOKEN YOK, ATLANDI")
        return

    try:
        await bot.load_extension(extension)
        await bot.start(token)
    except Exception as e:
        print(f"🔥 {name} HATA:", e)


# ===== LOG BOT =====
log_bot = commands.Bot(command_prefix="!", intents=intents)

# ===== MOD BOT =====
mod_bot = commands.Bot(command_prefix="!", intents=intents)

# ===== MLOG BOT =====
mlog_bot = commands.Bot(command_prefix="?", intents=intents)

# ===== MUSIC BOT =====
music_bot = commands.Bot(command_prefix="!", intents=intents)

# ===== MINECRAFT BOT =====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"🟢 BOT AKTİF: {bot.user}")

async def main():
    await bot.load_extension("cogs.minecraft")
    await bot.start(os.getenv("MC_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())

async def main():
    await asyncio.gather(
        start_bot(log_bot, os.getenv("LOG_TOKEN"), "LOG BOT", "cogs.logs"),
        start_bot(mod_bot, os.getenv("MOD_TOKEN"), "MOD BOT", "cogs.mod"),
        start_bot(mlog_bot, os.getenv("MLOG_TOKEN"), "MLOG BOT", "cogs.mlog"),
        start_bot(music_bot, os.getenv("MUSIC_TOKEN"), "MUSIC BOT", "cogs.music"),
        start_bot(minecraft_bot, os.getenv("MC_TOKEN"), "MC BOT", "cogs.minecraft"),
    )

if __name__ == "__main__":
    asyncio.run(main())

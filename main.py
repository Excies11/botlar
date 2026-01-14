import os
import asyncio
import discord
from discord.ext import commands

# ========= INTENTS =========
intents = discord.Intents.default()
intents.message_content = True

# ========= BOTLAR =========
log_bot = commands.Bot(command_prefix="!", intents=intents)
mod_bot = commands.Bot(command_prefix="!", intents=intents)
mlog_bot = commands.Bot(command_prefix="?", intents=intents)
music_bot = commands.Bot(command_prefix="!", intents=intents)
mc_bot = commands.Bot(command_prefix="!", intents=intents)

# ========= BOT BAŞLATICI =========
async def start_bot(bot, token, name, extension):
    if not token:
        print(f"❌ {name} TOKEN YOK, ATLANDI")
        return

    try:
        await bot.load_extension(extension)
        await bot.start(token)
    except Exception as e:
        print(f"🔥 {name} HATA:", e)

# ========= READY LOG =========
@log_bot.event
async def on_ready():
    print(f"🟢 LOG BOT AKTİF: {log_bot.user}")

@mod_bot.event
async def on_ready():
    print(f"🟢 MOD BOT AKTİF: {mod_bot.user}")

@mlog_bot.event
async def on_ready():
    print(f"🟢 MLOG BOT AKTİF: {mlog_bot.user}")

@music_bot.event
async def on_ready():
    print(f"🟢 MUSIC BOT AKTİF: {music_bot.user}")

@mc_bot.event
async def on_ready():
    print(f"🟢 MC BOT AKTİF: {mc_bot.user}")

# ========= MAIN =========
async def main():
    await asyncio.gather(
        start_bot(log_bot,   os.getenv("LOG_TOKEN"),   "LOG BOT",   "cogs.logs"),
        start_bot(mod_bot,   os.getenv("MOD_TOKEN"),   "MOD BOT",   "cogs.mod"),
        start_bot(mlog_bot,  os.getenv("MLOG_TOKEN"),  "MLOG BOT",  "cogs.mlog"),
        start_bot(music_bot, os.getenv("MUSIC_TOKEN"), "MUSIC BOT", "cogs.music"),
        start_bot(mc_bot,    os.getenv("MC_TOKEN"),    "MC BOT",    "cogs.minecraft"),
    )

if __name__ == "__main__":
    asyncio.run(main())

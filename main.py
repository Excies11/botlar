import os
import asyncio
import discord
from discord.ext import commands

# ================= INTENTS =================
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# ================= LOG BOT =================
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
print("selam")
# ================= MOD BOT =================
mod_bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)
# ================= MUSIC BOT =================
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

music_bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@music_bot.event
async def on_ready():
    print(f"🎵 MUSIC BOT AKTİF: {music_bot.user}")

async def main():
    await music_bot.load_extension("cogs.music")
    await music_bot.start(os.getenv("MUSIC_TOKEN"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())





@mod_bot.event
async def on_ready():
    print(f"🔵 MOD BOT AKTİF: {mod_bot.user}")

async def start_mod_bot():
    await mod_bot.load_extension("cogs.mod")
    await mod_bot.start(os.getenv("MOD_TOKEN"))

# ================= MLOG BOT =================
mlog_bot = commands.Bot(
    command_prefix="?",
    intents=intents,
    help_command=None
)

@mlog_bot.event
async def on_ready():
    print(f"🟣 MLOG BOT AKTİF: {mlog_bot.user}")

async def start_mlog_bot():
    await mlog_bot.load_extension("cogs.mlog")
    await mlog_bot.start(os.getenv("MLOG_TOKEN"))


# ================= MAIN =================
async def main():
    await asyncio.gather(
        start_log_bot(),
        start_mod_bot(),
        start_mlog_bot(),
        start_music_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())

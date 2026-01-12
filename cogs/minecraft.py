import os
import asyncio
import discord
from discord.ext import commands

# ================= BASE INTENTS =================
base_intents = discord.Intents.default()
base_intents.members = True
base_intents.message_content = True

# ================= LOG BOT =================
log_bot = commands.Bot(
    command_prefix="!",
    intents=base_intents,
    help_command=None
)

async def start_log_bot():
    await log_bot.load_extension("cogs.logs")
    await log_bot.start(os.getenv("LOG_TOKEN"))

@log_bot.event
async def on_ready():
    print(f"🟢 LOG BOT AKTİF: {log_bot.user}")


# ================= MOD BOT =================
mod_bot = commands.Bot(
    command_prefix="!",
    intents=base_intents,
    help_command=None
)

async def start_mod_bot():
    await mod_bot.load_extension("cogs.mod")
    await mod_bot.start(os.getenv("MOD_TOKEN"))

@mod_bot.event
async def on_ready():
    print(f"🔵 MOD BOT AKTİF: {mod_bot.user}")


# ================= MLOG BOT =================
mlog_bot = commands.Bot(
    command_prefix="?",
    intents=base_intents,
    help_command=None
)

async def start_mlog_bot():
    await mlog_bot.load_extension("cogs.mlog")
    await mlog_bot.start(os.getenv("MLOG_TOKEN"))

@mlog_bot.event
async def on_ready():
    print(f"🟣 MLOG BOT AKTİF: {mlog_bot.user}")


# ================= MUSIC BOT =================
music_intents = discord.Intents.default()
music_intents.message_content = True
music_intents.voice_states = True

music_bot = commands.Bot(
    command_prefix="!",
    intents=music_intents,
    help_command=None
)

async def start_music_bot():
    await music_bot.load_extension("cogs.music")
    await music_bot.start(os.getenv("MUSIC_TOKEN"))

@music_bot.event
async def on_ready():
    print(f"🎵 MUSIC BOT AKTİF: {music_bot.user}")


# ================= MINECRAFT BOT =================
mc_intents = discord.Intents.default()
mc_intents.message_content = True

minecraft_bot = commands.Bot(
    command_prefix="!",
    intents=mc_intents,
    help_command=None
)

async def start_minecraft_bot():
    await minecraft_bot.load_extension("cogs.minecraft")
    await minecraft_bot.start(os.getenv("MC_TOKEN"))

@minecraft_bot.event
async def on_ready():
    print(f"⛏️ MINECRAFT BOT AKTİF: {minecraft_bot.user}")


# ================= MAIN =================
async def main():
    await asyncio.gather(
        start_log_bot(),
        start_mod_bot(),
        start_mlog_bot(),
        start_music_bot(),
        start_minecraft_bot()   # 👈 EKLENDİ
    )

# ================= ENTRY =================
if __name__ == "__main__":
    asyncio.run(main())

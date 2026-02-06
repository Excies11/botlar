import os
import asyncio
import discord
from discord.ext import commands

# ========= INTENTS =========
intents = discord.Intents.all()
intents.message_content = True

# ========= BOTLAR =========
log_bot = commands.Bot(command_prefix="!", intents=intents)
mod_bot = commands.Bot(command_prefix="!", intents=intents)
mlog_bot = commands.Bot(command_prefix="?", intents=intents)
music_bot = commands.Bot(command_prefix="!", intents=intents)
mc_bot = commands.Bot(command_prefix="!", intents=intents)
ticket_bot = commands.Bot(command_prefix="!", intents=intents)

# ========= BOT BAŞLATICI =========
async def start_bot(bot, token, name, extension, voice_channel_id=None):
    if not token:
        print(f"❌ {name} TOKEN YOK, ATLANDI")
        return

    try:
        await bot.load_extension(extension)

        @bot.event
        async def on_ready():
            print(f"🟢 {name} AKTİF: {bot.user}")

            # İSTEĞE BAĞLI: SES KANALINA GİR
            if voice_channel_id:
                channel = bot.get_channel(voice_channel_id)
                if channel:
                    await channel.connect()
                    print(f"🔊 {name} ses kanalına girdi")

        await bot.start(token)

    except Exception as e:
        print(f"🔥 {name} HATA:", e)

# ========= MAIN =========
async def main():
    await asyncio.gather(
        start_bot(
            log_bot,
            os.getenv("LOG_TOKEN"),
            "LOG BOT",
            "cogs.logs",
            voice_channel_id=1464939407139147890
        ),
        start_bot(
            mod_bot,
            os.getenv("MOD_TOKEN"),
            "MOD BOT",
            "cogs.mod",
            voice_channel_id=1464939407139147890
        ),
        start_bot(
            mlog_bot,
            os.getenv("MLOG_TOKEN"),
            "MLOG BOT",
            "cogs.mlog",
            voice_channel_id=1464939407139147890
        ),
        start_bot(
            music_bot,
            os.getenv("MUSIC_TOKEN"),
            "MUSIC BOT",
            "cogs.music",
  # 👈 music bot ses kanalına girer
        ),
        start_bot(
            mc_bot,
            os.getenv("MC_TOKEN"),
            "MC BOT",
            "cogs.minecraft",
            voice_channel_id=1464939407139147890
        ),
        start_bot(
            ticket_bot,
            os.getenv("TICKET_TOKEN"),
            "TICKET BOT",
            "cogs.ticket",
            voice_channel_id=1464939407139147890
        ),
    )

if __name__ == "__main__":
    asyncio.run(main())

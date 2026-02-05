import os
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"🟢 BOT AKTİF: {bot.user}")

    # İSTEĞE BAĞLI: ses kanalına girsin
    CHANNEL_ID = 1464939407139147890
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.connect()
        print("🔊 Ses kanalına girildi")

async def main():
    await asyncio.gather(
        start_bot(log_bot,   os.getenv("LOG_TOKEN"),   "LOG BOT",   "cogs.logs"),
        start_bot(mod_bot,   os.getenv("MOD_TOKEN"),   "MOD BOT",   "cogs.mod"),
        start_bot(mlog_bot,  os.getenv("MLOG_TOKEN"),  "MLOG BOT",  "cogs.mlog"),
        start_bot(music_bot, os.getenv("MUSIC_TOKEN"), "MUSIC BOT", "cogs.music"),
        start_bot(mc_bot,    os.getenv("MC_TOKEN"),    "MC BOT",    "cogs.minecraft"),
        start_bot(ticket_bot,os.getenv("TICKET_TOKEN"),"TICKET",    "cogs.ticket"),
    )

if __name__ == "__main__":
    asyncio.run(main())

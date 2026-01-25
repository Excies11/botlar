import os
import discord
from discord.ext import commands

VOICE_CHANNEL_ID = 1464939407139147890  # SES KANALI ID

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"🟢 BOT AKTİF: {bot.user}")

    channel = bot.get_channel(VOICE_CHANNEL_ID)

    if not channel:
        print("❌ Ses kanalı bulunamadı")
        return

    if not isinstance(channel, discord.VoiceChannel):
        print("❌ ID ses kanalı değil")
        return

    # Zaten bağlıysa tekrar bağlanmasın
    if discord.utils.get(bot.voice_clients, guild=channel.guild):
        print("🔊 Zaten ses kanalında")
        return

    try:
        await channel.connect()
        print("🔊 Ses kanalına girildi ve bekleniyor")
    except Exception as e:
        print("🔥 Ses kanalına girilemedi:", e)

@bot.event
async def on_disconnect():
    print("🔴 BOT BAĞLANTI KOPTU")

bot.run(os.getenv("TOKEN"))

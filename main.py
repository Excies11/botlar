import discord
from discord.ext import commands
import os
import datetime

TOKEN = os.getenv("TOKEN")
LOG_KANAL_ID = (os.getenv("LOG_KANAL_ID"))

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

@bot.event
async def on_member_join(member):
    kanal = bot.get_channel(LOG_KANAL_ID)
    if kanal:
        await kanal.send(
            f"🟢 **Sunucuya katıldı**\n"
            f"👤 {member.mention}\n"
            f"🕒 {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )

@bot.event
async def on_member_remove(member):
    kanal = bot.get_channel(LOG_KANAL_ID)
    if kanal:
        await kanal.send(
            f"🔴 **Sunucudan ayrıldı**\n"
            f"👤 {member.name}\n"
            f"🕒 {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )

bot.run(TOKEN)

import os
from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("TOKEN bulunamadı! Railway Variables kontrol et.")

bot.run(TOKEN)

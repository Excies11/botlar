import os
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f"🟢 MINECRAFT BOT AKTİF: {bot.user}")

async def main():
    await bot.load_extension("cogs.minecraft")
    await bot.start(os.getenv("MC_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())

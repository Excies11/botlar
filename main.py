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
    for cog in ["mod", "music", "ticket", "logs"]:
        await bot.load_extension(f"cogs.{cog}")

    await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())

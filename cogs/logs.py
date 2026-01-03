import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("LOG_TOKEN")
LOG_CHANNEL_ID = 1409915479438393425
OTOROL_ID = 1409896783743549512

if TOKEN is None:
    raise ValueError("LOG_TOKEN bulunamadı!")

@bot.event
async def on_ready():
    print(f"{bot.user} | Log bot aktif")

@bot.event
async def on_member_join(member):
    role = member.guild.get_role(OTOROL_ID)
    if role:
        await member.add_roles(role)

    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🟢 Sunucuya Katıldı",
            description=f"{member.mention}",
            color=0x2ecc71
        )
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🔴 Sunucudan Ayrıldı",
            description=f"{member}",
            color=0xe74c3c
        )
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

bot.run(TOKEN)

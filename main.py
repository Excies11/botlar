import os
import discord
from discord.ext import commands
from datetime import datetime

# ---------- AYARLAR ----------
LOG_CHANNEL_ID = 1409915479438393425

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise ValueError("TOKEN bulunamadı! Railway Variables kontrol et.")

# ---------- BOT HAZIR ----------
@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

# ---------- ÜYE GİRİŞ ----------
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel is None:
        return

    embed = discord.Embed(
        title="🟢 Sunucuya Katıldı",
        description=f"**{member.mention}** sunucuya giriş yaptı.",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="👤 Kullanıcı", value=f"{member} (`{member.id}`)", inline=False)
    embed.set_footer(text="Giriş Logu")

    await channel.send(embed=embed)

# ---------- ÜYE ÇIKIŞ ----------
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel is None:
        return

    embed = discord.Embed(
        title="🔴 Sunucudan Ayrıldı",
        description=f"**{member}** sunucudan ayrıldı.",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="👤 Kullanıcı ID", value=str(member.id), inline=False)
    embed.set_footer(text="Çıkış Logu")

    await channel.send(embed=embed)

# ---------- BOTU BAŞLAT ----------
bot.run(TOKEN)

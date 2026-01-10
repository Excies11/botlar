import discord
from discord.ext import commands
import yt_dlp
import re

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "default_search": "ytsearch",
    "noplaylist": True
}

FFMPEG_OPTIONS = {
    "options": "-vn"
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

YOUTUBE_REGEX = re.compile(
    r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/"
)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ========= LINK ALGILAMA =========
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if YOUTUBE_REGEX.search(message.content):
            ctx = await self.bot.get_context(message)
            await self.play(ctx, search=message.content)

    # ========= PLAY =========
    @commands.command()
    async def play(self, ctx, *, search: str):
        if not ctx.author.voice:
            return await ctx.send("🎧 Ses kanalına gir")

        vc = ctx.voice_client
        if not vc:
            vc = await ctx.author.voice.channel.connect()

        with ytdl:
            info = ytdl.extract_info(search, download=False)
            if "entries" in info:
                info = info["entries"][0]

        source = discord.FFmpegPCMAudio(
            info["url"],
            **FFMPEG_OPTIONS
        )

        vc.play(source)

        await ctx.send(
            f"🎶 **Çalıyor:** {info['title']}"
        )

    # ========= STOP =========
    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("⏹️ Durduruldu")

# ========= SETUP =========
async def setup(bot):
    await bot.add_cog(Music(bot))

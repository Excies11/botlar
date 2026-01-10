import discord
from discord.ext import commands
import yt_dlp
import asyncio

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "default_search": "ytsearch",
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, search: str):
        if not ctx.author.voice:
            return await ctx.send("❌ Önce ses kanalına gir")

        channel = ctx.author.voice.channel

        if not ctx.voice_client:
            await channel.connect()

        vc = ctx.voice_client

        if vc.is_playing():
            vc.stop()

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(search, download=False)
            if "entries" in info:
                info = info["entries"][0]

            url = info["url"]
            title = info.get("title", "Bilinmeyen")

        source = await discord.FFmpegOpusAudio.from_probe(
            url, **FFMPEG_OPTIONS
        )

        vc.play(source)

        await ctx.send(f"🎶 **Çalıyor:** {title}")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("⏹️ Durduruldu")


async def setup(bot):
    await bot.add_cog(Music(bot))

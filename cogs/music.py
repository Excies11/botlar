import discord
from discord.ext import commands
import yt_dlp
import asyncio

YDL_OPTS = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True,
}

FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, query: str):
        if not ctx.author.voice:
            return await ctx.send("❌ Ses kanalında değilsin")

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        vc = ctx.voice_client

        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if "entries" in info:
                info = info["entries"][0]

            url = info["url"]
            title = info.get("title", "Bilinmeyen")

        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTS)

        if vc.is_playing():
            vc.stop()

        vc.play(source)
        await ctx.send(f"▶️ **{title}**")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("⏹️ Durduruldu")

async def setup(bot):
    await bot.add_cog(Music(bot))

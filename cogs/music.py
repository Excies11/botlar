import discord
from discord.ext import commands
import yt_dlp

ytdlp_opts = {
    "format": "bestaudio/best",
    "quiet": True,
    "default_search": "ytsearch",
}

ffmpeg_opts = {
    "options": "-vn"
}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("🔊 Ses kanalında değilsin")

    @commands.command()
    async def play(self, ctx, *, query):
        if not ctx.voice_client:
            await ctx.invoke(self.join)

        with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if "entries" in info:
                info = info["entries"][0]

        source = discord.FFmpegPCMAudio(info["url"], **ffmpeg_opts)
        ctx.voice_client.play(source)

        await ctx.send(f"🎶 Çalıyor: **{info['title']}**")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Music(bot))

import discord
from discord.ext import commands
import yt_dlp
import asyncio

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": False,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0"
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.loop = False
        self.current = None
        self.volume = 0.5

    # ===================== UTILS =====================
    async def join_channel(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("❌ Ses kanalında değilsin")

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)

    async def play_next(self, ctx):
        if not self.queue and not self.loop:
            await ctx.voice_client.disconnect()
            return

        if self.loop and self.current:
            source = self.current
        else:
            source = self.queue.pop(0)
            self.current = source

        ctx.voice_client.play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx), self.bot.loop
            )
        )
        ctx.voice_client.source.volume = self.volume
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Streaming(
                name="SSD Discord 🤍",
                url="https://twitch.tv/ssd"
            )
        )
        print("🎵 MUSIC BOT READY")
    # ===================== COMMANDS =====================
    @commands.command()
    async def join(self, ctx):
        await self.join_channel(ctx)
        await ctx.send("🔊 Ses kanalına girdim")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            self.queue.clear()
            self.current = None
            await ctx.send("👋 Çıktım")

    @commands.command()
    async def play(self, ctx, *, search):
        await self.join_channel(ctx)

        msg = await ctx.send("🔎 Aranıyor...")

        data = ytdl.extract_info(search, download=False)

        if "entries" in data:
            data = data["entries"][0]

        url = data["url"]
        title = data["title"]
        duration = data.get("duration", 0)

        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS),
            volume=self.volume
        )

        self.queue.append(source)

        embed = discord.Embed(
            title="🎵 Kuyruğa Eklendi",
            description=f"**{title}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Süre", value=f"{duration//60}:{duration%60:02d}")
        await msg.edit(content=None, embed=embed)

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭ Şarkı geçildi")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            self.queue.clear()
            self.current = None
            await ctx.send("⏹ Müzik durduruldu")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸ Duraklatıldı")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Devam ediyor")

    @commands.command()
    async def volume(self, ctx, vol: int):
        if 0 <= vol <= 100:
            self.volume = vol / 100
            if ctx.voice_client and ctx.voice_client.source:
                ctx.voice_client.source.volume = self.volume
            await ctx.send(f"🔊 Ses: %{vol}")
        else:
            await ctx.send("❌ 0-100 arası gir")

    @commands.command()
    async def loop(self, ctx):
        self.loop = not self.loop
        await ctx.send(f"🔁 Loop: {'Açık' if self.loop else 'Kapalı'}")

    @commands.command()
    async def queue(self, ctx):
        if not self.queue:
            return await ctx.send("📭 Kuyruk boş")

        desc = ""
        for i, _ in enumerate(self.queue[:10], start=1):
            desc += f"{i}. Şarkı\n"

        embed = discord.Embed(
            title="🎶 Müzik Kuyruğu",
            description=desc,
            color=discord.Color.blurple()
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))

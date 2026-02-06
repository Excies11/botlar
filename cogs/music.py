import discord
from discord.ext import commands
import yt_dlp
import asyncio

YDL_OPTS = {
    "format": "bestaudio/best",
    "quiet": True,
    "default_search": "ytsearch",
    "noplaylist": False
}

FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}


class MusicState:
    def __init__(self, bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.current = None
        self.loop = False
        self.volume = 0.5
        self.playing = False

    async def add(self, query):
        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(query, download=False)
            if "entries" in info:
                info = info["entries"][0]
        await self.queue.put(info)
        return info

    async def play_next(self, ctx):
        if not self.loop:
            self.current = await self.queue.get()

        vc = ctx.voice_client
        if not vc:
            return

        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(self.current["url"], **FFMPEG_OPTS),
            volume=self.volume
        )

        vc.play(
            source,
            after=lambda _: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx), self.bot.loop
            )
        )

        embed = discord.Embed(
            title="🎶 Çalıyor",
            description=self.current["title"],
            color=discord.Color.green()
        )
        await ctx.send(embed=embed, view=MusicControls(self))


class MusicControls(discord.ui.View):
    def __init__(self, state):
        super().__init__(timeout=None)
        self.state = state

    @discord.ui.button(emoji="⏯️", style=discord.ButtonStyle.blurple)
    async def pause(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc.is_playing():
            vc.pause()
        elif vc.is_paused():
            vc.resume()
        await interaction.response.defer()

    @discord.ui.button(emoji="⏭️", style=discord.ButtonStyle.gray)
    async def skip(self, interaction: discord.Interaction, _):
        interaction.guild.voice_client.stop()
        await interaction.response.defer()

    @discord.ui.button(emoji="🔁", style=discord.ButtonStyle.green)
    async def loop(self, interaction: discord.Interaction, _):
        self.state.loop = not self.state.loop
        await interaction.response.send_message(
            f"🔁 Loop {'AÇIK' if self.state.loop else 'KAPALI'}",
            ephemeral=True
        )

    @discord.ui.button(emoji="⏹️", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc:
            await vc.disconnect()
        self.state.queue = asyncio.Queue()
        self.state.playing = False
        await interaction.response.defer()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.state = MusicState(bot)

    @commands.command()
    async def play(self, ctx, *, query):
        if not ctx.author.voice:
            return await ctx.send("❌ Ses kanalında değilsin")

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        info = await self.state.add(query)
        await ctx.send(f"➕ **{info['title']}** kuyruğa eklendi")

        if not ctx.voice_client.is_playing():
            await self.state.play_next(ctx)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        self.state.queue = asyncio.Queue()
        self.state.playing = False

    @commands.command()
    async def volume(self, ctx, vol: int):
        self.state.volume = max(0, min(vol / 100, 1))
        await ctx.send(f"🔊 Ses %{vol}")

    @commands.command(name="queue")
    async def queue_cmd(self, ctx):
        if self.state.queue.empty():
            return await ctx.send("📭 Kuyruk boş")

        items = list(self.state.queue._queue)
        msg = "\n".join(f"{i+1}. {x['title']}" for i, x in enumerate(items))
        await ctx.send(f"🎼 **Kuyruk**\n{msg}")


async def setup(bot):
    await bot.add_cog(Music(bot))

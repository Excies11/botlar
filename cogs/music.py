import discord
from discord.ext import commands
import yt_dlp
import asyncio

YDL_OPTS = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True
}

FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

class MusicView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="⏯️ Pause/Resume", style=discord.ButtonStyle.blurple)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc.is_playing():
            vc.pause()
        elif vc.is_paused():
            vc.resume()
        await interaction.response.defer()

    @discord.ui.button(label="⏭️ Skip", style=discord.ButtonStyle.gray)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.guild.voice_client.stop()
        await interaction.response.defer()

    @discord.ui.button(label="🔁 Loop", style=discord.ButtonStyle.green)
    async def loop(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.cog.loop = not self.cog.loop
        await interaction.response.send_message(
            f"🔁 Loop {'AÇIK' if self.cog.loop else 'KAPALI'}",
            ephemeral=True
        )

    @discord.ui.button(label="⏹️ Stop", style=discord.ButtonStyle.red)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        vc.stop()
        await vc.disconnect()
        self.cog.queue.clear()
        await interaction.response.defer()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.loop = False

    async def play_next(self, ctx):
        if not self.queue:
            return

        url = self.queue[0] if self.loop else self.queue.pop(0)

        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info["url"]
            title = info["title"]

        vc = ctx.guild.voice_client
        vc.play(
            discord.FFmpegPCMAudio(stream_url, **FFMPEG_OPTS),
            after=lambda e: asyncio.run_coroutine_threadsafe(
                self.play_next(ctx), self.bot.loop
            )
        )

        embed = discord.Embed(
            title="🎶 Çalıyor",
            description=title,
            color=discord.Color.green()
        )
        await ctx.send(embed=embed, view=MusicView(self))

    @commands.command()
    async def play(self, ctx, *, query: str):
        if not ctx.author.voice:
            return await ctx.send("❌ Ses kanalında değilsin")

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
            url = info["webpage_url"]

        self.queue.append(url)
        await ctx.send(f"➕ Kuyruğa eklendi: **{info['title']}**")

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    @commands.command()
    async def skip(self, ctx):
        ctx.voice_client.stop()

    @commands.command()
    async def stop(self, ctx):
        self.queue.clear()
        await ctx.voice_client.disconnect()

    @commands.command()
    async def queue(self, ctx):
        if not self.queue:
            return await ctx.send("📭 Kuyruk boş")

        msg = "\n".join(f"{i+1}. {q}" for i, q in enumerate(self.queue))
        await ctx.send(f"🎼 **Kuyruk**\n{msg}")


async def setup(bot):
    await bot.add_cog(Music(bot))

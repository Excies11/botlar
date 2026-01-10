import discord
from discord.ext import commands
import yt_dlp
import asyncio

YDL_OPTS = {
    "format": "bestaudio",
    "quiet": True,
    "default_search": "ytsearch",
    "noplaylist": True,
}

FFMPEG_OPTS = {
    "options": "-vn",
}

class MusicView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="⏸️", style=discord.ButtonStyle.secondary)
    async def pause(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("Duraklatıldı", ephemeral=True)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.success)
    async def resume(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("Devam ediyor", ephemeral=True)

    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, _):
        vc = interaction.guild.voice_client
        if vc:
            await vc.disconnect()
            await interaction.response.send_message("Durduruldu", ephemeral=True)


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Streaming(
                name="SSD Discord 🤍",
                url="https://twitch.tv/ssd"
            )
        )
        print("🎵 MUSIC BOT READY")

    @commands.command()
    async def play(self, ctx, *, query: str):
        if not ctx.author.voice:
            return await ctx.send("❌ Ses kanalında değilsin")

        if not ctx.voice_client:
            await ctx.author.voice.channel.connect()

        vc = ctx.voice_client

        with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(query, download=False)
            if "entries" in info:
                info = info["entries"][0]

            url = info["url"]
            title = info.get("title", "Bilinmeyen")

        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTS)

        if vc.is_playing():
            vc.stop()

        vc.play(source)

        await ctx.send(
            embed=discord.Embed(
                title="🎶 Çalıyor",
                description=title,
                color=discord.Color.green()
            ),
            view=MusicView()
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))

import discord
from discord.ext import commands
import yt_dlp

YDL_OPTS = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True,
}

FFMPEG_OPTS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}
@commands.Cog.listener()
async def on_ready(self):
    await self.bot.change_presence(
        activity=discord.Streaming(
            name="SSD Discord 🤍",
            url="https://twitch.tv/ssd"
        ),
        status=discord.Status.online
    )
    print("🎵 MUSIC COG YÜKLENDİ")


class MusicView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="⏸️ Duraklat", style=discord.ButtonStyle.secondary)
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("⏸️ Duraklatıldı", ephemeral=True)

    @discord.ui.button(label="▶️ Devam", style=discord.ButtonStyle.success)
    async def resume(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("▶️ Devam ediyor", ephemeral=True)

    @discord.ui.button(label="⏹️ Durdur", style=discord.ButtonStyle.danger)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc:
            await vc.disconnect()
            await interaction.response.send_message("⏹️ Müzik durduruldu", ephemeral=True)


class MusicUI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="Müzik 🎵"
            )
        )
        print("🎵 MUSIC COG YÜKLENDİ")

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

        embed = discord.Embed(
            title="🎶 Şimdi Çalıyor",
            description=f"**{title}**",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed, view=MusicView())


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicUI(bot))

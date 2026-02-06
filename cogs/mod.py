import discord
from discord.ext import commands
from datetime import timedelta
import re
import time

BAD_WORDS = [
    "amk", "aq", "orospu", "sik", "yarrak", "ananı", "piç", "ibne"
]

LINK_REGEX = re.compile(r"(https?:\/\/|www\.)", re.IGNORECASE)

SPAM_LIMIT = 5          # mesaj
SPAM_SECONDS = 6        # saniye
CAPS_PERCENT = 0.7      # %70 büyük harf
CAPS_MIN_LEN = 8        # min uzunluk


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_messages = {}  # spam takip

    # ================= PRESENCE =================
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Streaming(
                name="SSD Moderation 🤍",
                url="https://twitch.tv/ssd"
            )
        )
        print("🛡️ MODERATION BOT READY")

    # ================= AUTOMOD CORE =================
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.guild_permissions.administrator:
            return

        content = message.content.lower()

        # ---- Küfür filtresi ----
        for word in BAD_WORDS:
            if word in content:
                await self.punish(
                    message,
                    "Küfür / Hakaret",
                    delete=True
                )
                return

        # ---- Link engel ----
        if LINK_REGEX.search(content):
            await self.punish(
                message,
                "İzinsiz link",
                delete=True
            )
            return

        # ---- CAPS spam ----
        if len(message.content) >= CAPS_MIN_LEN:
            upper = sum(1 for c in message.content if c.isupper())
            if upper / len(message.content) >= CAPS_PERCENT:
                await self.punish(
                    message,
                    "Caps spam",
                    delete=True
                )
                return

        # ---- Flood / spam ----
        now = time.time()
        uid = message.author.id

        self.user_messages.setdefault(uid, [])
        self.user_messages[uid].append(now)

        self.user_messages[uid] = [
            t for t in self.user_messages[uid]
            if now - t <= SPAM_SECONDS
        ]

        if len(self.user_messages[uid]) >= SPAM_LIMIT:
            await self.punish(
                message,
                "Spam / Flood",
                timeout=30,
                delete=True
            )
            return

        await self.bot.process_commands(message)

    # ================= CEZA SİSTEMİ =================
    async def punish(self, message, reason, timeout=15, delete=False):
        member = message.author

        if delete:
            try:
                await message.delete()
            except:
                pass

        try:
            await member.timeout(
                timedelta(seconds=timeout),
                reason=reason
            )
        except:
            pass

        embed = discord.Embed(
            title="🚨 AutoMod Ceza",
            color=discord.Color.red()
        )
        embed.add_field(name="Kullanıcı", value=member.mention, inline=False)
        embed.add_field(name="Sebep", value=reason, inline=False)
        embed.add_field(name="Süre", value=f"{timeout} saniye", inline=False)

        await message.channel.send(embed=embed, delete_after=5)

    # ================= MANUEL KOMUTLAR =================
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member} atıldı | {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Sebep yok"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member} banlandı | {reason}")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, süre: int, *, reason="Sebep yok"):
        await member.timeout(
            timedelta(seconds=süre),
            reason=reason
        )
        await ctx.send(f"🔇 {member} {süre}s mute | {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        await ctx.channel.purge(limit=amount)
        await ctx.send(
            f"🧹 {amount} mesaj silindi",
            delete_after=3
        )


async def setup(bot):
    await bot.add_cog(Moderation(bot))

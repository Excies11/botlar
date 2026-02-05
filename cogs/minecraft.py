import discord
from discord.ext import commands
import random
import time
import aiosqlite

DB_PATH = "owo.db"
DAILY_COOLDOWN = 86400  # 24 saat

class OwO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.init_db())

    async def init_db(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                last_daily INTEGER DEFAULT 0
            )
            """)
            await db.commit()

    async def get_user(self, user_id: int):
        async with aiosqlite.connect(DB_PATH) as db:
            cur = await db.execute(
                "SELECT balance, last_daily FROM users WHERE user_id = ?",
                (user_id,)
            )
            row = await cur.fetchone()
            if row is None:
                await db.execute(
                    "INSERT INTO users (user_id, balance, last_daily) VALUES (?, 0, 0)",
                    (user_id,)
                )
                await db.commit()
                return 0, 0
            return row

    async def update_balance(self, user_id: int, new_balance: int):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE users SET balance = ? WHERE user_id = ?",
                (new_balance, user_id)
            )
            await db.commit()

    # ================== COMMANDS ==================

    @commands.command()
    async def bal(self, ctx):
        bal, _ = await self.get_user(ctx.author.id)
        await ctx.send(f"💰 **Bakiyen:** `{bal}` coin")

    @commands.command()
    async def daily(self, ctx):
        bal, last = await self.get_user(ctx.author.id)
        now = int(time.time())

        if now - last < DAILY_COOLDOWN:
            kalan = DAILY_COOLDOWN - (now - last)
            saat = kalan // 3600
            dk = (kalan % 3600) // 60
            return await ctx.send(f"⏳ Daily için **{saat}s {dk}dk** kaldı")

        reward = random.randint(500, 1000)

        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE users SET balance = ?, last_daily = ? WHERE user_id = ?",
                (bal + reward, now, ctx.author.id)
            )
            await db.commit()

        await ctx.send(f"🎁 Daily aldın! **+{reward} coin**")

    @commands.command()
    async def cf(self, ctx, amount: int):
        bal, _ = await self.get_user(ctx.author.id)

        if amount <= 0:
            return await ctx.send("❌ Geçersiz miktar")
        if amount > bal:
            return await ctx.send("❌ Yeterli paran yok")

        win = random.choice([True, False])

        if win:
            bal += amount
            msg = f"🪙 **Kazandın!** +{amount}"
        else:
            bal -= amount
            msg = f"💀 **Kaybettin!** -{amount}"

        await self.update_balance(ctx.author.id, bal)
        await ctx.send(msg)

    @commands.command()
    async def blackjack(self, ctx, bet: int):
        bal, _ = await self.get_user(ctx.author.id)

        if bet <= 0 or bet > bal:
            return await ctx.send("❌ Geçersiz bahis")

        def draw():
            return random.randint(1, 11)

        player = draw() + draw()
        dealer = draw() + draw()

        if player > 21:
            bal -= bet
            result = "💥 Bust! Kaybettin"
        elif dealer > 21 or player > dealer:
            bal += bet
            result = "🃏 Kazandın!"
        elif player == dealer:
            result = "🤝 Berabere"
        else:
            bal -= bet
            result = "💀 Kaybettin"

        await self.update_balance(ctx.author.id, bal)

        embed = discord.Embed(
            title="🃏 Blackjack",
            color=discord.Color.gold()
        )
        embed.add_field(name="Sen", value=str(player))
        embed.add_field(name="Dealer", value=str(dealer))
        embed.add_field(name="Sonuç", value=result, inline=False)
        embed.add_field(name="Bakiye", value=f"{bal} coin", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def helpowo(self, ctx):
        embed = discord.Embed(
            title="🐾 OwO Bot Komutları",
            color=discord.Color.pink()
        )
        embed.add_field(name="💰 Ekonomi", value="`!bal` `!daily`", inline=False)
        embed.add_field(name="🎲 Oyunlar", value="`!cf <miktar>` `!blackjack <bahis>`", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(OwO(bot))

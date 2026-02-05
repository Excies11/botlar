import discord
from discord.ext import commands
import random
import time
import aiosqlite

DB = "economy.db"

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.init_db())

    async def init_db(self):
        async with aiosqlite.connect(DB) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER DEFAULT 0,
                last_daily INTEGER DEFAULT 0
            )
            """)
            await db.commit()

    async def get_user(self, user_id):
        async with aiosqlite.connect(DB) as db:
            cur = await db.execute(
                "SELECT balance, last_daily FROM users WHERE user_id=?",
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

    @commands.command()
    async def bal(self, ctx):
        bal, _ = await self.get_user(ctx.author.id)
        await ctx.send(f"💰 Bakiyen: **{bal} coin**")

    @commands.command()
    async def daily(self, ctx):
        bal, last = await self.get_user(ctx.author.id)
        now = int(time.time())

        if now - last < 86400:
            return await ctx.send("⏳ Daily zaten alındı")

        reward = random.randint(300, 700)

        async with aiosqlite.connect(DB) as db:
            await db.execute(
                "UPDATE users SET balance=?, last_daily=? WHERE user_id=?",
                (bal + reward, now, ctx.author.id)
            )
            await db.commit()

        await ctx.send(f"🎁 Günlük ödül: **{reward} coin**")

    @commands.command()
    async def cf(self, ctx, amount: int):
        bal, _ = await self.get_user(ctx.author.id)
        if amount <= 0 or amount > bal:
            return await ctx.send("❌ Geçersiz miktar")

        win = random.choice([True, False])

        async with aiosqlite.connect(DB) as db:
            if win:
                bal += amount
                msg = f"🪙 Kazandın! +{amount}"
            else:
                bal -= amount
                msg = f"💀 Kaybettin! -{amount}"

            await db.execute(
                "UPDATE users SET balance=? WHERE user_id=?",
                (bal, ctx.author.id)
            )
            await db.commit()

        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(Economy(bot))

import discord
from discord.ext import commands
import random
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "owo_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class Owo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()

    # ========= YARDIMCI =========
    def get_user(self, user_id):
        uid = str(user_id)
        if uid not in self.data:
            self.data[uid] = {
                "money": 100,
                "last_daily": None
            }
        return self.data[uid]

    # ========= BALANCE =========
    @commands.command()
    async def balance(self, ctx):
        user = self.get_user(ctx.author.id)
        await ctx.send(f"💰 **{ctx.author.name}** bakiyesi: `{user['money']}` coin")

    # ========= DAILY =========
    @commands.command()
    async def daily(self, ctx):
        user = self.get_user(ctx.author.id)
        now = datetime.utcnow()

        if user["last_daily"]:
            last = datetime.fromisoformat(user["last_daily"])
            if now - last < timedelta(hours=24):
                kalan = timedelta(hours=24) - (now - last)
                return await ctx.send(
                    f"⏳ Daily için `{kalan.seconds//3600}s {kalan.seconds%3600//60}dk` kaldı"
                )

        reward = random.randint(200, 400)
        user["money"] += reward
        user["last_daily"] = now.isoformat()
        save_data(self.data)

        await ctx.send(f"🎁 Daily aldın! **+{reward} coin**")

    # ========= HUNT =========
    @commands.command()
    async def hunt(self, ctx):
        user = self.get_user(ctx.author.id)

        outcomes = [
            ("🐱 Kedi yakaladın", random.randint(50, 120)),
            ("🐶 Köpek çıktı", random.randint(30, 80)),
            ("🦊 Tilki kaçtı", -random.randint(20, 60)),
            ("☠️ Tuzak!", -random.randint(50, 100))
        ]

        result, amount = random.choice(outcomes)
        user["money"] = max(0, user["money"] + amount)
        save_data(self.data)

        await ctx.send(f"{result} → `{amount}` coin")

    # ========= COINFLIP =========
    @commands.command()
    async def cf(self, ctx, amount: int, choice: str):
        user = self.get_user(ctx.author.id)

        if amount <= 0:
            return await ctx.send("❌ Geçersiz miktar")
        if user["money"] < amount:
            return await ctx.send("❌ Paran yetmiyor")
        if choice.lower() not in ["yazi", "tura"]:
            return await ctx.send("❌ yazi / tura yaz")

        flip = random.choice(["yazi", "tura"])

        if flip == choice.lower():
            user["money"] += amount
            msg = f"🎉 Kazandın! **+{amount}** coin"
        else:
            user["money"] -= amount
            msg = f"💀 Kaybettin! **-{amount}** coin"

        save_data(self.data)
        await ctx.send(f"🪙 Sonuç: **{flip}**\n{msg}")

    # ========= LEADERBOARD =========
    @commands.command()
    async def top(self, ctx):
        sorted_users = sorted(
            self.data.items(),
            key=lambda x: x[1]["money"],
            reverse=True
        )[:5]

        msg = ""
        for i, (uid, info) in enumerate(sorted_users, 1):
            user = await self.bot.fetch_user(int(uid))
            msg += f"**{i}. {user.name}** → {info['money']} coin\n"

        await ctx.send(f"🏆 **Top 5 Zenginler**\n{msg}")


async def setup(bot):
    await bot.add_cog(Owo(bot))

import discord
from discord.ext import commands
from discord.ui import View, Button
import random
import aiosqlite

DB = "economy.db"

def hand_value(hand):
    total = sum(hand)
    aces = hand.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

class BlackjackView(View):
    def __init__(self, ctx, bet, player, dealer):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.bet = bet
        self.player = player
        self.dealer = dealer
        self.finished = False

    async def end_game(self, interaction, result):
        async with aiosqlite.connect(DB) as db:
            if result == "win":
                await db.execute(
                    "UPDATE users SET balance = balance + ? WHERE user=? AND guild=?",
                    (self.bet, self.ctx.author.id, self.ctx.guild.id)
                )
                msg = "🎉 **Kazandın!**"
            elif result == "lose":
                await db.execute(
                    "UPDATE users SET balance = balance - ? WHERE user=? AND guild=?",
                    (self.bet, self.ctx.author.id, self.ctx.guild.id)
                )
                msg = "💀 **Kaybettin!**"
            else:
                msg = "➖ **Berabere**"

            await db.commit()

        self.finished = True
        self.clear_items()

        await interaction.response.edit_message(
            content=(
                f"🃏 **Blackjack Bitti**\n"
                f"Sen: {hand_value(self.player)} {self.player}\n"
                f"Bot: {hand_value(self.dealer)} {self.dealer}\n\n{msg}"
            ),
            view=self
        )

    @discord.ui.button(label="➕ Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, _):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message("❌ Sana ait değil", ephemeral=True)

        self.player.append(random.choice([2,3,4,5,6,7,8,9,10,11]))
        if hand_value(self.player) > 21:
            return await self.end_game(interaction, "lose")

        await interaction.response.edit_message(
            content=f"🃏 Elin: {self.player} ({hand_value(self.player)})",
            view=self
        )

    @discord.ui.button(label="⏹ Stand", style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, _):
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message("❌ Sana ait değil", ephemeral=True)

        while hand_value(self.dealer) < 17:
            self.dealer.append(random.choice([2,3,4,5,6,7,8,9,10,11]))

        p = hand_value(self.player)
        d = hand_value(self.dealer)

        if d > 21 or p > d:
            await self.end_game(interaction, "win")
        elif p < d:
            await self.end_game(interaction, "lose")
        else:
            await self.end_game(interaction, "draw")

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bj(self, ctx, bet: int):
        if bet <= 0:
            return await ctx.send("❌ Bahis geçersiz")

        async with aiosqlite.connect(DB) as db:
            cur = await db.execute(
                "SELECT balance FROM users WHERE user=? AND guild=?",
                (ctx.author.id, ctx.guild.id)
            )
            row = await cur.fetchone()

        if not row or row[0] < bet:
            return await ctx.send("❌ Yetersiz bakiye")

        deck = [2,3,4,5,6,7,8,9,10,10,10,11] * 4
        random.shuffle(deck)

        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]

        view = BlackjackView(ctx, bet, player, dealer)
        await ctx.send(
            f"🃏 **Blackjack**\nElin: {player} ({hand_value(player)})",
            view=view
        )

async def setup(bot):
    await bot.add_cog(Blackjack(bot))

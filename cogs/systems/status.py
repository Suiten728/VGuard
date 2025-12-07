import discord
from discord.ext import commands, tasks
import asyncio
import random

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_status.start()  # 起動時にループ開始

    def cog_unload(self):
        self.update_status.cancel()

    @tasks.loop(seconds=10)  # 10秒ごとに更新
    async def update_status(self):
        await self.bot.wait_until_ready()

        ping = round(self.bot.latency * 1000)
        server_count = len(self.bot.guilds)
        user_count = sum(g.member_count for g in self.bot.guilds)

        # ランダムにステータス切り替え（例：2パターン）
        statuses = [
            f"/help┃ping:{ping}ms",
            f"{server_count}server┃{user_count}user"
        ]

        activity = discord.Game(name=random.choice(statuses))
        await self.bot.change_presence(activity=activity)

    @update_status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Status(bot))
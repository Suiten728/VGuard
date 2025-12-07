from database import init_db
init_db()

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True  # メッセージ監視用

load_dotenv(dotenv_path="ci/.env")
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

bot = commands.Bot(command_prefix="V!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await bot.tree.sync()

async def load_extensions():
    await bot.load_extension("cogs.owner")
    await bot.load_extension("cogs.moderation")

bot.loop.create_task(load_extensions())
bot.run(TOKEN)

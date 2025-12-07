import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

# .envからトークン読み込み
load_dotenv(dotenv_path="ci/.env")
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if TOKEN is None:
    raise ValueError("DISCORD_BOT_TOKEN が見つかりません")

# インテント設定
intents = discord.Intents.default()
intents.message_content = True

class Mhelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help-m")
    @commands.has_permissions(administrator=True)
    async def help_command(self, ctx: commands.Context):
        """モデレーター用ヘルプコマンド"""
        view = discord.ui.View(timeout=None)
        view.add_item(LanguageSelect())

        await ctx.send(view=view)

class LanguageSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="日本語", value="ja", description="日本語のガイドを表示"),
            discord.SelectOption(label="English", value="en", description="Display guide in English"),
            discord.SelectOption(label="中文", value="zh", description="显示中文指南"),
            discord.SelectOption(label="한국어", value="ko", description="한국어 가이드 보기"),
            discord.SelectOption(label="Bahasa Indonesia", value="id", description="Tampilkan panduan dalam Bahasa Indonesia"),
        ]
        super().__init__(placeholder="言語を選択してください / Select a language", options=options, min_values=1, max_values=1, ephemeral=True)

    async def callback(self, interaction: discord.Interaction):
        selected_language = self.values[0]
        embed = guides.get(selected_language)
        if embed:
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("選択された言語のガイドが見つかりませんでした。", ephemeral=True)

# --- 言語別ガイド ---
guides = {
    "ja": discord.Embed(
        title="VGuard Bot モデレーター用ヘルプ",
        description="VGuard Botのモデレータ向けの使い方を説明します。\n\n"
                    "以下のコマンドを使用して、Botの機能を利用できます。",
        color=discord.Color.blue()
    ),
    "en": discord.Embed(
        title="VGuard Bot Help",
        description="This is how to use the VGuard Bot.\n\n"
                    "Use the following commands to utilize the bot's features.",
        color=discord.Color.blue()
    ),
    "zh": discord.Embed(
        title="VGuard 机器人帮助",
        description="这是如何使用 VGuard 机器人的说明。\n\n"
                    "使用以下命令来利用机器人的功能。",
        color=discord.Color.blue()
    ),
    "ko": discord.Embed(
        title="VGuard 봇 도움말",
        description="VGuard 봇 사용 방법입니다。\n\n"
                    "다음 명령어를 사용하여 봇의 기능을 이용할 수 있습니다。",
        color=discord.Color.blue()
    ),
    "id": discord.Embed(
        title="Bantuan Bot VGuard",
        description="Ini adalah cara menggunakan Bot VGuard.\n\n"
                    "Gunakan perintah berikut untuk memanfaatkan fitur bot.",
        color=discord.Color.blue()
    )
}

# Botクラス（本体）
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="V!",
            intents=intents
        )

    async def setup_hook(self):
        await self.add_cog(Mhelp(self))
        await self.tree.sync()
        print("🔧 setup_hook 完了（Mhelp Cog 読み込み & スラッシュコマンド同期）")

    async def on_message(self, message):
        await self.process_commands(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(Mhelp(bot))

# 実行部分
if __name__ == "__main__":
    bot = MyBot()
    bot.run(TOKEN)
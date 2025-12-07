import discord
from discord.ext import commands

class LanguageSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="日本語", value="ja", description="日本語のガイドを表示"),
            discord.SelectOption(label="English", value="en", description="Display guide in English"),
            discord.SelectOption(label="中文", value="zh", description="显示中文指南"),
            discord.SelectOption(label="한국어", value="ko", description="한국어 가이드 보기"),
            discord.SelectOption(label="Bahasa Indonesia", value="id", description="Tampilkan panduan dalam Bahasa Indonesia"),
        ]
        super().__init__(
            placeholder="言語を選択してください / Select a language",
            options=options,
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        embed = guides.get(self.values[0])
        if embed:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("その言語のガイドは見つかりません。", ephemeral=True)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Botのヘルプを表示します")
    async def help_command(self, ctx: commands.Context):
        view = discord.ui.View(timeout=None)
        view.add_item(LanguageSelect())
        await ctx.send(content="🌐 言語を選択してください：", view=view)

guides = {
    "ja": discord.Embed(
        title="VGuard Bot ヘルプ", 
        description="以下のコマンドが使用できます。また、`V!`をプレフィックスとして使用できます。", 
        color=discord.Color.blue())
        .add_field(name="</help:1380891085345128459>", value="VGuard Botのヘルプを表示します。", inline=False)
        .add_field(name="</help-m:1381265490080698495>", value="モデレーター限定のヘルプを表示します。", inline=False)
        .add_field(name="</ping:1381265490080698495>", value="Botの応答速度を測定します。", inline=False)
        .add_field(name="</userinfo:1380891085345128459>", value="指定したユーザーの情報を表示します。", inline=False)
        .add_field(name="</coin:1383481556026261586>", value="ウェザプラコインの情報を表示します。", inline=False),

    "en": discord.Embed(
        title="VGuard Bot Help",
        description="You can use the following commands. Use `V!` as the prefix.",
        color=discord.Color.blue())
        .add_field(name="</help:1380891085345128459>", value="Displays the help for VGuard Bot.", inline=False)
        .add_field(name="</ping:1381265490080698495>", value="Measures the bot's response speed.", inline=False)
        .add_field(name="</userinfo:1383481556026261586>", value="Displays information about a specified user.", inline=False),

    "zh": discord.Embed(
        title="VGuard 机器人帮助",
        description="您可以使用以下命令。使用 `V!` 作为前缀。",
        color=discord.Color.blue())
        .add_field(name="</help:1380891085345128459>", value="显示 VGuard 机器人的帮助信息。", inline=False)
        .add_field(name="</ping:1381265490080698495>", value="测量机器人的响应速度。", inline=False)
        .add_field(name="</userinfo:1383481556026261586>", value="显示指定用户的信息。", inline=False),

    "ko": discord.Embed(
        title="VGuard 봇 도움말",
        description="다음 명령어를 사용할 수 있습니다. 접두사로 `V!`를 사용하세요.",
        color=discord.Color.blue())
        .add_field(name="</help:1380891085345128459>", value="VGuard 봇의 도움말을 표시합니다.", inline=False)
        .add_field(name="</ping:1381265490080698495>", value="봇의 응답 속도를 측정합니다.", inline=False)
        .add_field(name="</userinfo:1383481556026261586>", value="지정한 사용자의 정보를 표시합니다.", inline=False),

    "id": discord.Embed(
        title="Bantuan Bot VGuard",
        description="Anda dapat menggunakan perintah berikut. Gunakan `V!` sebagai awalan.",
        color=discord.Color.blue())
        .add_field(name="</help:1380891085345128459>", value="Menampilkan bantuan untuk Bot VGuard.", inline=False)
        .add_field(name="</ping:1381265490080698495>", value="Mengukur kecepatan respons bot.", inline=False)
        .add_field(name="</userinfo:1383481556026261586>", value="Menampilkan informasi tentang pengguna yang ditentukan.", inline=False),
}

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))

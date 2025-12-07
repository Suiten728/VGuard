import discord
from discord.ext import commands
from discord.ext.commands import hybrid_command, Context
import re
import datetime
import sqlite3
from database import get_owner, get_admin, get_report_channel  # ← 重複インポートを整理

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # ボット／DMは無視
        if message.author.bot or not message.guild:
            return

        guild = message.guild

        # 権限（オーナー or 運営ロール）判定を先に用意
        owner_id = get_owner(guild.id)
        admin_role_id = get_admin(guild.id)  # DBにはロールIDが入っている想定
        has_admin_role = False
        if admin_role_id:
            admin_role = guild.get_role(admin_role_id)
            if admin_role and admin_role in getattr(message.author, "roles", []):
                has_admin_role = True

        is_owner = bool(owner_id and message.author.id == owner_id)
        is_privileged = is_owner or has_admin_role

        # 1) @everyone / @here の検出は、文字列検索より mention_everyone が確実
        if message.mention_everyone:
            if not is_privileged:
                try:
                    await message.delete()
                except (discord.Forbidden, discord.NotFound):
                    pass

                report_channel_id = get_report_channel(guild.id)
                if report_channel_id:
                    report_channel = guild.get_channel(report_channel_id)
                    if report_channel:
                        try:
                            await report_channel.send(
                                f"🚨 **@everyone / @here 使用検出！**\n"
                                f"ユーザー: {message.author.mention}\n"
                                f"内容: \n{message.content}\n"
                                f"チャンネル: {message.channel.mention}"
                            )
                        except discord.Forbidden:
                            pass
                return  # このメッセージの処理はここで終了

        # 2) 大量メンション（ユーザー）検出：5人以上で削除＆通報（権限者は除外）
        unique_mentions = {m.id for m in message.mentions if isinstance(m, discord.Member)}
        if len(unique_mentions) >= 5 and not is_privileged:
            try:
                await message.delete()
            except (discord.Forbidden, discord.NotFound):
                pass

            report_channel_id = get_report_channel(guild.id)
            if report_channel_id:
                report_channel = guild.get_channel(report_channel_id)
                if report_channel:
                    try:
                        await report_channel.send(
                            f"🚨 **大量メンション検出！**\n"
                            f"ユーザー: {message.author.mention}\n"
                            f"人数: {len(unique_mentions)}人\n"
                            f"内容:\n {message.content}\n"
                            f"チャンネル: {message.channel.mention}\n"
                            f"⚠ 荒らしの可能性があります。ご注意ください。"
                        )
                    except discord.Forbidden:
                        pass
            return

        # 3) 危険URL（ホワイトリスト外）検出：削除＆通報
        urls = re.findall(r"http?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+", message.content) 
        for url in urls:
            domain = re.sub(r"^http?://", "", url).split("/")[0]
            if not is_whitelisted(domain):
                try:
                    await message.delete()
                except (discord.Forbidden, discord.NotFound):
                    pass

                report_channel_id = get_report_channel(guild.id)
                if report_channel_id:
                    channel = guild.get_channel(report_channel_id)
                    if channel:
                        try:
                            await channel.send(
                                f"⚠️ 危険なURL検出: {url}\n"
                                f"ユーザー: {message.author.mention}\n"
                                f"内容: \n{message.content}\n"
                                f"チャンネル: {message.channel.mention}"
                            )
                        except discord.Forbidden:
                            pass
                return

    @hybrid_command(name="timeout", description="指定ユーザーをタイムアウト")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx: Context, member: discord.Member, minutes: int, *, reason: str = "理由なし"):
        until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        await member.timeout(until, reason=reason)
        await ctx.send(f"⏳ {member.mention} を {minutes}分間タイムアウトしました。")

    @hybrid_command(name="untimeout", description="タイムアウト解除")
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx: Context, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"✅ {member.mention} のタイムアウトを解除しました。")

    @hybrid_command(name="warn", description="ユーザーに警告を与える")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx: Context, member: discord.Member, *, reason: str = "なし"):
        now = datetime.datetime.now().isoformat()
        conn = sqlite3.connect("warnings.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO warnings (guild_id, user_id, reason, timestamp) VALUES (?, ?, ?, ?)",
            (ctx.guild.id, member.id, reason, now)
        )
        conn.commit()
        conn.close()
        await ctx.send(f"⚠️ {member.mention} に警告を与えました。理由: {reason}")

    @hybrid_command(name="warnings", description="警告履歴を表示")
    async def warnings(self, ctx: Context, member: discord.Member):
        conn = sqlite3.connect("warnings.db")
        c = conn.cursor()
        c.execute(
            "SELECT reason, timestamp FROM warnings WHERE guild_id = ? AND user_id = ?",
            (ctx.guild.id, member.id)
        )
        rows = c.fetchall()
        conn.close()

        if rows:
            msg = [f"📄 {member.mention} の警告履歴:"]
            for i, (reason, ts) in enumerate(rows, 1):
                msg.append(f"{i}. {reason} ({ts})")
            await ctx.send("\n".join(msg))
        else:
            await ctx.send(f"{member.mention} に警告履歴はありません。")

    @hybrid_command(name="setreport", description="レポート送信先チャンネルを設定")
    @commands.has_permissions(administrator=True)
    async def setreport(self, ctx: Context, channel: discord.TextChannel):
        from database import set_report_channel
        set_report_channel(ctx.guild.id, channel.id)
        await ctx.send(f"✅ 通報チャンネルを {channel.mention} に設定しました。")

# 危険URLのホワイトリスト確認関数
def is_whitelisted(domain: str) -> bool:
    conn = sqlite3.connect("warnings.db")
    c = conn.cursor()
    c.execute("SELECT domain FROM url_whitelist WHERE domain = ?", (domain,))
    result = c.fetchone()
    conn.close()
    return result is not None

async def setup(bot):
    await bot.add_cog(Moderation(bot))


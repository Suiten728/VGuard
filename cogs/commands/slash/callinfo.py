import discord
from discord.ext import commands
import os
import datetime


class CallInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="userinfo", description="指定したユーザーの情報を表示します")
    async def userinfo(self, ctx: commands.Context, user: discord.Member = None):
        user = user or ctx.author

        embed = discord.Embed(
            title=f"{user.display_name} のユーザー情報",
            color=discord.Color.blurple(),
            timestamp=ctx.message.created_at if ctx.message else discord.utils.utcnow()
        )

        embed.set_thumbnail(url=user.display_avatar.url)

        embed.add_field(name="📛 名前", value=f"{user.name}#{user.discriminator}", inline=True)
        embed.add_field(name="🆔 ユーザーID", value=user.id, inline=True)
        embed.add_field(name="🤖 Botか？", value="はい" if user.bot else "いいえ", inline=True)

        embed.add_field(name="🗓️ アカウント作成日", value=user.created_at.strftime("%Y/%m/%d %H:%M:%S"), inline=False)
        if user.joined_at:
            embed.add_field(name="📥 サーバー参加日", value=user.joined_at.strftime("%Y/%m/%d %H:%M:%S"), inline=False)

        roles = [role.mention for role in user.roles if role.name != "@everyone"]
        embed.add_field(name="🏷️ 役職", value=", ".join(roles) if roles else "なし", inline=False)
        embed.add_field(name="⭐ トップロール", value=user.top_role.mention if user.top_role else "なし", inline=True)
        embed.add_field(name="📶 ステータス", value=str(user.status).title(), inline=True)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="serverinfo", description="サーバーの情報を表示します")
    async def serverinfo(self, ctx: commands.Context):
     guild = ctx.guild

     bot_count = sum(1 for member in guild.members if member.bot)
     roles = [role.mention for role in guild.roles if role.name != "@everyone"]
     total_members = guild.member_count
     human_members = sum(1 for member in guild.members if not member.bot)

     embed = discord.Embed(
        title=f"{guild.name} のサーバー情報",
        color=discord.Color.blurple(),
        timestamp=datetime.datetime.utcnow()
    )

     if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

     embed.add_field(name="🆔 サーバーID", value=guild.id, inline=True)
     embed.add_field(name="👑 オーナー", value=guild.owner.mention, inline=True)
     embed.add_field(name="📅 作成日", value=guild.created_at.strftime("%Y/%m/%d %H:%M:%S"), inline=False)
     embed.add_field(
      name="👥 メンバー数",
      value=f"{total_members} 人（うちユーザー {human_members} 人）",
      inline=True
      )
     embed.add_field(name="🤖 Bot数", value=bot_count, inline=True)
     embed.add_field(name="🌐 ロケール", value=guild.preferred_locale, inline=True)
     embed.add_field(name="🏷️ 役職数", value=len(roles), inline=True)
     embed.add_field(name="📂 チャンネル数", value=len(guild.channels), inline=True)

     await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(CallInfo(bot))
import discord
from discord.ext import commands
from discord.ext.commands import Context, has_permissions
from discord.ext.commands import hybrid_command
from database import set_owner, get_owner
from database import set_admin, get_admin

class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setowner")
    @commands.has_permissions(administrator=True)
    async def set_owner_cmd(self, ctx: Context, member: discord.Member):
        """このサーバーのオーナーを設定します。(管理者のみ)"""
        set_owner(ctx.guild.id, member.id)
        await ctx.send(f"✅ {member.mention} をこのサーバーのBotオーナーに設定しました。")

    @hybrid_command(name="showowner", description="現在設定されているBotオーナーを表示")
    async def show_owner_cmd(self, ctx: Context):
        owner_id = get_owner(ctx.guild.id)
        if owner_id:
            owner = ctx.guild.get_member(owner_id)
            if owner:
                await ctx.send(f"👑 現在のBotオーナーは {owner.mention} です。")
                return
        await ctx.send("⚠️ オーナーはまだ設定されていません。")

    @commands.command(name="setadmin")
    @commands.has_permissions(administrator=True)
    async def set_admin_role_cmd(self, ctx: Context, role: discord.Role):
        """このサーバーの運営ロールを設定します。(管理者のみ)"""
        set_admin(ctx.guild.id, role.id)  # DBにはロールIDを保存
        await ctx.send(f"✅ {role.mention} をこのサーバーの運営ロールに設定しました。")

    @hybrid_command(name="showadmin", description="現在設定されている運営ロールを表示")
    async def show_admin_role_cmd(self, ctx: Context):
        role_id = get_admin(ctx.guild.id)  # DBからロールIDを取得
        if role_id:
            role = ctx.guild.get_role(role_id)
            if role:
                await ctx.send(f"👑 現在の運営ロールは {role.mention} です。")
                return
        await ctx.send("⚠️ 運営ロールはまだ設定されていません。")

async def setup(bot):
    await bot.add_cog(OwnerCog(bot))

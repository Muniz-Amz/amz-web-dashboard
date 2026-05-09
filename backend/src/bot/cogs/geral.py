import discord
from discord.ext import commands
from backend.src.database.manager import db

class Geral(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="status")
    async def status(self, ctx):
        ping = round(self.bot.latency * 1000)
        embed = discord.Embed(title="📊 Status AMZ Studios", color=0xFFFFFF)
        embed.add_field(name="📡 Latência", value=f"`{ping}ms`", inline=True)
        embed.add_field(name="🗄️ Banco", value="`Conectado ✅`", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="registrar")
    async def registrar(self, ctx):
        user_id = str(ctx.author.id)
        user_data = {"discord_id": user_id, "name": ctx.author.name, "status": "Ativo"}
        
        try:
            await db.db.users.update_one({"discord_id": user_id}, {"$set": user_data}, upsert=True)
            await ctx.send(f"✅ **{ctx.author.name}**, você foi registrado no AMZCore!")
        except Exception as e:
            await ctx.send(f"❌ Erro no Banco: {e}")

async def setup(bot):
    await bot.add_cog(Geral(bot))
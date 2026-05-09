import discord
from discord.ext import commands
from backend.src.database.manager import db

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Substitua pelo seu ID real do Discord se quiser segurança total
        self.OWNER_ID = 1389503739018219571

    @commands.command(name="setrank")
    async def set_rank(self, ctx, member: discord.Member, *, novo_rank: str):
        """Altera o rank de um usuário no banco"""
        if ctx.author.id != self.OWNER_ID:
            return await ctx.send("❌ Acesso negado. Apenas o Founder pode usar este comando.")

        try:
            await db.db.users.update_one(
                {"discord_id": str(member.id)},
                {"$set": {"rank": novo_rank}},
                upsert=True
            )
            await ctx.send(f"✅ Rank de **{member.name}** atualizado para `{novo_rank}`!")
        except Exception as e:
            await ctx.send(f"❌ Erro: {e}")

    @commands.command(name="addcoins")
    async def add_coins(self, ctx, member: discord.Member, quantidade: int):
        """Adiciona moedas a um usuário"""
        if ctx.author.id != self.OWNER_ID:
            return await ctx.send("❌ Acesso negado.")

        try:
            await db.db.users.update_one(
                {"discord_id": str(member.id)},
                {"$inc": {"coins": quantidade}}, # $inc aumenta o valor atual
                upsert=True
            )
            await ctx.send(f"💰 **{quantidade}** coins adicionados ao saldo de {member.name}!")
        except Exception as e:
            await ctx.send(f"❌ Erro: {e}")

async def setup(bot):
    await bot.add_cog(Admin(bot))
import discord
from discord.ext import commands
# Remova o "backend." do início
from src.database.manager import db

class Perfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="p")
    async def ver_perfil(self, ctx, member: discord.Member = None):
        """Mostra o perfil AMZ de um usuário"""
        member = member or ctx.author
        user_id = str(member.id)

        try:
            # Busca os dados no MongoDB
            data = await db.db.users.find_one({"discord_id": user_id})

            if not data:
                # Se não existir, cria um perfil básico na hora
                data = {
                    "discord_id": user_id,
                    "name": member.name,
                    "rank": "Membro",
                    "coins": 0,
                    "scripts": []
                }
                await db.db.users.insert_one(data)

            # Estética Minimalista AMZ (Preto e Branco)
            embed = discord.Embed(
                title=f"👤 PERFIL AMZ - {member.name.upper()}",
                color=0x000000 
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            
            embed.add_field(name="🏷️ Rank", value=f"`{data.get('rank', 'Membro')}`", inline=True)
            embed.add_field(name="💰 AMZ Coins", value=f"`${data.get('coins', 0)}`", inline=True)
            
            # Lista os scripts se o usuário tiver algum
            scripts = data.get('scripts', [])
            scripts_list = ", ".join(scripts) if scripts else "Nenhum script ativo"
            embed.add_field(name="📜 Scripts Autorizados", value=f"```{scripts_list}```", inline=False)
            
            embed.set_footer(text=f"ID: {user_id} | AMZ Studios")
            
            await ctx.send(embed=embed)

        except Exception as e:
            print(f"❌ [PERFIL] Erro ao buscar dados: {e}")
            await ctx.send("⚠️ Houve um erro ao carregar o perfil.")

async def setup(bot):
    await bot.add_cog(Perfil(bot))
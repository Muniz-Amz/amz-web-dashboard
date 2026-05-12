import discord
from discord.ext import commands
import os
import threading
from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
from backend.src.database.manager import db

# 1. CONFIGURAÇÃO DE CAMINHOS E AMBIENTE
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

# 2. SISTEMA ANTI-HIBERNAÇÃO (KEEP-ALIVE)
# O Render desliga o bot se não houver tráfego HTTP. Isso mantém uma porta aberta.
app = Flask('')

@app.route('/')
def home():
    return "AMZ BOT ONLINE"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# 3. CLASSE PRINCIPAL DO BOT
class AMZBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True 
        intents.members = True
        intents.guilds = True # Necessário para detectar entrada em servidores
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        # Conexão com o banco de dados MongoDB
        await db.connect()
        
        # Carregamento Automático de Cogs (Módulos de comandos)
        cogs_path = Path(__file__).parent / "cogs"
        for file in cogs_path.glob("*.py"):
            if file.name != "__init__.py":
                extension = f"backend.src.bot.cogs.{file.stem}"
                try:
                    await self.load_extension(extension)
                    print(f"⚙️  [AMZ] Módulo carregado: {file.name}")
                except Exception as e:
                    print(f"❌ [AMZ] Erro ao carregar {file.name}: {e}")

    async def on_ready(self):
        print(f"---")
        print(f"🚀 AMZ BOT OPERALIONAL")
        print(f"🤖 Usuário: {self.user.name}")
        print(f"🔗 ID: {self.user.id}")
        print(f"---")

    # FUNÇÃO CRÍTICA: Registra o servidor no banco assim que o bot entra
    async def on_guild_join(self, guild):
        print(f"✅ [AMZ] Bot adicionado ao servidor: {guild.name} (ID: {guild.id})")
        
        dados_servidor = {
            "guild_id": str(guild.id),
            "nome": guild.name,
            "canal_id": "Não configurado",
            "dias": 1
        }
        
        try:
            # Salva no MongoDB para aparecer no seu site HTML
            await db.db.servidores.update_one(
                {"guild_id": str(guild.id)},
                {"$set": dados_servidor},
                upsert=True
            )
            print(f"💾 [AMZ] Servidor {guild.name} sincronizado com sucesso.")
        except Exception as e:
            print(f"❌ [AMZ] Erro ao sincronizar com banco: {e}")

# 4. EXECUÇÃO
bot = AMZBot()

if __name__ == "__main__":
    # Inicia o Flask em uma thread separada antes do Bot
    t = threading.Thread(target=run_flask)
    t.start()
    
    # Inicia o Bot do Discord
    bot.run(os.getenv("DISCORD_TOKEN"))
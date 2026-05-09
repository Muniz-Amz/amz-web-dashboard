import discord
from discord.ext import commands
import os
from pathlib import Path
from dotenv import load_dotenv
from backend.src.database.manager import db

# Caminhos automáticos baseados na sua estrutura
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

class AMZBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True # Essencial para ler o !limpar
        intents.members = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        # 1. Conexão com MongoDB
        await db.connect()
        
        # 2. Carregamento Automático de todas as Cogs na sua pasta
        cogs_path = Path(__file__).parent / "cogs"
        for file in cogs_path.glob("*.py"):
            if file.name != "__init__.py":
                # Converte o caminho do arquivo para o formato de importação do Python
                extension = f"backend.src.bot.cogs.{file.stem}"
                try:
                    await self.load_extension(extension)
                    print(f"⚙️  [AMZ] Módulo carregado: {file.name}")
                except Exception as e:
                    print(f"❌ [AMZ] Erro ao carregar {file.name}: {e}")

    async def on_ready(self):
        print(f"🚀 AMZ CLEANER ONLINE | {self.user.name}")

bot = AMZBot()

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
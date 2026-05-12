import os
import sys
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# ==========================================================
# 1. CONFIGURAÇÃO DE CAMINHOS (O segredo para o Render)
# ==========================================================
# Isso ensina o Python a encontrar a pasta 'src' dentro de 'backend'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Tenta importar o bot com os dois caminhos possíveis para evitar erros
try:
    from src.bot.events.bot_client import bot
except ImportError:
    try:
        from bot.events.bot_client import bot
    except ImportError as e:
        print(f"❌ ERRO CRÍTICO DE IMPORTAÇÃO: {e}")
        print(f"Pastas visíveis para o Python: {os.listdir(BASE_DIR)}")
        sys.exit(1)

load_dotenv()

# ==========================================================
# 2. SISTEMA ANTI-DESLIGAMENTO (FLASK)
# ==========================================================
app = Flask(__name__)

@app.route('/')
def health_check():
    # O Render acessa isso para confirmar que o app está vivo
    return "AMZ Studios: Bot Status Online!", 200

def run_flask():
    # O Render define a porta automaticamente na variável 'PORT'
    port = int(os.environ.get("PORT", 8080))
    print(f"🌐 Servidor de Verificação rodando na porta {port}")
    app.run(host='0.0.0.0', port=port)

# ==========================================================
# 3. INICIALIZAÇÃO DO BOT E BANCO DE DADOS
# ==========================================================
async def start_services():
    print("🚀 Iniciando serviços da AMZ Studios...")
    
    # Pega as chaves que você configurou no painel do Render
    uri = os.getenv("MONGO_URI")
    token = os.getenv("DISCORD_TOKEN")
    
    if not uri or not token:
        print("❌ ERRO: Faltam MONGO_URI ou DISCORD_TOKEN nas variáveis de ambiente!")
        return

    try:
        # Testa a conexão com o MongoDB
        print("🔗 Conectando ao MongoDB...")
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("✅ BANCO DE DADOS: AMZCore Conectado!")
        
        # Inicia o Bot do Discord
        print("🤖 DISCORD: Fazendo login...")
        await bot.start(token)
        
    except Exception as e:
        print(f"❌ FALHA NO START: {e}")

# ==========================================================
# 4. EXECUÇÃO PRINCIPAL (THREADING)
# ==========================================================
if __name__ == "__main__":
    # Inicia o Flask em um "fio" (thread) separado
    # Assim o Flask responde ao Render enquanto o Bot roda no loop principal
    web_thread = threading.Thread(target=run_flask)
    web_thread.daemon = True
    web_thread.start()
    
    # Inicia o Bot
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        print("🛑 Sistema encerrado manualmente.")
    except Exception as e:
        print(f"⚠️ Erro inesperado no loop principal: {e}")
import os
import sys
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# --- CONFIGURAÇÃO DE CAMINHO (Obrigatório para o Render achar a pasta 'src') ---
# Isso garante que a pasta 'backend' seja tratada como a raiz das buscas do Python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 1. Importação do Bot (O Python agora encontrará 'src' dentro de 'backend')
try:
    from src.bot.events.bot_client import bot 
except ImportError as e:
    print(f"❌ ERRO DE IMPORTAÇÃO: Não foi possível encontrar o Bot. Verifique a estrutura de pastas. Detalhes: {e}")
    sys.exit(1)

load_dotenv()

# --- SISTEMA PARA O RENDER NÃO DESLIGAR (FLASK) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    # O Render acessa essa rota para saber que o app está vivo
    return "AMZ Bot is Online!", 200

def run_flask():
    # O Render passa a porta na variável de ambiente 'PORT'
    port = int(os.environ.get("PORT", 8080))
    print(f"🌐 Servidor Web iniciado na porta {port}")
    app.run(host='0.0.0.0', port=port)

# --- SERVIÇOS PRINCIPAIS ---
async def start_services():
    print("🚀 Iniciando serviços da AMZ Studios...")
    uri = os.getenv("MONGO_URI")
    token = os.getenv("DISCORD_TOKEN")
    
    if not uri or not token:
        print("❌ ERRO: Verifique MONGO_URI e DISCORD_TOKEN no painel Environment do Render!")
        return

    try:
        # Teste de Conexão com MongoDB
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("✅ BANCO DE DADOS: Conectado (AMZCore).")
        
        # 2. Inicia o Bot do Discord
        print("🤖 DISCORD: Autenticando...")
        await bot.start(token)
        
    except Exception as e:
        print(f"❌ FALHA CRÍTICA NO BOT/BANCO: {e}")

if __name__ == "__main__":
    # Inicia o Flask em uma Thread (fio) separada para não travar o Bot
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # Inicia o loop assíncrono principal
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        print("🛑 Processo encerrado pelo usuário.")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")
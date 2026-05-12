import os
import sys
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# 1. FORÇANDO O "GPS" DO PYTHON
# Isso descobre onde o run.py está e diz: "Aqui é o começo de tudo"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 2. IMPORTAÇÃO DIRETA
# Como o BASE_DIR (pasta backend) está no topo do sistema, 
# ele VAI achar a pasta 'src' que você me mostrou na foto.
try:
    from src.bot.events.bot_client import bot
    print("✅ Módulo do Bot localizado com sucesso!")
except Exception as e:
    print(f"❌ ERRO DE IMPORTAÇÃO: {e}")
    print(f"O que o Python vê nesta pasta: {os.listdir(BASE_DIR)}")
    sys.exit(1)

load_dotenv()

# --- FLASK (O "Coração" para o Render não desligar) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "AMZ Studios: Status Online!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    print(f"🌐 Servidor Web ativo na porta {port}")
    app.run(host='0.0.0.0', port=port)

# --- INICIALIZAÇÃO DOS SERVIÇOS ---
async def start_services():
    print("🚀 Iniciando serviços da AMZ Studios...")
    uri = os.getenv("MONGO_URI")
    token = os.getenv("DISCORD_TOKEN")
    
    if not uri or not token:
        print("❌ ERRO: Faltam variáveis MONGO_URI ou DISCORD_TOKEN!")
        return

    try:
        # Banco de Dados
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("✅ BANCO DE DADOS: AMZCore Conectado!")
        
        # Bot do Discord
        print("🤖 DISCORD: Conectando bot...")
        await bot.start(token)
    except Exception as e:
        print(f"❌ FALHA NO START: {e}")

if __name__ == "__main__":
    # Inicia o Flask (Diz pro Render que o app está vivo)
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # Inicia o Bot
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        print("Desligando...")
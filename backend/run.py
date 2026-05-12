
import os
import sys
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 1. Importe o seu bot aqui (ajuste o caminho se necessário)
# Supondo que seu bot_client está em backend/src/bot/events/
from src.bot.events.bot_client import bot 

load_dotenv()

# --- SISTEMA PARA O RENDER NÃO DESLIGAR (FLASK) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "AMZ Bot is Online!", 200

def run_flask():
    # O Render usa a porta 8080 por padrão
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
# --------------------------------------------------

async def start_services():
    print("🚀 Iniciando serviços da AMZ Studios...")
    uri = os.getenv("MONGO_URI")
    token = os.getenv("DISCORD_TOKEN")
    
    if not uri or not token:
        print("❌ ERRO: Verifique MONGO_URI e DISCORD_TOKEN no Render!")
        return

    try:
        # Teste do Banco
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("✅ BANCO DE DADOS: Conectado (AMZCore).")
        
        # 2. Inicia o Bot do Discord
        print("🤖 DISCORD: Ligando Bot...")
        await bot.start(token)
        
    except Exception as e:
        print(f"❌ FALHA CRÍTICA: {e}")

if __name__ == "__main__":
    # Inicia o Flask em uma Thread separada (Essencial para o Render)
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # Inicia o loop assíncrono para o Bot
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        print("Desligando...")
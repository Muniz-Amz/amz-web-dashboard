import os
import sys
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# 1. LOCALIZADOR DE ELITE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
BOT_DIR = os.path.join(SRC_DIR, 'bot')

# Adicionamos os caminhos ao GPS do Python
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, SRC_DIR)

print(f"🔍 [DEBUG AMZ] Pasta Backend: {os.listdir(BASE_DIR)}")
if os.path.exists(BOT_DIR):
    print(f"🔍 [DEBUG AMZ] O que tem dentro da BOT: {os.listdir(BOT_DIR)}")
else:
    print("❌ [DEBUG AMZ] ERRO: A pasta 'bot' não existe em 'src'!")

# 2. TENTATIVA DE IMPORTAÇÃO
try:
    # Tentando o caminho absoluto
    from src.bot.events.bot_client import bot
    print("✅ BOT: Módulo localizado e carregado!")
except Exception as e:
    print(f"❌ ERRO DE IMPORTAÇÃO: {e}")
    # Se falhar, tentamos o caminho curto (sem o src)
    try:
        from bot.events.bot_client import bot
        print("✅ BOT: Localizado via caminho curto!")
    except:
        print("❌ FALHA TOTAL: O arquivo 'bot_client.py' não foi achado no caminho esperado.")
        sys.exit(1)

load_dotenv()

# --- FLASK (ESTILO PRETO E BRANCO AMZ) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "<body style='background:#000;color:#fff;'><h1>AMZ STUDIOS</h1><p>Bot: ONLINE</p></body>", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- INICIALIZAÇÃO ---
async def start_services():
    uri = os.getenv("MONGO_URI")
    token = os.getenv("DISCORD_TOKEN")
    try:
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("✅ BANCO: AMZCore Online!")
        await bot.start(token)
    except Exception as e:
        print(f"❌ ERRO: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(start_services())
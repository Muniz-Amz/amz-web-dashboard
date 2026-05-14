import os
import sys
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# 1. AJUSTE DE "GPS"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 2. IMPORTAÇÃO CORRIGIDA (O segredo estava aqui!)
try:
    # Removido o ".events" porque o arquivo está na pasta bot
    from src.bot.bot_client import bot
    print("✅ SUCESSO: O Bot foi encontrado na sala (pasta bot)!")
except ImportError as e:
    print(f"❌ ERRO: O Python ainda não achou o Bot. Detalhes: {e}")
    sys.exit(1)

load_dotenv()

# --- FLASK (PÁGINA AMZ PRETO E BRANCO) ---
app = Flask(__name__)
@app.route('/')
def health_check():
    return "<body style='background:#000;color:#fff;font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;'><div><h1>AMZ STUDIOS</h1><p style='text-align:center;'>BOT ONLINE</p></div></body>", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- INICIALIZAÇÃO ---
async def start_services():
    uri = os.getenv("MONGO_URI")
    token = os.getenv("DISCORD_TOKEN")
    try:
        print("🔗 Conectando ao Banco AMZCore...")
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("✅ BANCO: Conectado!")
        
        print("🤖 DISCORD: Ligando...")
        await bot.start(token)
    except Exception as e:
        print(f"❌ ERRO NO START: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(start_services())
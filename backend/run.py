import os
import sys
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# ==========================================
# 1. FORÇANDO O CAMINHO (O "ARROMBA-PORTA")
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')

# Adiciona tanto a pasta 'backend' quanto a 'src' no mapa do Python
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, SRC_DIR)

print(f"🔍 DEBUG: Eu estou na pasta: {BASE_DIR}")
print(f"🔍 DEBUG: Conteúdo da backend: {os.listdir(BASE_DIR)}")

if os.path.exists(SRC_DIR):
    print(f"🔍 DEBUG: Conteúdo da src: {os.listdir(SRC_DIR)}")
else:
    print("❌ ERRO GRAVE: A pasta 'src' não foi encontrada!")

# ==========================================
# 2. TENTATIVA DE IMPORTAÇÃO INTELIGENTE
# ==========================================
bot = None
try:
    # Tenta o caminho completo
    from src.bot.events.bot_client import bot
    print("✅ Módulo do Bot localizado via 'src.bot'!")
except ImportError:
    try:
        # Tenta o caminho direto (já que adicionamos a 'src' no sys.path)
        from bot.events.bot_client import bot
        print("✅ Módulo do Bot localizado via 'bot' direto!")
    except ImportError as e:
        print(f"❌ ERRO FINAL DE IMPORTAÇÃO: {e}")
        # Se chegar aqui, vamos parar o processo com erro detalhado
        sys.exit(1)

load_dotenv()

# ==========================================
# 3. FLASK (PARA O RENDER NÃO DORMIR)
# ==========================================
app = Flask(__name__)

@app.route('/')
def health_check():
    # Estilo minimalista preto e branco para o criador da AMZ
    return "<body style='background:#000;color:#fff;font-family:sans-serif;'><h1>AMZ Studios</h1><p>Bot Status: Online</p></body>", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    print(f"🌐 Servidor Web ativo na porta {port}")
    app.run(host='0.0.0.0', port=port)

# ==========================================
# 4. INICIALIZAÇÃO
# ==========================================
async def start_services():
    uri = os.getenv("MONGO_URI")
    token = os.getenv("DISCORD_TOKEN")
    
    try:
        print("🔗 Conectando ao Banco AMZCore...")
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("✅ BANCO DE DADOS: Conectado!")
        
        print("🤖 DISCORD: Ligando...")
        await bot.start(token)
    except Exception as e:
        print(f"❌ FALHA NO START: {e}")

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        pass
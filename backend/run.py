import asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Carrega as variáveis do .env
load_dotenv()

async def test_connection():
    print("🚀 Iniciando teste de conexão da AMZ Studios...")
    uri = os.getenv("MONGO_URI")
    
    if not uri:
        print("❌ ERRO: MONGO_URI não encontrada no .env!")
        return

    try:
        client = AsyncIOMotorClient(uri)
        await client.admin.command('ping')
        print("✅ CONECTADO! O banco AMZCore está online.")
    except Exception as e:
        print(f"❌ FALHA NA CONEXÃO: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
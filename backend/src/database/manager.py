import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.uri = os.getenv("MONGO_URI")
        self.client = None
        self.db = None

    async def connect(self):
        if not self.client:
            self.client = AsyncIOMotorClient(self.uri)
            self.db = self.client["AMZCore"]
            print("🗄️  Banco de dados AMZCore conectado com sucesso.")

    async def save_guild(self, guild_id, data):
        if self.db is None: await self.connect()
        return await self.db.guilds.update_one(
            {"guild_id": str(guild_id)},
            {"$set": data},
            upsert=True
        )

# ESTA É A LINHA QUE ESTÁ FALTANDO:
db = DatabaseManager()
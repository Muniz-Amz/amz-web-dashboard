from datetime import datetime

def guild_config_model(guild_id, guild_name):
    """Estrutura padrão para as configurações de um servidor"""
    return {
        "guild_id": str(guild_id),
        "guild_name": guild_name,
        "configurations": {
            "cleaner_channel_id": None, # ID do canal que o bot deve limpar
            "is_active": True,           # Se o sistema de automação está ligado
            "logs_channel_id": None      # Onde o bot avisa o que foi feito
        },
        "metadata": {
            "last_update": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
    }
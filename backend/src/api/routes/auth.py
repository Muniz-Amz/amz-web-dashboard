from flask import Blueprint, request, jsonify
import requests
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth-callback', methods=['POST'])
def auth_callback():
    data = request.json
    access_token = data.get('access_token')
    
    # Valida o token com o Discord
    response = requests.get(
        'https://discord.com/api/users/@me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    if response.status_code == 200:
        user_data = response.json()
        # Aqui você verifica se o ID do usuário é o seu (Douglas Muniz)
        is_admin = user_data['id'] == "1389503739018219571" 
        return jsonify({"authorized": is_admin, "user": user_data})
    
    return jsonify({"authorized": False}), 401
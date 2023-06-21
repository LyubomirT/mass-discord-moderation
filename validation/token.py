
import requests
def check_token_validity(token):
    headers = {
        'Authorization': f'Bot {token}'
    }
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    return response.status_code == 200
import streamlit as st
import requests
import uuid
import json
import base64


CLIENT_ID = str(st.secrets['CLIENT_ID'])
CLIENT_SECRET = str(st.secrets['CLIENT_SECRET'])


def get_token() -> str:
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload={
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
        'Authorization': f'Basic {encoded_auth_string}'
    }

    res = requests.post(url=url, 
                        headers=headers,
                        data=payload,
                        verify=False)
    
    access_token = res.json()['access_token']
    return access_token



def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
    "model": "GigaChat-Pro",
    "messages": [
        {
            "role": "user",
            "content": msg
        }
    ],
    "update_interval": 0
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, 
                             headers=headers, 
                             data=payload, 
                             verify=False)

    return response.json()["choices"][0]["message"]["content"]
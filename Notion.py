from datetime import datetime
import requests
import os
import dotenv


class Logs():
    def __init__(self):
        dotenv.load_dotenv()
        
        self._header = {
            "Authorization": f"Bearer {os.getenv('NOTION_TOKEN')}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
    def fetch_data(self):
        response = requests.post(f'https://api.notion.com/v1/databases/{os.getenv("DATABASE_LOGS")}/query', headers=self._header)
        return response
        
        
    def send_data(self, username:str, url:str):
        payload = {
            "parent": {"database_id": os.getenv("DATABASE_LOGS")},
            "properties": {
                "Usuario": {
                    "title": [{"text": {"content": username}}]
                },
                "URL": {
                    "url": url
                },
                "Fecha": {
                    "date": {"start": datetime.now().isoformat()}
                }
            }
        }
        response = requests.post('https://api.notion.com/v1/pages', headers=self._header, json=payload)
        if response.status_code == 200:
            return True
        else:
            return False

class Usuario():
    def __init__(self):
        dotenv.load_dotenv()
        
        self._header = {
            "Authorization": f"Bearer {os.getenv("NOTION_TOKEN")}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
    def fetch_data(self):
        response = requests.post(f'https://api.notion.com/v1/databases/{os.getenv("DATABASE_ID")}/query', headers=self._header)
        return response
        
        
    def send_data(self, id:str, username:str, first_name:str):
        payload = {
            "parent": {"database_id": os.getenv("DATABASE_ID")},
            "properties": {
                "Nombre": {
                    "title": [{"text": {"content": first_name}}]
                },
                "Username": {
                    "rich_text": [{"text": {"content": username}}]
                },
                "ID": {
                    "number": id
                },
                "Fecha de Registro": {
                    "date": {"start": datetime.now().date().isoformat()}
                }
            }
        }

        response = requests.post('https://api.notion.com/v1/pages', headers=self._header, json=payload)
        if response.status_code == 200:
            return True
        else:
            return False
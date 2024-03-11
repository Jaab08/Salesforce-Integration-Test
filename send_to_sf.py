import sys
import os
import requests
import json
from html import escape

# Configuración inicial
consumer_key = os.getenv('SF_CONSUMER_KEY')
consumer_secret = os.getenv('SF_CONSUMER_SECRET')
username = os.getenv('SF_USERNAME')
password = os.getenv('SF_PASSWORD') + os.getenv('SF_SECURITY_TOKEN')
auth_url = 'https://login.salesforce.com/services/oauth2/token'

# ----- Headers y data para autorizacion -----
headers = {
    'Authorization': f'Bearer {sf_auth_token}',
    'Content-Type': 'application/json'
}

data = {
    'grant_type': 'password',
    'client_id': consumer_key,
    'client_secret': consumer_secret,
    'username': username,
    'password': password
}

# Solicitud de autenticación
response = requests.post(auth_url, data=data)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Extraer token
    access_token = response.json().get('access_token')
    instance_url = response.json().get('instance_url')
    print("Token de Acceso Obtenido:", access_token)
    print("URL de la Instancia:", instance_url)
else:
    print("Error al obtener el token de acceso:", response.text)

# ----- Header para peticion al webservice -----
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Webservice Url
service_url = f'{instance_url}/services/apexrest/knowledgeService'

# El primer argumento es el nombre del archivo que contiene los nombres de los archivos modificados
filename = sys.argv[1]

with open(filename, 'r') as f:
    # Crea una lista donde cada elemento es una línea (nombre de archivo) del archivo, eliminando espacios blancos y saltos de línea
    modified_files = [line.strip() for line in f]

print(modified_files)
for file_name in modified_files:
    with open(file_name, 'r', encoding='utf-8') as file:
        html_content = file.read()
        # Escapa comillas simples para evitar inyección de SOQL
        article_title = escape(file_name.replace('.html', '').replace("'", "\\'"))
        print(article_title)
        # Genera UrlName reemplazando espacios por guiones
        url_name = article_title.replace(' ', '-')

        # Datos para enviar al webservice
        data = {
            'answerId': article_title,
            'content': html_content
        }

        # Realizar solicitud POST
        response = requests.post(sf_endpoint, json=data, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200 or response.status_code == 201:
            # print(f'Artículo procesado exitosamente: {article_title}')
            print(response.json())
        else:
            print(f'Error al procesar el artículo {article_title}: {response.json()}')

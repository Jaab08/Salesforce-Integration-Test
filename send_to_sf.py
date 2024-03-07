import sys
import os
from simple_salesforce import Salesforce, bulk
from html import escape

# Configuración inicial
username = os.getenv('SF_USERNAME')
password = os.getenv('SF_PASSWORD')
security_token = os.getenv('SF_SECURITY_TOKEN')

# Autenticación
sf = Salesforce(username=username, password=password, security_token=security_token)

update_batch = []
create_batch = []

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

        # Buscar si existe un artículo con ese título
        articles = sf.query_all(f"SELECT Id, Title FROM Knowledge__kav WHERE Title = '{article_title}' LIMIT 1")
        print(articles)
        
        if articles['totalSize'] > 0:
            # Si el artículo existe, prepáralo para actualizar
            article_id = articles['records'][0]['Id']
            update_batch.append({'Id': article_id, 'Answer__c': html_content})
        else:
            # Si el artículo no existe, prepáralo para crear
            create_batch.append({'Title': article_title, 'UrlName': url_name, 'Answer__c': html_content})

# Realizar operaciones bulk
if update_batch:
    responseU = sf.bulk.Knowledge__kav.update(update_batch)
    print('--Update--')
    print(responseU)
if create_batch:
    responseC = sf.bulk.Knowledge__kav.insert(create_batch)
    print('--Create--')
    print(responseC)

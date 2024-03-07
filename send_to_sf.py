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

print(sys.argv)
for file_name in sys.argv[1:]:
    with open(file_name, 'r', encoding='utf-8') as file:
        html_content = file.read()
        # Escapa comillas simples para evitar inyección de SOQL
        article_title = escape(file_name.replace('.html', '').replace("'", "\\'"))
        # Genera UrlName reemplazando espacios por guiones
        url_name = article_title.replace(' ', '-')

        # Buscar si existe un artículo con ese título
        articles = sf.query_all("SELECT Id, Title FROM Knowledge__kav WHERE Title = '{article_title}' LIMIT 1")
        
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
    print(responseU)
if create_batch:
    responseC = sf.bulk.Knowledge__kav.insert(create_batch)
    print(responseC)

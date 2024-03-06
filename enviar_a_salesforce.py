from simple_salesforce import Salesforce
import os

sf = Salesforce(username=os.environ['SF_USERNAME'],
                password=os.environ['SF_PASSWORD'],
                security_token=os.environ['SF_SECURITY_TOKEN'],
                client_id=os.environ['SF_CONSUMER_KEY'],
                client_secret=os.environ['SF_CONSUMER_SECRET'])

with open('articleTest.html', 'r') as html_file:
    html_content = html_file.read()

# Ajusta los campos según tu modelo de datos en Salesforce
response = sf.Knowledge__kav.create({
    'Title': 'Título del Artículo de Prueba',
    'Content__c': html_content,
    # Añade otros campos necesarios aquí
})

print(response)

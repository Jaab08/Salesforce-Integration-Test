from simple_salesforce import Salesforce

sf = Salesforce(username='jesuan@itp.com',
                password='Jesus080498',
                security_token='is4pxqwxjeZ6fGxZelCFoyMZ')
                #consumer_key='3MVG9p1Q1BCe9GmA7_t1bydTwSMU2cQRuFZGYYYpnfs8_x2wGrtWJxOStK5qPr_D.SbdyttnGhnHpZ_C_ffTz', 
                #consumer_secret='142765CA1DC090A57CC6E94B39487D13E3ECFF782A28D63CA15EA161B290A049')

with open('articleTest.html', 'r') as html_file:
    html_content = html_file.read()

# Ajusta los campos según tu modelo de datos en Salesforce
response = sf.Knowledge__kav.create({
    'Title': 'Título del Artículo de Prueba',
    'UrlName': 'Título-del-Artículo-de-Prueba',
    'Answer__c': html_content,
    # Añade otros campos necesarios aquí
})

print(response)

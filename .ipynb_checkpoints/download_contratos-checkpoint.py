import pandas as pd
import requests
from requests_html import HTMLSession
import urllib.request
import shutil

url_main_contrato = 'http://sistemas.macae.rj.gov.br:84/transparencia/default/contratacoes/mostrarcontratos?id='

contratos_df = pd.read_csv('full_table_contratos.csv')

for link in contratos_df['link_id']:
    print(url_main_contrato+str(link))

url_test = 'http://sistemas.macae.rj.gov.br:84/transparencia/default/contratacoes/mostrarcontratos?id=908'

session = HTMLSession()
r = session.get(url_test)

links = r.html.absolute_links
for link in links:
    if link[-4:] == '.pdf':
        print(link)

file_url = 'http://sistemas.macae.rj.gov.br:84/sim/midia/contrato/908/1491490720.pdf'
path = './contratos/'

def download_file(url, path='./'):
    file_name = path + url.split('/')[-1]


    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return file_name



contratos_df['local_do_arquivo'] = contratos_df['link_id'].apply(download_file)
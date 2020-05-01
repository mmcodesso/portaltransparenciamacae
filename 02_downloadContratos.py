# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup
import shutil
import time
import os
import urllib
from tqdm import tqdm


def get_url_pdfs(contratos):
    links_pdfs = []
    links_outros = []
    urls = contratos.url

    for i in tqdm(urls):
        r = requests.get(i)
        soup = BeautifulSoup(r.content, 'lxml')
        pdf = soup.find(id='anexo1').find_all('a')[0]['href']
        if pdf:
            one_pdf = 'http://sistemas.macae.rj.gov.br:84' + pdf
            links_pdfs.append(one_pdf)
        else:
            links_pdfs.append('-')
            links_outros.append(i)
    return links_pdfs, links_outros


def download_file(url, path='./'):
    file_name = path + url.split('/')[-1]
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return file_name


def main():
    print('Processo Iniciado ---- ' + time.ctime(time.time()))
    contratos = pd.read_csv('full_table_contratos.csv')
    links_pdfs, links_outros = get_url_pdfs(contratos)
    contratos['pdf_url_contrato'] = links_pdfs
    contratos['pdf_file_contrato'] = [i.split('/')[-1] for i in links_pdfs]
    contratos['nro_contrato'] = [i.split('/')[-1].split('.')[0] for i in links_pdfs]
    contratos.to_csv('full_table_contratos.csv', index=0)

    print('Total de documentos: ' + str(len(links_pdfs)))
    for i, j in enumerate(links_pdfs):
        file = j.split('/')[-1]
        if not os.path.exists(folder + str(file)):
            try:
                download_file(j, path=folder)
                print('----> pdf atual: ' + str(j), end="\r")
            except:
                continue
    print('Captura finalizada ---- ' + time.ctime(time.time()))


if __name__ == "__main__":
    folder = './fontes_db/contratos/contratos_pdf/'
    main()

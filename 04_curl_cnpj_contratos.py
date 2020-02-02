# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import requests
import json
import time
from tqdm import tqdm

# https://receitaws.com.br/api'


def replace_dots_cnpj(string):
    char = ['.', '-', '/']
    try:
        for i in char:
            string = string.replace(i, '').strip()
    except Exception:
        pass
    return string


def clean_cnpj(cnpj):
    cnpj = cnpj.apply(lambda x: replace_dots_cnpj(x))
    cleaned_cnpjs = [x for x in cnpj if x]  # only not empty entries
    return cleaned_cnpjs


def controla_request(cleaned_cnpjs, cnpj):
    try:
        controle = pd.read_csv('controle_requests.csv')
    except Exception:
        controle = pd.DataFrame(cleaned_cnpjs).rename(columns={0: 'cpf/cnpj'})
        controle['curl_status'] = 0
    controle['curl_status'] = np.where((controle['cpf/cnpj'] == cnpj), 1, controle.curl_status)
    controle.to_csv('controle_requests.csv', index=0)
    return


def main():
    cleaned_cnpjs = set(clean_cnpj(cnpjs))  # turn into set to drop duplicates

    for i in tqdm(cleaned_cnpjs):
        url = base_api + str(i)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                jsonfile = response.json()
                filename = str(i) + str('.json')
                with open(folder_cnpj + filename, 'w') as out:
                    json.dump(jsonfile, out)
                controla_request(cleaned_cnpjs=cleaned_cnpjs, cnpj=i)
        except:
            pass
        time.sleep(21)


if __name__ == "__main__":
    base_api = 'https://www.receitaws.com.br/v1/cnpj/'
    empresas = pd.read_csv('portaltransparenciamacae/empresas_contratos.csv')
    cnpjs = empresas['cpf/cnpj']
    folder_cnpj = './folder_cnpj/'
    main()

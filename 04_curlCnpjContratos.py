# -*- coding: utf-8 -*-

import pandas as pd
import requests
import json
import time
import sys
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


def clean_cnpj(lista_cnpjs):
    """
    Função que recebe uma lista (ou série) de cnpj's e aplica a remoção de pontuação.
    :param cnpj: lista ou série com os cnpj's a serem tratados.
    :return: Lista com os cnpj's tratados.
    """
    cnpj = lista_cnpjs.apply(lambda x: replace_dots_cnpj(x))
    cnpj = cnpj[cnpj.notnull()]
    cleaned_cnpjs = [int(x) for x in cnpj if x and len(x) == 14]  # only not empty entries and correct size
    return cleaned_cnpjs


def controla_request(cleaned_cnpjs, cnpj):
    """
    Função para criação de arquivo de gerenciamento de consulta de cnpj's na API.
    No arquivo, é possível identificar os cnpj's que já foram consultados, de acordo com a coluna "controle".
    controle = 1 => cnpj já consultado.
    controle = 0 => cnpj ainda não consultado.
    :param cleaned_cnpjs: Lista com os cnpj's já tratados (sem pontuação).
    :param cnpj: cnpj a ser registrado como 1 na coluna de controle (já consultado).
    :return:
    """
    controle_temp = pd.DataFrame(cleaned_cnpjs).rename(columns={0: 'cnpj'})
    controle_temp['curl_status'] = 0

    try:
        controle = pd.read_csv('controle_requests.csv', sep="\t")
        controle = controle.append(controle_temp, sort=True)
        controle['curl_status'] = controle['curl_status'].mask(controle['cnpj'] == cnpj, other=1)
        controle.to_csv('controle_requests.csv', index=0, mode='a', sep="\t")
    except Exception:
        controle_temp['curl_status'] = controle_temp['curl_status'].mask(controle_temp['cnpj'] == cnpj, other=1)
        controle_temp.to_csv('controle_requests.csv', index=0, mode='a', sep="\t")
    return


def main():
    cleaned_cnpjs = clean_cnpj(lista_cnpjs)
    cleaned_cnpjs = set(cleaned_cnpjs)  # turn into set, to drop duplicates

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
            continue
        # time.sleep(21)


if __name__ == "__main__":
    base_api = 'https://www.receitaws.com.br/v1/cnpj/'
    # empresas = pd.read_csv('empresas_contratos.csv')
    # lista_cnpjs = empresas['cpf/cnpj']
    file = sys.argv[1]
    lista_cnpjs = pd.read_csv(file, header=0)['CNPJ']
    folder_cnpj = './folder_cnpj/'
    main()

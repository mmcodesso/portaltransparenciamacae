# -*- coding: utf-8 -*-

import pandas as pd
import requests
import json
import time
import sys
from tqdm import tqdm

# https://receitaws.com.br/api'
def replace_dots_cnpj(string):
    """
    Individual punctuation removal
    :param string: CNPJ with possible punctuation presence
    :return: Only numbers CNPJ (striped and with removed punctuation)
    """
    char = ['.', '-', '/']
    try:
        for i in char:
            string = string.replace(i, '').strip()
    except Exception:
        pass
    return string


def clean_cnpj(lista_cnpjs):
    """
    Receives a List (or Series) of CNPJs and applies punctuation removal.
    :param cnpj: List (or Series) of CNPJs
    :return: List with cleaned CNPJs.
    """
    cnpj = lista_cnpjs.apply(lambda x: replace_dots_cnpj(x))
    cnpj = cnpj[cnpj.notnull()]
    cleaned_cnpjs = [int(x) for x in cnpj if x]  # only not empty entries
    return cleaned_cnpjs


def controla_request(cleaned_cnpjs, cnpj):

    """
    Creates a file for management of the requests made in API for retrieving the CNPJs data.
    controle = 1 => already visited CNPJ.
    controle = 0 => not visited CNPJ.
    :param cleaned_cnpjs: List with already cleaned CNPJs.
    :param cnpj: CNPJ being analyzed.
    :return:
    """
    try:
        controle = pd.read_csv('controle_requests.csv', sep="\t")
    except Exception:
        controle = pd.DataFrame(cleaned_cnpjs).rename(columns={0: 'cnpj'})
        controle['curl_status'] = 0
    controle['curl_status'] = controle['curl_status'].mask(controle['cnpj'] == cnpj, other=1)
    # controle['curl_status'] = np.where((controle['cnpj'] == cnpj), 1, controle.curl_status)
    controle.to_csv('controle_requests.csv', index=0, sep="\t")
    return


class BearerAuth(requests.auth.AuthBase):
    """
    Class for bearer authentication in web service for retrieving information about CNPJs
    """
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def main():
    cleaned_cnpjs = clean_cnpj(lista_cnpjs)
    cleaned_cnpjs = set(cleaned_cnpjs)  # turn into set, to drop duplicates
    for i in tqdm(cleaned_cnpjs):
        url = base_api + str(i)
        try:
            response = requests.get(url, auth=BearerAuth(token))
            if response.status_code == 200:
                jsonfile = response.json()
                filename = str(i) + str('.json')
                with open(folder_cnpj + filename, 'w') as out:
                    json.dump(jsonfile, out)
                controla_request(cleaned_cnpjs=cleaned_cnpjs, cnpj=i)
        except:
            continue
        time.sleep(5)


if __name__ == "__main__":
    base_api = 'https://www.receitaws.com.br/v1/cnpj/'
    token = '73cfa07bb83025e781610db9fff55f0680b302fa7837e75335393b8f59b1e6bf'
    file = sys.argv[1]
    lista_cnpjs = pd.read_csv(file, header=0)['CNPJ']
    folder_cnpj = './folder_doadores/'
    main()

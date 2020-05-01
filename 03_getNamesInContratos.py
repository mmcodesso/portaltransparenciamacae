# -*- coding: utf-8 -*-

import re
import operator
import pandas as pd
from docx import Document
from tqdm import tqdm
import time
from itertools import zip_longest  # lib to zip two lists that are not of same size


def get_text(filename):
    """
    Transforms docx in machine readable form for parsing.
    :param filename: name of the file, including extension
    :return: document transformed to machine readable form
    """
    file = Document(filename)
    full_text = []
    for i in file.paragraphs:
        full_text.append(i.text)
    doc = '\n'.join(full_text)
    doc = doc.replace('\n', ' ')
    return doc


def get_names(filename, only_first_page=True, chars_first_page=3000):
    """
    Captura expressões em maiúsculo, entre vírgulas, aceitando acentuação (regex1 = r',\s([A-ZÀ-Ú\s]+),') E
        em maiúsculo, entre Sr. e vírgula, aceitando acentuação regex2 = r'\Sr.\s([A-ZÀ-Ú\s]+),' E
        em maiúsculo, entre Sra. e vírgula, aceitando acentuação regex3 = r'\Sra.\s([A-ZÀ-Ú\s]+),'.
    Assume-se que estas regras capturem todos os nomes de pessoas presentes no documento.
    :param filename: documento a ser consumido pela função que mapeia DOCX (get_text)
    :param only_first_page: flag para indicar se é para pegar apenas a primeira página do documento (proxy: 3000 chars)
    :param chars_first_page: quantidade de caracteres a se considerar no documento (proxy para primeira página)
    :return: lista com os nomes encontrados e os índices das suas posições
    """
    doc = get_text(filename)
    nomes_bruto = re.findall(r',\s([A-ZÀ-Ú\s]+),'
                             r'|\Sr.\s([A-ZÀ-Ú\s]+),'
                             r'|\Sra.\s([A-ZÀ-Ú\s]+),', doc)
    nomes, places = [], []   # lista places é para capturar o indice do termo, no texto
    for i in nomes_bruto:
        if i[0]:
            if 6 > len(i[0].split()) > 1:
                nomes.append(i[0])
                places.append(doc.find(i[0]))
        else:
            if 6 > len(i[1].split()) > 1:
                nomes.append(i[1])
                places.append(doc.find(i[1]))
    nomes = [i.rstrip().replace('\n', ' ').replace('\r', ' ') for i in nomes]  # replace for removing line breaks
    names_and_places = dict(zip(nomes, places))

    if only_first_page:
        new = dict()
        for (key, value) in names_and_places.items():
            if value < chars_first_page:
                new[key] = value
        names_and_places = new
    names_and_places = dict(sorted(names_and_places.items(), key=operator.itemgetter(1)))
    return names_and_places


def get_cpf(filename, only_first_page=True, chars_first_page=3000):
    """
    Identifica os CPFs presentes no documento.
    :param filename: documento a ser consumido pela função que mapeia DOCX (get_text)
    :param only_first_page: flag para indicar se é para pegar apenas a primeira página do documento (proxy: 3000 chars)
    :param chars_first_page: quantidade de caracteres a se considerar no documento (proxy para primeira página)
    :return:
    """
    doc = get_text(filename)
    regex_cpf = r'\d{3}\.\d{3}\.\d{3}\-\d{2}'
    cpfs = re.findall(regex_cpf, doc)
    cpf, places = [], []  # lista places é para capturar o indice do termo, no texto

    for i in cpfs:
        cpf.append(i)
        places.append(doc.find(i))
    cpf_and_places = dict(zip(cpf, places))

    if only_first_page:
        new = dict()
        for (key, value) in cpf_and_places.items():
            if value < chars_first_page:
                new[key] = value
        cpf_and_places = new
    cpf_and_places = dict(sorted(cpf_and_places.items(), key=operator.itemgetter(1)))
    return cpf_and_places


def get_empresas(filename, empresas, only_first_page=True, chars_first_page=3000):
    """
    Identifica os CNPJs presentes no documento.
    :param filename: documento a ser consumido pela função que mapeia DOCX (get_text)
    :param empresas: lista de empresas a procurar no contrato (buscar em full_table_contratos.csv)
    :param only_first_page: flag para indicar se é para pegar apenas a primeira página do documento (proxy: 3000 chars)
    :param chars_first_page: quantidade de caracteres a se considerar no documento (proxy para primeira página)
    :return:
    """
    doc = get_text(filename)
    regex_cnpj = ''
    if type(empresas) == str:
        regex_cnpj += str('|') + empresas
    elif type(empresas) == list:
        for i in empresas:
            regex_cnpj += str('|') + i

    cnpj = re.findall(regex_cnpj, doc)
    cnp, places = [], []  # lista places é para capturar o indice do termo, no texto

    for i in cnpj:
        cnp.append(i)
        places.append(doc.find(i))
    cnp_and_places = dict(zip(cnp, places))

    if only_first_page:
        new = dict()
        for (key, value) in cnp_and_places.items():
            if value < chars_first_page:
                new[key] = value
        cnp_and_places = new
    cnp_and_places = dict(sorted(cnp_and_places.items(), key=operator.itemgetter(1)))
    cnp_and_places = {k: v for k, v in cnp_and_places.items() if v}  # remove keys with empty strings from the dict
    return cnp_and_places


def get_cnpj(filename, only_first_page=True, chars_first_page=3000):
    """
    Identifica os CNPJs presentes no documento.
    :param filename: documento a ser consumido pela função que mapeia DOCX (get_text)
    :param only_first_page: flag para indicar se é para pegar apenas a primeira página do documento (proxy: 3000 chars)
    :param chars_first_page: quantidade de caracteres a se considerar no documento (proxy para primeira página)
    :return:
    """
    doc = get_text(filename)
    regex_cnpj = r'\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}'

    cnpj = re.findall(regex_cnpj, doc)
    cnp, places = [], []  # lista places é para capturar o indice do termo, no texto

    for i in cnpj:
        cnp.append(i)
        places.append(doc.find(i))
    cnp_and_places = dict(zip(cnp, places))

    if only_first_page:
        new = dict()
        for (key, value) in cnp_and_places.items():
            if value < chars_first_page:
                new[key] = value
        cnp_and_places = new
    cnp_and_places = dict(sorted(cnp_and_places.items(), key=operator.itemgetter(1)))
    return cnp_and_places


def get_empresas_and_cnpjs(filename, empresas, only_first_page=True, chars_first_page=3000):
    nms = get_empresas(filename, empresas, only_first_page, chars_first_page)
    cnpjs = get_cnpj(filename, only_first_page, chars_first_page)

    junto = zip_longest(nms, cnpjs)
    full = dict(junto)
    return full


def get_names_and_cpfs(filename, only_first_page=True, chars_first_page=3000):
    nms = get_names(filename, only_first_page, chars_first_page)
    cpfs = get_cpf(filename, only_first_page, chars_first_page)

    junto = zip_longest(nms, cpfs)
    full = dict(junto)
    return full


def gera_nomes_contratos(table_contratos):
    contratos_empresas = table_contratos[['nro_contrato', 'Empresa']]
    content = []
    for i, j in tqdm(contratos_empresas.iterrows()):
        try:
            filename = folder_contratos_docx + str(int(j[0])) + '.docx'
            aux = get_names_and_cpfs(filename, only_first_page=True, chars_first_page=3000)
            content.append(aux)
        except:
            content.append('{}')
            continue
    data = {'nro_contrato': list(contratos_empresas['nro_contrato']),
            'content': list(content)}
    nomes_contratos = pd.DataFrame(data)

    nomes_contratos_final = pd.DataFrame()
    for i, j in nomes_contratos.dropna().iterrows():
        try:
            aux = pd.DataFrame.from_dict(j[1], orient='index').reset_index()
            aux['contrato'] = j[0]
            nomes_contratos_final = nomes_contratos_final.append(aux, sort=True)
        except AttributeError:
            pass

    nomes_contratos_final = nomes_contratos_final.reset_index(drop=True)
    nomes_contratos_final = nomes_contratos_final.rename(columns={'index': 'Nome', 0: 'cpf/cnpj'})
    return nomes_contratos_final


def gera_empresas_contratos(table_contratos):
    numeros_contratos = table_contratos['nro_contrato']
    contratos_empresas = table_contratos[['nro_contrato', 'Empresa']]
    content = []
    for i, j in tqdm(contratos_empresas.iterrows()):
        try:
            filename = folder_contratos_docx + str(int(j[0])) + '.docx'
            aux = get_empresas_and_cnpjs(filename, j[1], only_first_page=True, chars_first_page=3000)
            content.append(aux)
        except:
            content.append('{}')
            continue
    data = {'nro_contrato': list(numeros_contratos), 'content': list(content)}
    empresas_contratos = pd.DataFrame(data)

    empresas_contratos_final = pd.DataFrame()
    for i, j in empresas_contratos.dropna().iterrows():
        try:
            aux = pd.DataFrame.from_dict(j[1], orient='index').reset_index()
            aux['contrato'] = j[0]
            empresas_contratos_final = empresas_contratos_final.append(aux, sort=True)
        except AttributeError as error:
            pass

    empresas_contratos_final = empresas_contratos_final.reset_index(drop=True)
    empresas_contratos_final = empresas_contratos_final.rename(columns={'index': 'Nome', 0: 'cpf/cnpj'})
    return empresas_contratos_final


def main():
    print('Processo Iniciado ---- ' + time.ctime(time.time()))

    nomes_contratos_final = gera_nomes_contratos(table_contratos=table_contratos)
    empresas_contratos_final = gera_empresas_contratos(table_contratos=table_contratos)

    nomes_contratos_final.to_csv("./raw_data/contratos_nomes.csv", index=0)
    empresas_contratos_final.to_csv("./raw_data/contratos_empresas.csv", index=0)
    print('Processo finalizado ---- ' + time.ctime(time.time()))
    return nomes_contratos_final, empresas_contratos_final


if __name__ == "__main__":
    table_contratos = pd.read_csv('full_table_contratos.csv')
    folder_contratos_docx = './fontes_db/contratos/contratos_word/'
    main()


"""
ranges = [(121, 21), (1000, 2429), (2545, 2575), (2640, 2686), (2890, 2890)]
postcode = 1200

for i, j in enumerate(ranges):
    if j[0] < postcode < j[1]:
        print(i)
"""

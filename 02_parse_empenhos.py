# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup
import time
import sys


def parse_empenho(table):
    rows = table.find_all('tr')
    key_name = 0
    key_value = 0
    keys_list = []
    keys_values = []

    for i in rows:
        for col in i.find_all('td'):
            col_value = str(col.text.strip())

            if key_name == 1:
                key_value = 1
                key_value_text = col_value

            if col_value[-1:] == ':' or col_value[-1:] == '-':
                key_name = 1
                key_name_text = col_value

            if key_value == 1 & key_name == 1:
                key_value = 0
                key_name = 0
                keys_list.append(key_name_text)
                keys_values.append(key_value_text)

    values_dict = {}
    keys_and_values = zip(keys_list, keys_values)
    for keys, values in keys_and_values:
        values_dict[keys] = values

    detalhes_emp = pd.DataFrame.from_dict(values_dict, orient='index').T

    return detalhes_emp


def generate_total_empenhos():

    export_detalhes_emp = pd.DataFrame()

    for i, det_emp in enumerate(lista_empenhos):
        emp = str(lista_empenhos[i])
        soup = BeautifulSoup(emp, 'html.parser')
        table = soup.find('table')
        det_empenho_df = parse_empenho(table)
        export_detalhes_emp = export_detalhes_emp.append(det_empenho_df, sort=True)
        export_detalhes_emp = export_detalhes_emp.reset_index(drop=True)

    result = pd.concat([emp_df, export_detalhes_emp], axis=1)

    return result


def main(year):
    print('Iniciando geração da tabela de empenhos ----' + time.ctime(time.time()))
    result = generate_total_empenhos()
    file_name = 'detalhes_emp_' + str(year) + '.csv'
    result.to_csv(file_name, index=0)
    print('Processo finalizado! ----' + time.ctime(time.time()))

    return


if __name__ == "__main__":
    try:
        year = sys.argv[1]
        file = 'credores_empenhos_' + str(year) + '.csv'
        emp_df = pd.read_csv(file)
        lista_empenhos = emp_df.detalhe_empenho
        main(year)
    except:
        print('\nInformar ano desejado.\n')
# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup
import time
import sys
import unicodedata


# def parse_empenho(table):
#     rows = table.find_all('tr')
#     key_name = 0
#     key_value = 0
#     keys_list = []
#     keys_values = []
#
#     for i in rows:
#         for col in i.find_all('td'):
#             col_ = str(col.text.strip())
#             col_value = unicodedata.normalize("NFKD", col_)
#
#             if key_name == 1:
#                 key_value = 1
#                 key_value_text = col_value
#
#             if ":" in col_value and "/" not in col_value:
#                 if col_value[-1:] == ':' or col_value[-1:] == '-':
#                     key_name = 1
#                     key_name_text = col_value
#                 else:
#                     key_name_text = col_value.split(":")[0].strip()
#                     key_value_text = col_value.split(":")[1].strip()
#                     key_value = 0
#                     key_name = 0
#                     keys_list.append(key_name_text)
#                     keys_values.append(key_value_text)
#
#             # if col_value[-1:] == ':' or col_value[-1:] == '-':
#             #     key_name = 1
#             #     key_name_text = col_value
#
#             if key_value == 1 and key_name == 1:
#                 key_value = 0
#                 key_name = 0
#                 keys_list.append(key_name_text)
#                 keys_values.append(key_value_text)
#
#
#     keys_and_values = zip(keys_list, keys_values)
#     values_dict = dict(keys_and_values)
#
#     detalhes_emp = pd.DataFrame.from_dict(values_dict, orient='index').T
#     detalhes_emp.columns = detalhes_emp.columns.str.replace("[:-]", "")
#
#     return detalhes_emp

def parse_empenho(table):
    rows = table.find_all('tr')
    key_name = 0
    key_value = 0
    keys_list = []
    keys_values = []

    for i in rows:
        for j in i.find_all('td'):
            if j.text:
                text = str(j.text.strip())
                content = unicodedata.normalize("NFKD", text)

                if key_name == 1 and key_value == 0:
                    key_value = 1
                    key_value_text = content.strip()
                if ":" in content and "/" not in content:
                    if content[-1] == ":":
                        key_name = 1
                        key_name_text = content[:-1].strip()
                    else:
                        key_name = 1
                        key_value = 1
                        key_name_text = content.split(":")[0].strip()
                        key_value_text = content.split(":")[1].strip()
                if key_value == 1 and key_name == 1:
                    key_value = 0
                    key_name = 0
                    keys_list.append(key_name_text)
                    keys_values.append(key_value_text)

    keys_and_values = zip(keys_list, keys_values)
    values_dict = dict(keys_and_values)
    detalhes_emp = pd.DataFrame.from_dict(values_dict, orient='index').T
    return detalhes_emp


def generate_total_empenhos():

    appended_list = []

    # for i, j in enumerate(lista_empenhos):
    #     try:
    #         emp = str(lista_empenhos[i])
    #         soup = BeautifulSoup(emp, 'html.parser')
    #         table = soup.find('table')
    #         det_empenho_df = parse_empenho(table)
    #         appended_list.append(det_empenho_df)
    #     except Exception:
    #         continue

    for i, j in enumerate(lista_empenhos):
        try:
            emp = lista_empenhos[i]
            soup = BeautifulSoup(emp, 'html.parser')
            table = soup.find('table')
            det_empenho_df = parse_empenho(table)
            appended_list.append(det_empenho_df)
        except:
            print(i)
            continue

    export_detalhes_emp = pd.concat(appended_list, sort=True)
    result = pd.concat([emp_df,
                        export_detalhes_emp.reset_index(drop=True)],
                       sort=True,
                       axis=1)
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
        try:
            emp_df = pd.read_csv(file)
        except pd.errors.ParserError:
            emp_df = pd.read_csv(file, sep="\t")

        lista_empenhos = emp_df.detalhe_empenho
        main(year)
    except IndexError:
        print('\nInformar ano desejado. ---- ' + time.ctime(time.time()))
        sys.exit(1)
    except Exception:
        print('\nErro de processamento. ---- ' + time.ctime(time.time()))
        sys.exit(1)

# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup
import time
import sys
import unicodedata
import unidecode  # remove special chars


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

                if 'cnpj' in content.lower():
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


def generate_total_empenhos(emp_df):

    appended_list = []
    failed_ids = []

    for i, j in enumerate(lista_empenhos):
        try:
            emp = lista_empenhos[i]
            #emp = emp_df[emp_df.Credor.str.contains('AGRIT')].detalhe_empenho[447]
            #emp = emp_df[emp_df.Credor.str.contains('AHAVAT')].detalhe_empenho[454]

            soup = BeautifulSoup(emp, 'html.parser')
            table = soup.find('table')
            det_empenho_df = parse_empenho(table)
            appended_list.append(det_empenho_df)
        except:
            failed_ids.append(i)
            print(i)
            continue

    print('total failed: ', len(failed_ids))
    export_detalhes_emp = pd.concat(appended_list, sort=True)

    thresh = int(export_detalhes_emp.shape[1] * .97)
    export_detalhes_emp = export_detalhes_emp.dropna(thresh=thresh)

    export_detalhes_emp['Número Empenho'] = export_detalhes_emp['Número Empenho'].astype(int)

    emp_df['Credor'] = [unicodedata.normalize("NFKD", str(i)) for i in emp_df.Credor]
    emp_df['Credor'] = [unidecode.unidecode(str(i)) for i in emp_df.Credor]
    emp_df['Credor_temp'] = emp_df['Credor'].apply(lambda x: x.replace(" ", ""))

    export_detalhes_emp['Credor'] = [unicodedata.normalize("NFKD", str(i)) for i in export_detalhes_emp.Credor]
    export_detalhes_emp['Credor'] = [unidecode.unidecode(str(i)) for i in export_detalhes_emp.Credor]
    export_detalhes_emp['Credor_temp'] = export_detalhes_emp['Credor'].apply(lambda x: x.replace(" ", ""))


    result = pd.merge(emp_df,
                      export_detalhes_emp,
                      left_on=['Credor_temp', 'Número do Empenho'],
                      right_on=['Credor_temp', 'Número Empenho']).drop_duplicates()

    result = result.drop(columns=['Credor_temp', 'Credor_y'])
    result = result.rename(columns={'Credor_x': 'Credor'})

    # result = pd.concat([emp_df,
    #                     export_detalhes_emp.reset_index(drop=True)],
    #                    sort=True,
    #                    axis=1)
    return result


def main(year, emp_df):
    print('Iniciando geração da tabela de empenhos ----' + time.ctime(time.time()))
    result = generate_total_empenhos(emp_df)
    file_name = 'detalhes_emp_' + str(year) + '.csv'
    result.to_csv(file_name, index=0)
    print('Processo finalizado! ----' + time.ctime(time.time()))
    return


if __name__ == "__main__":
    try:
        year = sys.argv[1]
        file = 'credores_empenhos_' + str(year) + '.csv'

        if year in [2015, 2018, 2019]:
            emp_df = pd.read_csv(file, sep="\t")
        else:
            emp_df = pd.read_csv(file)
        lista_empenhos = emp_df.detalhe_empenho
        main(year, emp_df)
    except IndexError:
        print('\nInformar ano desejado. ---- ' + time.ctime(time.time()))
        sys.exit(1)
    except Exception:
        print('\nErro de processamento. ---- ' + time.ctime(time.time()))
        sys.exit(1)
# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup
import time
import sys
import unicodedata
import unidecode  # remove special chars
import glob


def get_csv_batch():
    path = r'./raw_data/cred_2016'  # use your path
    all_files = glob.glob(path + "/credores_empenhos_2016_*.csv")

    li = []

    for filename in all_files:
        df_temp = pd.read_csv(filename, index_col=None, header=0)
        li.append(df_temp)

    df = pd.concat(li, axis=0, ignore_index=True, sort=True)
    return df


def parse_empenho(table):
    rows = table.find_all('tr')
    key_name = 0
    key_value = 0
    keys_list = []
    keys_values = []

    for i in rows:
        for j in i.find_all('td'):
            if j.text:
                text = unidecode.unidecode(str(j.text.strip()))
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

    export_detalhes_emp = export_detalhes_emp[~export_detalhes_emp['Numero Empenho'].isna()]
    export_detalhes_emp['Numero Empenho'] = export_detalhes_emp['Numero Empenho'].astype(float)

    emp_df['Credor'] = [unicodedata.normalize("NFKD", str(i)) for i in emp_df.Credor]
    emp_df['Credor'] = [unidecode.unidecode(str(i)) for i in emp_df.Credor]
    emp_df['Credor_temp'] = emp_df['Credor'].apply(lambda x: x.replace(" ", ""))
    emp_df['Número do Empenho'] = emp_df['Número do Empenho'].astype(float)

    if year == 2016:
        path = r'./cred16_pags89/'
        files = glob.glob(path + "jl_*.htm")
        det_empenho_df = pd.DataFrame()
        for filename in files:
            with open(filename, "r", encoding='latin-1') as f:
                contents = f.read()
                page = BeautifulSoup(contents, 'lxml')
                table_det_empenho = page.find('table', id='tbEmpenho')
                temp = parse_empenho(table_det_empenho)
                det_empenho_df = det_empenho_df.append(temp)

        det_empenho_df = det_empenho_df.reset_index(drop=True)
        det_empenho_df = det_empenho_df.drop(det_empenho_df.index[18])
        det_empenho_df = det_empenho_df.reset_index(drop=True)

    export_detalhes_emp = export_detalhes_emp.append(det_empenho_df).reset_index(drop=True)

    export_detalhes_emp['Credor'] = [unicodedata.normalize("NFKD", str(i)) for i in export_detalhes_emp.Credor]
    export_detalhes_emp['Credor'] = [unidecode.unidecode(str(i)) for i in export_detalhes_emp.Credor]
    export_detalhes_emp['Credor_temp'] = export_detalhes_emp['Credor'].apply(lambda x: x.replace(" ", ""))

    export_detalhes_emp['Numero Empenho'] = export_detalhes_emp['Numero Empenho'].astype(float)

    result = pd.merge(emp_df,
                      export_detalhes_emp,
                      left_on=['Credor_temp', 'Número do Empenho'],
                      right_on=['Credor_temp', 'Numero Empenho']).drop_duplicates()

    result = result.drop(columns=['Credor_temp', 'Credor_y', 'Unidade Gestora_y'])
    result = result.rename(columns={'Credor_x': 'Credor', 'Unidade Gestora_x':'Unidade Gestora'})

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

    if year == 2016:
        path = r'./cred16_pags89/'
        files = glob.glob(path + "cred_*.htm")
        empenho_df = pd.DataFrame()
        for filename in files:
            with open(filename, "r", encoding='latin-1') as f:
                contents = f.read()
                page = BeautifulSoup(contents, 'lxml')
                table_empenhos = page.find('table', id='tbTabela1')
                temp = pd.read_html(str(table_empenhos), header=0, skiprows=1,
                                    converters={'Número do Empenho': str})
                empenho_df = empenho_df.append(temp)

        empenho_df = empenho_df.reset_index(drop=True)
        empenho_df = empenho_df[empenho_df.Orçamentário != 'Totais']
        empenho_df = empenho_df.reset_index(drop=True)
        empenho_df.columns = empenho_df.iloc[0]
        empenho_df = empenho_df[empenho_df.Credor != 'Credor']
        empenho_df = empenho_df.reset_index(drop=True)

        emp_df = emp_df.append(empenho_df).reset_index(drop=True)

        lista_empenhos = emp_df.detalhe_empenho
        main(year, emp_df)
    except IndexError:
        print('\nInformar ano desejado. ---- ' + time.ctime(time.time()))
        sys.exit(1)
    except Exception:
        print('\nErro de processamento. ---- ' + time.ctime(time.time()))
        sys.exit(1)
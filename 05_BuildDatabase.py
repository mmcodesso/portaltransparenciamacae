import sqlite3
from sqlite3 import Error
import numpy as np
import pandas as pd
import json
import os
import glob
import unicodedata as ud
import unicodedata
from functools import reduce
import unidecode  # remove special chars


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    connect = None
    try:
        connect = sqlite3.connect(db_file)
        return connect
    except Error as e:
        print(e)
    return connect


def select_table(connect, table):
    """ Query all rows in a table """
    cur = connect.cursor()
    query = "SELECT * FROM " + str(table)
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def sql_fetch(connex):
    cursor_obj = connex.cursor()
    cursor_obj.execute('SELECT name from sqlite_master where type= "table"')
    print(cursor_obj.fetchall())


def beautifier_cols(dataframe):
    cols = dataframe.columns
    cols_new = [j.lower().strip().replace(" ", "_") for j in cols]
    df_new = dataframe.rename(columns=dict(zip(cols, cols_new))).drop_duplicates().reset_index(drop=True)
    return df_new


# Prefeito, Vice-Prefeito e Secretários
def pref():
    df1 = pd.read_excel('./fontes_db/Prefeito, Vice-Prefeito e Secretários.xlsx')
    df1 = df1.drop(columns='ID')
    df1 = beautifier_cols(df1)
    return df1


# Vereadores
def vereadores_dir():
    df_2_dir = pd.read_excel('./fontes_db/Câmara dos Vereadores - Mesa Diretora e Comissões.xlsx',
                             sheet_name='diretora')
    df_2_dir = df_2_dir.iloc[:15, :]
    df_2_dir = beautifier_cols(df_2_dir)
    return df_2_dir


def vereadores_com():
    df_2_com = pd.read_excel('./fontes_db/Câmara dos Vereadores - Mesa Diretora e Comissões.xlsx',
                             sheet_name='comissao')
    df_2_com = beautifier_cols(df_2_com)
    return df_2_com


# Doadores


def doadores():
    df_3_doadores_veread_2012 = pd.read_excel(
        './fontes_db/doadores_vereadores/Eleições 2012 - Doadores Vereadores Mesa Diretora e Comissões.xlsx',
        sheet_name='DOAÇÕES CONSOLIDADO 2').ffill(0)
    df_3_doadores_veread_2012['eleicao'] = 'vereador'
    df_3_doadores_veread_2012['ano'] = '2012'
    df_3_doadores_veread_2014 = pd.read_excel(
        './fontes_db/doadores_vereadores/Eleições 2014 - Doadores Deputados Mesa Diretora e Comissões.xlsx',
        sheet_name='DOAÇÕES CONSOLIDADO 2').ffill(0)
    df_3_doadores_veread_2014['eleicao'] = 'vereador'
    df_3_doadores_veread_2014['ano'] = '2014'
    df_3_doadores_veread_2016 = pd.read_excel(
        './fontes_db/doadores_vereadores/Eleições 2016 - Doadores Vereadores Mesa Diretora e Comissões.xlsx',
        sheet_name='DOAÇÕES CONSOLIDADO 2').ffill(0)
    df_3_doadores_veread_2016['eleicao'] = 'vereador'
    df_3_doadores_veread_2016['ano'] = '2016'
    df_3_doadores_veread_2018 = pd.read_excel(
        './fontes_db/doadores_vereadores/Eleições 2018 - Doadores Deputados Mesa Diretora e Comissões.xlsx',
        sheet_name='DOAÇÕES CONSOLIDADO 2').ffill(0)
    df_3_doadores_veread_2018['eleicao'] = 'vereador'
    df_3_doadores_veread_2018['ano'] = '2018'
    df_3_doadores_pref_2012 = pd.read_excel(
        './fontes_db/doadores_pref/Eleições 2012 - Doadores Comitê Coligação Prefeito e Vice-Prefeito.xlsx',
        sheet_name='DOAÇÕES CONSOLIDADAS 2').ffill(0)
    df_3_doadores_pref_2012['eleicao'] = 'prefeito'
    df_3_doadores_pref_2012['ano'] = '2012'
    df_3_doadores_pref_2012_2 = pd.read_excel(
        './fontes_db/doadores_pref/Eleições 2012 - Doadores Prefeito e Vice-Prefeito.xlsx',
        sheet_name='DOAÇÕES CONSOLIDADAS 2').ffill(0)
    df_3_doadores_pref_2012_2['eleicao'] = 'prefeito'
    df_3_doadores_pref_2012_2['ano'] = '2012'
    df_3_doadores_pref_2014 = pd.read_excel(
        './fontes_db/doadores_pref/Eleições 2014 - Doadores Vice-Prefeito - Campanha Deputado Federal.xlsx',
        sheet_name='DOAÇÕES CONSOLIDADAS 2').ffill(0)
    df_3_doadores_pref_2014['eleicao'] = 'prefeito'
    df_3_doadores_pref_2014['ano'] = '2014'
    df_3_doadores_pref_2016 = pd.read_excel(
        './fontes_db/doadores_pref/Eleições 2016 - Doadores Prefeito e Vice-Prefeito.xlsx',
        sheet_name='DOAÇÕES CONSOLIDADAS 2').ffill(0)
    df_3_doadores_pref_2016['eleicao'] = 'prefeito'
    df_3_doadores_pref_2016['ano'] = '2016'
    df_3_doadores_pref_2016_2 = pd.read_excel(
        './fontes_db/doadores_pref/Eleições 2016 - Doadores Partidos Coligação Prefeito e Vice-Prefeito.xlsx',
        sheet_name='DOAÇÕES CONSOLIDADAS 2').ffill(0)
    df_3_doadores_pref_2016_2['eleicao'] = 'prefeito'
    df_3_doadores_pref_2016_2['ano'] = '2016'
    df_doadores = pd.concat([df_3_doadores_veread_2012,
                             df_3_doadores_veread_2014,
                             df_3_doadores_veread_2016,
                             df_3_doadores_veread_2018,
                             df_3_doadores_pref_2012,
                             df_3_doadores_pref_2012_2,
                             df_3_doadores_pref_2014,
                             df_3_doadores_pref_2016,
                             df_3_doadores_pref_2016_2], sort=True)

    df_doadores = beautifier_cols(df_doadores)
    df_doadores['nome_doador_receita_federal'] = \
        np.where(df_doadores['nome_do_doador'].isna(),
                 df_doadores['nome_do_doador_(receita_federal)'],
                 df_doadores['nome_do_doador'])
    df_doadores['nome_doador_receita_federal'] = \
        np.where(df_doadores['nome_doador_receita_federal'].isna(),
                 df_doadores['nm_doador'],
                 df_doadores['nome_doador_receita_federal'])
    df_doadores = df_doadores.drop(columns=['nm_doador', 'nome_do_doador', 'nome_do_doador_(receita_federal)'])
    df_doadores = df_doadores.rename(columns={'soma_de_pecentual_de_doação': 'soma_de_percentual_de_doação'})
    return df_doadores


# Fornecedores


def fornecedores():
    df_forne_pref_2012 = pd.read_excel(
        './fontes_db/fornecedores_pref/Eleições 2012 - Despesas Comitê Coligação Prefeito e Vice-Prefeito.xlsx',
        sheet_name='DESPESAS CONSOLIDADAS 2').ffill(0)
    df_forne_pref_2012['ano'] = '2012'
    df_forne_pref_2012_2 = pd.read_excel(
        './fontes_db/fornecedores_pref/Eleições 2012 - Despesas Prefeito e Vice-Prefeito.xlsx',
        sheet_name='DESPESAS CONSOLIDADAS 2').ffill(0)
    df_forne_pref_2012_2['ano'] = '2012'
    df_forne_pref_2014 = pd.read_excel(
        './fontes_db/fornecedores_pref/Eleições 2014 - Despesas Vice-Prefeito - Campanha Deputado Federal.xlsx',
        sheet_name='DESPESAS CONSOLIDADAS 2').ffill(0)
    df_forne_pref_2014['ano'] = '2014'
    df_forne_pref_2016 = pd.read_excel(
        './fontes_db/fornecedores_pref/Eleições 2016 - Despesas Partidos Coligação Prefeito e Vice-Prefeito.xlsx',
        sheet_name='DESPESAS CONSOLIDADAS 2').ffill(0)
    df_forne_pref_2016['ano'] = '2016'
    df_forne_pref_2016_2 = pd.read_excel(
        './fontes_db/fornecedores_pref/Eleições 2016 - Despesas Prefeito e Vice-Prefeito.xlsx',
        sheet_name='DESPESAS CONSOLIDADAS 2').ffill(0)
    df_forne_pref_2016_2['ano'] = '2016'
    df_forne_veread_2012 = pd.read_excel(
        './fontes_db/fornecedores_veread/Eleições 2012 - Despesas Vereadores Mesa Diretora e Comissões.xlsx',
        sheet_name='DESPESAS CONSOLIDADAS 2').ffill(0)
    df_forne_veread_2012['ano'] = '2012'
    df_forne_veread_2014 = pd.read_excel(
        './fontes_db/fornecedores_veread/Eleições 2014 - Despesas Deputados Mesa Diretora e Comissões.xlsx',
        sheet_name='DESPESAS CONSOLIDADAS 2').ffill(0)
    df_forne_veread_2014['ano'] = '2014'
    df_forne_veread_2016 = pd.read_excel(
        './fontes_db/fornecedores_veread/Eleições 2016 - Despesas Vereadores Mesa Diretora e Comissões.xlsx',
        sheet_name='DESPESAS CONSOLIDADAS 2').ffill(0)
    df_forne_veread_2016['ano'] = '2016'
    df_forne_veread_2018 = pd.read_excel(
        './fontes_db/fornecedores_veread/Eleições 2018 - Despesas Deputados Mesa Diretora e Comissões.xlsx',
        sheet_name='DESPESAS CONSOLIDADAS 2').ffill(0)
    df_forne_veread_2018['ano'] = '2018'
    df_fornecedores = pd.concat([df_forne_pref_2012,
                                 df_forne_pref_2012_2,
                                 df_forne_pref_2014,
                                 df_forne_pref_2016,
                                 df_forne_pref_2016_2,
                                 df_forne_veread_2012,
                                 df_forne_veread_2014,
                                 df_forne_veread_2016,
                                 df_forne_veread_2018], sort=True)

    df_fornecedores = df_fornecedores.reset_index(drop=True)
    df_fornecedores = df_fornecedores.drop(df_fornecedores.index[361]).reset_index(drop=True)
    df_fornecedores = beautifier_cols(df_fornecedores)
    df_fornecedores['soma_de_percentual_de_despesas'] = \
        np.where(df_fornecedores['soma_de_percentual_de_despesas'].isna(),
                 df_fornecedores['soma_de_pecentual_de_despesas'],
                 df_fornecedores['soma_de_percentual_de_despesas'])

    df_fornecedores['nome_do_fornecedor_receita_federal'] = \
        np.where(df_fornecedores['nome_do_fornecedor'].isna(),
                 df_fornecedores['nome_do_fornecedor_(receita_federal)'],
                 df_fornecedores['nome_do_fornecedor'])

    df_fornecedores = df_fornecedores.drop(columns=['soma_de_pecentual_de_despesas',
                                                    'nome_do_fornecedor',
                                                    'nome_do_fornecedor_(receita_federal)'])
    return df_fornecedores


# Servidores da câmara


def servidores_camara():
    df_serv_camara = pd.read_excel('./fontes_db/Servidores_camara.xlsx')
    df_serv_camara = beautifier_cols(df_serv_camara)
    return df_serv_camara


# Servidores prefeitura


def servidores_pref():
    df_serv_pref = pd.read_excel('./fontes_db/Servidores Prefeitura.xlsx')
    df_serv_pref = beautifier_cols(df_serv_pref)
    return df_serv_pref


# Filiacao Partidaria


def filiacao():
    df_1 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_dc_rj.csv', sep=';', encoding="ISO-8859-1")
    df_2 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_mdb_rj.csv', sep=';',
                       dtype='unicode', encoding="ISO-8859-1")
    df_3 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_pcdob_rj.csv', sep=';',
                       dtype='unicode', encoding="ISO-8859-1")
    df_4 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_psb_rj.csv', sep=';',
                       dtype='unicode', encoding="ISO-8859-1")
    df_5 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_psdb_rj.csv', sep=';',
                       dtype='unicode', encoding="ISO-8859-1")
    df_6 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_psl_rj.csv', sep=';', encoding="ISO-8859-1")
    df_7 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_pt_rj.csv', sep=';',
                       dtype='unicode', encoding="ISO-8859-1")
    df_8 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_pv_rj.csv', sep=';', encoding="ISO-8859-1")
    df_9 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_rede_rj.csv', sep=';', encoding="ISO-8859-1")
    df_10 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_psd_rj.csv', sep=';', encoding="ISO-8859-1")

    df_filiacao_pref = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10], sort=True)
    df_filiacao_pref['eleicao'] = 'PREFEITO'

    df_1_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_avante_rj.csv", sep=";", encoding="ISO-8859-1")
    df_2_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_cidadania_rj.csv", sep=";", encoding="ISO-8859-1")
    df_3_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pdt_rj.csv", sep=";",
                           dtype='unicode', encoding="ISO-8859-1")
    df_4_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pl_rj.csv", sep=";",
                           dtype='unicode', encoding="ISO-8859-1")
    df_5_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pode_rj.csv", sep=";",
                           dtype='unicode', encoding="ISO-8859-1")
    df_6_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pros_rj.csv", sep=";", encoding="ISO-8859-1")
    df_7_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_psc_rj.csv", sep=";", encoding="ISO-8859-1")
    df_8_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_ptc_rj.csv", sep=";", encoding="ISO-8859-1")
    df_9_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_republicanos_rj.csv",
                           sep=";",
                           encoding="ISO-8859-1")
    df_10_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_solidariedade_rj.csv",
                            sep=";",
                            encoding="ISO-8859-1")

    df_filiacao_veread = pd.concat(
        [df_1_ver, df_2_ver, df_3_ver, df_4_ver, df_5_ver, df_6_ver, df_7_ver, df_8_ver, df_9_ver, df_10_ver],
        sort=True)

    df_filiacao_veread['eleicao'] = 'VEREADOR'

    df_filiacao = pd.concat([df_filiacao_pref,
                             df_filiacao_veread], sort=True)

    df_filiacao = beautifier_cols(df_filiacao)
    df_filiacao = df_filiacao.drop(columns=['unnamed:_19'])
    return df_filiacao


# CNPJ RECEITA (JSONS)
def parse_json_files(folder):
    """
    look at the folder with documents and search for json files to parse
    """
    json_list = []
    df_full = pd.DataFrame()
    qsa_full = pd.DataFrame()
    ativ_sec_full = pd.DataFrame()

    # for Path, subdirs, File in os.walk(folder):
    #     for name in File:
    #         if os.path.splitext(os.path.join(Path, name))[1] == ".json":
    #             json_list.append(os.path.join(Path, name))

    for file in os.listdir(folder):
        if file.split(".")[-1] == "json":
            json_list.append(file)
        else:
            pass

    for j in json_list:
        try:
            with open(j) as json_data:
                data = json.load(json_data)
        except:
            continue

        dtframe = pd.DataFrame([data])
        try:
            dtframe['atividade_principal'] = dtframe['atividade_principal'].apply(lambda x: x[0])
            dtframe[['atividade_principal_text', 'atividade_principal_code']] = \
                dtframe.atividade_principal.apply(pd.Series)
            dtframe = dtframe.drop('atividade_principal', axis=1)
        except:
            continue

        dtframe[['billing_free', 'billing_database']] = dtframe.billing.apply(pd.Series)
        dtframe = dtframe.drop('billing', axis=1)

        qsa = pd.DataFrame(dtframe.qsa[0])
        qsa['cnpj_empresa'] = dtframe.cnpj[0]
        dtframe = dtframe.drop('qsa', axis=1)

        ativ_sec = pd.DataFrame(dtframe.atividades_secundarias[0])
        ativ_sec['cnpj_empresa'] = dtframe.cnpj[0]
        dtframe = dtframe.drop('atividades_secundarias', axis=1)

        df_full = df_full.append(dtframe, sort=True)
        qsa_full = qsa_full.append(qsa, sort=True)
        ativ_sec_full = ativ_sec_full.append(ativ_sec, sort=True)
    return df_full, qsa_full, ativ_sec_full


# JSON CREDORES
def dados_receita():
    json_credores_2015, qsa_credores_2015, ativ_sec_credores_2015 = \
        parse_json_files("./fontes_db/jsons/folder_credores_2015/")
    json_credores_2016, qsa_credores_2016, ativ_sec_credores_2016 = \
        parse_json_files("./fontes_db/jsons/folder_credores_2016/")
    json_credores_2017, qsa_credores_2017, ativ_sec_credores_2017 = \
        parse_json_files("./fontes_db/jsons/folder_credores_2017/")
    json_credores_2018, qsa_credores_2018, ativ_sec_credores_2018 = \
        parse_json_files("./fontes_db/jsons/folder_credores_2018/")
    json_credores_2019, qsa_credores_2019, ativ_sec_credores_2019 = \
        parse_json_files("./fontes_db/jsons/folder_credores_2019/")
    json_credores_2015['ano'] = '2015'
    json_credores_2016['ano'] = '2016'
    json_credores_2017['ano'] = '2017'
    json_credores_2018['ano'] = '2018'
    json_credores_2019['ano'] = '2019'
    cnpj_credores = pd.concat([json_credores_2015,
                               json_credores_2016,
                               json_credores_2017,
                               json_credores_2018,
                               json_credores_2019], sort=True).reset_index(drop=True)
    cnpj_credores['categoria'] = 'credores'
    qsa_credores = pd.concat([qsa_credores_2015,
                              qsa_credores_2016,
                              qsa_credores_2017,
                              qsa_credores_2018,
                              qsa_credores_2019], sort=True).reset_index(drop=True)
    qsa_credores['categoria'] = 'credores'
    ativ_sec_credores = pd.concat([ativ_sec_credores_2015,
                                   ativ_sec_credores_2016,
                                   ativ_sec_credores_2017,
                                   ativ_sec_credores_2018,
                                   ativ_sec_credores_2019], sort=True).reset_index(drop=True)
    ativ_sec_credores['categoria'] = 'credores'

    # JSON DOADORES VEREADORES E PREFEITO
    json_doadores_vereadores, qsa_doadores_vereadores, ativ_sec_doadores_vereadores = \
        parse_json_files("./fontes_db/jsons/folder_doadores_vereadores/")
    json_doadores_vereadores['eleicao'] = 'vereadores'

    json_doadores_prefeito, qsa_doadores_prefeito, ativ_sec_doadores_prefeito = \
        parse_json_files("./fontes_db/jsons/folder_doadores_prefeito/")
    json_doadores_prefeito['eleicao'] = 'prefeito'

    doad = pd.concat([json_doadores_prefeito,
                      json_doadores_vereadores], sort=True).reset_index(drop=True)
    doad['categoria'] = 'doadores'

    qsa_doadores = pd.concat([qsa_doadores_prefeito,
                              qsa_doadores_vereadores], sort=True).reset_index(drop=True)
    qsa_doadores['categoria'] = 'doadores'

    ativ_sec_doadores = pd.concat([ativ_sec_doadores_prefeito,
                                   ativ_sec_doadores_vereadores], sort=True).reset_index(drop=True)
    ativ_sec_doadores['categoria'] = 'doadores'

    # JSON FORNECEDORES VEREADORES E PREFEITO

    json_fornecedores_vereadores, qsa_fornecedores_vereadores, ativ_sec_fornecedores_vereadores = \
        parse_json_files("./fontes_db/jsons/folder_fornecedores_vereadores/")
    json_fornecedores_vereadores['eleicao'] = 'vereadores'

    json_fornecedores_prefeito, qsa_fornecedores_prefeito, ativ_sec_fornecedores_prefeito = \
        parse_json_files("./fontes_db/jsons/folder_fornecedores_prefeito/")
    json_fornecedores_prefeito['eleicao'] = 'prefeito'

    fornec = pd.concat([json_fornecedores_prefeito,
                        json_fornecedores_vereadores], sort=True).reset_index(drop=True)
    fornec['categoria'] = 'fornecedores'

    qsa_fornecedores = pd.concat([qsa_fornecedores_prefeito,
                                  qsa_fornecedores_vereadores], sort=True).reset_index(drop=True)
    qsa_fornecedores['categoria'] = 'fornecedores'

    ativ_sec_fornecedores = pd.concat([ativ_sec_fornecedores_prefeito,
                                       ativ_sec_fornecedores_vereadores], sort=True).reset_index(drop=True)
    ativ_sec_fornecedores['categoria'] = 'fornecedores'

    # JUNTANDO AS BASES DOS JSONS

    receita_cnpj = pd.concat([cnpj_credores,
                              doad,
                              fornec], sort=True).reset_index(drop=True)

    receita_qsa = pd.concat([qsa_credores,
                             qsa_doadores,
                             qsa_fornecedores], sort=True).reset_index(drop=True)

    receita_ativ_sec = pd.concat([ativ_sec_credores,
                                  ativ_sec_doadores,
                                  ativ_sec_fornecedores], sort=True).reset_index(drop=True)

    # receita_cnpj = receita_cnpj.drop(columns='extra')

    receita_cnpj = beautifier_cols(receita_cnpj)
    receita_qsa = beautifier_cols(receita_qsa)
    receita_ativ_sec = beautifier_cols(receita_ativ_sec)
    return receita_cnpj, receita_qsa, receita_ativ_sec


# CREDORES


def credores():
    # 2016
    path = r'./raw_data/cred_2016/'
    files = glob.glob(path + "credores_2016_*.csv")
    credores_list = []
    for filename in files:
        df = pd.read_csv(filename, index_col=None, header=0)
        df = df.rename(columns={'Valor Em LiquidaÃ§Ã£o': 'Valor Em Liquidação'})
        credores_list.append(df)
    cred16 = pd.concat(credores_list, axis=0, ignore_index=True, sort=True).reset_index(drop=True)
    cred16 = cred16.drop(cred16.filter(like=r'Unnamed').columns, axis=1)
    cred16 = cred16.iloc[cred16['Nome'].str.normalize('NFKD').argsort()]  # sort columns containing special chars

    # 2018
    path = r'./raw_data/cred_2018/'
    files = glob.glob(path + "credores_2018_*.csv")
    credores_list = []
    for filename in files:
        df = pd.read_csv(filename, index_col=None, header=0)
        df = df.rename(columns={'Valor Em LiquidaÃ§Ã£o': 'Valor Em Liquidação'})
        credores_list.append(df)
    cred18 = pd.concat(credores_list, axis=0, ignore_index=True, sort=True).reset_index(drop=True)
    cred18 = cred18.drop(cred18.filter(like=r'Unnamed').columns, axis=1)
    cred18 = cred18.iloc[cred18['Nome'].str.normalize('NFKD').argsort()]  # sort columns containing special chars

    creds = pd.concat([pd.read_csv('raw_data/credores_2015.csv', sep="\t"),
                       cred16,
                       pd.read_csv('./raw_data/credores_2017.csv'),
                       cred18,
                       pd.read_csv('./raw_data/credores_2019.csv', sep="\t")], sort=True).drop_duplicates()
    creds = creds[['Nome', 'CNPJ/CPF', 'Valor Empenhado', 'Valor Em Liquidação',
                   'Valor Liquidado', 'Valor Pago', 'Valor Anulado', 'ano']]
    creds = beautifier_cols(creds)
    creds['nome'] = [i.strip() for i in creds.nome]
    creds['nome'] = [unidecode.unidecode(str(i)) for i in creds.nome]

    creds = creds.iloc[creds['nome'].str.normalize('NFKD').argsort()]  # sort columns containing special chars
    creds = creds.sort_values(['ano', 'nome']).sort_index()

    creds['nome'] = [unidecode.unidecode(str(i)) for i in creds.nome]

    creds = replace_names(creds)

    return creds


def credores_liquida():
    cred_liq = ['credores_liquidacoes_2015.csv',
                'credores_liquidacoes_2016.csv',
                'credores_liquidacoes_2017.csv',
                'credores_liquidacoes_2018.csv',
                'credores_liquidacoes_2019.csv']
    credores_liquid = pd.DataFrame()
    for i in cred_liq:
        file = './raw_data/' + str(i)
        df = pd.read_csv(file, sep='\t')
        df['ano'] = i.split('.')[0][-4:]
        credores_liquid = credores_liquid.append(df).drop_duplicates()

    credores_liquid = credores_liquid[~credores_liquid['Data da Liquidação'].str.contains("Data da")]
    credores_liquid = credores_liquid[['Data da Liquidação', 'Número de Liquidação', 'Complemento Histórico',
                                       'Valor Liquidado', 'Valor Estornado', 'credor', 'empenho', 'ano']]
    credores_liquid['empenho'] = credores_liquid['empenho'].astype(float)
    credores_liquid = beautifier_cols(credores_liquid)

    credores_liquid['credor'] = [unicodedata.normalize("NFKD", str(i)) for i in credores_liquid.credor]
    credores_liquid['credor'] = [unidecode.unidecode(str(i)) for i in credores_liquid.credor]

    credores_liquid = replace_names(credores_liquid)

    return credores_liquid


def credores_pagtos():
    cred_pagtos = ['credores_pagamentos_2015.csv',
                   'credores_pagamentos_2016.csv',
                   'credores_pagamentos_2017.csv',
                   'credores_pagamentos_2018.csv',
                   'credores_pagamentos_2019.csv']
    credores_pagamentos = pd.DataFrame()
    for i in cred_pagtos:
        file = './raw_data/' + str(i)
        df = pd.read_csv(file, sep='\t')
        df['ano'] = i.split('.')[0][-4:]
        credores_pagamentos = credores_pagamentos.append(df).drop_duplicates()

    credores_pagamentos = credores_pagamentos[
        ~credores_pagamentos['Data do Pagamento'].str.contains("Data do Pagamento")]
    credores_pagamentos = credores_pagamentos[['Data do Pagamento', 'Número do Pagamento', 'Número de liquidação',
                                               'Complemento Histórico', 'Valor Pago', 'Valor Estornado', 'credor',
                                               'empenho', 'ano']]
    credores_pagamentos = beautifier_cols(credores_pagamentos)

    credores_pagamentos['credor'] = [unicodedata.normalize("NFKD", str(i)) for i in credores_pagamentos.credor]
    credores_pagamentos['credor'] = [unidecode.unidecode(str(i)) for i in credores_pagamentos.credor]

    credores_pagamentos = replace_names(credores_pagamentos)

    return credores_pagamentos


# DETALHES EMPENHOS
def detalhes_empenhos(df_credores):
    det_emp = ['detalhes_emp_2015_new.csv',
               'detalhes_emp_2016_new.csv',
               'detalhes_emp_2017_new.csv',
               'detalhes_emp_2018_new.csv',
               'detalhes_emp_2019_new.csv']

    detalhes_emp_list = []
    for i in det_emp:
        file = './raw_data/' + str(i)
        df = pd.read_csv(file, dtype='unicode')
        df.columns = [unidecode.unidecode(str(i)) for i in df.columns]
        df['ano_referencia'] = i.split('_')[2]
        df = df.iloc[df['Credor'].str.normalize('NFKD').argsort()]  # sort columns containing special chars
        detalhes_emp_list.append(df)

    detalhes_emp = pd.concat(detalhes_emp_list, sort=True).drop_duplicates()

    detalhes_emp = detalhes_emp.sort_index(axis=1)
    detalhes_emp = detalhes_emp.loc[:, 'Ação de Governo':]
    detalhes_emp = detalhes_emp.loc[:, ~detalhes_emp.columns.duplicated()]

    detalhes_emp = beautifier_cols(detalhes_emp)
    detalhes_emp['credor'] = [i.strip() for i in detalhes_emp.credor]

    detalhes_emp = replace_names(detalhes_emp)
    detalhes_emp['credor'] = [ud.normalize("NFKD", str(i)) for i in detalhes_emp.credor]
    detalhes_emp['credor'] = [unidecode.unidecode(str(i)) for i in detalhes_emp.credor]
    detalhes_emp = replace_names(detalhes_emp)

    detalhes_emp['credor_temp'] = detalhes_emp['credor'].apply(lambda x: x.replace(" ", ""))

    df_credores['nome'] = [ud.normalize("NFKD", str(i)) for i in df_credores.nome]
    df_credores['nome'] = [unidecode.unidecode(str(i)) for i in df_credores.nome]
    df_credores['nome_temp'] = df_credores['nome'].apply(lambda x: x.replace(" ", ""))

    detalhes_emp.columns = [unidecode.unidecode(str(i)) for i in detalhes_emp.columns]
    df_credores.columns = [unidecode.unidecode(str(i)) for i in df_credores.columns]

    detalhes_emp = pd.merge(detalhes_emp, df_credores[['nome_temp', 'cnpj/cpf']],
                            left_on=['credor_temp', 'cpf/cnpj'],
                            right_on=['nome_temp', 'cnpj/cpf'],
                            how='inner').drop_duplicates()

    detalhes_emp['ugest'] = np.where((detalhes_emp.unidade_gestora.isna()), detalhes_emp.unidade_gestora_x,
                                     detalhes_emp.unidade_gestora)
    detalhes_emp = detalhes_emp[['data_emissao_empenho', 'numero_empenho', 'ugest', 'credor',
                                 'cnpj/cpf', 'valor_empenhado', 'valor_em_liquidacao', 'valor_liquidado',
                                 'valor_pago', 'valor_anulado', 'atualizado_em', 'periodo',
                                 'tipo_empenho', 'categoria', 'orgao', 'unidade', 'funcao', 'subfuncao',
                                 'programa_de_governo', 'esfera', 'ie',
                                 'categoria_economica', 'grupo_da_despesa', 'modalidade_de_aplicacao',
                                 'natureza_da_despesa', 'desdobramento_da_despesa', 'fonte_de_recursos',
                                 'detalhamento_da_fonte', 'licitacao', 'numero_da_licitacao',
                                 'data_de_homologacao', 'processo_da_compra', 'processo_administrativo', 'contrato',
                                 'convenio', 'empenhado', 'em_liquidacao', 'liquidado',
                                 'pago', 'anulado', 'ano_referencia']]

    detalhes_emp = detalhes_emp.rename(columns={'ugest': 'unidade_gestora'})

    detalhes_emp = detalhes_emp.reset_index(drop=True)

    detalhes_emp['numero_empenho'] = detalhes_emp['numero_empenho'].fillna(0).astype(float)
    detalhes_emp = detalhes_emp[detalhes_emp['numero_empenho'] != 0]

    detalhes_emp['credor'] = detalhes_emp['credor'].apply(lambda x: ud.normalize('NFKD', x))
    detalhes_emp = detalhes_emp.sort_values(['ano_referencia', 'credor']).drop_duplicates().reset_index(drop=True)

    d_emp = pd.to_datetime(detalhes_emp['data_emissao_empenho'], format='%d/%m/%Y')
    d_hom = pd.to_datetime(detalhes_emp['data_de_homologacao'], format='%d/%m/%Y')

    detalhes_emp['tempo_entre_homologacao_empenho'] = (d_emp - d_hom) / np.timedelta64(1, 'D')

    detalhes_emp['credor'] = [unidecode.unidecode(str(i)) for i in detalhes_emp.credor]

    detalhes_emp = replace_names(detalhes_emp)

    return detalhes_emp


# BENS PREFEITOS E VEREADORES
def bens():
    df_bens = pd.read_excel('./fontes_db/bens prefeito e veradores.xlsx')
    return df_bens


# CONTRATOS
def dados_contratos():
    df_contratos_nomes = pd.read_csv('./raw_data/contratos_nomes.csv')
    df_contratos_nomes['Nome'] = df_contratos_nomes['Nome'].fillna('-').apply(lambda x: x.strip())
    df_contratos_nomes = beautifier_cols(df_contratos_nomes).sort_values(['nome', 'contrato']).reset_index(drop=True)
    df_contratos_nomes['contrato'] = df_contratos_nomes.contrato.apply(lambda x: int(x))
    df_contratos_nomes['tipo'] = 'PF'

    df_contratos_empresas = pd.read_csv('./raw_data/contratos_empresas.csv')
    df_contratos_empresas['Nome'] = df_contratos_empresas['Nome'].fillna('-').apply(lambda x: x.strip())
    df_contratos_empresas = beautifier_cols(df_contratos_empresas).sort_values(['nome', 'contrato']).reset_index(
        drop=True)
    df_contratos_empresas['contrato'] = df_contratos_empresas.contrato.apply(lambda x: int(x))
    df_contratos_empresas['tipo'] = 'PJ'

    df_contratos = pd.concat([df_contratos_nomes,
                              df_contratos_empresas], sort=True)
    df_contratos = df_contratos[['nome', 'cpf/cnpj', 'antes_depois', 'contrato', 'tipo']].fillna('-')
    df_contratos = df_contratos.sort_values(['contrato', 'antes_depois'])
    return df_contratos


def tempos_consolidados(detalhes_emp, credores_liquidacoes, credores_pagamentos):
    """
    merge tables to calculate time deltas. Return a full data frame including all columns of merged dataframes

    select liq."data_da_liquidação", emp."data_emissão_empenho", emp."data_de_homologação", pag."data_do_pagamento"
    from credores_liquidacoes liq
    inner join detalhes_emp emp on liq."empenho" = emp."número_do_empenho"
    inner join detalhes_emp emp on lower(liq."credor") = lower(emp."credor")
    inner join credores_pagamentos pag on lower(liq."credor") = lower(pag."credor")
    inner join credores_pagamentos pag on liq."empenho" = pag."empenho"
    inner join credores_pagamentos pag on liq."número_de_liquidação" = pag."número_de_liquidação"


    /* tempo entre homologacao e empenho */
    emp."data_emissão_empenho" - emp."data_de_homologação"

    /* tempo entre empenho e liquidacao */
    liq."data_da_liquidação" - emp."data_emissão_empenho"

    /* tempo entre liquidacao e pagamento*/
    pag."data_do_pagamento" - liq."data_da_liquidação"

    /* tempo total */
    pag."data_do_pagamento" - liq."data_da_liquidação" - emp."data_emissão_empenho" - emp."data_de_homologação"
    """
    detalhes_emp = detalhes_emp.rename(columns={'numero_empenho': 'empenho', 'ano_referencia': 'ano'})
    credores_pagamentos['empenho'] = credores_pagamentos.empenho.astype(float)

    first_join = [credores_liquidacoes, credores_pagamentos]
    df = reduce(lambda x, y: pd.merge(x, y, on=['empenho', 'credor', 'número_de_liquidação', 'ano']), first_join)
    df_final = pd.merge(detalhes_emp, df, on=['empenho', 'credor', 'ano'])

    df_dates = df_final[['data_da_liquidação', 'data_emissao_empenho', 'data_de_homologacao', 'data_do_pagamento']]

    for i in df_dates:
        df_dates = df_dates.copy()
        df_dates[i] = pd.to_datetime(df_dates[i], format='%d/%m/%Y')

    tempo_entre_homologacao_empenho = (df_dates['data_emissao_empenho'] - df_dates[
        'data_de_homologacao']) / np.timedelta64(1, 'D')

    tempo_entre_empenho_liquidacao = (df_dates['data_da_liquidação'] - df_dates[
        'data_emissao_empenho']) / np.timedelta64(1, 'D')

    tempo_entre_liquidacao_pagamento = (df_dates['data_do_pagamento'] - df_dates[
        'data_da_liquidação']) / np.timedelta64(1, 'D')

    tempo_entre_empenho_pagamento = (df_dates['data_do_pagamento'] - df_dates['data_emissao_empenho']) / np.timedelta64(
        1, 'D')

    tempo_entre_homologacao_pagamento = (df_dates['data_do_pagamento'] - df_dates[
        'data_de_homologacao']) / np.timedelta64(1, 'D')

    df_final['tempo_entre_empenho_liquidacao'] = tempo_entre_empenho_liquidacao
    df_final['tempo_entre_homologacao_empenho'] = tempo_entre_homologacao_empenho
    df_final['tempo_entre_liquidacao_pagamento'] = tempo_entre_liquidacao_pagamento
    df_final['tempo_entre_empenho_pagamento'] = tempo_entre_empenho_pagamento  # antigo tempo_total2
    df_final['tempo_entre_homologacao_pagamento'] = tempo_entre_homologacao_pagamento  # antigo tempo_total

    df_liq_pagto_emp = df_final.copy()
    return df_liq_pagto_emp


def replace_names(df):
    df = df.replace(
        ["UNIMED MACAE COOP. DE TRABALHO MEDICO", "SAME-SERVIA++O DE ATUAA++AO EM MEDICINA DE EMERG. LTDA",
         "RAV COMA%0RCIO SERVIA++OS E LOCAA++A*ES LTDA-ME", "POSTO TIC TAC DE MACAA%0 LTDA",
         "P. R. VIANA JUNIOR ART'S GRAFICAS", "NUCLEO DE MEDICINA DIAGNOSTICA DE MACAA%0 LTDA",
         "NEWEASY SOLUA++A*ES EM TECNOLOGIA LTDA", "MAILLET SINALIZACAO LTDA"],
        ["UNIMED DE MACAE COOPERATIVA DE ASSISTENCIA A SAUDE", "SAME - SERVIÇOS DE ATUAÇÃO EM MEDICINA",
         "RAV COMÉRCIO SERVIÇOS E LOCAÇÕES LTDA-ME", "POSTO TIC TAC DE MACAE LTDA", "P R VIANA JUNIOR ARTS GRAFICAS",
         "NUCLEO DE MEDICINA DIAGNOSTICA DE MACAÉ LTDA", "NEWEASY SOLUCOES EM TECNOLOGIA LTDA",
         "MAILLET SINALIZAÇÃO E PAPELARIA LTDA"])

    df = df.replace(
        ["TORNADO-VIGILANCIA E CONSERVAÇAO LTDA", "TOMOGRAFIA MACAE LTDA - CEDI", "TAECO MATERIAIS DE CONSTRUÇAO LTDA",
         "T K S SERVICE LTDA", "SUCBRAS VEND. DE EQUIP. DE SEG. E SERVIÇOS LTDA",
         "SAME-SERVICO DE ATUACAO EM MEDICINA DE EMERG. LTDA", "SAME SERVICOS ATUACAO EM MEDICINA DE EMERGENCIA",
         "SAME - SERVIÇOS DE ATUAÇÃO EM MEDICINA", "RAV COMÉRCIO SERVIÇOS E LOCAÇÕES LTDA-ME",
         "POSTO CANCELA SERVIÇOS E COMERCIO LTDA", "P R Viana junior Arts Graficas",
         "NUCLEO DE INFORMAÇÃO E COORDENAÇÃO DO PONTO BR", "NUCLEO DE DANCA PORTADORES DE ALEGRIA",
         "MOREIRA ARANTES CORRETORA DE SEGUROS LTDA", "MOREIRA ARANTES CORRETORA SEGUROS LTDA",
         "MEDGROUP OFFSHORE DIST. DE MED. E PROD. FARMA", "MAILLET SINALIZAÇÃO E PAPELARIA LTDA",
         "L. N. CARVALHO COMERCIO E SERVIÇOS LTDA -ME", "L. ALVES VIDRAÇARIA LTDA",
         "J L EMPREENDIMENTOS COMERCIAIS EIRELI", "IRMAOS PRATA CONSTRUCAO E CONSERVACAO LTDA-ME",
         "IRMAOS PRATA CONSTRUÇÃO E CONSERVAÇÃO LTDA-ME", "GRAFICA LITORAL DE MACAE LTDA - ME", "G.T. NAUTICA LTDA",
         "FRANCA & MARINS LTDA", "FRANÇA E MARINS LTDA", "FLASH PRINT ARTES GRAFICAS LTDA.",
         "FLASH PRINT ARTES GRAFICAS LTDA ME", "FERRAGENS MAG DE MACAE LTDA EPP", "FERRAGENS MAG DE MACAE LTDA - EPP",
         "ELEMIO SERVIÇOS LTDA", "EJORAN-ED.DE JORNAIS, REV.E AG.DE NOTICIAS",
         "EJORAN EDITORA DE JORNAIS,REV. E AG. DE NOTICIAS L", "EJORAN EDITORA DE JORNAIS REVISTAS E AGENCIA DE NO",
         "EJORAN EDITORA DE JORNAIS E REV E AG DE NOTICIAS", "EJORAN EDIT.DE JORNAIS,REV. E AG.NOT.",
         "EJORAN EDIT. JORNAIS, REVISTAS E AG. NOTICIAS LTDA", "EJORAN EDIT. DE JORN. REVISTAS E AGENC.DE NOTICIAS",
         "EJORAN - ED DE JORNAIS, REVISTAS E AGENCIA DE NOTI", "E. SOUZA & FILHO MATERIAIS DE CONSTRUCAO LTDA",
         "E. SOUZA & FILHO MATERIAIS DE CONSTRUÇAO LTDA", "E. L. MIDIA EDITORA LTDA/DIARIO DA COSTA DO SOL",
         "DISTRIPAPER DISTRIB. DE MATERIAL P/ ESCRITORIO LTD", "DISTRIPAPER DIST. DE MAT. P/ ESCRITORIO LTDA",
         "COMACHARQUE COM. DE MAQUINAS E EQUIP. LTDA EPP", "COMACHARQUE COM. DE MÁQUINAS E EQUIP. LTDA EPP",
         "CELEM & CIA LTDA", "CELEM & CIA LTDA - ME", "CASA BELLA DE MACAE MATERIAL DE CONSTRUÇÃO LTDA-EP",
         "CARMELO COMERCIO E SERVICOS LTDA-ME", "CARMELO COMERCIO E SERVIÇOS LTDA-ME", "CARDIM & CARDIM LTDA - ME",
         "CARDIM & CARDIM LTDA ME", "AUTOLAGOS COM. DE PECAS LTDA", "AUTOLAGOS COMERCIO DE PECAS LTDA - ME",
         "AUTOLAGOS COMERCIO DE PEÇAS LTDA - ME",
         "ASSOCIAÇÃO PAIS E AMIGOS DOS JUDOCAS", "ARLEY AMARAL DE CARVALHO (NAO USAR) USAR 418",
         "ALCYR ALVES FERREIRA & CIA LTDA", "AHAVAT COMERCIO E SERVICOS LTDA - ME",
         "AHAVAT COMERCIO E SERVICOS LTDA -ME", "AHAVAT COMERCIO E SERVICOS LTDA ME",
         "AHAVAT COMERCIO E SERVICOS LTDA-ME", "IRMANDADE DE SAO JOAO BATISTA MACAE",
         "IRMANDADE SAO JOAO BATISTA DE MACAE",
         "MOREIRA ARANTES CORRETORA SEGUROS LTDA", "MOREIRA ARANTES CORRETORA DE SEGUROS LTDA",
         "Nucleo de Informecao e Coordenacao do Ponto BR", "TAECO MATERIAIS DE CONSTRUÇAO LTDA",
         "CANAA DE CARMO DISTRIB. DE PROD. ALIMENTICIOS LTDA", "CELEM E CIA LTDA",
         "DISTRIPAPER DISTRIBUIDORA DE MAT.P/ESCRITORIO LTDA", "L. ALVES VIDRACARIA LTDA",
         "R A V COMERCIO SERVICOS & LOCACOES LTDA"],
        ["TORNADO-VIGILANCIA E CONSERVACAO LTDA", "TOMOGRAFIA MACAE LTDA", "TAECO MATERIAIS DE CONSTRUCAO LTDA.",
         "T.K.S.SERVICE LTDA", "SUCBRASIL COM. EXTINTORES DE INCENDIO E SERV MARIT",
         "SAME - SERVICOS DE ATUACAO EM MEDICINA", "SAME - SERVICOS DE ATUACAO EM MEDICINA",
         "SAME - SERVICOS DE ATUACAO EM MEDICINA", "RAV COMERCIO SERVICOS E LOCACOES LTDA-ME",
         "POSTO CANCELA SERVICOS E COMERCIO LTDA", "P R VIANA JUNIOR ARTS GRAFICAS",
         "NUCLEO DE INFORMACAO E COORDENACAO DO PONTO BR", "NUCLEO DE DANCA PORTADORES DA ALEGRIA",
         "MOREIRA ARANTES CORRETORA DE SEGUROS", "MOREIRA ARANTES CORRETORA DE SEGUROS",
         "MEDGROUP OFFSHORE DIST.MED.E PROD.FARMACEUTICOS LT", "MAILLET SINALIZACAO E PAPELARIA LTDA",
         "L. N. CARVALHO COMERCIO E SERVICOS LTDA -ME", "L ALVES VIDRACARIA LTDA-ME",
         "J L EMPREENDIMENTOS COMERCIAIS EIRELI ME", "IRMAOS PRATA COM. SERV. DE CONSERV. LTDA",
         "IRMAOS PRATA COM. SERV. DE CONSERV. LTDA", "GRAFICA E PAPELARIA LITORAL DE MACAE LTDA",
         "G. T. NAUTICA LTDA",
         "FRANCA E MARINS LTDA", "FRANCA E MARINS LTDA", "FLASH PRINT ARTES GRAFICAS LTDA - ME",
         "FLASH PRINT ARTES GRAFICAS LTDA - ME", "FERRAGENS MAG DE MACAE LTDA", "FERRAGENS MAG DE MACAE LTDA",
         "ELEMIO SERVICOS LTDA", "EJORAN ED.JORNAIS REVISTAS AG NOTICIA", "EJORAN ED.JORNAIS REVISTAS AG NOTICIA",
         "EJORAN ED.JORNAIS REVISTAS AG NOTICIA", "EJORAN ED.JORNAIS REVISTAS AG NOTICIA",
         "EJORAN ED.JORNAIS REVISTAS AG NOTICIA", "EJORAN ED.JORNAIS REVISTAS AG NOTICIA",
         "EJORAN ED.JORNAIS REVISTAS AG NOTICIA", "EJORAN ED.JORNAIS REVISTAS AG NOTICIA",
         "E. SOUZA E FILHOS MATERIAIS DE CONSTRUCAO LTDA", "E. SOUZA E FILHOS MATERIAIS DE CONSTRUCAO LTDA",
         "E. L. MIDIA EDITORA LTDA", "DISTRIPAPER DISTRIB DE MATERIAL PARA ESCRITORIO LT",
         "DISTRIPAPER DISTRIB DE MATERIAL PARA ESCRITORIO LT", "COMACHARQUE MAQUINAS E EQUIP.PARA ALIMENTACAO",
         "COMACHARQUE MAQUINAS E EQUIP.PARA ALIMENTACAO", "CELEM CIA LTDA", "CELEM CIA LTDA",
         "CASA BELLA DE MACAE MATERIAL DE CONSTRUCAO LTDA-EP", "CARMELO COMERCIO E SERVICOS LTDA ME",
         "CARMELO COMERCIO E SERVICOS LTDA ME", "CARDIM E CARDIM LTDA ME", "CARDIM E CARDIM LTDA ME",
         "AUTOLAGOS COMERCIO DE PECAS", "AUTOLAGOS COMERCIO DE PECAS", "AUTOLAGOS COMERCIO DE PECAS",
         "ASSOCIACAO PAIS E AMIGOS DOS JUDOCAS",
         "ARLEY AMARAL DE CARVALHO", "ALCYR ALVES FERREIRA E CIA LTDA", "AHAVAT COMERCIO E SERVICOS LTDA - ME",
         "AHAVAT COMERCIO E SERVICOS LTDA - ME", "AHAVAT COMERCIO E SERVICOS LTDA - ME",
         "AHAVAT COMERCIO E SERVICOS LTDA - ME",
         "IRMANDADE SAO JOAO BATISTA DE MACAE", "IRMANDADE SAO JOAO BATISTA DE MACAE",
         "MOREIRA ARANTES CORRETORA DE SEGUROS",
         "MOREIRA ARANTES CORRETORA DE SEGUROS", "NUCLEO DE INFORMACAO E COORDENACAO DO PONTO BR",
         "TAECO MATERIAIS DE CONSTRUCAO LTDA.",
         "CANAA DE CARMO DISTRIBUIDORA LTDA ME", "CELEM CIA LTDA", "DISTRIPAPER DISTRIB DE MATERIAL PARA ESCRITORIO LT",
         "L ALVES VIDRACARIA LTDA-ME", "RAV COMERCIO SERVICOS E LOCACOES LTDA-ME"])
    return df


def main1():
    df1 = pref()
    df1.to_sql('prefeito_vp_secretarios', con=conn, if_exists='replace', index=False)

    df_2_dir = vereadores_dir()
    df_2_dir.to_sql('vereadores_mesa_diretora', con=conn, if_exists='replace', index=False)

    df_2_com = vereadores_com()
    df_2_com.to_sql('vereadores_comissao', con=conn, if_exists='replace', index=False)

    df_doadores = doadores()
    df_doadores.to_sql('doadores', con=conn, if_exists='replace', index=False)

    df_fornecedores = fornecedores()
    df_fornecedores.to_sql('fornecedores', con=conn, if_exists='replace', index=False)

    df_serv_camara = servidores_camara()
    df_serv_camara.to_sql('servidores_camara', con=conn, if_exists='replace', index=False)

    df_serv_pref = servidores_pref()
    df_serv_pref.to_sql('servidores_pref', con=conn, if_exists='replace', index=False)

    df_filiacao = filiacao()
    df_filiacao.to_sql('filiacao_partidaria', con=conn, if_exists='replace', index=False)

    receita_cnpj, receita_qsa, receita_ativ_sec = dados_receita()
    receita_cnpj.to_sql('receita_CNPJ', con=conn, if_exists='replace', index=False)
    receita_qsa.to_sql('receita_QSA', con=conn, if_exists='replace', index=False)
    receita_ativ_sec.to_sql('receita_ATIV_SEC', con=conn, if_exists='replace', index=False)

    df_credores = credores()
    df_credores.to_sql('credores', con=conn, if_exists='replace', index=False)

    credores_liquidacoes = credores_liquida()
    credores_liquidacoes.to_sql('credores_liquidacoes', con=conn, if_exists='replace', index=False)

    credores_pagamentos = credores_pagtos()
    credores_pagamentos.to_sql('credores_pagamentos', con=conn, if_exists='replace', index=False)

    detalhes_emp = detalhes_empenhos(df_credores)
    detalhes_emp.to_sql('detalhes_emp', con=conn, if_exists='replace', index=False)

    df_bens = bens()
    df_bens.to_sql('bens', con=conn, if_exists='replace', index=False)

    df_contratos = dados_contratos()
    df_contratos.to_sql('contratos', con=conn, if_exists='replace', index=False)

    return


def main2():
    xlsx = pd.ExcelFile('./fontes_db/Tabela_Partes_Relacionadas.xlsx')

    partes_list = []
    d = {}
    for sheet in xlsx.sheet_names:
        d[f'{sheet}'] = pd.read_excel(xlsx, sheet_name=sheet)

    for df_name in d.keys():
        df = d[df_name]
        df = beautifier_cols(df)
        if df_name == 'credores_doadores_pf':
            df = df.rename(columns={'ano': 'ano_eleicao'})
        elif df_name in ['credores_doadres_direto', 'credores_fornecedores_direto']:
            df = df.rename(columns={'ano2': 'ano_eleicao'})
        elif df_name in ['credores_doadores_pj', 'credores_fornecedores_pf', 'credores_fornedores_pj']:
            df = df.rename(columns={'ano3': 'ano_eleicao'})

        for i in df:
            if i == "nome":
                df['nome'] = [unidecode.unidecode(str(i)) for i in df.nome]
            elif i == "nome_do_político":
                df['nome_do_político'] = [unidecode.unidecode(str(i)) for i in df['nome_do_político']]

        df.columns = [unidecode.unidecode(str(i)) for i in df.columns]
        df = beautifier_cols(df)
        partes_list.append(df)
        d[df_name] = df
        df.to_sql(df_name, con=conn2, if_exists='replace', index=False)

    # adding partes relacionadas flag in merged_times table
    part = pd.concat([beautifier_cols(d['credores_assessores_camara']),
                      beautifier_cols(d['credores_doadores_pf']),
                      beautifier_cols(d['credores_doadores_pj']),
                      beautifier_cols(d['credores_doadres_direto']),
                      beautifier_cols(d['credores_filiacao_direta']),
                      beautifier_cols(d['credores_filiacao_partidaria']),
                      beautifier_cols(d['credores_fornecedores_direto']),
                      beautifier_cols(d['credores_fornecedores_pf']),
                      beautifier_cols(d['credores_fornedores_pj']),
                      beautifier_cols(d['credores_secretarios']),
                      beautifier_cols(d['credores_fornedores_pj']),
                      beautifier_cols(d['credores_servidores_pref']),
                      beautifier_cols(d['credores_vereadores'])])[['nome']].drop_duplicates()

    part = replace_names(part)

    part['nome'] = [unidecode.unidecode(str(i)) for i in part.nome]

    part = replace_names(part)

    df_credores = credores()
    detalhes_emp = detalhes_empenhos(df_credores)
    credores_pagamentos = credores_pagtos()
    credores_liquidacoes = credores_liquida()
    df_liq_pagto_emp = tempos_consolidados(detalhes_emp, credores_liquidacoes, credores_pagamentos)  # merged times

    df = pd.merge(part['nome'], df_liq_pagto_emp, left_on='nome', right_on='credor', how='right')
    df['parte_relac'] = np.where(df.nome.isna(), 0, 1)

    df_liq_pagto_emp = df.drop(columns=['nome']).drop_duplicates().reset_index(drop=True)
    df_liq_pagto_emp.to_sql('merged_times', con=conn, if_exists='replace', index=False)

    credores_doadores_pf = d['credores_doadores_pf'][['nome', 'soma_de_percentual_de_doacao', 'ano_eleicao', 'eleicao']]
    credores_doadores_pj = d['credores_doadores_pj'][['nome', 'soma_de_percentual_de_doacao', 'ano_eleicao', 'eleicao']]
    credores_doadres_direto = d['credores_doadres_direto'][
        ['nome', 'soma_de_percentual_de_doacao', 'ano_eleicao', 'eleicao']]
    credores_doa = pd.concat([credores_doadores_pf, credores_doadores_pj, credores_doadres_direto]).drop_duplicates()

    credores_filiacao_direta = d['credores_filiacao_direta'][['nome', 'sigla_do_partido']]
    credores_filiacao_partidaria = d['credores_filiacao_partidaria'][['nome', 'sigla_do_partido']]
    credores_fil = pd.concat([credores_filiacao_direta, credores_filiacao_partidaria]).drop_duplicates()

    credores_fornecedores_direto = d['credores_fornecedores_direto'][
        ['nome', 'soma_de_percentual_de_despesas', 'ano_eleicao']]
    credores_fornecedores_pf = d['credores_fornecedores_pf'][['nome', 'soma_de_percentual_de_despesas', 'ano_eleicao']]
    credores_fornedores_pj = d['credores_fornedores_pj'][['nome', 'soma_de_percentual_de_despesas', 'ano_eleicao']]
    cred_forn = pd.concat(
        [credores_fornecedores_direto, credores_fornecedores_pf, credores_fornedores_pj]).drop_duplicates()

    credores_servidores_pref = d['credores_servidores_pref'][['nome', 'secretaria/_orgao']]

    credores_doa = credores_doa.rename(columns={'ano_eleicao': 'ano_eleicao_cred_doa'})
    df = pd.merge(df_liq_pagto_emp, credores_doa, left_on='credor', right_on='nome', how='left')
    df_liq_pagto_emp = df.drop(columns=['nome']).drop_duplicates().reset_index(drop=True)

    df = pd.merge(df_liq_pagto_emp, credores_fil, left_on='credor', right_on='nome', how='left')
    df_liq_pagto_emp = df.drop(columns=['nome']).drop_duplicates().reset_index(drop=True)

    cred_forn = cred_forn.rename(columns={'ano_eleicao': 'ano_eleicao_cred_forn'})
    df = pd.merge(df_liq_pagto_emp, cred_forn, left_on='credor', right_on='nome', how='left')
    df_liq_pagto_emp = df.drop(columns=['nome']).drop_duplicates().reset_index(drop=True)

    pd.merge(df_liq_pagto_emp, credores_servidores_pref, left_on='credor', right_on='nome', how='left')
    df_liq_pagto_emp = df.drop(columns=['nome']).drop_duplicates().reset_index(drop=True)

    df_liq_pagto_emp.to_sql('merged_times', con=conn, if_exists='replace', index=False)

    # generating merged_times_2

    cur = conn.cursor()
    query = str("""SELECT * FROM
    merged_times as mer

    WHERE
    mer.grupo_da_despesa in (
    "NULL", "3.3 - OUTRAS DESPESAS CORRENTES", "4.4 - INVESTIMENTOS", "4.5 - INVERSÕES FINANCEIRAS")
    AND
    mer.natureza_da_despesa
    NOT in ("3.3.90.01 - APOSENTADORIAS E REFORMAS", "3.3.90.01 - PROVENTOS - PESSOAL CIVIL - RPPS",
            "3.3.90.03 - PENSIONISTAS CIVIS - RPPS", "3.3.90.03 - PENSÕES",
            "3.3.90.33.10 - TAXA  SERV. EMISSAO BILHETES NAO UTILIZ.", "3.3.90.05 - OUTROS BENEFICIOS PREVIDENCIÁRIOS",
            "3.3.90.08 - OUTROS BENEFICIOS ASSISTENCIAIS DO SERVI",
            "3.3.90.08 - OUTROS BENEFÍCIOS ASSISTENCIAIS DO SERVIDOR OU DO MILITAR", "3.3.90.14 - DIARIAS - CIVIL",
            "3.3.90.14 - DIARIAS NO PAIS", "3.3.90.14 - DIÁRIAS - CIVIL",
            "3.3.90.14 - DIÁRIAS NO PAÍS", "3.3.90.18 - AUXILIO FINANCEIRO A ESTUDANTES",
            "3.3.90.18 - AUXÍLIO FINANCEIRO A ESTUDANTES", "3.3.90.18 - Bolsas Alunos Colég. Aplic. FUNEMAC",
            "3.3.90.20 - AUXÍLIO FINANCEIRO A PESQUISADORES",
            "3.3.90.31 - PREMIAÇÕES CLT., ART., C., DESP. E OUTRAS",
            "3.3.90.33.06 - PASSAGENS E LOCOMOCAO NA SUPERV.  VENDAS",
            "3.3.90.36.06 - SERVICOS TECNICOS PROFISSIONAIS", "3.3.90.36.44.01. - MULTAS", "3.3.90.36.44.01. - MULTAS",
            "3.3.90.39.36 - MULTAS INDEDUTIVEIS", "3.3.90.39.36 - MULTAS INDEDUTIVEIS",
            "3.3.90.46 - AUXILIO REFEIÇÃO", "3.3.90.46 - Auxilio-Alimentacao servidores",
            "3.3.90.46 - Auxilio-Alimentação", "3.3.90.47 - OBRIGACOES TRIBUTARIAS E CONTRIBUTIVAS",
            "3.3.90.47 - OBRIGAÇÕES TRIBUTÁRIAS E CONTRIBUTIVAS", "3.3.90.48 - AUXILIO A PESSOAS FISICAS",
            "3.3.90.48 - OUTROS AUXILIOS FINANCEIROS A PESSOAS FISICAS",
            "3.3.90.48 - OUTROS AUXÍLIOS FINANCEIROS A PESSOAS FÍSICAS", "3.3.90.91 -  SUCUMBENCIAIS DE PRECATORIOS",
            "3.3.90.91 - Precatorios Incluidos na LOA", "3.3.90.92 - DESPESAS DE EXERCICIOS ANTERIORES",
            "3.3.90.92 - DESPESAS DE EXERCÍCIOS ANTERIORES", "3.3.90.93 - INDENIZACOES E RESTITUICOES",
            "3.3.91.47 - OBRIGAÇÕES TRIBUTÁRIAS E CONTRIBUTIVAS", "4.4.90.92 - DESPESAS DE EXERCICIOS ANTERIORES",
            "4.4.90.92 - DESPESAS DE EXERCÍCIOS ANTERIORES", "4.5.90.92 - DESPESAS DE EXERCÍCIOS ANTERIORES",
            "4.4.90.93 - INDENIZACOES E RESTITUICOES", "4.5.90.61 - AQUISIÇÃO DE IMÓVEIS")

    AND
    desdobramento_da_despesa
    NOT in ("3.3.90.30.96 - MATERIAL DE CONSUMO - PAGTO ANTECIPADO", "3.3.90.33.08 - PEDAGIOS",
            "3.3.90.33.03 - LOCACAO DE MEIOS DE TRANSPORTE",
            "3.3.90.33.05 - LOCOMOCAO URBANA", "3.3.90.33.06 - PASSAGENS E LOCOMOCAO NA SUPERV. VENDAS",
            "3.3.90.33.09 - TRANSPORTE DE SERVIDORES", "3.3.90.36.28 - SERVICO DE SELECAO E TREINAMENTO",
            "3.3.90.36.35 - SERV. DE APOIO ADMIN., TECNICO E OPERACI",
            "3.3.90.36.45 - JETONS E GRATIFICACOES A CONSELHEIROS",
            "3.3.90.36.96 - OUTROS SERV. TERCEIROS PF. PAGT ANTECIPA",
            "3.3.90.39.25 - TAXA DE ADMINISTRACAO", "3.3.90.39.36 - MULTAS HONORARIOSINDEDUTIVEIS",
            "3.3.90.39.36 - MULTAS INDEDUTIVEIS", "3.3.90.39.37 - JUROS", "3.3.90.39.43 - SERVICOS DE ENERGIA ELETRICA",
            "3.3.90.39.81 - SERVICOS BANCARIOS", "3.3.90.39.02 - CONDOMINIOS", "3.3.90.39.03 - COMISSOES E CORRETAGENS",
            "3.3.90.39.25 - TAXA DE ADMINISTRACAO",
            "3.3.90.39.35 - MULTAS DEDUTIVEIS", "3.3.90.93.02 - RESTITUICOES", "3.3.90.39.36.01. - MULTAS",
            "3.3.90.39.39 - ENCARGOS FINANCEIROS INDEDUTIVEIS",
            "3.3.90.39.64 - SERV.DE PERICIA MEDICA/ODONTOLOG P/BENEF", "3.3.90.39.65 - SERVICOS DE APOIO AO ENSINO",
            "3.3.90.39.66 - SERVICOS JUDICIARIOS", "3.3.90.39.81 - SERVIÇOS BANCARIOS",
            "3.3.90.36.44.01. - MULTAS", "3.3.90.47.10 - TAXAS", "3.3.90.47.12 - CONTRIBUIÇÃO PARA O PIS/PASEP",
            "3.3.90.47.27 - MULTAS INDEDUTÍVEIS", "3.3.90.48.01.05. - AUX. FIN. ALUGUEL EMERGENCIA",
            "3.3.90.39.96 - OUTROS SERV.TERC. P.J.- PAGTO ANTECIPADO", "3.3.90.48.01.10. - AUX. FINANC. BOLSA ATLETA",
            "3.3.90.48.99 - Outros Auxilios Financeiros a P. Fisicas",
            "3.3.90.91.01 - Sent.Judic.Transit.em Julgado - Ano Corr",
            "3.3.90.91.03 - SENTENCAS JUDICIAIS DE PEQUENO VALOR",
            "3.3.90.91.06 - HONORARIOS SUCUMBENCIAIS DE PRECATORIOS",
            "3.3.90.92.81 - SERVICOS BANCARIOS", "3.3.90.92.93 - INDENIZACOES E RESTITUICOES",
            "3.3.90.92.93 - INDENIZACOES E RESTITUICOES", "3.3.90.92.14 - DIARIAS - CIVIL",
            "3.3.90.92.18 - AUXILIO FINANCEIRO A ESTUDANTES", "3.3.90.92.46 - AUXILIO-ALIMENTACAO",
            "3.3.90.92.47 - OBRIGACOES TRIBUTARIAS E CONTRIBUTIVAS", "3.3.90.92.50 - MULTAS E JUROS",
            "3.3.90.93.01 - INDENIZACOES", "4.4.90.52.91 - VARIACAO CAMBIAL NEGATIVA")

    --excluding municipality entities

    AND
    mer.credor
    NOT in ("A. DE A. ES. DO COL. MU. TARCISIO PAES DE FIGUEIRE", "AAE C.M. BOTAFOGO", "AAE C.M. ELZA IBRAHIM",
            "AAE CIEP - 371 - BARRA DE MACAE", "AAE CIEP 058 - OSCAR CORDEIRO",
            "AAE CIEP 454 - NOVA HOLANDA", "AAE CIEP MUNICIPALIZADO PROF. DARCY RIBEIRO",
            "AAE CM DR. CLAUDIO MOACYR DE AZEVEDO", "AAE COL. MUN. NEUZA GOULART BRIZOLA",
            "AAE COLEGIO ESTADUAL MUNICIPAL RAUL VEIGA", "AAE COLEGIO MUN. PROF. SAMUEL BRUST",
            "AAE COLEGIO MUNICIPAL JOAQUIM AUGUSTO BORGES", "AAE COLEGIO MUNICIPAL ZELITA ROCHA DE AZEVEDO",
            "AAE DO CIEP MARINGA", "AAE E. M. SOL Y MAR", "AAE E.M. CHRISTOS JEAN KOUSOULAS",
            "AAE E.M. MARIA ISABEL DAMASCENO", "AAE E.M. PROF. ANTONIO ALVAREZ PARADA",
            "AAE EM LEONEL DE MOURA BRIZOLA", "AAE EST. MUNIC. NOSSO SENHOR DOS PASSOS",
            "AAE EST. MUNICIPALIZADA CORREGO DO OURO", "AAE ESTADUAL MUN. CAROLINA C. BENJAMIN",
            "AAE ESTADUAL MUN. FAZENDA SANTA MARIA", "AAE ESTADUAL MUN. JACYRA TAVARES DURVAL",
            "AAE ESTADUAL MUNIC. CAETANO DIAS", "AAE ESTADUAL MUNICIPALIZADA CAETANO DIAS",
            "AAE ESTADUAL MUNICIPALIZADA COQUINHO", "AAE ESTADUAL MUNICIPALIZADA FANTINA DE MELO",
            "AAE ESTADUAL MUNICIPALIZADA IM", "AAE ESTADUAL MUNICIPALIZADA POLIVALENTE A. TEIXEIR",
            "AAE JARDIM DE INF. ANA BENEDICTA DA S. SANTOS", "AAE JARDIM DE INFANCIA VIRGEM SANTA",
            "AAE M. PRE ESCOLAR ALMIR F. LAPA", "AAE COLEGIO MUNICIPAL TARCISIO PAES DE FIGUEIREDO",
            "AAE M. PROFa LETICIA PECANHA DE AGUIAR", "AAE MARIA LETICIA DE CARVALHO", "AAE MEI AFONSO CORREA SABINO",
            "AAE MEI ANDRE VINICIUS DE SOUZA GONCALVES", "AAE MEI MARLENE DINIZ CALDAS",
            "AAE MEI PROFESSOR JOSE BRUNO DE AZEVEDO", "AAE MEI PROFESSORA HILDA RAMOS MACHADO",
            "AAE MEI PROFa CANDIDA MARIA DA SILVA VIEIRA", "AAE MEI THEREZINHA LOURENCO DA SILVA",
            "AAE MUN. MARIA CRISTINA CASTELLO BRANCO", "AAE MUN. PROFa. SANDRA MARIA O. A FRANCO",
            "AAE MUN. SONIA REGINA DE SOUZA LAPA DOS SANTOS", "AAE MUN. ZELIA DE SOUZA AGUIAR",
            "AAE MUNIC. JOAQUIM LUIZ FREIRE PINHEIRO-COD 10707", "AAE MUNICIPAL ALMIR FRANCISCO LAPA",
            "AAE MUNICIPAL AMIL TANOS", "AAE MUNICIPAL BALNEARIO LAGOMAR", "AAE MUNICIPAL DA AROEIRA",
            "AAE MUNICIPAL DE ALFABETIZACAO", "AAE MUNICIPAL DO SANA", "AAE MUNICIPAL DOLORES GARCIA RODRIGUES",
            "AAE MUNICIPAL ENGENHO DA PRAIA", "AAE MUNICIPAL ERALDO MUSSI",
            "AAE MUNICIPAL INTERAGIR", "AAE MUNICIPAL IVETE SANTANA DRUMOND DE AGUIAR",
            "AAE MUNICIPAL JARDIM DE INFANCIA A. GONCALVES", "AAE MUNICIPAL JOAQUIM BREVES",
            "AAE MUNICIPAL JOFFRE FROSSARD", "AAE MUNICIPAL JOSE CALIL FILHO", "AAE MUNICIPAL LIONS",
            "AAE MUNICIPAL MARIA LETICIA S. CARVALHO", "AAE MUNICIPAL OLGA BENARIO PRESTES",
            "AAE MUNICIPAL ONILDA MARIA DA COSTA", "AAE MUNICIPAL PARQUE AEROPORTO", "AAE MUNICIPAL PAULO FREIRE",
            "AAE MUNICIPAL PEDRO ADAMI", "AAE MUNICIPAL PROFESSOR ANTONI ALVARES PARADA",
            "AAE MUNICIPAL PROFESSORA EDA MOREIRA DAFLON", "AAE MUNICIPAL RENATO MARTINS",
            "AAE MUNICIPAL WOLFANGO FERREIRA", "AAE PARQUE MUN. PROF. MARIA ANGEL. RIB. BENJAMIN",
            "AAE PARQUE MUNICIPAL DA AROEIRA", "AAE TEC. MUN. NATALIO SALVADOR ANTUNES",
            "AAE. COL. DE APLIC. DA FUND. EDUC. DE MACAE", "AAEEMEI IRACY PINHEIRO MARQUES", "AAEM ATERRADO DO IMBURO",
            "AAEME PROFa ARLEA CARVALHO JOSE", "AAEMEI ALCINA MUZZY DE JESUS", "AAEMEI AMCORIN", "AAEMEI APRISCO",
            "AAEMEI ATTILA DE AGUIAR MALTEZ JUNIOR", "AAEMEI CLEIDE CANELA DE SOUZA",
            "AAE MEI PROFa CANDIDA MARIA DA SILVA VIERA", "AAEMEI DR. JUVENTINO DA SILVA PACHECO",
            "AAEMEI ELEA TATAGIBA DE AZEVEDO", "AAEMEI MAI CARMEN DE JESUS FRANCA",
            "AAEMEI MAI MARIA CECILIA TOURINHO FURTADO", "AAEMEI NOSSA SENHORA DA CONCEICAO",
            "AAEMEI OLIMPIA RIBEIRO DOS SANTOS MACHADO", "AAEMEI PROF. MARIA DE MARIS SARMENTO TORRES",
            "AAEMEI PROFESSOR EMILSON DE JESUS MACHADO", "AAEMEI PROFESSORA THEREZINHA CARVALHO MOREIRA",
            "AAEMEI PROFa ANA CRISTINA FERREIRA AZARANY ALMEIDA", "AAEMEI PROFa ANGELA MARIA FELIX PEREIRA",
            "AAEMEI PROFa ARLETE RIBEIRO JOSE", "AAEMEI PROFa CELITA REID FERNANDES",
            "AAEMEI PROFa ESMERIA PEREIRA REID DOS SANTOS", "AAEMEI PROFa GESIA DE OLIVEIRA - USAR COD 10658",
            "AAEMEI PROFa LAURA SUELI DE CAMPOS BACELAR", "AAEMEI PROFa LEDA MARIA LEDO ESTEVES",
            "AAEMEI PROFa LIA KOPP FRANCO (USA O COD. 10881)", "AAEMEI PROFa MARIA ANG. DE OLIVEIRA DAS DORES",
            "AAEMEI PROFa MARIA DA CONCEICAO CARVALHO", "AAEMEI PROFa MARIA DAS DORES SOUZA TAVARES",
            "AAEMEI PROFa MARIA DAS GRACAS DA SILVA RIBEIRO", "AAEMEI PROFa MARIA JOSE FERREIRA BARROS",
            "AAEMEI PROFa MARIA LIRA BERALDINI CAMPOS", "AAEMEI PROFa MARIA MAGDALA AGOSTINHO CIPRIANE",
            "AAEMEI PROFa MARLI VASCONCELOS LEMOS", "AAEMEI PROFa NEIVA MARIANO DOS SANTOS",
            "AAEMEI WANDERLEY QUINTINO TEIXEIRA", "CAMARA MUNICIPAL DE MACAE", "CONSORCIO PREF. MACAE PP 216/2013",
            "E. P. MONTEIRO")

    --excluding governmental entites

    AND
    mer.credor
    NOT in ("POLICIA MILITAR DO ESTADO DO RIO DE JANEIRO", "PODER JUDICIARIO",
            "TRIBUNAL DE JUSTICA DO ESTADO DO RIO DE JANEIRO", "PETROBRAS DISTRIBUIDORA S/A",
            "CEDAE-COMPANHIA EST. AGUAS E ESGOTOS", "EMPRESA BRAS.DE CORREIOS E TELEGRAFOS",
            "DETRAN/RJ - USAR COD 9109", "SEFAZ/RJ", "SECRETARIA DE ESTADO DE FAZENDA E PLANEJAMENTO",
            "CAIXA ECONOMICA FEDERAL S/A", "EMPRESA BRAS. CORREIOS E TELEGRAFOS", "DETRAN - RJ", "PR-IMPRENSA NACIONAL",
            "CONSORCIO PREF. MACAE PP 216/2013", "CONSOLIDACAO ORCAMENTARIA MACAEPREV",
            "CARTORIO DO 1o VARA CIVEL DA COMARCA DE MACAE/RJ", "AGENCIA NACIONAL DE TELECOMUNICACOES-ANATEL", "AMPLA",
            "AMPLA - ENERGIA E SERVICOS S/A",
            "AMPLA ENERGIA E SERVICOS LTDA", "AMPLA ENERGIA E SERVICOS S.A", "AMPLA ENERGIA E SERVICOS S.A.",
            "AMPLA ENERGIA E SERVICOS S/A", "ASSOC DAS ENT DA PREV DOS MUN DO ESTADO DO RJ",
            "ASSOC. BRAS. DE ENSINO E PESQUISA DE SERVICO SOCIA", "COMPANHIA DE ELETRECIDA DO RJ - AMPLA",
            "COMPANHIA ESTADUAL DE AGUA E ESGOTO - CEDAE", "CORPO DE BOMBEIROS DO ESTADO DO RIO DE JANEIRO",
            "Corpo de Bombeiros do Estado do Rio de Janeiro", "DEPARTAMENTO DE TRANSITO DO ESTADO DO R.J",
            "DETRAN - DEPARTAMENTO DE TRANSITO EST.RIO DE JANEI", "DETRAN - ESTADO DO RIO DE JANEIRO",
            "DETRAN-RJ", "EMPRESA BRASILEIRA DE CORREIOS E TELEGRAFOS - ECT",
            "FEDERACAO DE ATLETISMO DO ESTADO DO RIO DE JANEIRO", "FEDERACAO DE TENIS DE MESA DO EST DO RIO DE JANEIR",
            "FUND. EUC. DA C. DE A. INST. A UNIVER. F. FLUMINEN", "FUNDACAO DE DESENVOLVIMENTO DA UNICAMP - FUNCAMP",
            "FUNDO DE FISCALIZACAO DAS TELECOMUNICACOES", "FUNDO ESPECIAL DO CORPO DE BOMBEIROS - FUNESBOM",
            "Federacao de Teatro Associativo do estado do RJ", "GOVERNO DO E.DO RIO DE JANEIRO-FUNDACAO DER-RJ",
            "HOSPITAL CONFERENCIA SAO JOSE DO HAVAI", "HOSPITAL ESCOLA ALVARO ALVIM",
            "HOSPITAL OFTALMOLOGICO SANTA BEATRIZ", "IMPRENSA OFICIAL DO EST. DO RJ - USAR COD 6100",
            "INSS-INSTITUTO NACIONAL S. SOCIAL", "INST. NACIONAL DO SEGURO - INSS",
            "INSTITUTO ESTAUDAL DO AMBIENTE - INEA",
            "INSTITUTO NACIONAL DA SEGURIDADE SOCIAL - INSS", "INSTITUTO NACIONAL DE CONCURSO PUBLICO",
            "INSTITUTO NACIONAL DE SEG. SOCIAL", "INSTITUTO NACIONAL DO SEGURO SOCIAL",
            "INSTITUTO NACIONAL DO SEGURO SOCIAL - INSS", "INSTITUTO NACIONAL S SOCIAL - I.N.S.S",
            "MINISTERIO DA FAZENDA", "MINISTERIO DA PREVIDENCIA E ASSISTENCIA SOCIAL", "MJ - IMPRENSA NACIONAL",
            "NOVA IMPRENSA OFICIAL DO RIO DE JANEIRO", "RECEITA FEDERAL DO BRASIL - RFB", "RIO PREVIDENCIA",
            "SECRETARIA DA RECEITA FEDERAL", "SECRETARIA DE ESTADO DA DEF CIVIL - USAR COD 10229",
            "SECRETARIA DE ESTADO DE FAZENDA - SEFAZ", "SECRETARIA DE ESTADO DE FAZENDA-RJ",
            "SECRETARIA DE FAZENDA RJ SEFAZ", "SECRETRIA DE FAZENDA DO ESTADO DO RIO DE JANEIRO",
            "SECRETARIA DE ESTADO E FAZENDA-RJ",
            "SUPERINTENDENCIA REG. POL. RODOV. FED. NO RIO DE J", "UNIVERSIDADE FEDERAL FLUMINENSE",
            "IMPRENSA OFICIAL DO ESTADO DO RIO DE JANEIRO")

    --droping other employees expenses

    AND
    mer.credor
    NOT in ("ADILSON GUSMAO DOS SANTOS", "ADRIANA H. AZEVEDO E OUTROS", "ADRIANA MORAES PORTO MAT. 22065",
            "ADRIANA TAVARES PINTO e OUTROS", "ALAN VELASCO DA SILVA", "ALCIDES ABREU DA SILVA",
            "ALEX CRUZ DO NASCIMENTO RASMA", "ALFREDO JOSE DOS SANTOS FILHO", "ALFREDO JOSE GUIMARAES",
            "ALFREDO TANOS FILHO", "ALUCIMAR DAMES DE ANDRADE", "ANA PAULA MONTEIRO BARBOSA",
            "ANA CRISTINA BRAGA DE LUCA REIS", "ANA LUCIA DE CAMARGO BARROS", "ANA PAULA PREVITALI - MAT. 039.778",
            "ANDERSON MOREIRA VIEIRA", "ANDRE SILVA CABRAL", "ANDREIA BERNARDO PINHEIRO MAT 44126",
            "ANNY MAIA DE SOUZA", "ANTONIO CLAUDIO MARQUES E OUTROS", "ANTONIO OLINTO BORDALO",
            "ANTONIO SERGIO B. DA SILVA", "AUGUSTO ROMULO FAUAZ DE ANDRADE", "BIANCA DE SOUZA",
            "BRUNO DA SILVA CARVALHO CARNEIRO", "CAMILA DA CONCEICAO ROCHA DELFINO", "CARLA M. TAVARES SANCHO BRASIL",
            "CARLOS ALBERTO PINTO DA SILVA", "CARLOS EDUARDO ARAUJO FREIMAN",
            "CARLOS EDUARDO D'AVILA GARCIA ISAIAS", "CARLOS MAGNO F. ABREU MAT. 1701",
            "CARLOS MANUEL FIGUEIREDO MACARIO", "CARLOS MANUEL FIGUEIREDO MACARIO E OUTROS",
            "CARLOS MANUEL FIGUEIREDO MACARIO MAT 23554",
            "CATIA MARIA HERCULES DE MUROS", "CELSO DE OLIVEIRA FREIMAN", "CLEIDE SORAIA MONTEIRO RIBEIRO",
            "DEBORA MEDINA BARROSO LIMA", "DIEGO LEMGRUBER REZENDE",
            "DILMA ROUGE GODIM", "EDILSON AUGUSTO DA SILVA", "EDSON GUERHART FERNANDES",
            "EIGON ELRICK SARDINHA LEOCADIO", "ELIAS ALVES DA SILVA", "ELIZARDO GODIM DE OLIVEIRA",
            "EMERSON LUIZ GABRIELLI",
            "EMERSON LUIZ GABRIELLI", "ERENILDO MOTTA DA SILVA JUNIOR", "EVANDRO DA SILVA LAMEU MAT. 39127",
            "EZEQUIAS DE OLIVEIRA NUNES", "FABIANA DOS SANTOS DA ANUNCIACAO", "FABIO THOMAZ CARNEIRO",
            "FATIMA BARBOSA DE SOUZA", "FERNANDO DA SILVA MATOS", "GABRIEL CARVALHO PAIXAO EMERIK",
            "GABRIEL PEREIRA ABREU DOS SANTOS", "GIOVANNI LUCIANO HAAS", "HELANDRA MARCIA S. RISCADO E OUTROS",
            "HERICA NEVES AFONSO - Mat. 12.721", "HINSLENA ANTONIA BERTANHA DAS NEVES MONZATO",
            "IGOR DE MATOS HENRIQUE ASSIS", "IRAN ARAUJO BARRETO", " IRIS MARIA PIMENTEL SALLES MAT 4808",
            "JAIANA GOMES DA SILVA, MATR. 10695", "JAYME LOPES DO COUTO", "JONATHAN CASTICAL AZEVEDO", "JORGE CORREA",
            "JORGE LUIZ DA COSTA FRANCO E OUTROS", "JOSE DORLI KLEN", "JOSE JORGE LIMA GOMES",
            "JOSE RICARDO DE FREITAS CHIARETTI", "JOSELINO LEANDRO DE OLIVEIRA", "Jose Alfredo Resende de Jesus",
            "KELVIO GOMES SANTOS", "KENEDY MONTEIRO DE AZEVEDO", "LENISE MARIA BARRETO LIMA",
            "LIVIA MUSSI DE OLIVEIRA SANT'ANA", "LUCAS DA SILVA LIMA", "LUDMILA DE MATOS REIS FRANCO",
            "LUIS CLAUDIO DE LEMOS DAUT", "MADALENA DE OLIVEIRA RODRIGUES", "MAGNO ALVES FONSECA",
            "MAICON VIANA GOMES", "MARCELLE SANTOS TOME 11754807704", "MARCELLO MARTINS MAGALHAES",
            "MARCELO CHAVES DO NASCIMENTO", "MARCELO VIEIRA DAINEZ", "MARCIA ANDREIA GONCALVES DA SILVA CARVALHO",
            "MARCUS DA SILVA SOARES", "MARIA AUXILIADORA MOURA FERREIRA", "MARIA BERNARDETTE DE LOURDES G C SIMOES",
            "MARIANA GARRIDO GUIMARAES", "MARILIA CAVALCANTE RAMOS", "MARINA LATERCA MONTEIRO ALGEMIRO",
            "MARTINES PEREIRA AZEREDO", "MIRIAN CORREA RIBEIRO", "NABEL CRISTINA MACHADO RIBEIRO",
            "NEIVA DOS SANTOS MAT. 3834 - USAR COD 9846", "ORLANDO BENJAMIN DE AGUIAR", "OSVALDO LUIZ PORTUGAL",
            "OSWALDO BARROS TORRES MAT. 27410", "PAULO CESAR DA SILVA TEIXEIRA",
            "PAULO CESAR DA SILVA TEIXEIRA E OUTROS", "PAULO SERGIO ABREU DE CARVALHO", "PEDRO HENRIQUE BASTOS PINTO",
            "PATRIC ALVES DE VASCONCELLOS", "PEDRO PAULO PIRES CARVALHO", "RAFAEL BARCELOS COIMBRA",
            "RAFAEL GODIM DE OLIVEIRA", "RAIMUNDO PERCILIANO DE ARAUJO", "RAPHAEL GONCALVES GOUDARD",
            "RAQUEL DA SILVA MACIEL", " REGIS JATOBA DE SIQUEIRA", "RIZETE RIBEIRO DA SILVA MAT 400842",
            "ROBSON CHELLES IEKER - MAT. 0109", "ROBSON SILVA DE SOUSA", "RODOLFO LUIZ PINTO DA SILVA",
            "ROSANE DO NASCIMENTO GRACA", "ROSANE DO NASCIMENTO GRACA MAT 41646", "ROSANGELA TEIXEIRA PEDRA MAT 29428",
            "ROSE MARY GOMES", "SERGIO SANDRE GOMES", "SIDINEA CARLA COSTA", "TANIA BRAGANCA PAES",
            "TANISSE DA SILVA CANUTO", "TATIANA DA SILVA PEREIRA", "THIAGO CAMARGO ELIAS CARDOSO MAT.9575",
            "TULIO MARCO CASTRO BARRETO", "VILANIA FERREIRA TARDIN", "VITOR CHIARETTI FATURINI",
            "VIVIAN RAIMUNDO DA SILVA", "CAROLINA VERONEZI CAVALCANTE CARNEIRO", "HELIDA MARCIA DA COSTA MENDONCA",
            "ISABELLA FELIX VIANA", "RODRIGO DUARTE DE SOUZA",
            "JOSE EDUARDO DA SILVA GUINANCIO", "AILTON BRETAS DE ARAUJO ME",
            "ALCINO BRANDAO", "ALEXANDRE LUIZ PEREIRA", "ALUISIO DE SOUZA", "ANA PAULA DAL CIN TEIXEIRA",
            "CATIA MARIA HERCULES DE MUROS",
            "CLOVES FERREIRA MACHADO", "DEBORA CERTORIO MENDONCA", "EDUARDO LUIS MARTINS DE OLIVEIRA",
            "FELIPE CAMPOS ASSAD", "GLAUCO MIRANDA DE LACERDA", "JOCILENIO PEDRO DA CONCEICAO CAMILO",
            "JULIO CEZAR DE LIMA", "LILIAN PAULA CORREA LOPES", "LIVIA LOPES DA SILVA", "MARCIA FERRAZ AGOSTINHO",
            "MARCOS TULIO BENJAMIN PACHECO", "NALY SOARES DE ALMEIDA",
            "REGINALDO ALTIVO FERREIRA", "RIVIAN FERREIRA DE ANDRADE", "RODOLPHO ANTONIO DE OLIVEIRA JUNIOR",
            "ROMERO MANHAES DA SILVA", "RUTE TAVARES DA SILVA", "SILDO CASTRO JUNGER",
            "SERGIO LOPES DE SOUZA", "SUYLAN SODRE SATHLER", "VANESSA VASCONCELOS MENEZES")

    --droping beneficiaries

    AND
    mer.credor
    NOT in ("ADELINA DOS SANTOS", "ANA BEATRIZ MOUZER DA SILVA MACHADO", "JAMILIA APARECIDA GONCALVES",
            "ANDREIA SILVA DE ASSIS", "ANTONIA FERNANDES",
            "ALZIANE JACOB", "DIOGO STUTZ RODRIGUES", "DIVA MEDEIROS DA SILVA", "JORGE SILVA DA CRUZ",
            "JOSE ALVES DE OLIVEIRA", "JOSE AMARO BATISTA MACIEL", "L.A. FALCAO BAUER C. TEC. DE CONTROLE DE QUALIDADE",
            "LEANDRO DAUDT MACHADO", "MICHELLE CABRAL DE MACEDO", "MILTON DA SILVA",
            "NILSE MAFORT DA SILVEIRA OUVERNEY", "PAULO CESAR DE SALES", "PEDRO FERREIRA MACHADO",
            "REGINALDO GOMES BARRETO",
            "Paulo Vitor Pires de Miranda Marins", "TIAGO ROBERT MACIEL",
            "VERA LUCIA DE SOUZA COELHO", "VILMA DE OLIVEIRA LESSA CARDONA")

    -- droping financial services

    AND
    mer.credor
    NOT in (
    "BANCO BRADESCO S/A", "BANCO DO ESTADO DO RIO DE JANEIRO S/A", "BANCO ITAU", "BANCO ITAU S/A", "BRADESCO S/A",
    "CAIXA ECONOMICA FEDERAL",
    "ITAU SEGUROS DE AUTO E RESIDENCIA SA")

    -- droping other companies

    AND
    mer.credor
    NOT in ("ITACIR INDICATTI", "CONDOMINIO MACAE SHOPPING", "MCI BRASIL S/A")

    OR
    mer.grupo_da_despesa is null""")

    cur.execute(query)
    rows = cur.fetchall()
    col_name_list = [i[0] for i in cur.description]

    df_merged2 = pd.DataFrame(rows, columns=col_name_list)
    df_merged2.to_sql('merged_times2', con=conn, if_exists='replace', index=False)

    return


if __name__ == "__main__":
    database = r"database_macae.db"
    conn = create_connection(database)
    database2 = r"database_partes.db"
    conn2 = create_connection(database2)
    main1()
    main2()

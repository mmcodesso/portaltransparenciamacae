import sqlite3
from sqlite3 import Error
import numpy as np
import pandas as pd
import json
import os
import glob
import unicodedata as ud


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
    df_2 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_mdb_rj.csv', sep=';', encoding="ISO-8859-1")
    df_3 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_pcdob_rj.csv', sep=';', encoding="ISO-8859-1")
    df_4 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_psb_rj.csv', sep=';', encoding="ISO-8859-1")
    df_5 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_psdb_rj.csv', sep=';', encoding="ISO-8859-1")
    df_6 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_psl_rj.csv', sep=';', encoding="ISO-8859-1")
    df_7 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_pt_rj.csv', sep=';', encoding="ISO-8859-1")
    df_8 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_pv_rj.csv', sep=';', encoding="ISO-8859-1")
    df_9 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_rede_rj.csv', sep=';', encoding="ISO-8859-1")
    df_10 = pd.read_csv('./fontes_db/filiacao_prefeitura/filiados_psd_rj.csv', sep=';', encoding="ISO-8859-1")

    df_filiacao_pref = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10], sort=True)
    df_filiacao_pref['eleicao'] = 'PREFEITO'

    df_1_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_avante_rj.csv", sep=";", encoding="ISO-8859-1")
    df_2_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_cidadania_rj.csv", sep=";", encoding="ISO-8859-1")
    df_3_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pdt_rj.csv", sep=";", encoding="ISO-8859-1")
    df_4_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pl_rj.csv", sep=";", encoding="ISO-8859-1")
    df_5_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pode_rj.csv", sep=";", encoding="ISO-8859-1")
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

    # fili_dup = df_filiacao[df_filiacao.duplicated(subset=df_filiacao.columns.difference(['eleicao']))]
    # fili_dup = fili_dup.drop(columns='eleicao')
    # fili_dup['eleicao'] = 'VEREADOR_PREFEITO'
    # fili_non_dup = df_filiacao[~df_filiacao.duplicated(subset=df_filiacao.columns.difference(['eleicao']))]
    # df_filiacao = pd.concat([fili_dup, fili_non_dup])

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

    for Path, subdirs, File in os.walk(folder):
        for name in File:
            if os.path.splitext(os.path.join(Path, name))[1] == ".json":
                json_list.append(os.path.join(Path, name))

    for j in json_list:
        with open(j) as json_data:
            data = json.load(json_data)
        dtframe = pd.DataFrame([data])
        try:
            dtframe['atividade_principal'] = dtframe['atividade_principal'].apply(lambda x: x[0])
            dtframe[['atividade_principal_text', 'atividade_principal_code']] =\
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
    json_credores_2015, qsa_credores_2015, ativ_sec_credores_2015 =\
        parse_json_files("./fontes_db/jsons/folder_credores_2015/")
    json_credores_2016, qsa_credores_2016, ativ_sec_credores_2016 =\
        parse_json_files("./fontes_db/jsons/folder_credores_2016/")
    json_credores_2017, qsa_credores_2017, ativ_sec_credores_2017 =\
        parse_json_files("./fontes_db/jsons/folder_credores_2017/")
    json_credores_2018, qsa_credores_2018, ativ_sec_credores_2018 =\
        parse_json_files("./fontes_db/jsons/folder_credores_2018/")
    json_credores_2019, qsa_credores_2019, ativ_sec_credores_2019 =\
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
    json_doadores_vereadores, qsa_doadores_vereadores, ativ_sec_doadores_vereadores =\
        parse_json_files("./fontes_db/jsons/folder_doadores_vereadores/")
    json_doadores_vereadores['eleicao'] = 'vereadores'

    json_doadores_prefeito, qsa_doadores_prefeito, ativ_sec_doadores_prefeito =\
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

    json_fornecedores_vereadores, qsa_fornecedores_vereadores, ativ_sec_fornecedores_vereadores =\
        parse_json_files("./fontes_db/jsons/folder_fornecedores_vereadores/")
    json_fornecedores_vereadores['eleicao'] = 'vereadores'

    json_fornecedores_prefeito, qsa_fornecedores_prefeito, ativ_sec_fornecedores_prefeito =\
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

    receita_cnpj = receita_cnpj.drop(columns='extra')

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
    creds = creds.iloc[creds['nome'].str.normalize('NFKD').argsort()]  # sort columns containing special chars
    creds = creds.sort_values(['ano', 'nome']).sort_index()
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
    credores_liquid = beautifier_cols(credores_liquid)
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

    credores_pagamentos = credores_pagamentos[~credores_pagamentos['Data do Pagamento'].str.contains("Data do Pagamento")]
    credores_pagamentos = credores_pagamentos[['Data do Pagamento', 'Número do Pagamento', 'Número de liquidação',
                                               'Complemento Histórico', 'Valor Pago', 'Valor Estornado', 'credor',
                                               'empenho', 'ano']]
    credores_pagamentos = beautifier_cols(credores_pagamentos)
    return credores_pagamentos


# DETALHES EMPENHOS
def detalhes_empenhos(df_credores):
    det_emp = ['detalhes_emp_2015.csv',
               'detalhes_emp_2016.csv',
               'detalhes_emp_2017.csv',
               'detalhes_emp_2018.csv',
               'detalhes_emp_2019.csv']
    detalhes_emp_list = []
    for i in det_emp:
        file = './raw_data/' + str(i)
        df = pd.read_csv(file)
        df['ano_referencia'] = i.split('.')[0][-4:]
        df = df.iloc[df['Credor'].str.normalize('NFKD').argsort()]  # sort columns containing special chars
        detalhes_emp_list.append(df)
    detalhes_emp = pd.concat(detalhes_emp_list, sort=True).drop_duplicates()

    detalhes_emp = detalhes_emp.sort_index(axis=1)
    detalhes_emp = detalhes_emp.loc[:, 'Ação de Governo':]
    detalhes_emp = detalhes_emp.loc[:, ~detalhes_emp.columns.duplicated()]

    detalhes_emp = beautifier_cols(detalhes_emp)
    detalhes_emp = detalhes_emp.merge(df_credores[['nome', 'cnpj/cpf']],
                                      left_on='credor',
                                      right_on='nome',
                                      how='inner')
    detalhes_emp = detalhes_emp[['data_emissão_empenho', 'número_do_empenho', 'unidade_gestora',
                                 'credor', 'cnpj/cpf', 'valor_empenhado', 'valor_em_liquidação', 'valor_liquidado',
                                 'valor_pago', 'valor_anulado', 'atualizado_em', 'período', 'ano',
                                 'tipo_empenho', 'categoria',
                                 'órgão', 'unidade', 'função', 'subfunção', 'programa_de_governo',
                                 'ação_de_governo', 'ie', 'natureza_da_despesa', 'esfera',
                                 'categoria_econômica', 'grupo_da_despesa', 'modalidade_de_aplicação',
                                 'desdobramento_da_despesa', 'fonte_de_recursos',
                                 'detalhamento_da_fonte', 'licitação', 'número_da_licitação',
                                 'data_de_homologação', 'processo_da_compra', 'processo_administrativo', 'contrato',
                                 'convênio', 'empenhado', 'em_liquidação', 'liquidado',
                                 'pago', 'anulado', 'ano_referencia']]

    detalhes_emp = detalhes_emp.reset_index(drop=True)
    detalhes_emp['credor'] = detalhes_emp['credor'].apply(lambda x: ud.normalize('NFKD', x))
    detalhes_emp = detalhes_emp.sort_values(['ano_referencia', 'credor']).drop_duplicates().reset_index(drop=True)
    detalhes_emp.to_sql('detalhes_emp', con=conn, if_exists='replace', index=False)

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
    # df_contratos_nomes.to_sql('contratos_nomes', con=conn, if_exists='replace', index=False)

    df_contratos_empresas = pd.read_csv('./raw_data/contratos_empresas.csv')
    df_contratos_empresas['Nome'] = df_contratos_empresas['Nome'].fillna('-').apply(lambda x: x.strip())
    df_contratos_empresas = beautifier_cols(df_contratos_empresas).sort_values(['nome', 'contrato']).reset_index(drop=True)
    df_contratos_empresas['contrato'] = df_contratos_empresas.contrato.apply(lambda x: int(x))
    df_contratos_empresas['tipo'] = 'PJ'
    # df_contratos_empresas.to_sql('contratos_empresas', con=conn, if_exists='replace', index=False)

    df_contratos = pd.concat([df_contratos_nomes,
                              df_contratos_empresas], sort=True)
    df_contratos = df_contratos[['nome', 'cpf/cnpj', 'antes_depois', 'contrato', 'tipo']].fillna('-')
    df_contratos = df_contratos.sort_values(['contrato', 'antes_depois'])
    return df_contratos


def main(conn):
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


if __name__ == "__main__":
    database = r"database_macae.db"
    connection = create_connection(database)
    main(connection)

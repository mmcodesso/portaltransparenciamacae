import sqlite3
from sqlite3 import Error
import pandas as pd
import json
import os
import glob


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    connex = None
    try:
        connex = sqlite3.connect(db_file)
        return connex
    except Error as e:
        print(e)
    return connex


def select_table(connex, table):
    """ Query all rows in a table """
    cur = connex.cursor()
    query = "SELECT * FROM " + str(table)
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def sql_fetch(connex):
    cursor_obj = connex.cursor()
    cursor_obj.execute('SELECT name from sqlite_master where type= "table"')
    print(cursor_obj.fetchall())


database = r"database_macae.db"
conn = create_connection(database)

# Prefeito, Vice-Prefeito e Secretários
df1 = pd.read_excel('./fontes_db/Prefeito, Vice-Prefeito e Secretários.xlsx')
df1 = df1.drop(columns='ID')
df1.to_sql('prefeito_vp_secretarios', con=conn, if_exists='replace')

# Vereadores
df_2_dir = pd.read_excel('./fontes_db/Câmara dos Vereadores - Mesa Diretora e Comissões.xlsx', sheet_name='diretora')
df_2_dir = df_2_dir.iloc[:15, :]
df_2_dir.to_sql('vereadores_mesa_diretora', con=conn, if_exists='replace')
df_2_com = pd.read_excel('./fontes_db/Câmara dos Vereadores - Mesa Diretora e Comissões.xlsx', sheet_name='comissao')
df_2_com.to_sql('vereadores_comissao', con=conn, if_exists='replace')

# Doadores
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
df_doadores.to_sql('doadores', con=conn, if_exists='replace')

# Fornecedores
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
df_fornecedores.to_sql('fornecedores', con=conn, if_exists='replace')

# Servidores da câmara
df_serv_camara = pd.read_excel('./fontes_db/Servidores_camara.xlsx')
df_serv_camara.to_sql('servidores_camara', con=conn, if_exists='replace')

# Servidores prefeitura
df_serv_pref = pd.read_excel('./fontes_db/Servidores Prefeitura.xlsx')
df_serv_pref.to_sql('servidores_pref', con=conn, if_exists='replace')

# Filiacao Partidaria
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

df_filiacao_pref = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10])
df_filiacao_pref['eleicao'] = 'PREFEITO'

df_1_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_avante_rj.csv", sep=";", encoding="ISO-8859-1")
df_2_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_cidadania_rj.csv", sep=";", encoding="ISO-8859-1")
df_3_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pdt_rj.csv", sep=";", encoding="ISO-8859-1")
df_4_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pl_rj.csv", sep=";", encoding="ISO-8859-1")
df_5_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pode_rj.csv", sep=";", encoding="ISO-8859-1")
df_6_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_pros_rj.csv", sep=";", encoding="ISO-8859-1")
df_7_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_psc_rj.csv", sep=";", encoding="ISO-8859-1")
df_8_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_ptc_rj.csv", sep=";", encoding="ISO-8859-1")
df_9_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_republicanos_rj.csv", sep=";", encoding="ISO-8859-1")
df_10_ver = pd.read_csv("./fontes_db/filiacao_vereadores/filiados_solidariedade_rj.csv", sep=";", encoding="ISO-8859-1")

df_filiacao_veread = pd.concat(
    [df_1_ver, df_2_ver, df_3_ver, df_4_ver, df_5_ver, df_6_ver, df_7_ver, df_8_ver, df_9_ver, df_10_ver])

df_filiacao_veread['eleicao'] = 'VEREADOR'

df_filiacao = pd.concat([df_filiacao_pref,
                         df_filiacao_veread])

# fili_dup = df_filiacao[df_filiacao.duplicated(subset=df_filiacao.columns.difference(['eleicao']))]
# fili_dup = fili_dup.drop(columns='eleicao')
# fili_dup['eleicao'] = 'VEREADOR_PREFEITO'
# fili_non_dup = df_filiacao[~df_filiacao.duplicated(subset=df_filiacao.columns.difference(['eleicao']))]
# df_filiacao = pd.concat([fili_dup, fili_non_dup])

df_filiacao.to_sql('filiacao_partidaria', con=conn, if_exists='replace')

# CNPJ RECEITA (JSONS)


def parse_json_files(folder):
    """
    look at the folder with documents and search for json files to parse
    """
    json_list = []
    df_full = pd.DataFrame()
    qsa_full = pd.DataFrame()
    ativ_sec_full = pd.DataFrame()

    for path, subdirs, files in os.walk(folder):
        for name in files:
            if os.path.splitext(os.path.join(path, name))[1] == ".json":
                json_list.append(os.path.join(path, name))

    for j in json_list:
        with open(j) as json_data:
            data = json.load(json_data)
        df = pd.DataFrame([data])
        try:
            df['atividade_principal'] = df['atividade_principal'].apply(lambda x: x[0])
            df[['atividade_principal_text', 'atividade_principal_code']] = df.atividade_principal.apply(pd.Series)
            df = df.drop('atividade_principal', axis=1)
        except:
            continue

        df[['billing_free', 'billing_database']] = df.billing.apply(pd.Series)
        df = df.drop('billing', axis=1)

        qsa = pd.DataFrame(df.qsa[0])
        qsa['cnpj_empresa'] = df.cnpj[0]
        df = df.drop('qsa', axis=1)

        ativ_sec = pd.DataFrame(df.atividades_secundarias[0])
        ativ_sec['cnpj_empresa'] = df.cnpj[0]
        df = df.drop('atividades_secundarias', axis=1)

        df_full = df_full.append(df, sort=True)
        qsa_full = qsa_full.append(qsa, sort=True)
        ativ_sec_full = ativ_sec_full.append(ativ_sec, sort=True)
    return df_full, qsa_full, ativ_sec_full

json_credores_2015, qsa_credores_2015, ativ_sec_credores_2015 = parse_json_files("./fontes_db/jsons/folder_credores_2015/")
json_credores_2016, qsa_credores_2016, ativ_sec_credores_2016 = parse_json_files("./fontes_db/jsons/folder_credores_2016/")
json_credores_2017, qsa_credores_2017, ativ_sec_credores_2017 = parse_json_files("./fontes_db/jsons/folder_credores_2017/")
json_credores_2018, qsa_credores_2018, ativ_sec_credores_2018 = parse_json_files("./fontes_db/jsons/folder_credores_2018/")
json_credores_2019, qsa_credores_2019, ativ_sec_credores_2019 = parse_json_files("./fontes_db/jsons/folder_credores_2019/")
json_doadores_prefeito, qsa_doadores_prefeito, ativ_sec_doadores_prefeito = parse_json_files("./fontes_db/jsons/folder_doadores_prefeito/")
json_doadores_vereadores, qsa_doadores_vereadores, ativ_sec_doadores_vereadores = parse_json_files("./fontes_db/jsons/folder_doadores_vereadores/")
json_fornecedores_prefeito, qsa_fornecedores_prefeito, ativ_sec_fornecedores_prefeito = parse_json_files("./fontes_db/jsons/folder_fornecedores_prefeito/")
json_fornecedores_vereadores, qsa_fornecedores_vereadores, ativ_sec_fornecedores_vereadores = parse_json_files("./fontes_db/jsons/folder_fornecedores_vereadores/")

json_credores_2015['ano'] = '2015'
json_credores_2016['ano'] = '2016'
json_credores_2017['ano'] = '2017'
json_credores_2018['ano'] = '2018'
json_credores_2019['ano'] = '2019'

json_doadores_prefeito['eleicao'] = 'prefeito'
json_doadores_vereadores['eleicao'] = 'vereadores'

json_fornecedores_prefeito['eleicao'] = 'prefeito'
json_fornecedores_vereadores['eleicao'] = 'vereadores'

cnpj_credores = pd.concat([json_credores_2015,
                           json_credores_2016,
                           json_credores_2017,
                           json_credores_2018,
                           json_credores_2019]).reset_index(drop=True)
cnpj_credores['categoria'] = 'credores'

qsa_credores = pd.concat([qsa_credores_2015,
                          qsa_credores_2016,
                          qsa_credores_2017,
                          qsa_credores_2018,
                          qsa_credores_2019]).reset_index(drop=True)
qsa_credores['categoria'] = 'credores'

ativ_sec_credores = pd.concat([ativ_sec_credores_2015,
                               ativ_sec_credores_2016,
                               ativ_sec_credores_2017,
                               ativ_sec_credores_2018,
                               ativ_sec_credores_2019]).reset_index(drop=True)
ativ_sec_credores['categoria'] = 'credores'

doadores = pd.concat([json_doadores_prefeito,
                      json_doadores_vereadores]).reset_index(drop=True)
doadores['categoria'] = 'doadores'

qsa_doadores = pd.concat([qsa_doadores_prefeito,
                          qsa_doadores_vereadores], sort=True).reset_index(drop=True)
qsa_doadores['categoria'] = 'doadores'

ativ_sec_doadores = pd.concat([ativ_sec_doadores_prefeito,
                               ativ_sec_doadores_vereadores]).reset_index(drop=True)
ativ_sec_doadores['categoria'] = 'doadores'

fornecedores = pd.concat([json_fornecedores_prefeito,
                          json_fornecedores_vereadores]).reset_index(drop=True)
fornecedores['categoria'] = 'fornecedores'

qsa_fornecedores = pd.concat([qsa_fornecedores_prefeito,
                              qsa_doadores_vereadores]).reset_index(drop=True)
qsa_fornecedores['categoria'] = 'fornecedores'

ativ_sec_fornecedores = pd.concat([ativ_sec_fornecedores_prefeito,
                                   ativ_sec_fornecedores_vereadores]).reset_index(drop=True)
ativ_sec_fornecedores['categoria'] = 'fornecedores'


receita_CNPJ = pd.concat([cnpj_credores,
                          doadores,
                          fornecedores], sort=True).reset_index(drop=True)

receita_QSA = pd.concat([qsa_credores,
                         qsa_doadores,
                         qsa_fornecedores], sort=True).reset_index(drop=True)

receita_ATIV_SEC = pd.concat([ativ_sec_credores,
                              ativ_sec_doadores,
                              ativ_sec_fornecedores], sort=True).reset_index(drop=True)

receita_CNPJ = receita_CNPJ.drop(columns='extra')
receita_CNPJ.to_sql('receita_CNPJ', con=conn, if_exists='replace')

receita_QSA.to_sql('receita_QSA', con=conn, if_exists='replace')
receita_ATIV_SEC.to_sql('receita_ATIV_SEC', con=conn, if_exists='replace')


# CREDORES
path = r'./raw_data/cred_2016/'
files = glob.glob(path + "credores_2016_*.csv")
credores_list = []
for filename in files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df = df.rename(columns={'Valor Em LiquidaÃ§Ã£o': 'Valor Em Liquidação'})
    credores_list.append(df)
cred16 = pd.concat(credores_list, axis=0, ignore_index=True, sort=True).reset_index(drop=True)
cred16 = cred16.drop(cred16.filter(like=r'Unnamed').columns, axis=1)

path = r'./raw_data/cred_2018/'
files = glob.glob(path + "credores_2018_*.csv")
credores_list = []
for filename in files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df = df.rename(columns={'Valor Em LiquidaÃ§Ã£o': 'Valor Em Liquidação'})
    credores_list.append(df)
cred18 = pd.concat(credores_list, axis=0, ignore_index=True, sort=True).reset_index(drop=True)
cred18 = cred18.drop(cred18.filter(like=r'Unnamed').columns, axis=1)

credores = pd.concat([pd.read_csv('./raw_data/credores_2015.csv'),
                      cred16,
                      pd.read_csv('./raw_data/credores_2017.csv'),
                      cred18,
                      pd.read_csv('./raw_data/credores_2019.csv', sep="\t")]).drop_duplicates()
credores.to_sql('credores', con=conn, if_exists='replace')


cred_liq = ['credores_liquidacoes_2015.csv',
            'credores_liquidacoes_2016.csv',
            'credores_liquidacoes_2017.csv',
            'credores_liquidacoes_2018.csv',
            'credores_liquidacoes_2019.csv']
credores_liquidacoes = pd.DataFrame()
for i in cred_liq:
    file = './raw_data/' + str(i)
    df = pd.read_csv(file, sep='\t')
    df['ano'] = i.split('.')[0][-4:]
    credores_liquidacoes = credores_liquidacoes.append(df).drop_duplicates()
credores_liquidacoes.to_sql('credores_liquidacoes', con=conn, if_exists='replace')


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
credores_pagamentos.to_sql('credores_pagamentos', con=conn, if_exists='replace')


det_emp = ['detalhes_emp_2015.csv',
           'detalhes_emp_2016.csv',
           'detalhes_emp_2017.csv',
           'detalhes_emp_2018.csv',
           'detalhes_emp_2019.csv']
detalhes_emp = pd.DataFrame()
for i in det_emp:
    file = './raw_data/' + str(i)
    df = pd.read_csv(file)
    df['ano'] = i.split('.')[0][-4:]
    detalhes_emp = detalhes_emp.append(df).drop_duplicates()
detalhes_emp = detalhes_emp.drop(columns=['detalhe_empenho',
                                          '0 ',
                                          'Ano',
                                          'ATAC ASSISTENCIA TECNICA EM AR CONDICIONADO LTDA ',
                                          'MARIA JOSE QUINTANILHA BARBOSA ',
                                          'OFFICE SOLUÇAO EM COM DE MOVEIS PARA ESC EIRELLI ',
                                          'Unidade Gestora.1']).drop_duplicates()
detalhes_emp.to_sql('detalhes_emp', con=conn, if_exists='replace')

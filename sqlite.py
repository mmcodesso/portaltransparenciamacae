import sqlite3
from sqlite3 import Error
import pandas as pd


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def select_table(conn, table):
    """ Query all rows in a table """
    cur = conn.cursor()
    query = "SELECT * FROM " + str(table)
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)


database = r"db_macae.db"
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
df_fornecedores.to_sql('fornecedores', con=conn, if_exists='replace')

# Servidores da câmara
df_serv_camara = pd.read_excel('./fontes_db/Servidores_camara.xlsx')
df_serv_camara.to_sql('servidores_camara', con=conn, if_exists='replace')

# Servidores prefeitura
df_serv_pref = pd.read_excel('./fontes_db/Servidores Prefeitura.xlsx')
df_serv_pref.to_sql('servidores_pref', con=conn, if_exists='replace')

# Filiacao Partidaria
df_1 = pd.read_csv('./fontes_db/filiacao_pref/filiados_dc_rj.csv', sep=';', encoding="ISO-8859-1")
df_2 = pd.read_csv('./fontes_db/filiacao_pref/filiados_mdb_rj.csv', sep=';', encoding="ISO-8859-1")
df_3 = pd.read_csv('./fontes_db/filiacao_pref/filiados_pcdob_rj.csv', sep=';', encoding="ISO-8859-1")
df_4 = pd.read_csv('./fontes_db/filiacao_pref/filiados_psb_rj.csv', sep=';', encoding="ISO-8859-1")
df_5 = pd.read_csv('./fontes_db/filiacao_pref/filiados_psdb_rj.csv', sep=';', encoding="ISO-8859-1")
df_6 = pd.read_csv('./fontes_db/filiacao_pref/filiados_psl_rj.csv', sep=';', encoding="ISO-8859-1")
df_7 = pd.read_csv('./fontes_db/filiacao_pref/filiados_pt_rj.csv', sep=';', encoding="ISO-8859-1")
df_8 = pd.read_csv('./fontes_db/filiacao_pref/filiados_pv_rj.csv', sep=';', encoding="ISO-8859-1")
df_9 = pd.read_csv('./fontes_db/filiacao_pref/filiados_rede_rj.csv', sep=';', encoding="ISO-8859-1")
df_10 = pd.read_csv('./fontes_db/filiacao_pref/filiados_psd_rj.csv', sep=';', encoding="ISO-8859-1")

df_filiacao_pref = pd.concat([df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10])
df_filiacao_pref['eleicao'] = 'PREFEITO'

df_1_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_pt_rj.csv", sep=";", encoding="ISO-8859-1")
df_2_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_pl_rj.csv", sep=";", encoding="ISO-8859-1")
df_3_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_pv_rj.csv", sep=";", encoding="ISO-8859-1")
df_4_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_republicanos_rj.csv", sep=";", encoding="ISO-8859-1")
df_5_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_psc_rj.csv", sep=";", encoding="ISO-8859-1")
df_6_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_solidariedade_rj.csv", sep=";", encoding="ISO-8859-1")
df_7_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_rede_rj.csv", sep=";", encoding="ISO-8859-1")
df_8_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_mdb_rj.csv", sep=";", encoding="ISO-8859-1")
df_9_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_pros_rj.csv", sep=";", encoding="ISO-8859-1")
df_10_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_cidadania_rj.csv", sep=";", encoding="ISO-8859-1")
df_11_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_pode_rj.csv", sep=";", encoding="ISO-8859-1")
df_12_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_psb_rj.csv", sep=";", encoding="ISO-8859-1")
df_13_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_ptc_rj.csv", sep=";", encoding="ISO-8859-1")
df_14_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_avante_rj.csv", sep=";", encoding="ISO-8859-1")
df_15_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_pcdob_rj.csv", sep=";", encoding="ISO-8859-1")
df_16_ver = pd.read_csv("./fontes_db/filiacao_veread/filiados_pdt_rj.csv", sep=";", encoding="ISO-8859-1")

df_filiacao_veread = pd.concat(
    [df_1_ver, df_2_ver, df_3_ver, df_4_ver, df_5_ver, df_6_ver, df_7_ver, df_8_ver, df_9_ver, df_10_ver,
     df_11_ver, df_12_ver, df_13_ver, df_14_ver, df_15_ver, df_16_ver])

df_filiacao_veread['eleicao'] = 'VEREADOR'

df_filiacao = pd.concat([df_filiacao_pref,
                         df_filiacao_veread])

fili_dup = df_filiacao[df_filiacao.duplicated(subset=df_filiacao.columns.difference(['eleicao']))]
fili_dup = fili_dup.drop(columns='eleicao')
fili_dup['eleicao'] = 'VEREADOR_PREFEITO'
fili_non_dup = df_filiacao[~df_filiacao.duplicated(subset=df_filiacao.columns.difference(['eleicao']))]
df_filiacao = pd.concat([fili_dup,
                         fili_non_dup])
df_filiacao.to_sql('filiacao_partidaria', con=conn, if_exists='replace')

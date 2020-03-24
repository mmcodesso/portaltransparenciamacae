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
df1.to_sql('prefeito_vp_secretarios', con=conn, if_exists='replace')

# Vereadores
df_2_dir = pd.read_excel('./fontes_db/Câmara dos Vereadores - Mesa Diretora e Comissões.xlsx', sheet_name='diretora')
df_2_com = pd.read_excel('./fontes_db/Câmara dos Vereadores - Mesa Diretora e Comissões.xlsx', sheet_name='comissao')
df_2_dir.to_sql('vereadores_mesa_diretora', con=conn, if_exists='replace')
df_2_com.to_sql('vereadores_comissao', con=conn, if_exists='replace')
# Doadores
df_3_doadores_veread_2012 = pd.read_excel('./fontes_db/doadores_vereadores/Eleições 2012 - Doadores Vereadores Mesa Diretora e Comissões.xlsx', sheet_name = 'DOAÇÕES CONSOLIDADO 2').ffill(0)
df_3_doadores_veread_2012['eleicao'] = 'vereador'
df_3_doadores_veread_2012['ano'] = '2012'
df_3_doadores_veread_2014 = pd.read_excel('./fontes_db/doadores_vereadores/Eleições 2014 - Doadores Deputados Mesa Diretora e Comissões.xlsx', sheet_name = 'DOAÇÕES CONSOLIDADO 2').ffill(0)
df_3_doadores_veread_2014['eleicao'] = 'vereador'
df_3_doadores_veread_2014['ano'] = '2014'
df_3_doadores_veread_2016 = pd.read_excel('./fontes_db/doadores_vereadores/Eleições 2016 - Doadores Vereadores Mesa Diretora e Comissões.xlsx', sheet_name = 'DOAÇÕES CONSOLIDADO 2').ffill(0)
df_3_doadores_veread_2016['eleicao'] = 'vereador'
df_3_doadores_veread_2016['ano'] = '2016'
df_3_doadores_veread_2018 = pd.read_excel('./fontes_db/doadores_vereadores/Eleições 2018 - Doadores Deputados Mesa Diretora e Comissões.xlsx', sheet_name = 'DOAÇÕES CONSOLIDADO 2').ffill(0)
df_3_doadores_veread_2018['eleicao'] = 'vereador'
df_3_doadores_veread_2018['ano'] = '2018'
df_3_doadores_pref_2012 = pd.read_excel('./fontes_db/doadores_pref/Eleições 2012 - Doadores Comitê Coligação Prefeito e Vice-Prefeito.xlsx', sheet_name = 'DOAÇÕES CONSOLIDADAS 2').ffill(0)
df_3_doadores_pref_2012['eleicao'] = 'prefeito'
df_3_doadores_pref_2012['ano'] = '2012'
df_3_doadores_pref_2012_2 = pd.read_excel('./fontes_db/doadores_pref/Eleições 2012 - Doadores Prefeito e Vice-Prefeito.xlsx', sheet_name = 'DOAÇÕES CONSOLIDADAS 2').ffill(0)
df_3_doadores_pref_2012_2['eleicao'] = 'prefeito'
df_3_doadores_pref_2012_2['ano'] = '2012'
df_3_doadores_pref_2014 = pd.read_excel('./fontes_db/doadores_pref/Eleições 2014 - Doadores Vice-Prefeito - Campanha Deputado Federal.xlsx', sheet_name = 'DOAÇÕES CONSOLIDADAS 2').ffill(0)
df_3_doadores_pref_2014['eleicao'] = 'prefeito'
df_3_doadores_pref_2014['ano'] = '2014'
df_3_doadores_pref_2016 = pd.read_excel('./fontes_db/doadores_pref/Eleições 2016 - Doadores Prefeito e Vice-Prefeito.xlsx', sheet_name = 'DOAÇÕES CONSOLIDADAS 2').ffill(0)
df_3_doadores_pref_2016['eleicao'] = 'prefeito'
df_3_doadores_pref_2016['ano'] = '2016'
df_doadores = pd.concat([df_3_doadores_veread_2012,
                         df_3_doadores_veread_2014,
                         df_3_doadores_veread_2016,
                         df_3_doadores_veread_2018,
                         df_3_doadores_pref_2012,
                         df_3_doadores_pref_2012_2,
                         df_3_doadores_pref_2014,
                         df_3_doadores_pref_2016], sort=True)
df_doadores.to_sql('doadores', con=conn, if_exists='replace')

# Fornecedores
df_forne_pref_2012 = pd.read_excel('./fontes_db/fornecedores_pref/Eleições 2012 - Despesas Comitê Coligação Prefeito e Vice-Prefeito.xlsx', sheet_name = 'DESPESAS CONSOLIDADAS 2').ffill(0)
df_forne_pref_2012_2 = pd.read_excel('./fontes_db/fornecedores_pref/Eleições 2012 - Despesas Prefeito e Vice-Prefeito.xlsx', sheet_name = 'DESPESAS CONSOLIDADAS 2').ffill(0)
df_forne_pref_2014 = pd.read_excel('./fontes_db/fornecedores_pref/Eleições 2014 - Despesas Vice-Prefeito - Campanha Deputado Federal.xlsx', sheet_name = 'DESPESAS CONSOLIDADAS 2').ffill(0)
df_forne_pref_2016 = pd.read_excel('./fontes_db/fornecedores_pref/Eleições 2016 - Despesas Partidos Coligação Prefeito e Vice-Prefeito.xlsx', sheet_name = 'DESPESAS CONSOLIDADAS 2').ffill(0)
df_forne_pref_2016_2 = pd.read_excel('./fontes_db/fornecedores_pref/Eleições 2016 - Despesas Prefeito e Vice-Prefeito.xlsx', sheet_name = 'DESPESAS CONSOLIDADAS 2').ffill(0)
df_forne_veread_2012 = pd.read_excel('./fontes_db/fornecedores_veread/Eleições 2012 - Despesas Vereadores Mesa Diretora e Comissões.xlsx', sheet_name = 'DESPESAS CONSOLIDADAS 2').ffill(0)
df_forne_veread_2014 = pd.read_excel('./fontes_db/fornecedores_veread/Eleições 2014 - Despesas Deputados Mesa Diretora e Comissões.xlsx', sheet_name = 'DESPESAS CONSOLIDADAS 2').ffill(0)
df_forne_veread_2016 = pd.read_excel('./fontes_db/fornecedores_veread/Eleições 2016 - Despesas Vereadores Mesa Diretora e Comissões.xlsx', sheet_name = 'DESPESAS CONSOLIDADAS 2').ffill(0)
df_forne_veread_2018 = pd.read_excel('./fontes_db/fornecedores_veread/Eleições 2018 - Despesas Deputados Mesa Diretora e Comissões.xlsx', sheet_name = 'DESPESAS CONSOLIDADAS 2').ffill(0)
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
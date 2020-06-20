import pandas as pd
import numpy as np
from scipy.stats import f_oneway
from scipy.stats import ttest_ind
import sqlite3
from statsmodels.stats.weightstats import ztest
import statsmodels.api as sm
from statsmodels.formula.api import ols

# df = pd.read_csv('merged_times51373.csv')  # load data set
# df = pd.read_csv('merged_times2.csv')  # load data set

def run_query(query):
    database = r"database_macae.db"
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    col_name_list = [i[0] for i in cur.description]
    df = pd.DataFrame(rows, columns=col_name_list)
    return df


def descriptive_stats(df):
    grp = df.groupby('parte_relac')[['tempo_entre_liquidacao_pagamento']].agg(
        [np.size, np.mean, np.median, np.std, max, min]).T

    grp = round(grp, 2)
    print(grp)
    print("\n")
    return


def perform_anova(df, coluna):
    # Analysis of Variance test
    # references:
    # https://machinelearningmastery.com/parametric-statistical-significance-tests-in-python/
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html
    # https://www.statisticshowto.com/probability-and-statistics/f-statistic-value-test/
    col = str(coluna)
    data1 = df[df.parte_relac == 1][col]
    data2 = df[df.parte_relac == 0][col]

    # summarize
    print(coluna + ': ANOVA \n')
    print('parte_relac = 1: mean=%.2f stdv=%.2f' % (np.mean(data1), np.std(data1)))
    print('parte_relac = 0: mean=%.2f stdv=%.2f\n' % (np.mean(data2), np.std(data2)))
    # compare samples
    stat, p = f_oneway(data1, data2)
    alpha = 0.05
    print('F Stat=%.3f, p=%.3f, alpha=%.2f' % (stat, p, alpha))
    # interpret
    if p > alpha:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')
    print("\n")
    return


def perform_ttest(df, coluna):
    col = str(coluna)
    data1 = df[df.parte_relac == 1][col]
    data2 = df[df.parte_relac == 0][col]

    # summarize
    print(coluna + ': T-TEST\n')
    print('parte_relac = 1: mean=%.2f stdv=%.2f' % (np.mean(data1), np.std(data1)))
    print('parte_relac = 0: mean=%.2f stdv=%.2f\n' % (np.mean(data2), np.std(data2)))
    # compare samples
    stat, p = ttest_ind(data1, data2)
    alpha = 0.05
    print('Stat=%.3f, p=%.3f, alpha=%.2f' % (stat, p, alpha))
    # interpret
    if p > alpha:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')
    print("\n")
    return


def perform_ztest(df, coluna):
    col = str(coluna)
    data1 = df[df.parte_relac == 1][col]
    data2 = df[df.parte_relac == 0][col]

    # summarize
    print(coluna + ': Z-TEST\n')
    print('parte_relac = 1: mean=%.2f stdv=%.2f' % (np.mean(data1), np.std(data1)))
    print('parte_relac = 0: mean=%.2f stdv=%.2f\n' % (np.mean(data2), np.std(data2)))
    # compare samples
    stat, p = ztest(data1, data2)
    alpha = 0.05
    print('Stat=%.3f, p=%.3f, alpha=%.2f' % (stat, p, alpha))
    # interpret
    if p > alpha:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')
    print("\n")
    return


def plot_distribution(field, xlim=(-100, 100)):
    field = str(field)
    d = pd.DataFrame({
        'parte_relac 0': df[df.parte_relac == 0][field],
        'parte_relac 1': df[df.parte_relac == 1][field],
    })
    ax = d.plot.kde()
    ax.set_title(field)
    ax.set_xlim(xlim[0], xlim[1])
    return


def namestr(obj, namespace):
    """
    return variable name
    """
    name = [name for name in namespace if namespace[name] is obj]
    return name


all_accounts = """select
parte_relac, tempo_entre_liquidacao_pagamento
from merged_times2
"""

consuption_materials = """select
parte_relac, tempo_entre_liquidacao_pagamento
from merged_times2
WHERE natureza_da_despesa = "3.3.90.30 - MATERIAL DE CONSUMO"
"""

services = """select
parte_relac, tempo_entre_liquidacao_pagamento
from merged_times2
where categoria_economica not in ("4 - DESPESAS DE CAPITAL")
and natureza_da_despesa not in ("3.3.90.30 - MATERIAL DE CONSUMO")
and natureza_da_despesa is not NULL"""

capital_expenses = """select
parte_relac, tempo_entre_liquidacao_pagamento
from merged_times2
WHERE categoria_economica = "4 - DESPESAS DE CAPITAL"
"""

remaining_owed_whatsapp = """select
parte_relac, tempo_entre_liquidacao_pagamento
from merged_times2
WHERE tipo_empenho in ("Restos a Pagar")
"""

remaining_owed_email = """select
parte_relac, tempo_entre_liquidacao_pagamento
from merged_times2
WHERE natureza_da_despesa is NULL
"""

legal_ent_x_individuals = """select
parte_relac, tipo_pessoa, tempo_entre_liquidacao_pagamento
from (select
case when length("cnpj/cpf")>14
or "cnpj/cpf" = "999.999.999-99"
and credor not in ("ALDECI SOARES DA SILVA", "ALVIN ANTONIO MOZER E OUTROS VACINADORES", "ALEX MORAES L, DE FIGUEIREDO E OUTROS", "ANDRE LUIZ MARQUES DE AZEVEDO E OUTROS",
"ANDRE LUIZ RIBEIRO BRAGA E OUTROS", "CARLOS JOSE CARDOSO BARROCO E OUTROS", "DAVID RODRIGUES DA SILVA BEZERRA", "DENISE PROENCA DE FIGUEIREDO",
"ESP. DE SVEN LENZ INVET.ELVIRA MARIA MONTEIRO LENZ", "ESPOLIO JAEDER CAMPOS MIRANDA E OUTROS", "GEILCE B. GOMES/EDSON C.F.BARRETO", "GEORGIA KARLA B.G.ROCHA E OUTROS",
"IRIS MARIA PIMENTEL SALLES MAT 4808", "JAINE SANTOS MADALENA", "JONAS ALVES DE BRITO E OUTROS", "JORGE TAVARES SIQUEIRA E OUTROS", "LUCIMAR GRACA PAULA", "MANUEL RODRIGUES QUEIROZ",
"RICARDO YATES MEDEIROS", "ROSANE CAMPOS DE MIRANDA - USAR COD 4977", "SAMARA FALCAO JARDIM", "SINARA BASTOS TAVARES", "VALERIA F DE S PINHEIRO E OUTROS",
"VITOR SALEH FONSECA DE MENDONCA E OUTROS", "ARTHUR PECANHA DE AGUIAR", "WASHINGTON ROBERT DA CONCEICAO", "MARCIO DE AZEVEDO FERNANDES - USAR COD 7892",
"CARLOS MANUEL FIGUEIREDO MACARIO E OUTROS", "JORGE LUIZ DA COSTA FRANCO E OUTROS")
then "PJ"
else "PF"
end as tipo_pessoa,
* from merged_times2)
"""

query = [all_accounts, consuption_materials, services, capital_expenses, remaining_owed_whatsapp, remaining_owed_email,
         legal_ent_x_individuals]

for i in query:
    var = namestr(i, globals())[0]
    print("---> " + var + "\n")
    df = run_query(i)
    if i == legal_ent_x_individuals:
        for j in ["PF", "PJ"]:
            dfj = df[df.tipo_pessoa == j]
            print(j)
            descriptive_stats(dfj)
            perform_anova(dfj, 'tempo_entre_liquidacao_pagamento')
            perform_ttest(dfj, 'tempo_entre_liquidacao_pagamento')
    else:
        descriptive_stats(df)
        perform_anova(df, 'tempo_entre_liquidacao_pagamento')
        perform_ttest(df, 'tempo_entre_liquidacao_pagamento')


moore = sm.datasets.get_rdataset("Moore", "carData", cache=True) # load data
data = moore.data
data = data.rename(columns={"partner.status":  "partner_status"}) # make name pythonic
moore_lm = ols('conformity ~ C(fcategory, Sum)*C(partner_status, Sum)', data=data).fit()
moore_lm = ols('parte_relac ~ C(tempo_entre_liquidacao_pagamento)', data=df).fit()

sm.stats.anova_lm(moore_lm, typ=2).T
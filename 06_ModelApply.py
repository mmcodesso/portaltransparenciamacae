import pandas as pd
import numpy as np
from numpy.random import seed
from scipy.stats import f_oneway

# seed the random number generator
seed(1)

df = pd.read_csv('merged_times51373.csv', engine='python')  # load data set
a=df[df.columns.difference(['nome',
                 'soma_de_percentual_de_doacao',
                 'ano_eleicao',
                 'eleicao',
                 'sigla_do_partido',
                 'soma_de_percentual_de_despesas',
                 'secretaria/_orgao'])].drop_duplicates()
a.to_sql('merged_times', con=conn, if_exists='replace', index=False)

df = pd.read_csv('merged_times2.csv', engine='python')  # load data set
df = df[['empenho', 'credor', 'parte_relac', 'tempo_entre_empenho_liquidacao',
         'tempo_entre_liquidacao_pagamento', 'tempo_entre_empenho_pagamento',
         'tempo_entre_homologacao_pagamento']].drop_duplicates()

grp = df.groupby('parte_relac')[['tempo_entre_empenho_liquidacao',
                                 'tempo_entre_liquidacao_pagamento', 'tempo_entre_empenho_pagamento',
                                 'tempo_entre_homologacao_pagamento']].agg([np.mean, np.median, np.max, np.min]).T

grp = round(grp, 2)

perform_anova(df, 'tempo_entre_empenho_liquidacao')

d = pd.DataFrame({
    'parte_relac 0': df[df.parte_relac == 0]['tempo_entre_empenho_liquidacao'],
    'parte_relac 1': df[df.parte_relac == 1]['tempo_entre_empenho_liquidacao'],
})
ax = d.plot.kde()
ax.set_title("tempo_entre_empenho_liquidacao")
ax.set_xlim(-100, 500)


# Analysis of Variance test
# references:
# https://machinelearningmastery.com/parametric-statistical-significance-tests-in-python/
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html
# https://www.statisticshowto.com/probability-and-statistics/f-statistic-value-test/


def perform_anova(df, coluna):
    col = str(coluna)
    data1 = df[df.parte_relac == 0][col]
    data2 = df[df.parte_relac == 1][col]

    # summarize
    print(coluna + '\n')
    print('parte_relac = 0: mean=%.2f stdv=%.2f' % (np.mean(data1), np.std(data1)))
    print('parte_relac = 1: mean=%.2f stdv=%.2f\n' % (np.mean(data2), np.std(data2)))
    # compare samples
    stat, p = f_oneway(data1, data2)
    print('F Stat=%.3f, p=%.5f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')
    return

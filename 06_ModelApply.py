import pandas as pd
import numpy as np
from numpy.random import seed
from scipy.stats import f_oneway

# seed the random number generator
seed(1)

# df = pd.read_csv('merged_times.csv', engine='python')  # load data set
df = pd.read_csv('merged_times2.csv', engine='python')  # load data set

grp = df.groupby('parte_relac')[['tempo_entre_empenho_liquidacao',
                                 'tempo_entre_liquidacao_pagamento', 'tempo_entre_empenho_pagamento',
                                 'tempo_entre_homologacao_pagamento']].agg([np.mean, np.median, np.max, np.min]).T

# Analysis of Variance test
# references:
# https://machinelearningmastery.com/parametric-statistical-significance-tests-in-python/
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html
# https://www.statisticshowto.com/probability-and-statistics/f-statistic-value-test/

# generate three independent samples
data1 = df[df.parte_relac == 0]['tempo_entre_empenho_liquidacao']
data2 = df[df.parte_relac == 1]['tempo_entre_empenho_liquidacao']
data3 = df[df.parte_relac == 0]['tempo_entre_liquidacao_pagamento']
data4 = df[df.parte_relac == 1]['tempo_entre_liquidacao_pagamento']
data5 = df[df.parte_relac == 0]['tempo_entre_empenho_pagamento']
data6 = df[df.parte_relac == 1]['tempo_entre_empenho_pagamento']
data7 = df[df.parte_relac == 0]['tempo_entre_homologacao_pagamento']
data8 = df[df.parte_relac == 1]['tempo_entre_homologacao_pagamento']

first = data7
sec = data8

# summarize
print('tempo_entre_liquidacao_pagamento\n')
print('parte_relac = 0: mean=%.2f stdv=%.2f' % (np.mean(first), np.std(first)))
print('parte_relac = 1: mean=%.2f stdv=%.2f\n' % (np.mean(sec), np.std(sec)))
# compare samples
stat, p = f_oneway(first, sec)
print('F Stat=%.3f, p=%.5f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
    print('Same distributions (fail to reject H0)')
else:
    print('Different distributions (reject H0)')

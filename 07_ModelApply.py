import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import unidecode  # remove special chars


def run_query(query):
    database = r"database_macae.db"
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    col_name_list = [i[0] for i in cur.description]
    df = pd.DataFrame(rows, columns=col_name_list)
    return df


query = """select * from merged_times2"""

df = run_query(query)

df = df[['tempo_entre_liquidacao_pagamento',
         'soma_de_percentual_de_doacao',
         'soma_de_percentual_de_despesas',
         'servidor_prefeitura',
         'filiado_partido',
         'ano',
         'natureza_da_despesa',
         'categoria_economica',
         'tipo_empenho',
         'valor_pago_y']]

df['natureza_da_despesa'] = df.natureza_da_despesa.fillna('-')
df['categoria_economica'] = df.categoria_economica.fillna('-')

for i in df:
    df[i] = [unidecode.unidecode(str(j)) for j in df[i]]


def generate_dummies(dataframe, cols=[], drop_first=0):
    for k in cols:
        dummies = pd.get_dummies(dataframe[k], drop_first=drop_first)
        df = dataframe.drop(columns=k)
        df = df.join(dummies)
    return df


X = df[['soma_de_percentual_de_doacao',
        'soma_de_percentual_de_despesas',
        'servidor_prefeitura',
        'filiado_partido']]

y = df['tempo_entre_liquidacao_pagamento']

# Split the data into training/testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

regr = LinearRegression()

# Train the model using the training sets
regr.fit(X_train, y_train)

# Make predictions using the testing set
y_pred = regr.predict(X_test)

# The coefficients
print('Intercept: %.4f' % regr.intercept_)
# print('Coefficients: ', regr.coef_)
print('Coefficients: ')
print(dict(zip(X_train, [round(i, 2) for i in regr.coef_])))
# The mean squared error
print('Mean squared error: %.2f' % mean_squared_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print('Coefficient of determination (r2): %.2f' % r2_score(y_test, y_pred))



#############################################
#CHECKING LINEAR REGRESSION ASSUMPTIONS
#############################################

# LINEARITY
# Normality of the Error Terms
# No Multicollinearity among Predictors
# No Autocorrelation of the Error Terms
# Homoscedasticity

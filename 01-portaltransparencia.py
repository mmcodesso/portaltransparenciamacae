from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import pandas as pd


url_home = "http://sistemas.macae.rj.gov.br/transparencia/index.asp?acao=3&item=10"

# Creating drive
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
#options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(chrome_options=options)

url = url_home

# getting url

driver.get(url)


#Informa Ano na tela inicial
year = "2015|DW_LC131_FC_2|" #O ano no site é uma string
year = "2015" #O ano no site é uma string
initial_date = '01/01/2015'
final_date = '31/12/2015'

cmbAno_field = driver.find_element_by_id('cmbAno')
cmbAno_field.send_keys(year)

#Informa Data Inicial
initial_date_field = driver.find_element_by_id('txtDataInicial')
initial_date_field.clear()
initial_date_field.send_keys(initial_date)

#Informa Data Final
initial_date_field = driver.find_element_by_id('txtDataFinal')
initial_date_field.clear()
initial_date_field.send_keys(final_date)

#Cliba no botao Gerar
gerar_buton = driver.find_element_by_id('confirma')
gerar_buton.click()


page = BeautifulSoup(driver.page_source, 'lxml')

#acha a tabela dos credores
table = page.find('table', id='tbTabela')

tabela_df = pd.read_html(str(table))
tabela_df = tabela_df[0]
tabela_df.to_csv('credores.csv',mode='a')

credores = tabela_df[('Credores',                'Nome')]
credor = credores[10]

def goto_companies_documents(company_name):
    driver.find_element_by_link_text(company_name).click()
    #wait = WebDriverWait(driver, explicit_wait)
    #wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'LegendaPequenaC')))
    return

goto_companies_documents(credor)
#Terceira tela
page3 = BeautifulSoup(driver.page_source, 'lxml')
table2 = page3.find('table', id='tbTabela1')
empenho_df = pd.read_html(str(table2))
empenho_df = empenho_df[0]

numero_empenho = empenho_df[('Credores Empenho',       'Orçamentário',    'Número do Empenho')]
#todo converter inger

numero_empenho = '001175'

goto_companies_documents(numero_empenho)

#detalhe Empenho
lista_detalhe_empenho = []
page_detalhe_empenho = BeautifulSoup(driver.page_source, 'lxml')
table_empenho = page_detalhe_empenho.find_all('table', id='tbEmpenho')
lista_detalhe_empenho.append(table_empenho)


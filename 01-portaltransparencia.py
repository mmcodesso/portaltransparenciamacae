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

def download_empenho():

    page = BeautifulSoup(driver.page_source, 'lxml')
    table = page.find('table', id='tbTabela')

    tabela_df = pd.read_html(str(table))
    tabela_df = tabela_df[0]
    tabela_df.to_csv('credores.csv',mode='a')

    credores = tabela_df[('Credores',                'Nome')]
    credorteste = credores[10]
    credores = credores[10]


    for credor in credores:

        def goto_companies_documents(company_name):
            driver.find_element_by_link_text(company_name).click()
            #wait = WebDriverWait(driver, explicit_wait)
            #wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'LegendaPequenaC')))
            return

        print(credorteste)
        goto_companies_documents(credorteste)
        #Terceira tela
        page3 = BeautifulSoup(driver.page_source, 'lxml')
        table2 = page3.find('table', id='tbTabela1')
        empenho_df = pd.read_html(str(table2))
        empenho_df = empenho_df[0]
        empenho_df = empenho_df[:-1] #remove a ultima linha com totais

        numero_empenho = empenho_df[('Credores Empenho',       'Orçamentário',    'Número do Empenho')]
        #todo converter inger

        numero_empenho = ['001175','001032','001019','000765','000735']

        goto_companies_documents(numero_empenho)

        #detalhe Empenho
        lista_detalhe_empenho = []
        for empenho in numero_empenho:
            goto_companies_documents(empenho)
            page_detalhe_empenho = BeautifulSoup(driver.page_source, 'lxml')
            table_empenho = page_detalhe_empenho.find('table', id='tbEmpenho')
            lista_detalhe_empenho.append(table_empenho)

            #clica no botao voltar
            driver.find_element_by_xpath('//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]').click()

        empenho_df[('Credores Empenho',       'Orçamentário',    'detalhe do empenho')] = lista_detalhe_empenho

        #volta tela para lista de credores
        driver.find_element_by_xpath('//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]').click()


    #Avanca para a proxima pagina
    try:
        goto_companies_documents('Próxima página')
        #TODO Chamar a funcao novamente
        download_empenho()
    except:
        print('nao existem mais empenhos')

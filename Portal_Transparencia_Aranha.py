# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time


def set_initial_page(year, initial_date, final_date, driver):

    # Set year field
    cmb_ano_field = Select(driver.find_element_by_id('cmbAno'))
    cmb_ano_field.select_by_visible_text(year)

    # Set Initial_date
    initial_date_field = driver.find_element_by_id('txtDataInicial')
    initial_date_field.clear()
    initial_date_field.send_keys(initial_date)

    # set final_date
    initial_date_field = driver.find_element_by_id('txtDataFinal')
    initial_date_field.clear()
    initial_date_field.send_keys(final_date)

    # confirm
    gerar_button = driver.find_element_by_id('confirma')
    gerar_button.click()
    return


def goto_companies_documents(company_name):
    try:
        link = driver.find_element_by_link_text(company_name)
        link.click()
    except:
        pass
    return


def download_tabela_empenho(driver, year, pag_atual=True, last_credor=True):
    page = BeautifulSoup(driver.page_source, 'lxml')
    table = page.find('table', id='tbTabela')

    tabela_credores_site = pd.read_html(str(table), header=1)[0]
    tabela_credores_site['ano'] = year
    tabela_credores_site['download_status'] = 0

    try:
        credores_pagina = tabela_credores_site.Nome
    except:
        pass

    try:
        tabela_credores = pd.read_csv('credores_'+str(year)+'.csv')
        tabela_credores_site = tabela_credores_site[~tabela_credores_site.Nome.isin(tabela_credores.Nome)]
        tabela_credores_site = tabela_credores.append(tabela_credores_site, sort=True)
    except:
        pass

    tabela_credores_site.to_csv('credores_'+str(year)+'.csv', index=0)

    if pag_atual:
        credores = tabela_credores_site[(tabela_credores_site.Nome.isin(credores_pagina))
                                        &(tabela_credores_site.download_status == 0)].Nome
    else:
        credores = tabela_credores_site[(tabela_credores_site.download_status == 0)].Nome

    for i, credor in enumerate(credores):
        try:
            goto_companies_documents(credor)
            page_empenhos = BeautifulSoup(driver.page_source, 'lxml')
        except:
            continue
        try:
            table_empenhos = page_empenhos.find('table', id='tbTabela1')
            empenho_df = pd.read_html(str(table_empenhos), header=1, skiprows=1, converters={'Número do Empenho': str})
        except:
            try:
                table_empenhos = page_empenhos.find('table', id='tbTabela2')
                empenho_df = pd.read_html(str(table_empenhos), header=1, converters={'Número do Empenho': str})
            except:
                driver.find_element_by_xpath('//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]').click()
                continue
        empenho_df = empenho_df[0]
        empenho_df = empenho_df[:-1]  # remove a ultima linha com totais
        empenho_df = empenho_df[['Data Emissão Empenho', 'Número do Empenho', 'Unidade Gestora',
                                 'Credor', 'Valor Empenhado', 'Valor Em Liquidação', 'Valor Liquidado',
                                 'Valor Pago', 'Valor Anulado']]

        numeros_empenhos = empenho_df['Número do Empenho']

        lista_detalhe_empenho = []

        for empenho in numeros_empenhos:
            goto_companies_documents(empenho)
            page_detalhe_empenho = BeautifulSoup(driver.page_source, 'lxml')
            table_det_empenho = page_detalhe_empenho.find('table', id='tbEmpenho')
            lista_detalhe_empenho.append(table_det_empenho)
            voltar = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]')))
            voltar.click()

        empenho_df['detalhe_empenho'] = lista_detalhe_empenho
        voltar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]')))
        voltar.click()

        try:
            export_df = export_df.append(empenho_df, sort=True)
        except:
            export_df = empenho_df

        tabela_credores['download_status'] = np.where((tabela_credores.Nome == credor), 1, tabela_credores.download_status)
        tabela_credores.to_csv('credores_' + str(year) + '.csv', index=0)

        # exportando tabela com os empenhos
        try:
            export_df_local = pd.read_csv('credores_empenhos_' + str(year) + '.csv')
            export_df_local = export_df_local.append(export_df, sort=True)
            export_df_local = export_df_local.drop_duplicates(keep='first')
            export_df_local.to_csv('credores_empenhos_' + str(year) + '.csv', index=0)
            # export_df_local.to_json('credores_empenhos_' + str(year) + '.json')
        except:
            export_df = export_df.drop_duplicates(keep='first')
            export_df.to_csv('credores_empenhos_' + str(year) + '.csv', index=0)
            # export_df.to_json('credores_empenhos_' + str(year) + '.json')

    return


def check_exists_next_page():
    try:
        driver.find_element_by_link_text('Próxima página')
    except:
        return False
    return True


def main(url):
    print('Processo Iniciado ---- ' + time.ctime(time.time()))
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    # options.add_argument('--headless')

    driver = webdriver.Chrome(options=options,
                          executable_path='/home/rsa/PycharmProjects/selenium/portaltransparenciamacae/chromedriver')
    # driver.implicitly_wait(10)  # seconds

    # Open Chrome
    time.sleep(5)
    driver.get(url)
    time.sleep(5)
    # Set initial Page information
    set_initial_page(year, initial_date, final_date, driver)

    pag = 1
    while check_exists_next_page():
        time.sleep(5)
        download_tabela_empenho(driver, year)
        time.sleep(5)
        goto_companies_documents('Próxima página')
        pag += 1
        print('Passou para página ',pag)
    else:
        download_tabela_empenho(driver, year)
        print('Não existem mais empenhos ---- ' + time.ctime(time.time()))

    # Close Chrome
    driver.close()

    return


if __name__ == "__main__":
    # year = ["2015", "2014", "2013", "2012", "2011", "2010", "2018", "2017", "2016"]
    year = '2015'
    initial_date = '01/01/2015'
    final_date = '31/12/2015'
    url_home = "http://sistemas.macae.rj.gov.br/transparencia/index.asp?acao=3&item=10"
    url = url_home
    main(url)

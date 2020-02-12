# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import sys


def set_initial_page(ano, dt_inicio, dt_fim, drvr):

    # Set ano field
    cmb_ano_field = Select(drvr.find_element_by_id('cmbAno'))
    cmb_ano_field.select_by_visible_text(ano)

    # Set Initial_date
    initial_date_field = drvr.find_element_by_id('txtDataInicial')
    initial_date_field.clear()
    initial_date_field.send_keys(dt_inicio)

    # set final_date
    initial_date_field = drvr.find_element_by_id('txtDataFinal')
    initial_date_field.clear()
    initial_date_field.send_keys(dt_fim)

    # confirm
    gerar_button = drvr.find_element_by_id('confirma')
    gerar_button.click()
    return


def goto_companies_documents(drvr, company_name):
    link = drvr.find_element_by_link_text(company_name)
    link.click()
    return


def download_tabela_empenho(driver, ano, pag_atual=True):
    page = BeautifulSoup(driver.page_source, 'lxml')
    table = page.find('table', id='tbTabela')

    tabela_credores_site = pd.read_html(str(table), header=1)[0]
    tabela_credores_site['ano'] = ano
    tabela_credores_site['download_status_liquida'] = 0
    tabela_credores_site.download_status_liquida = \
        tabela_credores_site.download_status_liquida.mask(tabela_credores_site['Valor Liquidado'] == 'R$ 0,00', other=2)

    credores_pagina = tabela_credores_site[tabela_credores_site.download_status_liquida == 0].Nome

    try:
        tabela_credores = pd.read_csv('credores_V2_' + str(ano) + '.csv', delimiter='\t')
        tabela_credores_site = tabela_credores_site[~tabela_credores_site.Nome.isin(tabela_credores.Nome)]
        tabela_credores_site = tabela_credores.append(tabela_credores_site, sort=True)
    except Exception:
        pass

    if pag_atual:
        credores = tabela_credores_site[(tabela_credores_site.Nome.isin(credores_pagina))
                                        & (tabela_credores_site.download_status_liquida == 0)].Nome
    else:
        credores = tabela_credores_site[(tabela_credores_site.download_status_liquida == 0)].Nome

    for i, credor in enumerate(credores):
        try:
            goto_companies_documents(driver, credor)
            print('----> credor atual: ' + credor, end="\r")
            page_empenhos = BeautifulSoup(driver.page_source, 'lxml')
        except Exception:
            continue

        try:
            table_empenhos = page_empenhos.find('table', id='tbTabela1')
            empenho_df = pd.read_html(str(table_empenhos), header=1, skiprows=1, converters={'Número do Empenho': str})
        except Exception:
            try:
                table_empenhos = page_empenhos.find('table', id='tbTabela2')
                empenho_df = pd.read_html(str(table_empenhos), header=1, converters={'Número do Empenho': str})
            except Exception:
                tabela_credores_site['download_status_liquida'] = np.where((tabela_credores_site.Nome == credor), 2,
                                                                           tabela_credores_site.download_status_liquida)
                tabela_credores_site.to_csv('credores_V2_' + str(ano) + '.csv', index=0, sep="\t")
                driver.find_element_by_xpath('//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]').click()
                time.sleep(5)
                continue

        empenho_df = empenho_df[0]
        empenho_df = empenho_df[:-1]  # remove a ultima linha com totais

        numeros_empenhos = empenho_df['Número do Empenho']

        table_detalhe_liquida = pd.DataFrame()
        table_detalhe_pag = pd.DataFrame()

        if numeros_empenhos.any():
            for empenho in numeros_empenhos:
                goto_companies_documents(driver, empenho)
                page_detalhe_empenho = BeautifulSoup(driver.page_source, 'lxml')
                relevant_tables = page_detalhe_empenho.find_all('table', id='tbTabela')

                for j in relevant_tables:
                    if j.find('div', attrs={'style': "text-align:center;"}).text == 'Liquidações':
                        table_temp_liquida = pd.read_html(str(j), header=1)[0]
                        table_temp_liquida['empenho'] = empenho
                        table_temp_liquida['credor'] = credor
                        table_detalhe_liquida = table_detalhe_liquida.append(table_temp_liquida, sort=True)
                        del table_temp_liquida
                    elif j.find('div', attrs={'style': "text-align:center;"}).text == 'Pagamentos':
                        table_temp_pag = pd.read_html(str(j), header=1)[0]
                        table_temp_pag['empenho'] = empenho
                        table_temp_pag['credor'] = credor
                        table_detalhe_pag = table_detalhe_pag.append(table_temp_pag, sort=True)
                        del table_temp_pag

                driver.find_element_by_xpath('//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]').click()
                time.sleep(5)

            driver.find_element_by_xpath('//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]').click()
            time.sleep(5)

        table_detalhe_liquida.to_csv('credores_liquidacoes_' + str(ano) + '.csv', index=0, mode='a', sep="\t")
        table_detalhe_pag.to_csv('credores_pagamentos_' + str(ano) + '.csv', index=0, mode='a', sep="\t")

        tabela_credores_site['download_status_liquida'] = np.where((tabela_credores_site.Nome == credor), 1,
                                                                   tabela_credores_site.download_status_liquida)

        tabela_credores_site.to_csv('credores_V2_' + str(ano) + '.csv', index=0, sep="\t")

    return


def check_exists_next_page(drvr):
    try:
        drvr.find_element_by_link_text('Próxima página')
    except Exception:
        return False
    return True


def get_current_page(drvr):
    try:
        elem = drvr.find_element_by_id('txtPaginacao')
        curr_page = elem.get_attribute('innerHTML')
        return curr_page
    except Exception:
        print('Não foi possível obter a página atual.')
    return


def main():
    print('Processo Iniciado ---- ' + time.ctime(time.time()))
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)  # run if chromedriver is in PATH

    # driver = webdriver.Chrome(options=options,
    #                          executable_path='/home/rsa/PycharmProjects/ebape/portaltransparenciamacae/chromedriver')

    # Open Chrome and set initial page information
    driver.get(url)
    set_initial_page(year, initial_date, final_date, driver)

    while check_exists_next_page(driver):
        download_tabela_empenho(driver, year)
        goto_companies_documents(driver, 'Próxima página')
        print(get_current_page(driver) + ' ---- ' + time.ctime(time.time()))
    else:
        download_tabela_empenho(driver, year)
        print('Não existem mais empenhos ---- ' + time.ctime(time.time()))
        driver.close()
    return

if __name__ == "__main__":
    try:
        year = sys.argv[1]
        initial_date = '01/01/'+str(year)
        final_date = '31/12/'+str(year)
        url_home = "http://sistemas.macae.rj.gov.br/transparencia/index.asp?acao=3&item=10"
        url = url_home
        main()
    except:
        print('\nErro no processamento - ' + time.ctime(time.time()))

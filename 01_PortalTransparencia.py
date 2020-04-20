# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import sys
from webdriver_manager.chrome import ChromeDriverManager

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
    tabela_credores_site['download_status'] = 0

    credores_pagina = tabela_credores_site.Nome

    try:
        tabela_credores = pd.read_csv('credores_' + str(ano) + '.csv', sep="\t")
        tabela_credores_site = tabela_credores_site[~tabela_credores_site.Nome.isin(tabela_credores.Nome)]
        tabela_credores_site = tabela_credores.append(tabela_credores_site, sort=True)
        tabela_credores_site.to_csv('credores_' + str(ano) + '.csv', index=0, sep="\t")
    except Exception:
        tabela_credores_site.to_csv('credores_' + str(ano) + '.csv', index=0, sep="\t")

    if pag_atual:
        credores = tabela_credores_site[(tabela_credores_site.Nome.isin(credores_pagina))
                                        & (tabela_credores_site.download_status == 0)].Nome
    else:
        credores = tabela_credores_site[(tabela_credores_site.download_status == 0)].Nome

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
                tabela_credores_site['download_status'] = np.where((tabela_credores_site.Nome == credor), 2,
                                                                   tabela_credores_site.download_status)
                tabela_credores_site.to_csv('credores_' + str(ano) + '.csv', index=0, sep="\t")
                driver.find_element_by_xpath('//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]').click()
                time.sleep(5)
                continue

        empenho_df = empenho_df[0]
        empenho_df = empenho_df[:-1]  # remove a ultima linha com totais
        empenho_df = empenho_df[['Data Emissão Empenho', 'Número do Empenho', 'Unidade Gestora',
                                 'Credor', 'Valor Empenhado', 'Valor Em Liquidação', 'Valor Liquidado',
                                 'Valor Pago', 'Valor Anulado']]

        numeros_empenhos = empenho_df['Número do Empenho']

        lista_detalhe_empenho = []

        if numeros_empenhos.any():
            for empenho in numeros_empenhos:
                goto_companies_documents(driver, empenho)
                page_detalhe_empenho = BeautifulSoup(driver.page_source, 'lxml')
                table_det_empenho = page_detalhe_empenho.find('table', id='tbEmpenho')
                lista_detalhe_empenho.append(table_det_empenho)
                driver.find_element_by_xpath('//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]').click()
                time.sleep(5)

        driver.find_element_by_xpath('//*[@id="tbAtualizacao"]/tbody/tr[2]/td/input[1]').click()
        time.sleep(5)

        empenho_df['detalhe_empenho'] = lista_detalhe_empenho

        try:
            export_df = export_df.append(empenho_df, sort=True)
        except Exception:
            export_df = empenho_df

        tabela_credores_site['download_status'] = np.where((tabela_credores_site.Nome == credor), 1,
                                                           tabela_credores_site.download_status)
        tabela_credores_site.to_csv('credores_' + str(ano) + '.csv', index=0, sep="\t")

        # exportando tabela com os empenhos
        try:
            export_df_local = pd.read_csv('credores_empenhos_' + str(ano) + '.csv', sep="\t")
            export_df_local = export_df_local.append(export_df, sort=True)
            export_df_local = export_df_local.drop_duplicates(keep='first')
            export_df_local.to_csv('credores_empenhos_' + str(ano) + '.csv', index=0, sep="\t")
        except Exception:
            export_df = export_df.drop_duplicates(keep='first')
            export_df.to_csv('credores_empenhos_' + str(ano) + '.csv', index=0, sep="\t")

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
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    # driver = webdriver.Chrome(options=options)  # run if chromedriver is in PATH
    # driver = webdriver.Chrome(options=options, executable_path='/Users/renatoaranha/PycharmProjects/webdriver')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

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
        # Close Chrome
        driver.close()

    return


if __name__ == "__main__":
    try:
        year = sys.argv[1]
        # year = '2019'
        initial_date = '01/01/'+str(year)
        final_date = '31/12/'+str(year)
        url_home = "http://sistemas.macae.rj.gov.br/transparencia/index.asp?acao=3&item=10"
        url = url_home
        main()
    except:
        print('\nInformar ano desejado. - ' + time.ctime(time.time()))

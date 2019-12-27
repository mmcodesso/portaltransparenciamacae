from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_number_of_pages():
    html_list = driver.find_element_by_xpath('//*[@id="tb-result_paginate"]/div/ul')
    last = html_list.find_elements_by_tag_name("li")[-2].text
    last = int(last)
    return last


def goto_next_page():
    try:
        elem = driver.find_element_by_link_text('Próximo')
        elem.click()
    except:
        pass
    return


def get_one_table():
    page = BeautifulSoup(driver.page_source, 'lxml')
    element = page.find(id='tb-result_wrapper')
    table = pd.read_html(str(element))[0]
    return table


def get_full_table():
    full_table = pd.DataFrame()
    last = get_number_of_pages()
    for i in range(last):
        one_table = get_one_table()
        full_table = full_table.append(one_table)
        goto_next_page()
        time.sleep(1)
    return full_table


def main():
    print('Processo Iniciado ---- ' + time.ctime(time.time()))
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    # options.add_argument('--headless')

    driver = webdriver.Chrome(options=options,
                              executable_path='/home/rsa/PycharmProjects/selenium/portaltransparenciamacae/chromedriver')
    driver.implicitly_wait(10)  # seconds

    # Open Chrome
    driver.get(url_contratos)
    button = driver.find_element_by_id('btn-buscar')
    button.click()
    full_table = get_full_table()
    print('Captura finalizada ---- ' + time.ctime(time.time()))
    full_table.to_csv('full_table_contratos.csv', index=0)
    return


if __name__ == "__main__":
    url_contratos = "http://sistemas.macae.rj.gov.br:84/transparencia/contratacoes/contratos"
    url = url_contratos
    main()
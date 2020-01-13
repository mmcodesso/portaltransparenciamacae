from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_number_of_pages(driver):
    expand = Select(driver.find_element_by_name('tb-result_length'))
    expand.select_by_visible_text(str(100))
    html_list = driver.find_element_by_xpath('//*[@id="tb-result_paginate"]/div/ul')
    last = html_list.find_elements_by_tag_name("li")[-2].text
    last = int(last)
    return last


def goto_next_page(driver):
    try:
        elem = driver.find_element_by_link_text('Próximo')
        elem.click()
    except:
        pass
    return


def get_one_table(driver):
    lista_id = []
    page = BeautifulSoup(driver.page_source, 'lxml')
    element = page.find(id='tb-result')
    table = pd.read_html(str(element))[0]

    temp = element.find_all('tr')
    for i in range(len(temp)):
        if i > 0:
            id = temp[i]['id']
            lista_id.append(id)
    table['link_id'] = lista_id
    table['url'] = table.link_id.apply(
        lambda x: 'http://sistemas.macae.rj.gov.br:84/transparencia/default/contratacoes/mostrarcontratos?id=' + str(x))
    return table


def get_full_table(driver):
    full_table = pd.DataFrame()
    last = get_number_of_pages(driver)
    for i in range(last):
        one_table = get_one_table(driver)
        full_table = full_table.append(one_table)
        goto_next_page(driver)
        time.sleep(1)
    return full_table


def main():
    print('Processo Iniciado ---- ' + time.ctime(time.time()))
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    # options.add_argument('--headless')

    driver = webdriver.Chrome(
        options=options,
        executable_path='/home/rsa/PycharmProjects/ebape/portaltransparenciamacae/chromedriver')
    driver.implicitly_wait(10)  # seconds

    # Open Chrome
    time.sleep(5)
    driver.get(url)
    time.sleep(5)
    button = driver.find_element_by_xpath('//*[@id="btn-buscar"]')
    button.click()
    full_table = get_full_table(driver)
    print('Captura finalizada ---- ' + time.ctime(time.time()))
    full_table.to_csv('full_table_contratos.csv', index=0)

    driver.close()

    return


if __name__ == "__main__":
    url_contratos = "http://sistemas.macae.rj.gov.br:84/transparencia/contratacoes/contratos"
    url = url_contratos
    main()

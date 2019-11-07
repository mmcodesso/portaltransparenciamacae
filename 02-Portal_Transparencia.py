from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

url_home = "http://sistemas.macae.rj.gov.br/transparencia/index.asp?acao=3&item=10"


def set_initial_page(year,initial_date,final_date,driver):

    #Set year field
    cmbAno_field = driver.find_element_by_id('cmbAno')
    cmbAno_field.send_keys(year)

    # Set  Initial_date
    initial_date_field = driver.find_element_by_id('txtDataInicial')
    initial_date_field.clear()
    initial_date_field.send_keys(initial_date)

    # set final_date
    initial_date_field = driver.find_element_by_id('txtDataFinal')
    initial_date_field.clear()
    initial_date_field.send_keys(final_date)

    #confirm
    gerar_buton = driver.find_element_by_id('confirma')
    gerar_buton.click()
    return


def main(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    #Open Chrome
    driver.get(url)

    #Set initial Page information
    set_initial_page(year,inicial_date,final_date,driver)


    #Close Chrome

    driver.close()


if __name__ == "__main__":
    #explicit_wait = 3
    year = "2015"
    inicial_date = '01/01/2015'
    final_date = '31/12/2015'
    url = url_home

    main(url)

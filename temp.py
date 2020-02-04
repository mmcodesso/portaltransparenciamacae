# -*- coding: utf-8 -*-


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

def main():
    print('Processo Iniciado ---- ' + time.ctime(time.time()))
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')

    driver = webdriver.Chrome(
        options=options,
        executable_path='/home/rsa/PycharmProjects/ebape/portaltransparenciamacae/chromedriver')

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
        initial_date = '01/01/'+str(year)
        final_date = '31/12/'+str(year)
        url_home = "http://sistemas.macae.rj.gov.br/transparencia/index.asp?acao=3&item=10"
        url = url_home
        main()
    except:
        print('\nInformar ano desejado.\n')
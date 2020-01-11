import pandas as pd
from requests_html import HTMLSession
import urllib.request
import shutil


def get_url_pdfs(contratos):
    links_pdfs = []
    links_outros = []
    urls = contratos.url

    for i in urls:
        session = HTMLSession()
        r = session.get(i)
        pdf = [j for j in sorted(r.html.links) if '.pdf' in str(j) and '/contrato/' in str(j)]
        if pdf:
            one_pdf = 'http://sistemas.macae.rj.gov.br:84' + str(pdf[0])
            links_pdfs.append(one_pdf)
        else:
            links_pdfs.append('-')
            links_outros.append(i)
    return links_pdfs, links_outros


def download_file(url, path='./'):
    file_name = path + url.split('/')[-1]
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return file_name


def main():
    contratos = pd.read_csv('full_table_contratos.csv')
    links_pdfs, links_outros = get_url_pdfs(contratos)
    contratos['pdf_url_contrato'] = links_pdfs
    contratos['pdf_file_contrato'] = [i.split('/')[-1] for i in links_pdfs]
    contratos.to_csv('full_table_contratos.csv')

    for i in links_pdfs:
        download_file(i, path=folder)


if __name__ == "__main__":
    folder = './contratos/'
    main()

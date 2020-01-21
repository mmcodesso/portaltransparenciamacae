import re
import operator
import pandas as pd
from docx import Document
from tqdm import tqdm


def get_text(filename):
    file = Document(filename)
    full_text = []
    for i in file.paragraphs:
        full_text.append(i.text)
    doc = '\n'.join(full_text)
    return doc


def get_names(doc, only_first_page=True):
    """
    Captura expressões em maiúsculo, entre vírgulas, aceitando acentuação (regex1 = r',\s([A-ZÀ-Ú\s]+),') E
        em maiúsculo, entre Sr. e vírgula, aceitando acentuação regex2 = r'\Sr.\s([A-ZÀ-Ú\s]+),' E
        em maiúsculo, entre Sra. e vírgula, aceitando acentuação regex3 = r'\Sra.\s([A-ZÀ-Ú\s]+),'.
    Assume-se que estas regras capturem todos os nomes de pessoas presentes no documento.
    :param doc: documento gerado função que mapeia DOCX (get_text)
    :param only_first_page: flag para indicar se é para pegar apenas a primeira página do documento (proxy: 3000 chars)
    :return: lista com os nomes encontrados
    """
    nomes_bruto = re.findall(r',\s([A-ZÀ-Ú\s]+),|\Sr.\s([A-ZÀ-Ú\s]+),|\Sra.\s([A-ZÀ-Ú\s]+),', doc)
    nomes, places = [], [] # lista places é para capturar o indice do termo, no texto
    for i in nomes_bruto:
        if i[0]:
            if 6 > len(i[0].split()) > 1:
                nomes.append(i[0])
                places.append(doc.find(i[0]))
        else:
            if 6 > len(i[1].split()) > 1:
                nomes.append(i[1])
                places.append(doc.find(i[1]))
    nomes = [i.rstrip().replace('\n', ' ').replace('\r', ' ') for i in nomes] # the replaces here are for removing line breaks
    names_and_places = dict(zip(nomes, places))

    if only_first_page: #
        new = dict()
        for (key, value) in names_and_places.items():
            if value < 3000:
                new[key] = value
        names_and_places = new
    names_and_places = dict(sorted(names_and_places.items(), key=operator.itemgetter(1)))
    return names_and_places


def get_cpf(doc, only_first_page=True):
    """
    Identifica os CPFs presentes no documento.
    :param doc: documento a ser consumido pela função que mapeia DOCX (get_text)
    :param only_first_page: flag para indicar se é para pegar apenas a primeira página do documento (proxy: 3000 chars)
    :return:
    """
    regex_cpf = r'\d{3}\.\d{3}\.\d{3}\-\d{2}'
    cpfs = re.findall(regex_cpf, doc)
    cpf, places = [], [] # lista places é para capturar o indice do termo, no texto

    for i in cpfs:
        cpf.append(i)
        places.append(doc.find(i))
    cpf_and_places = dict(zip(cpf, places))

    if only_first_page:
        new = dict()
        for (key, value) in cpf_and_places.items():
            if value < 3000:
                new[key] = value
        cpf_and_places = new
    cpf_and_places = dict(sorted(cpf_and_places.items(), key=operator.itemgetter(1)))
    return cpf_and_places


def get_cnpj(doc, only_first_page=True):
    """
    Identifica os CNPJs presentes no documento.
    :param doc: documento a ser consumido pela função que mapeia DOCX (get_text)
    :param only_first_page: flag para indicar se é para pegar apenas a primeira página do documento (proxy: 3000 chars)
    :return:
    """
    regex_cnpj = r'\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}'
    cnpj = re.findall(regex_cnpj, doc)
    cnp, places = [], [] # lista places é para capturar o indice do termo, no texto

    for i in cnpj:
        cnp.append(i)
        places.append(doc.find(i))
    cnp_and_places = dict(zip(cnp, places))

    if only_first_page:
        new = dict()
        for (key, value) in cnp_and_places.items():
            if value < 3000:
                new[key] = value
        cnp_and_places = new
    cnp_and_places = dict(sorted(cnp_and_places.items(), key=operator.itemgetter(1)))
    return cnp_and_places


def get_names_and_cpfs(doc, only_first_page=True):
    if only_first_page:
        nms = get_names(doc)
        cpfs = get_cpf(doc)
    else:
        nms = get_names(doc, False)
        cpfs = get_cpf(doc, False)

    junto = zip(nms, cpfs)
    full = dict(junto)
    return full


def generate_one_file_output(filename, only_first_page=True):
    doc = get_text(filename)
    out = get_names_and_cpfs(doc, only_first_page)
    return out


def main():
    content = []
    for i in tqdm(numeros_contratos):
        try:
            filename = folder_contratos_docx + str(int(i)) + '.docx'
            item = generate_one_file_output(filename)
            content.append(item)
        except:
            content.append('{}')
            continue
    data = {'nro_contrato': list(numeros_contratos), 'content': list(content)}
    nomes_contratos = pd.DataFrame(data)
    nomes_contratos.to_csv("nomes_contratos.csv", index=0)
    return nomes_contratos


if __name__ == "__main__":
    contratos = pd.read_csv('full_table_contratos.csv')
    numeros_contratos = contratos['nro_contrato']
    folder_contratos_docx = '../contratos_word/'
    # filename = 'portaltransparenciamacae/sample2.docx'
    main()


"""
ranges = [(121, 21), (1000, 2429), (2545, 2575), (2640, 2686), (2890, 2890)]
postcode = 1200

for i, j in enumerate(ranges):
    if j[0] < postcode < j[1]:
        print(i)
"""

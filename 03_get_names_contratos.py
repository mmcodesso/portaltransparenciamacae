import re
import operator
from docx import Document


def get_text(filename):
    file = Document(filename)
    fullText = []
    for i in file.paragraphs:
        fullText.append(i.text)
    doc = '\n'.join(fullText)
    return doc


def get_names(doc, only_first_page=True):
    '''
    Captura expressões em maiúsculo, entre vírgulas, aceitando acentuação (regex1 = r',\s([A-ZÀ-Ú\s]+),') E
        em maiúsculo, entre Sr. e vírgula, aceitando acentuação regex2 = r'\Sr.\s([A-ZÀ-Ú\s]+),' E
        em maiúsculo, entre Sra. e vírgula, aceitando acentuação regex3 = r'\Sra.\s([A-ZÀ-Ú\s]+),'.
    Assume-se que estas regras capturem todos os nomes de pessoas presentes no documento.
    :param doc: documento a ser consumido pela função que mapeia DOCX (get_text)
    :param only_first_page: flag para indicar se é para pegar apenas a primeira página do documento (proxy: 3000 chars)
    :return: lista com os nomes encontrados
    '''
    nomes_bruto = re.findall(r',\s([A-ZÀ-Ú\s]+),|\Sr.\s([A-ZÀ-Ú\s]+),|\Sra.\s([A-ZÀ-Ú\s]+),', doc)
    nomes, places = [], [] # lista places é para capturar o indice do termo, no texto
    for i in nomes_bruto:
        if i[0]:
            if len(i[0].split()) > 1:
                nomes.append(i[0])
                places.append(doc.find(i[0]))
        else:
            if len(i[1].split()) > 1:
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
    '''
    Identifica os CPFs presentes no documento.
    :param doc: documento a ser consumido pela função que mapeia DOCX (get_text)
    :param only_first_page: flag para indicar se é para pegar apenas a primeira página do documento (proxy: 3000 chars)
    :return:
    '''
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
    '''
    Identifica os CNPJs presentes no documento.
    :param doc: documento a ser consumido pela função que mapeia DOCX (get_text)
    :param only_first_page: flag para indicar se é para pegar apenas a primeira página do documento (proxy: 3000 chars)
    :return:
    '''
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
        nms = get_names(doc, 0)
        cpfs = get_cpf(doc, 0)

    junto = zip(nms, cpfs)
    full = dict(junto)
    return full


def main(ofp=1):
    doc = get_text(filename)
    out = get_names_and_cpfs(doc, ofp)
    return print(out)


if __name__ == "__main__":
    filename = 'portaltransparenciamacae/sample2.docx'
    main()
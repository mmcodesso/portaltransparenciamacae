import re
import pandas as pd
from docx import Document

filename = 'portaltransparenciamacae/sample2.docx'

def get_text(filename):
    doc = Document(filename)
    fullText = []
    for i in doc.paragraphs:
        fullText.append(i.text)
    return '\n'.join(fullText)

doc = get_text(filename)

regex1 = r',\s([A-ZÀ-Ú\s]+),' # captura expressões em MAIÚSCULO e entre vírgulas e aceita acentuação
regex2 = r'\Sr.\s([A-ZÀ-Ú\s]+),' # captura expressões em MAIÚSCULO entre Sr. e vírgula e aceita acentuação
regex3 = r'\Sra.\s([A-ZÀ-Ú\s]+),' # captura expressões em MAIÚSCULO entre Sra. e vírgula e aceita acentuação

regex_cnpj = r'\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}'


def get_names(doc):
    nomes_bruto = re.findall(r',\s([A-ZÀ-Ú\s]+),|\Sr.\s([A-ZÀ-Ú\s]+),|\Sra.\s([A-ZÀ-Ú\s]+),', doc)
    nomes = []
    for i in nomes_bruto:
        if i[0]:
            if len(i[0].split()) > 1:
                nomes.append(i[0])
        else:
            if len(i[1].split()) > 1:
                nomes.append(i[1])
    return nomes


def get_cpf(doc):
    regex_cpf = r'\d{3}\.\d{3}\.\d{3}\-\d{2}'
    cpfs = re.findall(regex_cpf, doc)
    return cpfs


def get_cnpj(doc):
    regex_cnpj = r'\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}'
    cnpj = re.findall(regex_cnpj, doc)
    return cnpj
import re
import pandas as pd
from docx import Document

filename = 'portaltransparenciamacae/1574193595_sample2.docx'

def get_text(filename):
    doc = Document(filename)
    fullText = []
    for i in doc.paragraphs:
        fullText.append(i.text)
    return '\n'.join(fullText)

doc = get_text(filename)


regex_cpf = r'\d{3}\.\d{3}\.\d{3}\-\d{2}'
regex_cnpj = r'\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}'

re.findall(regex_cpf, doc)

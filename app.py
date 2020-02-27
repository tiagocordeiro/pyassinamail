import csv
import io
import re
from unicodedata import normalize

import jinja2
import requests
from dynaconf import settings

sheet_file_id = settings.FILE_ID


def gera_assinatura_html(file_id=sheet_file_id):
    file_id = file_id
    people_url = f"https://docs.google.com/spreadsheets/d/{file_id}/gviz/tq" \
                 f"?tqx=out:csv&sheet=people"
    people_file = requests.get(people_url)
    people_file.encoding = people_file.apparent_encoding
    people_file_io = io.StringIO(people_file.text, newline=None)

    company_url = f"https://docs.google.com/spreadsheets/d/{file_id}/gviz/tq" \
                  f"?tqx=out:csv&sheet=company"
    company_file = requests.get(company_url)
    company_file.encoding = company_file.apparent_encoding
    company_file_io = io.StringIO(company_file.text, newline=None)

    data = {}
    coluna = []
    linha = 0
    assinaturas = {'retorno': {'assinaturas': []}}

    people_data = csv.reader(people_file_io)
    company_data = list(csv.reader(company_file_io))
    company_dict = dict(zip(company_data[0], company_data[1]))
    company_site = company_dict['website'].split('//')[1]

    env = jinja2.Environment(autoescape=True)
    env.loader = jinja2.FileSystemLoader("templates/")
    template = env.get_template("assinatura.html")

    for row in people_data:
        if linha == 0:
            for col in row:
                data[col] = ''
                coluna.append(col)
        else:
            i = 0
            for col in row:
                data[coluna[i]] = col
                i = i + 1

            signature_name = name_normalizer(data['Nome'])
            nome_arquivo = remover_acentos(signature_name)
            arquivo_path = 'assinaturas/' + nome_arquivo + '.html'
            arquivo_assinatura = open(arquivo_path, 'w')
            arquivo_assinatura.write(template.render(company_site=company_site,
                                                     company=company_dict,
                                                     nome=data['Nome'],
                                                     cargo=data['Cargo'],
                                                     email=data['Email'],
                                                     ramal=data['Ramal'],
                                                     celular=data['Celular']))

            assinatura = (data['Nome'], data['Cargo'], data['Email'])
            assinaturas['retorno']['assinaturas'].append(assinatura)
        linha = linha + 1

    return assinaturas


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def name_normalizer(txt):
    signature_name = txt
    signature_name = re.sub(r'\s+', '', signature_name)
    return signature_name


if __name__ == '__main__':
    gera_assinatura_html()

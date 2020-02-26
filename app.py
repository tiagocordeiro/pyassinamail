import csv
import io
import re
from unicodedata import normalize

import jinja2
import requests

gsheet_file_id = "1Q6zlAQfVKr9Y7Hj2oRXLaWLuwefzc8f1PubEcE2B1gM"


def gera_assinatura_html(file_id=gsheet_file_id):
    file_id = file_id
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
    arquivo = requests.get(url)
    arquivo.encoding = arquivo.apparent_encoding
    env = jinja2.Environment(autoescape=True)
    env.loader = jinja2.FileSystemLoader("templates/")
    template = env.get_template("assinatura.html")
    arquivoio = io.StringIO(arquivo.text, newline=None)
    data = {}
    coluna = []
    linha = 0
    assinaturas = {'retorno': {'assinaturas': []}}

    dados_funcionarios = csv.reader(arquivoio)
    for row in dados_funcionarios:
        if linha == 0:
            for col in row:
                data[col] = ''
                coluna.append(col)
        else:
            i = 0
            for col in row:
                data[coluna[i]] = col
                i = i + 1

            nomeassinatura = data['Nome']
            nomeassinatura = re.sub(r'\s+', '', nomeassinatura)
            nomearquivo = remover_acentos(nomeassinatura)
            arquivo_path = 'assinaturas/' + nomearquivo + '.html'
            arquivo_assinatura = open(arquivo_path, 'w')
            arquivo_assinatura.write(template.render(data=data,
                                                     nome=data['Nome'],
                                                     cargo=data['Cargo'],
                                                     email=data['Email']))

            assinatura = (data['Nome'], data['Cargo'], data['Email'])
            assinaturas['retorno']['assinaturas'].append(assinatura)
        linha = linha + 1

    return assinaturas


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


if __name__ == '__main__':
    gera_assinatura_html()

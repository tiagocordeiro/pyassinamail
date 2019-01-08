from unicodedata import normalize
import requests
import jinja2
import csv
import io
import re
import json


gsheet_file_id = "1Q6zlAQfVKr9Y7Hj2oRXLaWLuwefzc8f1PubEcE2B1gM"


def gera_assinatura_html(file_id=gsheet_file_id):
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
    arquivo = requests.get(url)
    arquivo.encoding = arquivo.apparent_encoding
    env = jinja2.Environment()
    env.loader = jinja2.FileSystemLoader("templates/")
    template = env.get_template("assinatura.html")
    arquivoio = io.StringIO(arquivo.text, newline=None)
    data = {}
    coluna = []
    linha = 0
    retorno = {'retorno': {'assinaturas': []}}

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
            arquivo_assinatura = open('assinaturas/' + nomearquivo + '.html', 'w')
            arquivo_assinatura.write(
                template.render(data=data, nome=data['Nome'], cargo=data['Cargo'], email=data['Email']))

            # Se quiser imprimir na tela, remova o comentário na linha abaixo
            # print(template.render(data=data, nome=data['Nome'], cargo=data['Cargo'], email=data['Email']))
        linha = linha + 1

    return json.dumps(retorno)


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


if __name__ == '__main__':
    gera_assinatura_html()

import requests
import jinja2
import csv
import io
import re


def geraAssinaturaHTML():
    file_id = "1Q6zlAQfVKr9Y7Hj2oRXLaWLuwefzc8f1PubEcE2B1gM"
    url = "https://docs.google.com/spreadsheets/d/{0}/export?format=csv".format(file_id)
    arquivo = requests.get(url)
    arquivo.encoding = arquivo.apparent_encoding
    env = jinja2.Environment()
    env.loader = jinja2.FileSystemLoader("templates/")
    template = env.get_template("assinatura.html")
    arquivoio = io.StringIO(arquivo.text, newline=None)
    data = {}
    coluna = []
    linha = 0

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
            nomeassinatura = re.sub('ã','a', nomeassinatura)
            nomeassinatura = re.sub('é', 'e', nomeassinatura)
            # Caso queira testar a saída de texto remova o comentário da linha abaixo
            # print(nomeassinatura)
            nomearquivo = re.sub('[^A-Za-z0-9]+', '', nomeassinatura)
            arquivoAssinatura = open('assinaturas/' + nomearquivo + '.html', 'w')
            arquivoAssinatura.write(template.render(data=data, nome=data['Nome'], cargo=data['Cargo'], email=data['Email']))

            # Se quiser imprimir na tela, remova o comentário na linha abaixo
            # print(template.render(data=data, nome=data['Nome'], cargo=data['Cargo'], email=data['Email']))
        linha = linha + 1


if __name__ == '__main__':
    geraAssinaturaHTML()

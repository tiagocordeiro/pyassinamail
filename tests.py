import os
from click.testing import CliRunner

from .app import remover_acentos, gera_assinatura_html


def test_cria_arquivo(tmpdir):
    p = tmpdir.mkdir("sub").join("assinatura.html")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1


def test_remove_acentos():
    assert remover_acentos("Texto com açêntüs") == "Texto com acentus"
    assert remover_acentos("áéíóúâêîôûçüÁçÇ") == "aeiouaeioucuAcC"
    assert remover_acentos("àèìòùÀÈÌÒÙ") == "aeiouAEIOU"


def test_template_existe():
    template_file = os.path.isfile("templates/assinatura.html")
    assert template_file is True


def test_gera_assinaturas_html():
    assinaturas = gera_assinatura_html
    assert len(assinaturas.callback()['retorno']['assinaturas']) >= 1


def test_gera_assinaturas_html_com_click():
    runner = CliRunner()
    result = runner.invoke(gera_assinatura_html,
                           ['--template', 'assinatura.html'])
    assert not result.exception
    assert result.exit_code == 0

from .app import remover_acentos
import os


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
    assert template_file == True

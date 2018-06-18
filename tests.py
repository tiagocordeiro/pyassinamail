from .app import remover_acentos


def test_remove_acentos():
    assert remover_acentos("Texto com açêntüs") == "Texto com acentus"


def test_template_existe():
    pass
import re

def validar_senha(senha):
    return (
        len(senha) >= 8 and
        re.search(r"[A-Z]", senha) and
        re.search(r"[0-9]", senha)
    )

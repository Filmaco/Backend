import hashlib
import re

def validar_senha(senha):
    if len(senha) < 8:
        return False

    if not re.search(r"[A-Z]", senha):
        return False

    if not re.search(r"\d", senha): 
        return False

    return True

def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

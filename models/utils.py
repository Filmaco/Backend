import hashlib
import re
import bcrypt
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def validar_senha(senha):
    if len(senha) < 8:
        logger.error("Senha inválida: menor que 8 caracteres.")
        return False

    if not re.search(r"[A-Z]", senha):
        logger.error("Senha inválida: sem letra maiúscula.")
        return False

    if not re.search(r"\d", senha):
        logger.error("Senha inválida: sem número.")
        return False

    logger.info("Senha válida.")
    return True

def gerar_hash(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar_hash(senha_plain, senha_hash):
    return bcrypt.checkpw(senha_plain.encode(), senha_hash.encode())

def validar_campos_obrigatorios(dados, campos_obrigatorios):
    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] in [None, ""]:
            return {
                "status": 400,
                "mensagem": f"O campo '{campo}' é obrigatório."
            }

    return {
        "status": 200,
        "mensagem": "Todos os campos obrigatórios estão presentes."
    }

from models.usuario_model import (
    model_adicionar_usuario,
    model_editar_usuario,
    model_inativar_usuario
    )
from models.utils import gerar_hash  
from controllers.validacoes import validar_senha
from models.conection import get_connection
import jwt
from models.utils import verificar_hash
import logging
from models.utils import validar_campos_obrigatorios


logger = logging.getLogger(__name__)

SECRET_KEY = "minha_chave_secreta"

# criar usuario
def controller_criar_usuario(dados):
    campos_obrigatorios = [
        "nome_completo", "username", "email", "senha", "data_nascimento"
    ]
    validacao = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if validacao["status"] != 200:
        logger.error(f"Falha na criação do usuário: {validacao['mensagem']}")
        return validacao

    validacao_senha = validar_senha(dados['senha'])
    if not validacao_senha:
        logger.error("Falha ao criar usuário: senha inválida.")
        return {"status": 400, "mensagem": "Senha inválida. Deve conter pelo menos 8 caracteres, uma letra maiúscula e um número."}


    senha_hash = gerar_hash(dados['senha'])

    try:
        model_adicionar_usuario(
            nome_completo=dados["nome_completo"],
            username=dados["username"],
            email=dados["email"],
            senha=senha_hash,
            data_nascimento=dados["data_nascimento"],
            foto_perfil=dados.get("foto_perfil"),
            genero=dados.get("genero"),
            biografia=dados.get("biografia"),
            tipo=dados.get("tipo", "comum"),
            status=dados.get("status", "ativo")
        )
        logger.info(f"Usuário {dados['email']} criado com sucesso.")
        return {"status": 200, "mensagem": "Usuário criado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao criar usuário."}
 
 # atualizar usuario   
def controller_atualizar_usuario(usuario_id, dados):
    senha = dados.get("senha")
    senha = gerar_hash(senha) if senha else None

    try:
        model_editar_usuario(
            usuario_id=usuario_id,
            nome_completo=dados.get("nome_completo"),
            username=dados.get("username"),
            email=dados.get("email"),
            senha=senha,
            data_nascimento=dados.get("data_nascimento"),
            foto_perfil=dados.get("foto_perfil"),
            genero=dados.get("genero"),
            biografia=dados.get("biografia"),
            tipo=dados.get("tipo"),
            status=dados.get("status")
        )
        logger.info(f"Usuário {usuario_id} atualizado com sucesso.")
        return {"status": 200, "mensagem": "Usuário atualizado com sucesso"}
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao atualizar usuário."}

# inativar usuario
def controller_inativar_usuario(usuario_id, status):
    try:
        sucesso = model_inativar_usuario(usuario_id, status)
        if sucesso:
            logger.info(f"Usuário {usuario_id} inativado com sucesso.")
            return {"status": 200, "mensagem": "Usuário inativado com sucesso"}
        else:
            logger.error(f"Erro ao inativar usuário {usuario_id}.")
            return {"status": 400, "mensagem": "Erro ao inativar usuário"}
    except Exception as e:
        logger.error(f"Erro ao inativar usuário {usuario_id}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao inativar usuário."}
   
# listar usuarios 
def controller_listar_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        return usuarios

    except Exception as e:
        print("Erro ao listar usuários:", e)
        return []

    finally:
        cursor.close()
        conn.close()
  
# pegar usuario por email
def model_obter_usuario_por_email(email):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        return usuario

    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None

    finally:
        cursor.close()
        conn.close()
 
# realziar login por email
def controller_login(email, senha):
    usuario = model_obter_usuario_por_email(email)
    
    if not usuario:
        print("Usuário não encontrado")
        return None

    if not verificar_hash(senha, usuario['senha']):
        print("Senha inválida")
        return None

    token = jwt.encode({"usuario_id": usuario['usuario_id']}, SECRET_KEY, algorithm="HS256")
    return token     


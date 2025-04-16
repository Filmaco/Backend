from models.usuario_model import (
    model_adicionar_usuario,
    model_editar_usuario,
    model_inativar_usuario
    )
from models.utils import gerar_hash  
from controllers.validacoes import validar_senha
from models.conection import get_connection


def controller_criar_usuario(dados):
    senha_inicial = dados['senha']
    
    if not validar_senha(senha_inicial):
        print("Senha inválida. Deve conter pelo menos 8 caracteres, uma letra maiúscula e um número.")
        return

    senha = gerar_hash(senha_inicial)

    model_adicionar_usuario(
        nome_completo=dados["nome_completo"],
        username=dados["username"],
        email=dados["email"],
        senha=senha,
        data_nascimento=dados["data_nascimento"],
        foto_perfil=dados.get("foto_perfil"),
        genero=dados.get("genero"),
        biografia=dados.get("biografia"),
        tipo=dados.get("tipo", "comum"),
        status=dados.get("status", "ativo")
    )
    
def controller_atualizar_usuario(usuario_id, dados):
    senha = dados.get("senha")
    senha = gerar_hash(senha) if senha else None

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
    
def controller_inativar_usuario(usuario_id, status):
    sucesso = model_inativar_usuario(usuario_id, status)
    return sucesso
    
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
        


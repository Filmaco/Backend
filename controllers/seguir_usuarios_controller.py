from models.seguir__usuarios_model import (
    model_seguir_usuario, 
    model_ja_segue,
    model_deixar_de_seguir,
    model_listar_seguidores
    )

#seguir
def controller_seguir_usuario(seguidor_id: int, seguido_id: int):
    if seguidor_id == seguido_id:
        return {"status": 400, "mensagem": "Você não pode seguir a si mesmo."}

    if model_ja_segue(seguidor_id, seguido_id):
        return {"status": 400, "mensagem": "Você já segue este usuário."}

    try:
        model_seguir_usuario(seguidor_id, seguido_id)
        return {"status": 200, "mensagem": "Usuário seguido com sucesso."}
    except Exception as e:
        return {"status": 500, "mensagem": str(e)}

# deixar de seguir
from models.seguir__usuarios_model import model_deixar_de_seguir

def controller_deixar_de_seguir(seguidor_id: int, seguido_id: int):
    if seguidor_id == seguido_id:
        return {"status": 400, "mensagem": "Você não pode deixar de seguir a si mesmo."}

    if not model_ja_segue(seguidor_id, seguido_id):
        return {"status": 400, "mensagem": "Você não está seguindo este usuário."}

    try:
        model_deixar_de_seguir(seguidor_id, seguido_id)
        return {"status": 200, "mensagem": "Usuário deixado de seguir com sucesso."}
    except Exception as e:
        return {"status": 500, "mensagem": str(e)}

#listar seguidores por id
def controller_listar_seguidores(usuario_id: int):
    try:
        seguidores = model_listar_seguidores(usuario_id)
        return {"status": 200, "seguidores": seguidores}
    except Exception as e:
        return {"status": 500, "mensagem": str(e)}
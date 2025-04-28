from models.video_model import (
    model_adicionar_video,
    model_obter_video_por_id,
    model_atualizar_video,
    model_listar_videos_por_usuario,
    model_incrementar_visualizacoes,
    model_listar_videos_por_tipo
)
import logging
from models.utils import validar_campos_obrigatorios
from models.conection import get_connection

logger = logging.getLogger(__name__)

def controller_criar_video(dados):
    campos_obrigatorios = [
        "usuario_id", "nome", "genero", "duracao", "tipo", "link"
    ]
    
    validacao = validar_campos_obrigatorios(dados, campos_obrigatorios)
    if validacao["status"] != 200:
        logger.error(f"Falha na criação do vídeo: {validacao['mensagem']}")
        return validacao

    tipos_validos = ['curta-metragem', 'longa-metragem', 'documentário', 'clipe musical']
    if dados['tipo'] not in tipos_validos:
        logger.error(f"Tipo de vídeo inválido: {dados['tipo']}")
        return {"status": 400, "mensagem": "Tipo de vídeo inválido"}

    try:
        video_id = model_adicionar_video(
            usuario_id=dados["usuario_id"],
            nome=dados["nome"],
            genero=dados["genero"],
            duracao=dados["duracao"],
            tipo=dados["tipo"],
            link=dados["link"],
            descricao=dados.get("descricao"),
            tags=dados.get("tags")
        )
        
        if video_id:
            logger.info(f"Vídeo {video_id} criado com sucesso.")
            return {
                "status": 201,
                "mensagem": "Vídeo criado com sucesso",
                "video_id": video_id
            }
        else:
            logger.error("Erro ao criar vídeo.")
            return {"status": 500, "mensagem": "Erro ao criar vídeo"}
            
    except Exception as e:
        logger.error(f"Erro ao criar vídeo: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao criar vídeo"}

def controller_atualizar_video(video_id, dados):
    try:
        sucesso = model_atualizar_video(
            video_id=video_id,
            nome=dados.get("nome"),
            descricao=dados.get("descricao"),
            genero=dados.get("genero"),
            tags=dados.get("tags"),
            duracao=dados.get("duracao"),
            tipo=dados.get("tipo"),
            link=dados.get("link")
        )
        
        if sucesso:
            logger.info(f"Vídeo {video_id} atualizado com sucesso.")
            return {"status": 200, "mensagem": "Vídeo atualizado com sucesso"}
        else:
            logger.error(f"Erro ao atualizar vídeo {video_id}.")
            return {"status": 400, "mensagem": "Nenhum dado válido para atualização"}
            
    except Exception as e:
        logger.error(f"Erro ao atualizar vídeo {video_id}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao atualizar vídeo"}

def controller_obter_video_por_id(video_id):
    try:
        video = model_obter_video_por_id(video_id)
        if video:
            model_incrementar_visualizacoes(video_id)
            return {"status": 200, "data": video}
        else:
            return {"status": 404, "mensagem": "Vídeo não encontrado"}
    except Exception as e:
        logger.error(f"Erro ao buscar vídeo {video_id}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao buscar vídeo"}
    

def controller_listar_videos_por_tipo(tipo):
    try:
        videos = model_listar_videos_por_tipo(tipo)
        return {"status": 200, "data": videos}
    except Exception as e:
        logger.error(f"Erro ao listar vídeos do tipo {tipo}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar vídeos"}
    

def controller_listar_videos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM videos")
        videos = cursor.fetchall()

        return {"status": 200, "data": videos}

    except Exception as e:
        logger.error(f"Erro ao listar vídeos: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar vídeos"}

    finally:
        cursor.close()
        conn.close()


def controller_listar_videos_por_usuario(usuario_id):
    try:
        videos = model_listar_videos_por_usuario(usuario_id)
        return {"status": 200, "data": videos}
    except Exception as e:
        logger.error(f"Erro ao listar vídeos do usuário {usuario_id}: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao listar vídeos"}
    
def controller_incrementar_visualizacoes(video_id):
    try:
        sucesso = model_incrementar_visualizacoes(video_id)
        if sucesso:
            return {"status": 200, "mensagem": "Visualizações incrementadas"}
        else:
            return {"status": 400, "mensagem": "Erro ao incrementar visualizações"}
    except Exception as e:
        logger.error(f"Erro ao incrementar visualizações: {str(e)}")
        return {"status": 500, "mensagem": "Erro ao incrementar visualizações"}
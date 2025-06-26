from models.conection import get_connection
import logging

# usuario faz a denuncia
# id_usuario, id_video
def model_denunciar_conteudo(usuario_id, motivo, video_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO denuncias (usuario_id, motivo, video_id)
            VALUES (%s, %s, %s)
        """, (usuario_id, motivo, video_id))
        
        cursor.execute("""
            UPDATE videos
            SET status = 'investigando'
            WHERE video_id = %s
        """, (video_id,))

        conn.commit()
        return {"mensagem": "Denúncia registrada com sucesso."}

    except Exception as e:
        raise Exception(f"Erro ao registrar denúncia: {str(e)}")
    finally:
        cursor.close()
        conn.close()


# lista denuncia
# usuario, video, status
def model_listar_denuncias():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                d.denuncia_id, 
                d.usuario_id, 
                u.nome_completo, 
                d.motivo, 
                d.status, 
                d.video_id, 
                d.criado_em,
                v.nome AS titulo_video,
                v.status AS status_video
            FROM denuncias d
            JOIN usuarios u ON d.usuario_id = u.usuario_id
            LEFT JOIN videos v ON d.video_id = v.video_id
            ORDER BY d.criado_em DESC
        """)

        return cursor.fetchall()

    except Exception as e:
        raise Exception(f"Erro ao listar denúncias: {str(e)}")

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# atualzia denuncia
def model_atualizar_status_denuncia(denuncia_id, novo_status):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE denuncias
            SET status = %s
            WHERE denuncia_id = %s
        """, (novo_status, denuncia_id))

        conn.commit()
        return {"mensagem": "Status da denúncia atualizado com sucesso."}

    except Exception as e:
        raise Exception(f"Erro ao atualizar status da denúncia: {str(e)}")
    finally:
        cursor.close()
        conn.close()
        
# remover video
def model_remover_video(video_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM videos WHERE video_id = %s
        """, (video_id,))
        conn.commit()

        return {"mensagem": "Vídeo removido com sucesso."}
    except Exception as e:
        raise Exception(f"Erro ao remover vídeo: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# excluir comentarios dos videos
def model_remover_comentario(comentario_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM comentarios WHERE comentario_id = %s", (comentario_id,))
        conn.commit()
        return {"mensagem": "Comentário removido com sucesso"}
    finally:
        cursor.close()
        conn.close()

# obter denuncia por id
def model_obter_denuncia_por_id(denuncia_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(""" 
                       SELECT 
                            d.denuncia_id, 
                            d.usuario_id, 
                            u.nome_completo, 
                            d.motivo, 
                            d.status, 
                            d.video_id, 
                            d.criado_em,
                            v.link,  
                            v.status AS status_video,   
                            v.nome AS titulo_video
                        FROM denuncias d
                        JOIN usuarios u ON d.usuario_id = u.usuario_id
                        LEFT JOIN videos v ON d.video_id = v.video_id
                        WHERE d.denuncia_id = %s
                        ORDER BY d.criado_em DESC;
                       """, (denuncia_id,))
        return cursor.fetchone()
    except Exception as e:
        raise Exception(f"Erro ao buscar denúncia por ID: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def model_alterar_status_video(video_id, status):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(""" 
            UPDATE videos
            SET status = %s
            WHERE video_id = %s
        """, (status, video_id))

        cursor.execute("""
            UPDATE denuncias
            SET status = 'resolvido'
            WHERE video_id = %s
        """, (video_id,))

        conn.commit()
        return {"mensagem": "Status do vídeo e da denúncia atualizados com sucesso."}
    
    except Exception as e:
        conn.rollback()
        raise Exception(f"Erro ao alterar status do vídeo e denúncia: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()


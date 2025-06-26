from models.conection import get_connection
import logging

logger = logging.getLogger(__name__)

# estatistica usuario
def model_obter_estatisticas_usuario(usuario_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT COUNT(*) AS total_videos
            FROM videos
            WHERE usuario_id = %s
            AND status = 'ativo'
        """, (usuario_id,))
        total_videos = cursor.fetchone()["total_videos"]

        cursor.execute("""
            SELECT COUNT(*) AS total_seguidos
            FROM seguidores
            WHERE seguidor_id = %s
        """, (usuario_id,))
        total_seguidos = cursor.fetchone()["total_seguidos"]

        cursor.execute("""
            SELECT COUNT(*) AS total_seguidores
            FROM seguidores
            WHERE seguido_id = %s
        """, (usuario_id,))
        total_seguidores = cursor.fetchone()["total_seguidores"]

        return {
            "total_videos": total_videos,
            "total_seguidos": total_seguidos,
            "total_seguidores": total_seguidores
        }

    except Exception as e:
        print(f"Erro ao obter estatísticas do usuário: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

# estatistica seguidores do usuario
def model_listar_seguidores_com_estatisticas(usuario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT u.usuario_id, u.nome_completo, u.username, u.foto_perfil
            FROM seguidores s
            JOIN usuarios u ON s.seguidor_id = u.usuario_id
            WHERE s.seguido_id = %s
        """, (usuario_id,))  

        seguidores = cursor.fetchall()

        for seguidor in seguidores:
            seguidor_id = seguidor["usuario_id"]

            cursor.execute("""
                SELECT COUNT(*) AS total_videos
                FROM videos
                WHERE usuario_id = %s AND status = 'ativo'
            """, (seguidor_id,))
            seguidor["total_videos"] = cursor.fetchone()["total_videos"]

            cursor.execute("""
                SELECT COUNT(*) AS total_seguidos
                FROM seguidores
                WHERE seguidor_id = %s
            """, (seguidor_id,))
            seguidor["total_seguidos"] = cursor.fetchone()["total_seguidos"]

            cursor.execute("""
                SELECT COUNT(*) AS total_seguidores
                FROM seguidores
                WHERE seguido_id = %s
            """, (seguidor_id,))
            seguidor["total_seguidores"] = cursor.fetchone()["total_seguidores"]

        return seguidores

    except Exception as e:
        raise Exception(f"Erro ao listar seguidores com estatísticas: {str(e)}")
    finally:
        cursor.close()
        conn.close()
   
# estatistica seguidos do usuario     
def model_listar_seguidos_com_estatisticas(usuario_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                u.usuario_id, 
                u.nome_completo, 
                u.username, 
                u.foto_perfil,
                (SELECT COUNT(*) FROM videos v WHERE v.usuario_id = u.usuario_id AND v.status = 'ativo') AS total_videos,
                (SELECT COUNT(*) FROM seguidores sg WHERE sg.seguidor_id = u.usuario_id) AS total_seguidos,
                (SELECT COUNT(*) FROM seguidores sr WHERE sr.seguido_id = u.usuario_id) AS total_seguidores
            FROM seguidores s
            JOIN usuarios u ON s.seguido_id = u.usuario_id
            WHERE s.seguidor_id = %s
        """, (usuario_id,))

        return cursor.fetchall()

    except Exception as e:
        raise Exception(f"Erro ao listar seguidos com estatísticas: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# todas as estatisticas por usuario
def model_estatisticas_usuario_avancado(usuario_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # vizualizacoes totais e por periodos
        cursor.execute("""
            SELECT 
                COUNT(*) AS total_visualizacoes,
                SUM(CASE WHEN DATE(data_visualizacao) = CURDATE() THEN 1 ELSE 0 END) AS hoje,
                SUM(CASE WHEN MONTH(data_visualizacao) = MONTH(CURDATE()) AND YEAR(data_visualizacao) = YEAR(CURDATE()) THEN 1 ELSE 0 END) AS este_mes,
                SUM(CASE WHEN YEAR(data_visualizacao) = YEAR(CURDATE()) THEN 1 ELSE 0 END) AS este_ano
            FROM visualizacoes v
            JOIN videos vi ON v.video_id = vi.video_id
            WHERE vi.usuario_id = %s
        """, (usuario_id,))
        visualizacoes = cursor.fetchone()

        # total avaliacoes
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN tipo = '1' THEN 1 ELSE 0 END) AS nao_gostei,
                SUM(CASE WHEN tipo = '2' THEN 1 ELSE 0 END) AS gostei
                SUM(CASE WHEN tipo = '3' THEN 1 ELSE 0 END) AS gostei_muito
            FROM avaliacoes r
            JOIN videos v ON r.video_id = v.video_id
            WHERE v.usuario_id = %s
        """, (usuario_id,))
        avaliacoes = cursor.fetchone()

        # comentarios
        cursor.execute("""
            SELECT COUNT(*) AS total_comentarios
            FROM comentarios c
            JOIN videos v ON c.video_id = v.video_id
            WHERE v.usuario_id = %s
        """, (usuario_id,))
        total_comentarios = cursor.fetchone()["total_comentarios"]

        # vieos com vizualizacoes 
        cursor.execute("""
            SELECT v.video_id, v.nome,
                (SELECT COUNT(*) FROM visualizacoes WHERE video_id = v.video_id) AS visualizacoes,
                (SELECT COUNT(*) FROM comentarios WHERE video_id = v.video_id) AS comentarios,
                (SELECT COUNT(*) FROM avaliacoes WHERE video_id = v.video_id AND tipo = 'positiva') AS curtidas
            FROM videos v
            WHERE v.usuario_id = %s
        """, (usuario_id,))
        videos = cursor.fetchall()

        for v in videos:
            total_engajamento = v["curtidas"] + v["comentarios"]
            v["taxa_engajamento"] = (total_engajamento / v["visualizacoes"]) if v["visualizacoes"] > 0 else 0

        return {
            "visualizacoes": visualizacoes,
            "avaliacoes": avaliacoes,
            "total_comentarios": total_comentarios,
            "videos": videos
        }

    except Exception as e:
        raise Exception(f"Erro ao obter estatísticas avançadas do usuário: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# todas as estatísticas admin
def model_estatisticas_admin():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # total usuarios
        cursor.execute("SELECT COUNT(*) AS total_usuarios FROM usuarios")
        total_usuarios = cursor.fetchone()["total_usuarios"]
        
        # total playlist
        cursor.execute("SELECT COUNT(*) AS total_playlists FROM playlists")
        total_playlists = cursor.fetchone()["total_playlists"]
        
        # total playlist por usuario
        # cursor.execute("""
        #     SELECT usuario_id, COUNT(*) AS total_playlists
        #     FROM playlist
        #     GROUP BY usuario_id;
        # """)
        # playlist_usuarios = cursor.fetchall()

        # for linha in playlist_usuarios:
        #     print(f"Usuário {linha['usuario_id']} tem {linha['total_playlists']} playlists.")

        # total de usuários ativos e inativos
        cursor.execute("SELECT COUNT(*) AS total_ativos FROM usuarios WHERE status = 'ativo'")
        total_ativos = cursor.fetchone()["total_ativos"]

        cursor.execute("SELECT COUNT(*) AS total_inativos FROM usuarios WHERE status = 'inativo'")
        total_inativos = cursor.fetchone()["total_inativos"]

        cursor.execute("SELECT COUNT(*) AS total_bloqueados FROM usuarios WHERE status = 'bloqueado'")
        total_bloqueados = cursor.fetchone()["total_bloqueados"]
        # total de vídeos
        cursor.execute("SELECT COUNT(*) AS total_videos FROM videos")
        total_videos = cursor.fetchone()["total_videos"]

        # total de interações
        cursor.execute("SELECT COUNT(*) AS total_comentarios FROM comentarios")
        total_comentarios = cursor.fetchone()["total_comentarios"]

        cursor.execute("SELECT COUNT(*) AS total_avaliacoes FROM avaliacoes")
        total_avaliacoes = cursor.fetchone()["total_avaliacoes"]

        # vídeos mais populares
        cursor.execute("""
            SELECT v.video_id, v.nome,
                (SELECT visualizacoes FROM videos WHERE video_id = v.video_id) AS visualizacoes,
                (SELECT COUNT(*) FROM comentarios WHERE video_id = v.video_id) AS comentarios,
                (SELECT COUNT(*) FROM avaliacoes WHERE video_id = v.video_id AND avaliacao = '3' AND avaliacao = '2') AS curtidas
            FROM videos v
            WHERE v.status = 'ativo'
            ORDER BY visualizacoes DESC
            LIMIT 10
        """)
        populares = cursor.fetchall()

        # média de visualizações
        cursor.execute("""
            SELECT AVG(visualizacoes) AS media_visualizacoes
            FROM (
                SELECT visualizacoes
                FROM videos
                WHERE status = 'ativo'
                ORDER BY visualizacoes DESC
                LIMIT 10
            ) AS top_videos
        """)
        media_visualizacoes = cursor.fetchone()["media_visualizacoes"]

        # total de comentários por data
        cursor.execute("""
            SELECT DATE(criado_em) AS data, COUNT(*) AS total
            FROM comentarios
            GROUP BY DATE(criado_em)
            ORDER BY data ASC
        """)
        comentarios_por_data = cursor.fetchall()

        # total de avaliações por data
        cursor.execute("""
            SELECT DATE(criado_em) AS data, COUNT(*) AS total
            FROM avaliacoes
            GROUP BY DATE(criado_em)
            ORDER BY data ASC
        """)
        avaliacoes_por_data = cursor.fetchall()

        # contagem de vídeos por status
        cursor.execute("""
            SELECT status, COUNT(*) AS quantidade
            FROM videos
            GROUP BY status
        """)
        videos_por_status = cursor.fetchall()
        videos_status_dict = {row["status"]: row["quantidade"] for row in videos_por_status}
        
        # media comentarios
        cursor.execute("""
            SELECT AVG(comentario_count) AS media_comentarios
            FROM (
                SELECT COUNT(*) AS comentario_count
                FROM comentarios
                GROUP BY video_id
            ) AS comentarios_por_video
        """)
        media_comentarios = cursor.fetchone()["media_comentarios"]
        
        # media por usuario
        cursor.execute("""
            SELECT
            AVG(videos_por_usuario.total_videos) AS media_videos_por_usuario,
            AVG(videos_por_usuario.total_visualizacoes) AS media_visualizacoes_por_usuario,
            AVG(comentarios_por_usuario.total_comentarios) AS media_comentarios_por_usuario
            FROM (
                SELECT u.usuario_id,
                    COUNT(v.video_id) AS total_videos,
                    COALESCE(SUM(v.visualizacoes), 0) AS total_visualizacoes
                FROM usuarios u
                LEFT JOIN videos v ON u.usuario_id = v.usuario_id
                GROUP BY u.usuario_id
            ) AS videos_por_usuario
            LEFT JOIN (
                SELECT u.usuario_id,
                    COUNT(c.comentario_id) AS total_comentarios
                FROM usuarios u
                LEFT JOIN comentarios c ON u.usuario_id = c.usuario_id
                GROUP BY u.usuario_id
            ) AS comentarios_por_usuario ON videos_por_usuario.usuario_id = comentarios_por_usuario.usuario_id
        """)
        medias = cursor.fetchone()
        media_videos_por_usuario = medias["media_videos_por_usuario"]
        media_visualizacoes_por_usuario = medias["media_visualizacoes_por_usuario"]
        media_comentarios_por_usuario = medias["media_comentarios_por_usuario"]

        return {
            "usuarios": {
                "total": total_usuarios,
                "ativos": total_ativos,
                "inativos": total_inativos,
                "bloqueados": total_bloqueados
            },
            "videos": {
                "total": total_videos,
                "por_status": videos_status_dict
            },
            "interacoes": {
                "comentarios": total_comentarios,
                "avaliacoes": total_avaliacoes
            },
            "playlist" : {
                "total": total_playlists,
                # "por_usuario": playlist_usuarios
            },
            "medias_por_usuario": {
                "videos": media_videos_por_usuario,
                "visualizacoes": media_visualizacoes_por_usuario,
                "comentarios": media_comentarios_por_usuario
            },
            "videos_populares": populares,
            "media_visualizacoes": media_visualizacoes,
            "media_comentarios": media_comentarios,
            "comentarios_por_data": comentarios_por_data,
            "avaliacoes_por_data": avaliacoes_por_data
        }

    except Exception as e:
        raise Exception(f"Erro ao obter estatísticas administrativas: {str(e)}")
    finally:
        cursor.close()
        conn.close()

from models.conection import get_connection
from typing import Optional, List
from datetime import datetime

# buscar videos
def model_buscar_videos_avancado(
    nome: Optional[str] = None,
    generos: Optional[List[str]] = None,
    tipos: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    duracao: Optional[str] = None
):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        filtros = ["v.status = 'ativo'"]
        valores = []

        if nome:
            filtros.append("v.nome LIKE %s")
            valores.append(f"%{nome}%")

        if generos:
            filtros.append("v.genero IN (" + ", ".join(["%s"] * len(generos)) + ")")
            valores.extend(generos)

        if tipos:
            filtros.append("v.tipo IN (" + ", ".join(["%s"] * len(tipos)) + ")")
            valores.extend(tipos)

        if duracao:
            filtros.append("v.duracao = %s")
            valores.append(duracao)

        if data_inicio and data_fim:
            filtros.append("DATE(v.criado_em) BETWEEN %s AND %s")
            valores.extend([data_inicio, data_fim])
        elif data_inicio:
            filtros.append("DATE(v.criado_em) >= %s")
            valores.append(data_inicio)
        elif data_fim:
            filtros.append("DATE(v.criado_em) <= %s")
            valores.append(data_fim)

        base_query = """
            SELECT 
                v.*, 
                u.usuario_id,
                u.nome_completo AS nome_usuario,
                u.foto_perfil,
                GROUP_CONCAT(DISTINCT t.nome_tag) AS tags
            FROM videos v
            JOIN usuarios u ON v.usuario_id = u.usuario_id
            LEFT JOIN tags_videos t ON v.video_id = t.video_id
        """

        if tags:
            filtros.append("t.nome_tag IN (" + ", ".join(["%s"] * len(tags)) + ")")
            valores.extend(tags)

        if filtros:
            base_query += " WHERE " + " AND ".join(filtros)

        base_query += " GROUP BY v.video_id"
        base_query += " ORDER BY v.criado_em DESC"

        cursor.execute(base_query, valores)
        resultados = cursor.fetchall()

        for video in resultados:
            if video.get("tags"):
                video["tags"] = [t.strip() for t in video["tags"].split(",")]
            else:
                video["tags"] = []

        return resultados

    except Exception as e:
        print("Erro na busca avançada:", e)
        return []

    finally:
        cursor.close()
        conn.close()

# listar por tipo
def model_listar_videos_por_tipo(tipo):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM videos WHERE tipo = %s ORDER BY v.criado_em DESC"
        cursor.execute(sql, (tipo,))
        return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao listar vídeos por tipo: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

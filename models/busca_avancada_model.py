from models.conection import get_connection
from typing import Optional, List
from datetime import datetime

def model_buscar_videos_avancado(
    nome: Optional[str] = None,
    genero: Optional[str] = None,
    tags: Optional[List[str]] = None,
    tipo: Optional[str] = None,
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
        if genero:
            filtros.append("v.genero = %s")
            valores.append(genero)
        if tipo:
            filtros.append("v.tipo = %s")
            valores.append(tipo)
        if duracao:
            filtros.append("v.duracao = %s")
            valores.append(duracao)
        if data_inicio and data_fim:
            filtros.append("DATE(v.criado_em) BETWEEN %s AND %s")
            valores.append(data_inicio)
            valores.append(data_fim)
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
                GROUP_CONCAT(t.nome_tag) AS tags
            FROM videos v
            JOIN usuarios u ON v.usuario_id = u.usuario_id
            LEFT JOIN tags_videos t ON v.video_id = t.video_id
        """

        if tags and len(tags) > 0:
            # filtragem por tags usando HAVING
            base_query += " GROUP BY v.video_id HAVING "
            having_conditions = []
            for tag in tags:
                having_conditions.append("FIND_IN_SET(%s, GROUP_CONCAT(t.nome_tag)) > 0")
                valores.append(tag)
            base_query += " AND ".join(having_conditions)
        else:
            # sem filtro por tag
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

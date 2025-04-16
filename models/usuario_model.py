from models.conection import get_connection

def model_adicionar_usuario(
    nome_completo,
    username,
    email,
    senha,
    data_nascimento,
    foto_perfil=None,
    genero=None,
    biografia=None,
    tipo='comum',
    status='ativo'
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO usuarios (
            nome_completo, username, email, senha, data_nascimento,
            foto_perfil, genero, biografia, tipo, status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            nome_completo, username, email, senha, data_nascimento,
            foto_perfil, genero, biografia, tipo, status
        )

        cursor.execute(sql, valores)
        conn.commit()
        print("user adicionado")

    except Exception as e:
        print("error ", e)

    finally:
        cursor.close()
        conn.close()
        
def model_editar_usuario(
    usuario_id, nome_completo=None, username=None, email=None,
    senha=None, data_nascimento=None, foto_perfil=None,
    genero=None, biografia=None, tipo=None, status=None
):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        campos = []
        valores = []

        if nome_completo:
            campos.append("nome_completo = %s")
            valores.append(nome_completo)
        if username:
            campos.append("username = %s")
            valores.append(username)
        if email:
            campos.append("email = %s")
            valores.append(email)
        if senha:
            campos.append("senha = %s")
            valores.append(senha)
        if data_nascimento:
            campos.append("data_nascimento = %s")
            valores.append(data_nascimento)
        if foto_perfil:
            campos.append("foto_perfil = %s")
            valores.append(foto_perfil)
        if genero:
            campos.append("genero = %s")
            valores.append(genero)
        if biografia:
            campos.append("biografia = %s")
            valores.append(biografia)
        if tipo:
            campos.append("tipo = %s")
            valores.append(tipo)
        if status:
            campos.append("status = %s")
            valores.append(status)

        if not campos:
            print("Nenhum dado para atualizar.")
            return

        query = f"""
            UPDATE usuarios
            SET {', '.join(campos)}
            WHERE usuario_id = %s
        """
        valores.append(usuario_id)
        cursor.execute(query, valores)
        conn.commit()
        print("Usuário atualizado.")

    except Exception as e:
        print("Erro ao editar usuário:", e)

    finally:
        cursor.close()
        conn.close()

def model_inativar_usuario(usuario_id, status):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "UPDATE usuarios SET status = %s WHERE usuario_id = %s"
        cursor.execute(sql, (status, usuario_id))
        conn.commit()

        print("Usuário inativado com sucesso!", status)
        return True

    except Exception as e:
        print(f"Erro ao inativar usuário: {e} - ", status)
        return False

    finally:
        cursor.close()
        conn.close()
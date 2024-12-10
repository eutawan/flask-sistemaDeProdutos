import psycopg2

def insert_user(connection, id, loginuser, senha, tipouser):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "INSERT INTO usuario (id, loginuser, senha, tipouser) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (id, loginuser, senha, tipouser))
            connection.commit()
        except psycopg2.Error as error:
            print(f"Erro ao registrar usuário: {str(error)}")
        finally:
            cur.close()
            connection.close()


def get_user(connection, loginuser):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "SELECT * FROM usuario WHERE loginuser = %s"
            cur.execute(sql, (loginuser,))
            recset = cur.fetchone()
            return recset if recset else False
        except psycopg2.Error as error:
            print(f"Erro ao buscar usuário: {str(error)}")
        finally:
            cur.close()
        

def get_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuario")
    data = cursor.fetchall()
    print(data)

    connection.commit()
    cursor.close()
    

    return data

def update_user(connection, loginuser, senha, tipouser):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "UPDATE usuario SET loginuser=%s, senha=%s, tipouser=%s WHERE loginuser=%s"
            cur.execute(sql, (loginuser, senha, tipouser))
            connection.commit()
        except psycopg2.Error as error:
            print(f"Erro ao atualizar usuário: {str(error)}")
        finally:
            cur.close()
            connection.close()

def delete_user(connection, loginuser):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "DELETE FROM usuario WHERE loginuser=%s"
            cur.execute(sql, (loginuser,))
            connection.commit()
        except psycopg2.Error as error:
            print(f"Erro ao deletar usuário: {str(error)}")
        finally:
            cur.close()
            connection.close()
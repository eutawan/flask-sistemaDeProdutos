import psycopg2

def insert_product(connection, id, nome, loginuser, qtde, preco):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "INSERT INTO produto (id, nome, loginuser, qtde, preco) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(sql, (id, nome, loginuser, qtde, preco))
        except psycopg2.Error as error:
            print(f"Erro ao inserir produto {str(error)}")
        finally:
            cur.close()
            connection.close()

def get_all_products(connection, loginUser):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "SELECT * FROM produto WHERE loginUser = %s"
            cur.execute(sql, (loginUser,))
            recset = cur.fetchall()
            return recset if recset else False
        except psycopg2.Error as error:
            print(f"Erro ao buscar produtos para o usuário selecionado: {str(error)}")
        finally:
            cur.close()


def get_product_by_iduser(connection, id):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM produto WHERE id = %s", (id))

    data = cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()
    return data

def get_product(connection, nomeProduto=None, id=None):
    cursor = connection.cursor()
    if id is not None:
        cursor.execute("SELECT * FROM produto WHERE id = %s", (id,))
    else:
        cursor.execute("SELECT * FROM produto WHERE nome = %s", (nomeProduto,))
    
    data = cursor.fetchone()
    print(data)

    connection.commit()
    cursor.close()
    connection.close()
    return data

def update_product(connection, id, nomeProduto, qtde, preco):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "UPDATE produto SET nome=%s, qtde=%s, preco=%s WHERE id=%s"
            cur.execute(sql, (nomeProduto, qtde, preco, id))
            connection.commit()
        except psycopg2.Error as error:
            print(f"Erro ao atualizar: {str(error)}")
        finally:
            cur.close()
            connection.close()

def delete_product(connection, id):
    if connection is not None:
        cur = connection.cursor()
        try:
            sql = "DELETE FROM produto WHERE id=%s"
            cur.execute(sql, str(id,))
            connection.commit()
        except psycopg2.Error as error:
            print(f"Erro ao deletar produto: {str(error)}")
        finally:
            cur.close()
            connection.close()
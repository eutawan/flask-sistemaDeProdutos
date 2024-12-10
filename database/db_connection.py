import psycopg2, os
from dotenv import load_dotenv

load_dotenv()

def db_connection():
    try:
        db = psycopg2.connect(f'dbname={os.getenv("NAME_DB")} user={os.getenv("USER_DB")} password={os.getenv("PASSWORD_DB")} host=localhost port=5432')
        return db
    except psycopg2.Error as error:
        print(f"Erro na conexão com o banco de dados: {str(error)}")
        return None
    
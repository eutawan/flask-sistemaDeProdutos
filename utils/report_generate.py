import threading
import os
import database as db
from datetime import datetime

def generate_report(user_id):
    report_folder = 'reports'
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    connection = db.db_connection()
    if connection is None:
        print("Erro na conexão com o banco de dados.")
        return
    
    try:
        data = db.get_all_products(connection, user_id)
        products = []

        if data:
            for i in data:
                product = {
                    "nome": i[1],
                    "qtde": i[3],
                    "preco": str(i[4]),
                }
                products.append(product)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'reports/product_report_{timestamp}.txt'

        with open(filename, 'w') as report_file:
            report_file.write("Products report:\n")
            for product in products:
                report_file.write(f"Produto -> {product['nome']}, Quantidade -> {product['qtde']} Preço -> {product['preco']}\n")
            
        print(f"Relatório gerado: {filename}")

    except Exception as e:
        print(f"Erro ao gerar relatório: {str(e)}")

    finally:
        connection.close()

def thread_generate_report(user_id):
    thread = threading.Thread(target=generate_report, args=(user_id,))
    thread.daemon = True
    thread.start()
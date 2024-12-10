from flask import Blueprint, redirect, render_template, session, jsonify
import os
from utils import quantityAnalisys, salesAnalisys, thread_generate_report
from database import db_connection, product_dao as pd

product_analisys_bp = Blueprint("analisys", __name__, url_prefix='/analisys')

UPLOAD_FOLDER = os.path.join(os.path.dirname("app.py"), 'uploads')
arquivo_csv = 'vendas_grande.csv'

@product_analisys_bp.route('/quantity', endpoint='quantity')
def products_analisys_quantity():
    if 'login_user' in session and session['user_type'] == 'admin':
        data = pd.get_all_products(db_connection(), session['login_user'])
        products = [{'name': i[1], 'quantity': i[2]} for i in data] if data else []
        htmlWithgraphic = quantityAnalisys(products)
        return render_template('product/analisys/quantity-product-analisys.html', graphic_html=htmlWithgraphic)

    return redirect('/')

@product_analisys_bp.route('/sales', endpoint='sales')
def products_analisys_sales():
    if 'login_user' in session and session['user_type'] == 'admin':
        htmlWithgraphic = salesAnalisys(os.path.join(UPLOAD_FOLDER, arquivo_csv))
        return render_template('product/analisys/sales-product-analisys.html', graphic_html=htmlWithgraphic)

    return redirect('/')

@product_analisys_bp.route('/generate_report', methods=['GET'])
def generate_report_route():
    if 'login_user' in session:
        thread_generate_report(session['login_user'])
        return jsonify({"message": "The report generation has started, you will be notified when it is ready"})
    return redirect('/')
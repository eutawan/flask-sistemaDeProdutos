from flask import Blueprint, redirect, render_template, session, request
from .analisys.product_analisys_routes import product_analisys_bp
from utils import generate_uuid 
from database import db_connection, get_all_products, insert_product, get_product, delete_product, update_product

product_bp = Blueprint("product", __name__, url_prefix='/product')
product_bp.register_blueprint(product_analisys_bp)

@product_bp.route('/register', methods=['GET', 'POST'], endpoint="register")
def register_products():
    if 'login_user' in session:
        if request.method == 'GET':
            return render_template('product/register-product.html')
        elif request.method == 'POST':
            user_id = session['login_user']
            user_type = session['user_type']

            if user_type == 'standard':
                current_products = get_all_products(db_connection(), user_id)
                print(current_products)
                if current_products and len(current_products) >= 3:
                    print("Usuários normais só podem cadastrar até 3 produtos.")
                    return redirect('/product/listall')

            nome = request.form.get('nome')
            qtde = request.form.get('qtde')
            preco = request.form.get('preco')

            if not nome or not qtde or not preco:
                return redirect('/product/register')

        
            if not qtde.isdigit() or not preco.replace('.', '', 1).isdigit():
                return redirect('/product/register')

            id = generate_uuid()
            insert_product(db_connection(), id, nome, qtde, preco['login_user'])


            return redirect('/product/listall')
    return redirect('/')

@product_bp.route('/listall', methods=['GET'], endpoint="listall")
def list_products():
    if 'login_user' in session:
        data = get_all_products(db_connection(), session['login_user'])
        products = [{'id': i[0], 'nome': i[1], 'qtde': i[3], 'preco': str(i[4])} for i in data] if data else[]
        return render_template('product/list-all-products.html', products=products)
    return redirect('/')

@product_bp.route('/update/<product_id>', methods=['GET', 'POST'], endpoint="update")
def update_product_by_id(product_id):
    if 'login_user' in session:
        if request.method == 'GET':
            data = get_product(db_connection(), id=product_id)

            if not data:
                return redirect('/product/listall')

            product = {'id': data[0], 'nome': data[1], 'qtde': data[3], 'preco': str(data[4])}
            
            return render_template('product/update-product.html', product=product)
        elif request.method == 'POST':
            nameProduct = request.form.get('nome')
            qtde = request.form.get('qtde')
            preco = request.form.get('preco')
            
            update_product(db_connection(), product_id, nameProduct, qtde, preco)
            return redirect('/product/listall')

@product_bp.route('/delete/<product_id>', methods=['GET'], endpoint="delete")
def delete_product_by_id(product_id):
    if 'login_user' in session:
        delete_product(db_connection(), product_id,)
        return redirect('/product/listall')
    return redirect('/')
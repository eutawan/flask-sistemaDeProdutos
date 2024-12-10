from flask import Blueprint, jsonify, request
from database import db_connection, product_dao as pd, user_dao as ud
from utils import is_uuid, generate_uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

api_bp = Blueprint("api", __name__, url_prefix='/api')

@api_bp.route("users/listall", methods=['GET'])
def json_all_users():
    conn = db_connection()

    if conn is None:
        return jsonify({'error': 'A conexao com o banco de dados falhou.'}), 500
    
    data = ud.get_usuario(conn)

    users = []

    for user in data:
        users.append({
            'id': user[0],
            'loginuser':user[1],
            'tipouser': user[3],
        })

    json = {
        'users': users
    }
    return jsonify(json)

@api_bp.route("/product/listall", methods=['GET'])
def all_products_json():
    conn = db_connection()

    if conn is None:
        return jsonify({'error': 'Erro ao conectar com o banco de dados'}), 500
    
    data = pd.get_products(conn)

    produtos = []

    for produto in data:
        produtos.append(
            {
                'id': produto[0],
                'name': produto[1],
                'loginuser': produto[2],
                'qtde': produto[3],
                'preco': produto[4],
            }
        )
        
        json = {
            'produtos': produtos
        }
        
        return jsonify(json)
    
@api_bp.route("product/getByUser", methods=['GET'])
@jwt_required()
def json_get_product_by_userLogin():
    conn = db_connection()

    current_user = get_jwt_identity()

    data = pd.get_product_by_loginuser(conn, current_user['loginuser'])
    print(data)

    products = []

    for product in data:
        products.append(
            {
                'id': product[0],
                'nome': product[1],
                'loginuser': product[2],
                'qtde': product[3],
                'preco': product[4]
            }
        )
    if data:
        response = {
            'status': 'deu certo',
            'data': products
        }
    else:
        response = {
            'status': 'deu errado',
            'data': 'produto não encontrado'
        }
    
    return jsonify(response), 200 if data else 400

@api_bp.route("/product/getByProduto/<string:keyProduct>", methods=['GET'])
@jwt_required()
def json_get_product(keyProduct):
    conn = db_connection()
    if is_uuid(keyProduct):
        data = pd.get_product(conn, id=str(keyProduct))
    else:
        data = pd.get_product(conn, nameProduct=keyProduct)
    
    product = {
        'id': data[0],
        'nome': data[1],
        'loginuser': data[2],
        'qtde': data[3],
        'preco': str(data[4])
    }
    if data:
        response = {
            'status': 'deu certo',
            'product': product
        }
    else:
        response = {
            'status': 'deu errado',
            'product': 'nao deu certo'
        }

    return jsonify(response), 200 if data else 400

@api_bp.route("/product/create", methods=['POST'])
@jwt_required()
def json_create_product():
    conn = db_connection()

    if conn is None:
        return jsonify({'error': 'Erro ao conectar com o banco de dados'}), 500
    
    produto = request.json["nome"]
    qtde = request.json["qtde"]
    preco = request.json["preco"]

    pd.insert_product(conn, produto, qtde, preco)

    return jsonify({"sucess": "Produto criado"})
    
api_bp.route("/users/verifyLogin", methods=['POST'])
def verify_login():
    username = request.json['loginuser']
    password = request.json['senha']

    data = ud.get_user(db_connection(), username)

    if not data or not check_password_hash(data[1], password):
        return jsonify({'error': 'username ou senha inválidos'}), 401
    
    token = create_access_token(identity={'loginuser': data[0], 'tipouser': data[2]})
    return jsonify(access_token=token), 200

api_bp.route("/users/register", methods=['POST'], endpoint= "signup")

def signup():
    username = request.json.get('loginuser')
    password = request.json.get('senha')
    confirmPassword = request.json.get('confirm-password')
    typeUser = request.json.get('tipouser')

    if password != confirmPassword:
        return jsonify({'error': 'as senhas não coincidem'}, 401)
    
    if ud.get_user(db_connection(), username):
        return jsonify({'error': 'O usuário já existe'}, 401)
    

    password_hash = generate_password_hash(password)

    ud.insert_user(db_connection(), username, password_hash, typeUser)

    return jsonify({'sucess': 'Registrado com sucesso'}, 201)
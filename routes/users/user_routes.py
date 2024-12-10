from flask import Blueprint, request, session, render_template, redirect
from database import *
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint("users", __name__, url_prefix='/users')

@user_bp.route('/login', methods=['GET', 'POST'], endpoint = "login")
def login():
    if request.method == 'GET':
        return render_template('users/login.html')
    elif request.method == 'POST':
        loginuser = request.form.get('loginuser')
        senha = request.form.get('senha')

        query = get_user(db_connection(), loginuser)

        if not query or not check_password_hash(query[2], senha):
            return redirect('/users/login')
        
        session['login_user'] = query[1]
        session['user_type'] = query[3]
        
        return redirect('/product/listall')

@user_bp.route('/signup', methods=['GET', 'POST'], endpoint = "signup")
def signup():
    if request.method == 'GET':
        return render_template('users/signup.html')
    elif request.method == 'POST':
        loginuser = request.form.get('loginuser')
        senha = request.form.get('senha')
        confirmarSenha = request.form.get('confirm-password')
        tipouser = request.form.get('tipouser')

        if senha != confirmarSenha:
            return redirect('/users/signup')
        
        if get_user(db_connection(), loginuser):
            return redirect('/users/signup')

        idUser = str(uuid.uuid4())
        password_hash = generate_password_hash(senha)
        
        insert_user(db_connection(), idUser, loginuser, password_hash, tipouser)

        return redirect('/users/login')
    
@user_bp.route('/logout', methods=['GET'], endpoint='logout')
def logout():
    session.pop('login_user', None)
    return redirect('/')
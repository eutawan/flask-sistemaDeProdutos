from flask import *
import os
from datetime import timedelta
from dotenv import load_dotenv
from routes import user_bp, product_bp, api_bp
from flask_jwt_extended import JWTManager

load_dotenv()

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(api_bp)

app.secret_key = os.getenv('SECRET_KEY_DEV')
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

@app.route('/')
def home():
    print(app.secret_key)
    return render_template('home.html')

if __name__ == "__main__":
    certificado = os.path.join('certs', 'certificate.crt')
    chave = os.path.join('certs', 'private.key')

    app.run(ssl_context=(certificado, chave), port=5001, debug=True)
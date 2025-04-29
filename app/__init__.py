# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importás el blueprint y lo registrás
    from app.routes import routes
    app.register_blueprint(routes)

    return app

# Esto permite que `from app import app` funcione
app = create_app()
'''
from flask import Flask

app = Flask(__name__)

# Importar las rutas y registrar el blueprint
from app.routes import routes
app.register_blueprint(routes)
'''
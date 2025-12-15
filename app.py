from flask import Flask
from config import Config
from models import db
from routes import api as api_blueprint 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(api_blueprint, url_prefix='/api/v1') 
    
    return app

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Comando para crear las tablas de la base de datos."""
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada (tablas creadas).")

if __name__ == '__main__':
    app.run(debug=True)

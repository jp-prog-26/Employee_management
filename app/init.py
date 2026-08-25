from flask import Flask, render_template
from app.database import init_db

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Inicializar SQLite (crea la tabla si no existe)
    init_db(app)

    # Registro de Blueprint de rutas web de empleados
    from app.routes.employee_routes import employees_bp, dashboard
    app.register_blueprint(employees_bp)

    # Alias para la ruta raiz y endpoint dashboard
    app.add_url_rule('/', endpoint='dashboard', view_func=dashboard)

    # Registro de Blueprint de la API REST
    from app.routes.api_routes import api_bp
    app.register_blueprint(api_bp)

    # Manejo de errores 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    return app